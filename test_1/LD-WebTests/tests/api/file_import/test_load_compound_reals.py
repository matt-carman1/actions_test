from helpers.api.actions.livereport import load_sdf_in_lr, live_report_details
from helpers.extraction import paths

test_type = 'api'


def test_load_compound_reals(ld_api_client, new_live_report):
    """
    Positive validation of the load_sdf ldclient method for reals.

    :param ld_api_client: Fixture that returns ldclient object for "demo:demo"
    :param new_live_report: Fixture that creates a new livereport.
    :return:
    """
    expected_real_ids = ['Real-1', 'Real-2']

    # Finding ID of the new livereport and setting data path
    lr_id = new_live_report.id
    data_path = paths.get_resource_path("api/")

    # ------ Test with importing only compounds and source as reals. ----- #
    load_valid_sdf_real = load_sdf_in_lr(ld_api_client,
                                         lr_id,
                                         '{0}/valid_sdf_real.sdf'.format(data_path),
                                         compounds_only=True,
                                         compound_source="non_pri")

    # Two way verification that both compounds reals are imported
    assert len(load_valid_sdf_real) == 2, \
        "There was an error while importing reals. Expected {} compounds but got {}".format(2, len(load_valid_sdf_real))

    sdf_comps = [compounds['corporate_id'] for compounds in load_valid_sdf_real]

    assert set(sdf_comps) == set(expected_real_ids), \
        "Expected list of ids {} does not match actual ids {}".format(sdf_comps, expected_real_ids)
