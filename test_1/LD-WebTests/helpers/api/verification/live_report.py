from itertools import product

from helpers.api.actions.row import get_live_report_rows
from helpers.api.actions.livereport import execute_live_report
from helpers.api.extraction.grid import get_cell_values_for_rows_and_columns
from helpers.api.extraction.livereport import get_live_report_column_names, get_live_report_compound_ids
from library.api.wait import wait_until_condition_met
from requests import RequestException
from ldclient import LDClient


def verify_live_report_columns(ldclient, lr_id, expected_column_count):
    """
    Verifying number of columns in live report

    :param ldclient: LDClient, LDClient
    :param lr_id: str, ID of the Live report
    :param expected_column_count: int, expected number of columns present in Live report
    """

    # creating callback function to get columns
    def get_columns():
        columns_dict = get_live_report_column_names(ldclient, lr_id)
        # validating column count
        assert expected_column_count == len(columns_dict), "Expected column count:{}, Actual column count:{}".format(
            expected_column_count, len(columns_dict))

    wait_until_condition_met(get_columns)


def verify_live_report_compounds(ldclient, lr_id, expected_compound_ids):
    """
    Verifying livereport compound ids

    :param ldclient: LDClient, LDClient
    :param lr_id: str, ID of the Live report
    :param expected_compound_ids: int, expected number of columns present in Live report
    """

    # validating whether compounds added to livereport
    def get_rows():
        rows = get_live_report_rows(ldclient, lr_id)
        assert sorted(rows) == sorted(expected_compound_ids), \
            "Live report row ids:{}, Expected row ids:{}".format(rows, expected_compound_ids)

    wait_until_condition_met(get_rows)


def verify_visible_row_count(ldclient: LDClient,
                             lr_id: str,
                             expected_visible_row_count: int,
                             should_execute_live_report: bool = True):
    """
    Asserts the current LR visible row count with expected visible row count.

    :param ldclient: ldclient object
    :param lr_id: LiveReport ID
    :param expected_visible_row_count: int, Expected number of visible rows
    :param should_execute_live_report: Whether or not we should manually execute the LiveReport.
        NOTE(badlato): For most cases, this should be False.  We want to test for cache invalidation bugs!
    """

    def assert_visible_row_count():
        if should_execute_live_report:
            response = execute_live_report(ldclient, lr_id)
            actual_visible_row_count = response['stats']['visible_rows']
        else:
            actual_visible_row_count = len(ldclient.live_report_rows(live_report_id=lr_id))
        assert actual_visible_row_count == expected_visible_row_count, \
            'Expected {} visible rows in LR, but got {} visible rows in LR'.format(
                expected_visible_row_count,
                actual_visible_row_count)

    wait_until_condition_met(condition_function=assert_visible_row_count)


def verify_execute_live_report_response(response, lr_id, expected_column_count=None, expected_row_count=None):
    """
    Verifies execute live report response.

    :param response: RequestException or JSON, RequestException for non existed lr, JSON for  existed lr
    :param lr_id: str, id of the LR
    :param expected_column_count: int, expected number of columns
    :param expected_row_count: int, expected number of rows
    """
    if expected_row_count is not None and expected_column_count is not None:
        # validating response for existed lr id execution
        assert response, "Metadata of the livereport is None."
        assert response['live_report_id'] == lr_id, "Livereport ID in metadata doesn't match with created Livereport id"
        assert not response['version'] == 0, "Livereport version is 0"

        # verifying number of columns
        assert len(response['columns']) == expected_column_count, "Expected number of column: {}, But got: {}".format(
            expected_column_count, len(response.get['columns']))
        # verify number of rows
        assert len(response['rows']) == expected_row_count, "Expected number of rows: {}, But got : {}".format(
            expected_row_count, len(response.get['rows']))
    else:
        # validating error for non existed lr execution, should get RequestException.
        assert isinstance(response, RequestException), "LR is executed for negative LR id : {}".format(lr_id)
        assert str(response.response) == '<Response [400]>', "Response code is not matching with expected."


def verify_compound_ids(ldclient, lr_id, expected_compound_ids):
    """
    Retrieves LiveReport Metadata and
    verifies that the actual compound ids from metadata are same as expected compound ids.

    :param ldclient: LDClient, ldclient object
    :param lr_id: str, LiveReport ID
    :param expected_compound_ids: list, List of expected filtered compound ids
    """

    def assert_compound_ids():
        actual_compound_ids = get_live_report_compound_ids(ldclient, lr_id)
        assert sorted(actual_compound_ids) == sorted(expected_compound_ids), \
            'Expected {} but got {}'.format(expected_compound_ids, actual_compound_ids)

    wait_until_condition_met(condition_function=assert_compound_ids)


def wait_until_models_successfully_run(ldclient, lr_id, addable_col_ids, row_keys):
    """
    Used to check if given columns and rows in a Live Report have values in their cells.
    This method will run until all Columns have atleast 1 value returned or until we've retried 50 times.
    This doesn't check if the actual content of the values, just waits until there is a 'values' field in a cell,
    meaning that the model successfully returned.

    :param ldclient: LDClient, ldclient object
    :param lr_id: str, LiveReport ID
    :param addable_col_ids: List, List of model addable column IDs to check for values
    :param row_keys: list, List of LR row keys to check for values
    """
    wait_until_condition_met(lambda: verify_lr_has_values_in_rows_and_columns(
        ldclient=ldclient, lr_id=lr_id, row_keys=row_keys, addable_col_ids=addable_col_ids),
                             retries=50,
                             interval=2000)


