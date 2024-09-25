import time

from helpers.api.extraction.grid import get_cell_values_for_rows_and_columns
from helpers.api.verification.general import verify_error_response
from library.api.wait import wait_until_condition_met


def verify_create_ffc_response(ld_api_client,
                               actual_ffc_object,
                               actual_response,
                               expected_status_code=None,
                               expected_error_message=None):
    """
    Verification for create freeform column

    :param ld_api_client: LDClient, ldclient
    :param actual_ffc_object: ldclient.models.FreeformColumn, Actual freeform column object
    :param actual_response: ldclient.models.FreeformColumn/RequestException, Response from creating ffc
    :param expected_status_code: str, Expected status code for ffc not created case, NA in successful ffc creation
    :param expected_error_message: str, error message for ffc not created case, NA in successful ffc creation
    """
    # Getting available freeform columns for specific project
    freeform_columns_for_project = ld_api_client.freeform_columns(actual_ffc_object.project_id)
    ffc_names_for_project = [str(ffc.name) for ffc in freeform_columns_for_project]

    if expected_status_code is not None:
        if expected_error_message is None:
            # raises an exception since there is no value passed for expected_error_message
            raise Exception('Value for expected_error_message param is missing')
        else:
            # verify response code and error message in unsuccessful ffc creation
            verify_error_response(actual_response, expected_status_code, expected_error_message)
    else:
        # verify whether created ffc present in project for published ffc, not present for unpublished ffc
        if actual_ffc_object.published:
            assert str(actual_ffc_object.name) in ffc_names_for_project, \
                "Unpublished FFC with name:{} created in project: {}, project ffcs:{}".format(
                    actual_ffc_object.name, actual_ffc_object.project_id, ffc_names_for_project)
        else:
            assert str(actual_ffc_object.name) not in ffc_names_for_project, \
                "Unpublished FFC with name:{} created in project: {}, project ffcs:{}".format(
                    actual_ffc_object.name, actual_ffc_object.project_id, ffc_names_for_project)
        # verify whether response ffc matched with the ffc got from same ffc id.
        assert ld_api_client.get_freeform_column_by_id(actual_response.id).as_dict() == actual_response.as_dict()


def verify_bulk_ffc_values(ld_api_client, lr_id, column_ids, row_ids, expected_cell_values):
    """
    Function to verify if the rows have same bulk of expected values in cell for columns

    :param ld_api_client:LDClient
    :param lr_id: str, LiveReport ID
    :param column_ids: list, List of column Ids
    :param row_ids: list, List of compound ids
    :param expected_cell_values: list, list of value expected for each column
    """

    def assert_cell_values():
        actual_cell_values = get_cell_values_for_rows_and_columns(ld_api_client,
                                                                  livereport_id=lr_id,
                                                                  column_ids=column_ids,
                                                                  row_ids=row_ids)
        # verify if each row has the expected values
        for compound_id in row_ids:
            assert actual_cell_values[compound_id] == expected_cell_values, \
                'Expected cell values {} but got {}'.format(expected_cell_values, actual_cell_values[compound_id])

    wait_until_condition_met(assert_cell_values, retries=3)
