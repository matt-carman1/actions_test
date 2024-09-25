"""
Selenium test for hiding multiple columns at once (SS-27056)
"""
import pytest

from helpers.change.grid_columns import select_multiple_columns, scroll_to_column_header
from helpers.flows.grid import hide_columns_selectively, hide_columns_contiguously
from helpers.verification.features_enabled_disabled import verify_menu_items_are_not_visible
from library import dom, simulate

from helpers.change.footer_actions import show_hidden_columns
from helpers.verification.grid import verify_footer_values, verify_columns_not_visible
from helpers.selection.grid import GRID_HEADER_DROPDOWN_MENU

live_report_to_duplicate = {'livereport_name': '5 Compounds 4 Assays', 'livereport_id': '882'}


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_hide_columns(selenium):
    """
    Test hiding multiple columns at once.

    :param selenium: Selenium WebDriver
    """

    # Select multiple columns using ctrl key and hide them
    hide_columns_selectively(selenium, 'Lot Scientist', 'Clearance (undefined)', 'Solubility (undefined)')
    verify_columns_not_visible(selenium, ['Lot Scientist', 'Clearance (undefined)', 'Solubility (undefined)'])
    # Verify the footer values
    verify_footer_values(selenium, {'column_hidden_count': '5 Hidden'})
    # Show the hidden columns by clicking on the footer link
    show_hidden_columns(selenium, 5)
    # Verify hidden columns reappeared
    verify_footer_values(selenium, {'column_all_count': '10 Columns'})

    # Select multiple columns along with the compound structure column
    select_multiple_columns(selenium, 'Compound Structure', 'Lot Scientist', 'Clearance (undefined)')
    column_header = scroll_to_column_header(selenium, 'Clearance (undefined)')
    # Simulate hover on the column header, then click the menu button when it appears
    simulate.hover(selenium, column_header)
    dom.click_element(selenium, GRID_HEADER_DROPDOWN_MENU)
    # Make sure the options for Remove and Hide columns are not visible/available
    verify_menu_items_are_not_visible(selenium, 'Remove', 'Hide')

    # Hide some columns using the shift action
    hide_columns_contiguously(selenium, 'ID', 'STABILITY-PB-PH 7.4 (%Rem@2hr) [%]')
    verify_columns_not_visible(selenium, ['ID', 'Rationale', 'Lot Scientist', 'STABILITY-PB-PH 7.4 (%Rem@2hr) [%]'])
    # Verify footer values
    verify_footer_values(selenium, {'column_hidden_count': '6 Hidden'})
    # Show them by clicking on the link in the footer
    show_hidden_columns(selenium, 6)
    # Verify hidden columns reappeared
    verify_footer_values(selenium, {'column_all_count': '10 Columns'})
