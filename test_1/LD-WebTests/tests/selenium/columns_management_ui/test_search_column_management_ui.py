import pytest

from helpers.change.columns_action import search_and_selecting_column_in_columns_tree
from helpers.change.columns_management_ui import open_add_data_panel
from helpers.flows.columns_tree import search_and_check_column_name_highlight
from helpers.selection.column_tree import COLUMN_TREE_PICKER_SEARCH
from helpers.verification.grid import check_for_butterbar

live_report_to_duplicate = {'livereport_name': 'RPE Test', 'livereport_id': '2048'}


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_search_column_management_ui(selenium):
    """
    Test for searching in Column Management UI:
    1. Duplicates 'RPE Test' LiveReport.
    2. Add a MPO column named 'Restricted FFC' to have a column group in LR.
    3. Open Columns Management UI.
    4. Search for some of the values mentioned:
        - 'PK' -> Check Assay columns with PK highlighted.
        - 'AUC' -> Check only one column gets highlighted.
        - 'FFC' -> Check that all values in the group gets highlighted.
        - 'ID' -> Check that value in Frozen column gets highlighted.
        - 'Lot' -> Check that value in both visible and hidden column gets highlighted.
    5. Search for column that is not in LR and check nothing gets highlighted.

    :param selenium: Selenium Webdriver
    """
    # For Adding MPO column 'Restricted FFC'
    open_add_data_panel(selenium)
    search_and_selecting_column_in_columns_tree(selenium, '(JS Testing) Restricted FFC', COLUMN_TREE_PICKER_SEARCH)
    check_for_butterbar(selenium, notification_text='Adding columns to LiveReport', visible=True)
    check_for_butterbar(selenium, notification_text='Adding columns to LiveReport', visible=False)

    search_and_check_column_name_highlight(selenium,
                                           search_term='PK',
                                           expected=['PK_PO_RAT (AUC)', 'PK_PO_RAT (Absorption)'])
    search_and_check_column_name_highlight(selenium, search_term='AUC', expected=['PK_PO_RAT (AUC)'])
    search_and_check_column_name_highlight(
        selenium,
        search_term='FFC',
        expected=['Restricted FFC Desirability Scores and Number of Missing Inputs', 'Restricted FFC'])
    search_and_check_column_name_highlight(selenium,
                                           search_term='ID',
                                           expected=['ID', 'All IDs', 'CorpID String (CorpID String)'])
    search_and_check_column_name_highlight(selenium,
                                           search_term='Lot',
                                           expected=['Lot Scientist', 'Lot Date Registered'])
    search_and_check_column_name_highlight(selenium, search_term='ABCD', expected=[])
