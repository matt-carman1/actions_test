from multiprocessing.pool import ThreadPool

from helpers.api.actions.livereport import create_new_live_report
from helpers.api.verification.live_report import verify_lr_has_values_in_rows_and_columns, \
    verify_lr_has_no_values
from library.api.wait import wait_until_condition_met


def test_delete_threed_structure(ld_api_client):
    """
    Test that deleting 3D structure also archives the pose on the LR. This is done by verifying
    the docking scores on the pose disappears from the LR

    Note that this test is NOT idempotent. If you rerun the test, it will fail. You can run this
    SQL to undo the changes made by the test so that you can rerun the test

    UPDATE ld_structure SET archived = false WHERE id IN (55548, 55549, 55550, 55551) AND archived = true;
    UPDATE ld_entity SET archived = 0 WHERE id IN (2116154,2116153) AND archived = 1;
    """
    # These are the 3D + docking score columns for the "Fake 3D model with 2 poses" model
    col_ids = ["11", "14"]
    entity_id = "CRA-035007"
    lr = create_new_live_report(ld_api_client, "test_delete_threed_structure")
    ld_api_client.add_columns(lr.id, col_ids)
    ld_api_client.add_rows(lr.id, [entity_id])

    def verify_model_cells_have_values():
        verify_lr_has_values_in_rows_and_columns(ld_api_client, lr.id, col_ids, [entity_id])

    def verify_model_cells_no_values():
        verify_lr_has_no_values(ld_api_client, lr.id, col_ids, [entity_id])

    def _archive_structure(structure_id):
        ld_api_client.client.delete(service_path="/threed_structures", path=f"/{structure_id}")

    wait_until_condition_met(condition_function=verify_model_cells_have_values)
    with ThreadPool(4) as pool:
        # Note(zou) I have verified the Global Interpreter Lock isn't a problem here
        pool.map(_archive_structure, [55548, 55549, 55550, 55551])
    wait_until_condition_met(condition_function=verify_model_cells_no_values)
