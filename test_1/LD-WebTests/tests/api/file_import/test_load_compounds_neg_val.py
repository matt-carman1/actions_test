from ldclient.exceptions import AsyncServiceTaskFailedError

from helpers.api.actions.livereport import load_sdf_in_lr
from helpers.api.actions.row import get_live_report_rows
from helpers.extraction import paths
from helpers.api.verification.general import verify_error_response
import pytest

test_type = 'api'


def test_load_compounds_neg_val(ld_api_client, new_live_report):
    """
    Negative validation of the load_sdf ldclient method.

    :param ld_api_client: Fixture that returns ldclient object for "demo:demo"
    :param new_live_report: Fixture that creates a new livereport.
    :return:
    """
    # Finding ID of the new livereport and setting data path
    lr_id = new_live_report.id
    data_path = paths.get_resource_path("api/")

    # ------ Test with invalid sdf file----- #
    invalid_sdf_response = load_sdf_in_lr(ld_api_client,
                                          lr_id,
                                          '{0}/invalid_sdf.sdf'.format(data_path),
                                          compounds_only=True,
                                          compound_source="pri")

    assert len(invalid_sdf_response) == 0, \
    "{} compounds got imported from an invalid sdf when it should not be".format(len(invalid_sdf_response))

    # ------ Test with unsupported format(.jpeg) file ----- #
    unsupported_format_response = load_sdf_in_lr(ld_api_client,
                                                 lr_id,
                                                 '{0}/snowman.jpg'.format(data_path),
                                                 compounds_only=True,
                                                 compound_source="pri")
    assert len(unsupported_format_response) == 0, \
        "{} compounds got imported from an invalid sdf when it should not be".format(len(unsupported_format_response))

    # Cross verification that no compounds are imported in the LR
    list_of_live_report_rows = get_live_report_rows(ld_api_client, lr_id)
    assert list_of_live_report_rows == [], \
        "Compounds {} registered with an invalid sdf when it should not be".format(list_of_live_report_rows)

    # ------ Test with invalid livereport id ------ #
    with pytest.raises(Exception) as invalid_lr_response:
        load_sdf_in_lr(ld_api_client,
                       live_report_id='0001',
                       file_path='{0}/valid_sdf_real.sdf'.format(data_path),
                       compounds_only=True,
                       compound_source="pri")
    verify_error_response(invalid_lr_response.value, '400', "One or more of the specified LiveReports do not exist")

    # ------ Test with invalid project ------ #
    with pytest.raises(Exception) as invalid_project_response:
        load_sdf_in_lr(ld_api_client,
                       lr_id,
                       file_path='{0}/valid_sdf_real.sdf'.format(data_path),
                       project='fake',
                       compounds_only=True,
                       compound_source="pri")
    verify_error_response(invalid_project_response.value, '400', "Project fake does not exist")

    # ------ Test with invalid compound_source------ #
    with pytest.raises(Exception) as invalid_cmpd_source_response:
        load_sdf_in_lr(ld_api_client,
                       lr_id,
                       file_path='{0}/valid_sdf_real.sdf'.format(data_path),
                       compounds_only=True,
                       compound_source="fake")
    verify_error_response(invalid_cmpd_source_response.value, '400', "Data source fake does not exist")

    # Cross verification that no compounds are imported into the LR
    list_of_live_report_rows = get_live_report_rows(ld_api_client, lr_id)
    assert list_of_live_report_rows == [], \
        "Compounds {} registered with an invalid parameter when it should not be".format(list_of_live_report_rows)
