import pytest

from helpers.change import actions_pane, filter_actions
from helpers.change.columns_action import add_column_by_name
from helpers.change.tile_view import click_property_menu_item, hide_multiple_contiguous_columns_in_tile_view, \
    switch_to_tile_view, sort_tile_by, show_column, select_multiple_tiles
from helpers.flows import add_compound
from helpers.selection.grid import Footer
from helpers.selection.tile_view import TILE_BASED_ON_ID_, SELECTED_TILE_BASED_ON_ID_, TILE_FIELD_NAME_
from helpers.verification.grid import check_for_butterbar, verify_footer_values
from library import dom, wait
from library.utils import is_k8s


@pytest.mark.xfail(not is_k8s(), reason="SS-40265: RMQ issues in Old Jenkins")
@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_footer_values_for_tile_view(selenium):
    """
    verify all the footer values for tile view:

    1. Search compounds by id and verify footer values
    2. Add a column to the lr and verify footer values
    3. Add a filter, filter compounds and verify footer values after the filter
    4. Hide a column and verify footer values
    5. Switch to different types of modes and verify footer values
    :param selenium: Webdriver
    :return:
    """
    switch_to_tile_view(selenium)

    search_keyword = "CHEMBL105*,CHEMBL103*"

    # ----- Search compounds by id and verify footer values ----- #
    actions_pane.open_add_compounds_panel(selenium)
    add_compound.search_by_id(selenium, search_keyword)

    # Wait for butterbars to appear and go away and then verify footer values
    check_for_butterbar(selenium, notification_text='Compound search in progress...')
    check_for_butterbar(selenium, notification_text='Updating LiveReport...', visible=False)
    verify_footer_values(selenium, ({Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(22)}))

    # sorting to make sure the row to be selected is visible on page
    sort_tile_by(selenium, 'ID')
    wait.until_loading_mask_not_visible(selenium)
    first_tile_id_after_sorting = 'CHEMBL103'

    column = "AlogP"
    # ----- Add a column to the lr and verify footer values ----- #
    actions_pane.open_add_data_panel(selenium)
    add_column_by_name(selenium, column)
    # The added column on selenium-testserver are represented by column(column).
    # For e.g. "Alog (AlogP)", "H-Bond Donors (H-Bond Donors)"
    column_name = "{} ({})".format(column, column)

    # This function would check in a way that the column is added to the LR
    show_column(selenium, column_name)
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(22),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(5),
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
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(5),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(1)
        })

    # ----- Hide a column and verify footer values ----- #
    click_property_menu_item(selenium, first_tile_id_after_sorting, column_name, 'Hide Property')
    wait.until_not_visible(selenium, TILE_FIELD_NAME_.format(column_name), text=column_name)
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(22),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(22),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(4),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(2)
        })

    # ----- Select a compound and verify footer values ----- #
    # Select a tile
    dom.click_element(selenium, TILE_BASED_ON_ID_.format(first_tile_id_after_sorting))
    wait.until_visible(selenium, SELECTED_TILE_BASED_ON_ID_.format(first_tile_id_after_sorting))
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(22),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(22),
            Footer.ROW_SELECTED_COUNT_KEY: Footer.ROW_SELECTED_COUNT_VALUE.format(1),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(4),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(2)
        })
    # Deselect the tile
    select_multiple_tiles(selenium, [first_tile_id_after_sorting])

    # ----- Hide all columns and verify footer values(test ss-30202) ----- #
    # hide all columns except one from configure tiles
    hide_multiple_contiguous_columns_in_tile_view(selenium, 'All IDs', 'Lot Scientist')
    # hiding remaining columns
    click_property_menu_item(selenium, first_tile_id_after_sorting, 'ID', 'Hide Property')
    # verify footer values
    verify_footer_values(
        selenium, {
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(0),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(6)
        })

    # ----- Switch to different types of modes and verify footer values ----- #
    actions_pane.toggle_lr_mode(selenium, 'Lot')
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_LOTS_KEY: Footer.ROW_ALL_COUNT_LOTS_VALUE.format(22),
            Footer.ROW_SELECTED_COUNT_KEY: Footer.ROW_SELECTED_COUNT_VALUE.format(0),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(0),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(6)
        })

    actions_pane.toggle_lr_mode(selenium, 'Salt')
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_SALTS_KEY: Footer.ROW_ALL_COUNT_SALTS_VALUE.format(22),
            Footer.ROW_SELECTED_COUNT_KEY: Footer.ROW_SELECTED_COUNT_VALUE.format(0),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(0),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(6)
        })

    actions_pane.toggle_lr_mode(selenium, 'Pose')
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_POSE_KEY: Footer.ROW_ALL_COUNT_POSE_VALUE.format(22),
            Footer.ROW_SELECTED_COUNT_KEY: Footer.ROW_SELECTED_COUNT_VALUE.format(0),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(0),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(6)
        })

    actions_pane.toggle_lr_mode(selenium, 'Lot Salt')
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_LOT_SALTS_KEY: Footer.ROW_ALL_COUNT_LOT_SALTS_VALUE.format(22),
            Footer.ROW_SELECTED_COUNT_KEY: Footer.ROW_SELECTED_COUNT_VALUE.format(0),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(0),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(6)
        })
