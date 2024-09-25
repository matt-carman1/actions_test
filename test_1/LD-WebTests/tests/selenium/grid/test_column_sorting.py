"""
Selenium test for Column Sorting
"""
import pytest

from helpers.change.grid_column_menu import sort_grid_by, click_column_menu_item
from helpers.change.columns_action import add_column_by_name
from helpers.change.actions_pane import open_add_data_panel
from helpers.change.grid_columns import scroll_to_column_header
from helpers.flows.grid import hide_columns_selectively
from helpers.verification.grid import verify_column_contents
from helpers.verification.element import verify_is_visible
from helpers.selection.grid import GRID_HEADER_CELL, GRID_COLUMN_HEADER_SORT_ICON_, GRID_ROWS_CONTAINER
from library.scroll import wheel_element
from library import dom, simulate, wait

live_report_to_duplicate = {'livereport_name': '5 Compounds 4 Assays', 'livereport_id': '882'}
# {'Compound Structure': '1228', 'Solubility (undefined)': '831', 'CYP450 2C19-LCMS (%INH)': '923',
#  'STABILITY-PB-PH 7.4 (%Rem@2hr)': '112', }
column_ids_subset = ['1228', '1226', '112', '831', '923']


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_column_sorting(selenium):
    """
    Test sorting on numeric and text columns, using double click and column menu.

    :param selenium: Selenium WebDriver
    """

    # Columns being used
    column_stability = 'STABILITY-PB-PH 7.4 (%Rem@2hr) [%]'
    column_solubility = 'Solubility (undefined)'
    column_appearance = 'Lot Appearance'
    column_cyp = 'CYP450 2C19-LCMS (%INH) [%]'

    # Hiding columns to improve verification speed
    hide_columns_selectively(selenium, 'Rationale', 'Lot Scientist', 'ID')

    # ----- Testing sort by double clicking ----- #

    # Sort by double click for ascending order, check column content and arrow in header
    simulate.double_click(dom.get_element(selenium, GRID_HEADER_CELL, text=column_stability))
    verify_column_contents(selenium, column_stability, ['59', '77', '88', '100', ''])
    verify_is_visible(selenium, GRID_COLUMN_HEADER_SORT_ICON_.format('ASC'))

    # Sort by double clicking again for descending order on a text column
    simulate.double_click(dom.get_element(selenium, GRID_HEADER_CELL, text=column_stability))
    verify_column_contents(selenium, column_stability, ['100', '88', '77', '59', ''])
    verify_is_visible(selenium, GRID_COLUMN_HEADER_SORT_ICON_.format('DESC'))

    # ----- Testing sort by right-click column menu ----- #
    sort_grid_by(selenium, column_solubility)
    verify_column_contents(selenium, column_solubility, ['1', '203', '264', '500', ''])

    # ----- Testing sort on text column ----- #
    # Adding Lot Appearance column to LR
    open_add_data_panel(selenium)
    add_column_by_name(selenium, column_appearance)
    # Sort descending by right-click column menu
    sort_grid_by(selenium, column_appearance, sort_ascending=False)

    # NOTE (pradeep): Until SS-38303 is fixed, the `column_appearance` column remains in a pending state.
    # I'm adding a hack (temporarily) to forcefully paginate the column by slightly scrolling the grid.
    grid_body = dom.get_element(selenium, GRID_ROWS_CONTAINER)
    wheel_element(selenium, grid_body, 1, horizontal=False)

    verify_column_contents(selenium, column_appearance, [
        'yellowish powder', 'yellow crystalline solid', 'off-white powder\noff-white powder\noff-white powder',
        'crystalline yellowish powder', ''
    ])

    # ----- Testing Secondary Sort (Add to Sort) ----- #
    # Sorting on primary column
    sort_grid_by(selenium, column_cyp)
    # Add to Sort, descending
    click_column_menu_item(selenium, column_solubility, 'Sort', 'Add to Sort, Descending')
    wait.until_live_report_loading_mask_not_visible(selenium)
    verify_column_contents(selenium, column_solubility, ['203', '1', '500', '264', ''])
    verify_is_visible(selenium, GRID_COLUMN_HEADER_SORT_ICON_.format('DESC[data-sortpriority="2"]'))

    # Sorting again on primary column
    sort_grid_by(selenium, column_cyp)
    # Shift + double-click to add to sort (ascending)
    element = scroll_to_column_header(selenium, column_appearance)
    simulate.double_click(element, shift_key_held_during_double_click=True)
    verify_column_contents(selenium, column_appearance, [
        'yellow crystalline solid', 'yellowish powder', 'crystalline yellowish powder',
        'off-white powder\noff-white powder\noff-white powder', ''
    ])
    verify_is_visible(selenium, GRID_COLUMN_HEADER_SORT_ICON_.format('ASC[data-sortpriority="2"]'))
