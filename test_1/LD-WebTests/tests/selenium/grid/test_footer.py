from helpers.selection.grid import GRID_ROW_CHECKBOX_, GRID_ROW_ID_, Footer
import pytest

from library import dom, wait
from library.utils import is_k8s
from helpers.verification import grid
from helpers.change import actions_pane, columns_action, grid_columns, \
    filter_actions, grid_column_menu
from helpers.flows import add_compound


@pytest.mark.xfail(not is_k8s(), reason="SS-40265: RMQ issues in Old Jenkins")
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_verify_footer_values(selenium):
    """
    verify all the footer values:
    1. Verify footer values in different modes viz Compound, lot, salt.
        [NOTE: RPE and Pose modes are not tested. Leaving it for Kenny to use
        the helpers for his RPE Test
    2. Verify footer values for hidden elements: rows or columns.
    3. Verify footer values for selected rows
    4. Verify footer values for filters
    :param selenium: Webdriver
    :return:
    """
    column = "AlogP"
    search_keyword = "CHEMBL105*,CHEMBL103*"

    # SEARCH COMPOUNDS BY ID AND VERIFY FOOTER VALUES
    actions_pane.open_add_compounds_panel(selenium)
    add_compound.search_by_id(selenium, search_keyword)

    # Wait for butterbars to appear and go away and then verify footer values
    grid.check_for_butterbar(selenium, notification_text='Compound search in progress...')
    grid.check_for_butterbar(selenium, notification_text='Updating LiveReport...', visible=False)
    grid.verify_footer_values(selenium, ({'row_all_count': '22 Total Compounds'}))

    # ADD A COLUMN TO THE LR AND VERIFY FOOTER VALUES
    actions_pane.open_add_data_panel(selenium)
    columns_action.add_column_by_name(selenium, column)
    # The added column on selenium-testserver are represented by column(column).
    # For e.g. "Alog (AlogP)", "H-Bond Donors (H-Bond Donors)"
    column_name = "{} ({})".format(column, column)

    # This function would check in a way that the column is added to the LR
    grid_columns.scroll_to_column_header(selenium, column_name)
    grid.verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(22),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(6),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(1)
        })

    # ADD A FILTER, FILTER COMPOUNDS AND VERIFY FOOTER VALUES AFTER THE FILTER
    # Open the Filter Panel and Clear filters if there were some leftover ones
    filter_actions.remove_all_filters(selenium)
    # Add a filter from the dropdown
    filter_actions.add_filter(selenium, column_name)
    wait.until_loading_mask_not_visible(selenium)
    grid.verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(22),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(22),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(6),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(1)
        })

    # HIDE A COLUMN AND VERIFY FOOTER VALUES
    grid_column_menu.click_column_menu_item(selenium, column_name, 'Hide')
    wait.until_not_visible(selenium, '.grid-header-cell[title="{}"]'.format(column_name))
    grid.verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(22),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(22),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(5),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(2)
        })

    # SELECT A COMPOUND AND VERIFY FOOTER VALUES
    # sorting to make sure the row to be selected is visible on page
    grid_column_menu.sort_grid_by(selenium, 'ID')
    wait.until_loading_mask_not_visible(selenium)

    # Select a row
    row_id = 'CHEMBL103'
    dom.click_element(selenium, GRID_ROW_CHECKBOX_.format(row_id))

    wait.until_visible(selenium, GRID_ROW_ID_.format(row_id) + ' .selected-cell.left-border')
    grid.verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(22),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(22),
            Footer.ROW_SELECTED_COUNT_KEY: Footer.ROW_SELECTED_COUNT_VALUE.format(1),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(5),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(2)
        })
    # Deselect the row
    dom.click_element(selenium, GRID_ROW_CHECKBOX_.format(row_id))

    # SWITCH TO ROW PER COMPOUND LOT MODE AND VERIFY FOOTER VALUES
    actions_pane.toggle_lr_mode(selenium, 'Lot')
    grid.verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_LOTS_KEY: Footer.ROW_ALL_COUNT_LOTS_VALUE.format(22),
            Footer.ROW_SELECTED_COUNT_KEY: Footer.ROW_SELECTED_COUNT_VALUE.format(0),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(5),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(2)
        })