def verify_lr_has_values_in_rows_and_columns(ldclient,
                                             lr_id,
                                             addable_col_ids=None,
                                             row_keys=None,
                                             list_of_row_key_and_column_id_pairs=None):
    """
    Verifies that every row/column combination has a value in it's cell.
    Please pass in either a list of tuples of (row_key, addable_col_id) that you want to check
    OR a list of addable_col_ids and a list of row_keys

    :param ldclient: LDClient, ldclient object
    :param lr_id: str, LiveReport ID
    :param addable_col_ids: List, List of Addable Column IDs to check -- Ignored if list_of_row_key_and_column_id_pairs has a value
    :param row_keys: List, List of Row Keys to check -- Ignored if list_of_row_key_and_column_id_pairs has a value
    :param list_of_row_key_and_column_id_pairs: List, A list of of tuples of (row_key, addable_col_id) to check if they have value
    """

    assert (list_of_row_key_and_column_id_pairs is None) != (row_keys is None or addable_col_ids is None), \
        "Specify either list_of_row_key_and_column_id_pairs or row_keys/addable_col_ids"
    if list_of_row_key_and_column_id_pairs is None:
        list_of_row_key_and_column_id_pairs = list(product(row_keys, addable_col_ids))

    executed_lr = ldclient.execute_live_report(lr_id)
    row_key_and_column_id_pairs_to_compare = []
    for row_key, addable_col_id in list_of_row_key_and_column_id_pairs:
        row_and_column_has_value = contains_values_in_lr_cell(executed_lr, row_key, addable_col_id)
        if row_and_column_has_value:
            row_key_and_column_id_pairs_to_compare.append((row_key, addable_col_id))
    assert list_of_row_key_and_column_id_pairs == row_key_and_column_id_pairs_to_compare


def verify_lr_has_no_values(ldclient, lr_id, addable_col_ids, row_keys):
    """
    Verify the given rows and columns in the LR has no values

    :type ldclient: LDClient
    :type addable_col_ids: list of str
    :type lr_id: str
    :type row_keys: list of str
    """
    executed_lr = ldclient.execute_live_report(lr_id)
    for row_key, col_id in product(row_keys, addable_col_ids):
        assert not contains_values_in_lr_cell(executed_lr, row_key, col_id), \
            f'{row_key}, {col_id} has value'


def contains_values_in_lr_cell(live_report, row_key, addable_col_id):
    """
    Checks if the LR contains a value in the cell indicated by row and column
    :param live_report: LiveReport, LiveReport with value to check
    :param row_key: str, Row key for row in LR
    :param addable_col_id: str, Column ID for column in LR
    :return: bool, Whether there is a value in the LR Cell. NOTE: Empty string counts as a value
    """
    value = live_report.get('rows', {}).get(row_key, {}).get('cells', {}).get(addable_col_id, {}).get('values', {})
    return bool(value)


def verify_column_values_for_compounds(ldclient, livereport_id, column_ids, expected_values):
    """
    Function to verify the values present on specific column ids against specific row_ids on the LR with expected_values

    :param ldclient: LDClient object
    :param livereport_id: str, LiveReport ID
    :param column_ids: list, List of addable column ids: Format: [column_id1, column_id2]
    :param expected_values: dict, Expected values. Format {row_id1 : [column_id1_value, column_id2_value]}
    """
    row_ids = expected_values.keys()

    def verify_values():
        actual_values = get_cell_values_for_rows_and_columns(ldclient,
                                                             livereport_id=livereport_id,
                                                             column_ids=column_ids,
                                                             row_ids=row_ids)
        for row_id in row_ids:
            assert actual_values[row_id] == expected_values[row_id], \
                'Expected column values {} for {} but got {}'.format(expected_values[row_id],
                                                                     row_id,
                                                                     actual_values[row_id])

    wait_until_condition_met(condition_function=verify_values, retries=10, interval=2000)


def verify_live_report_column_names(ld_client, live_report_id, expected_column_names):
    """
    Function to verify if the LiveReport column names

    :param ld_client: LDClient object
    :param live_report_id: str, str, ID of the Live report
    :param expected_column_names: list, expected list of column names
    """

    def assert_column_names():
        # Get column names in live report
        actual_column_names = get_live_report_column_names(ld_client, live_report_id)
        # verify if the live report has same column names as that of the template
        assert sorted(expected_column_names) == sorted(
            actual_column_names), "columns in template and applied live report are " \
                                  "not same"

    wait_until_condition_met(condition_function=assert_column_names)


def verify_column_names_and_compound_ids(ld_client, live_report_id, expected_column_names, expected_compound_ids):
    """
    Function to verify given LiveReport column names and compound ids

    :param ld_client: LDClient object
    :param live_report_id: str, id of the live report to which template is applied
    :param expected_column_names: list, expected list of column names in LR
    :param expected_compound_ids: list, expected list of compound ids in LR
    """

    # verify if live report has column names as that of expected list of compounds
    verify_live_report_column_names(ld_client, live_report_id, expected_column_names)
    # verify if live report has compounds as of expected list of compounds
    verify_compound_ids(ld_client, live_report_id, expected_compound_ids)
