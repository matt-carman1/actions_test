import pytest

from helpers.selection.grid import GRID_HEADER_SELECTOR_, GRID_ROW_CHECKBOX_, GRID_ROW_ID_, SELECTED_CELL_LEFT_BORDER, \
    Footer
from helpers.verification.grid import check_for_butterbar, verify_footer_values
from library import dom, wait
from helpers.change import actions_pane, columns_action, grid_columns, filter_actions, grid_column_menu
from helpers.flows import add_compound
from library.utils import is_k8s


@pytest.mark.xfail(not is_k8s(), reason="SS-40265: RMQ issues in Old Jenkins")
@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_footer_values(selenium):
    """
    verify all the footer values:

    1. Search compounds by id and verify footer values
    2. Add a column to the lr and verify footer values
    3. Add a filter, filter compounds and verify footer values after the filter
    4. Hide a column and verify footer values
    5. Select a compound and verify footer values
    6. Switch to different types of modes and verify footer values

    :param selenium: Webdriver
    :return:
    """
    column = "AlogP"
    search_keyword = "CHEMBL105*,CHEMBL103*"

    # ----- Search compounds by id and verify footer values ----- #
    actions_pane.open_add_compounds_panel(selenium)
    add_compound.search_by_id(selenium, search_keyword)

    # Wait for butterbars to appear and go away and then verify footer values
    check_for_butterbar(selenium, notification_text='Compound search in progress...')
    check_for_butterbar(selenium, notification_text='Updating LiveReport...', visible=False)
    verify_footer_values(selenium, ({Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(22)}))

    # ----- Add a column to the lr and verify footer values ----- #
    actions_pane.open_add_data_panel(selenium)
    columns_action.add_column_by_name(selenium, column)
    # The added column on selenium-testserver are represented by column(column).
    # For e.g. "Alog (AlogP)", "H-Bond Donors (H-Bond Donors)"
    column_name = "{} ({})".format(column, column)

    # This function would check in a way that the column is added to the LR
    grid_columns.scroll_to_column_header(selenium, column_name)
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(22),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(6),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(1)
        })

    # ----- Add a filter, filter compounds and verify footer values after the filter ----- #
    # Open the Filter Panel and Clear filters if there were some leftover ones
    filter_actions.remove_all_filters(selenium)
    # Add a filter from the dropdown
    filter_actions.add_filter(selenium, column_name)
    wait.until_loading_mask_not_visible(selenium)
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(22),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(22),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(6),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(1)
        })

    # ----- Hide a column and verify footer values ----- #
    grid_column_menu.click_column_menu_item(selenium, column_name, 'Hide')
    wait.until_not_visible(selenium, GRID_HEADER_SELECTOR_.format(column_name))
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(22),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(22),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(5),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(2)
        })

    # ----- Select a compound and verify footer values ----- #
    # sorting to make sure the row to be selected is visible on page
    grid_column_menu.sort_grid_by(selenium, 'ID')
    wait.until_loading_mask_not_visible(selenium)
    # Select a row
    dom.click_element(selenium, GRID_ROW_CHECKBOX_.format('CHEMBL103'))
    wait.until_visible(selenium, GRID_ROW_ID_.format('CHEMBL103 ') + SELECTED_CELL_LEFT_BORDER)
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(22),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(22),
            Footer.ROW_SELECTED_COUNT_KEY: Footer.ROW_SELECTED_COUNT_VALUE.format(1),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(5),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(2)
        })
    # Deselect the row
    dom.click_element(selenium, GRID_ROW_CHECKBOX_.format('CHEMBL103'))

    # ----- Switch to different types of modes and verify footer values ----- #
    actions_pane.toggle_lr_mode(selenium, 'Lot')
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_LOTS_KEY: Footer.ROW_ALL_COUNT_LOTS_VALUE.format(22),
            Footer.ROW_SELECTED_COUNT_KEY: Footer.ROW_SELECTED_COUNT_VALUE.format(0),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(5),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(2)
        })

    actions_pane.toggle_lr_mode(selenium, 'Salt')
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_LOT_SALTS_KEY: Footer.ROW_ALL_COUNT_SALTS_VALUE.format(22),
            Footer.ROW_SELECTED_COUNT_KEY: Footer.ROW_SELECTED_COUNT_VALUE.format(0),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(5),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(2)
        })

    actions_pane.toggle_lr_mode(selenium, 'Pose')
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_POSE_KEY: Footer.ROW_ALL_COUNT_POSE_VALUE.format(22),
            Footer.ROW_SELECTED_COUNT_KEY: Footer.ROW_SELECTED_COUNT_VALUE.format(0),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(5),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(2)
        })

    actions_pane.toggle_lr_mode(selenium, 'Lot Salt')
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_LOT_SALTS_KEY: Footer.ROW_ALL_COUNT_LOT_SALTS_VALUE.format(22),
            Footer.ROW_SELECTED_COUNT_KEY: Footer.ROW_SELECTED_COUNT_VALUE.format(0),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(5),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(2)
        })
