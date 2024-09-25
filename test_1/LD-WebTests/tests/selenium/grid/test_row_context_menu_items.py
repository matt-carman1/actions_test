"""
Selenium test to verify row context menu items
"""

import pytest

from helpers.change.grid_row_actions import select_row
from helpers.verification.grid import verify_row_menu_items, verify_rows_selected

live_report_to_duplicate = {'livereport_name': '3 Compounds 2 Poses', 'livereport_id': '883'}


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_row_context_menu_items(selenium):
    """
     Test for verify row context menu items.

     1. Select a row and verify row context menu items
     2. Select Multiple Non-contiguous rows and verify context menu items
     3. Select Contiguous rows and verify row context menu items

     :param selenium: Selenium WebDriver
     """
    # ------- Select a row and verify row context menu items ------- #
    select_row(selenium, 'CRA-035000')
    # Verify that the row is selected
    verify_rows_selected(selenium, ['CRA-035000'])
    # verify row context menu items for single compound
    verify_row_menu_items(selenium, 'CRA-035000', 'CRA-035000 SELECTED', 'Use in', 'Filter to selected',
                          'Set alignment...', 'Comment', 'Hide', 'Freeze', 'Remove', 'Copy to', 'Export as')

    # ------- Select Multiple Non-contiguous rows and verify context menu items ------- #
    select_row(selenium, 'CRA-035002')
    # Verify that the rows are selected
    verify_rows_selected(selenium, ['CRA-035000', 'CRA-035002'])
    # verify row context menu items for multiple non-contiguous compounds selection
    verify_row_menu_items(selenium, 'CRA-035002', '2 COMPOUNDS SELECTED', 'Filter to selected', 'Comment', 'Hide',
                          'Freeze', 'Remove', 'Copy to', 'Export as')

    # ------- Select Contiguous rows and verify row context menu items ------- #
    # selecting 2nd row to make contiguous selection
    select_row(selenium, 'CRA-035001')
    # Verify that the rows are selected
    verify_rows_selected(selenium, ['CRA-035000', 'CRA-035001', 'CRA-035002'])
    # verify row context menu items for multiple contiguous compounds selection
    verify_row_menu_items(selenium, 'CRA-035000', '3 COMPOUNDS SELECTED', 'Filter to selected', 'Comment', 'Hide',
                          'Freeze', 'Remove', 'Copy to', 'Export as')
