import pytest

from helpers.change.filter_actions import remove_all_filters
from helpers.change.grid_row_actions import pick_row_context_menu_item, select_rows_and_pick_context_menu_item
from helpers.verification.filter import verify_added_columns_in_filter_panel
from helpers.verification.grid import verify_footer_values

live_report_to_duplicate = {'livereport_name': '4 Compounds 3 formulas', 'livereport_id': '890'}


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_set_filter_on_compounds(selenium):
    """
    Test "Filter to Selected Compounds" option present in row context menu with
    single and multiple compounds selected

    :param selenium: selenium webdriver

    """

    # Open row context menu item of a single selected compounds
    pick_row_context_menu_item(selenium, 'V035625', 'Filter to selected')

    # To verify that All Ids filter has been added
    verify_added_columns_in_filter_panel(selenium, ["All IDs"])

    # Verify footer values after the filter is applied
    verify_footer_values(
        selenium, {
            'row_all_count': '4 Total Compounds',
            'row_filtered_count': '1 After Filter',
            'row_selected_count': '1 Selected',
            'column_all_count': '11 Columns',
            'column_hidden_count': '2 Hidden'
        })

    # Remove all applied filters
    remove_all_filters(selenium)

    # Open row context menu item for multiple selected compounds
    select_rows_and_pick_context_menu_item(selenium, ['V035626', 'V035624'], 'Filter to selected')

    # To verify that All Ids filter has been added
    verify_added_columns_in_filter_panel(selenium, ["All IDs"])

    # Verify footer values after the filter is applied
    verify_footer_values(
        selenium, {
            'row_all_count': '4 Total Compounds',
            'row_filtered_count': '3 After Filter',
            'row_selected_count': '3 Selected',
            'column_all_count': '11 Columns',
            'column_hidden_count': '2 Hidden'
        })
