import pytest

from helpers.change.actions_pane import close_add_data_panel
from helpers.change.columns_management_ui import open_column_mgmt_panel, hide_columns_selectively, show_columns_selectively
from helpers.verification import grid

live_report_to_duplicate = {'livereport_name': '5 Compounds 4 Assays', 'livereport_id': '882'}


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_hide_column_menu_item_helper(selenium):
    """
    Testing hide_column_menu_item function to check if it works with all kinds of menu options
    including sub menus. This is a short and simple test.

    :param selenium: Webdriver
    :return: None
    """
    assay_column = "STABILITY-PB-PH 7.4 (%Rem@2hr) [%]"
    id_column = "ID"

    # ----- Testing hide_column_menu_item helper ----- #

    # Try opening and clicking "ID" sub menu item inside Columns menu item which will hide the "ID" column
    open_column_mgmt_panel(selenium)

    hide_columns_selectively(selenium, 'ID')
    grid.verify_footer_values(selenium, {'column_all_count': '7 Columns', 'column_hidden_count': '3 Hidden'})

    show_columns_selectively(selenium, 'ID')
    grid.verify_footer_values(selenium, {'column_all_count': '8 Columns', 'column_hidden_count': '2 Hidden'})

    close_add_data_panel(selenium)
