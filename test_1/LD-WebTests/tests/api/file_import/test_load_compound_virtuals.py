from helpers.api.actions.livereport import load_sdf_in_lr
from helpers.api.actions.row import get_live_report_rows
from helpers.extraction import paths

test_type = 'api'


def test_load_compound_virtuals(ld_api_client, new_live_report):
    """
    Positive validation of the load_sdf ldclient method for virtuals.

    :param ld_api_client: Fixture that returns ldclient object for "demo:demo"
    :param new_live_report: Fixture that creates a new livereport.
    :return:
    """

    # Finding ID of the new livereport and setting data path
    lr_id = new_live_report.id
    data_path = paths.get_resource_path("api/")

    # ------ Test with importing only compounds and source as virtuals. ----- #
    load_valid_sdf_virtual = load_sdf_in_lr(ld_api_client,
                                            lr_id,
                                            '{0}/valid_sdf_virtual.sdf'.format(data_path),
                                            compounds_only=True,
                                            compound_source="pri")

    # Two way verification that both virtuals are imported
    assert len(load_valid_sdf_virtual) == 2, \
        "There was an error while importing virtuals. Expected {} compounds but got {}".format(2,
                                                                                            len(load_valid_sdf_virtual))

    list_of_live_report_rows = get_live_report_rows(ld_api_client, lr_id)
    sdf_comps = [compounds['corporate_id'] for compounds in load_valid_sdf_virtual]

    assert set(sdf_comps) == set(list_of_live_report_rows), \
        "Expected list of ids {} does not match actual ids {}".format(sdf_comps, list_of_live_report_rows)
