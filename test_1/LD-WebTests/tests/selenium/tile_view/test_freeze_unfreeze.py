import pytest

from helpers.change.tile_view import switch_to_tile_view, click_tile_context_menu_item, sort_tile_by, \
    get_the_position_of_tile_in_tile_view, select_multiple_tiles
from helpers.change.grid import switch_to_grid_view
from helpers.selection.tile_view import FROZEN_TILE
from helpers.selection.grid import GRID_ERROR_NOTIFICATION_LINK
from helpers.verification.element import verify_is_visible, verify_is_not_visible
from helpers.verification.grid import check_for_baconbar
from library import dom, wait

# Set LiveReport to duplicate
live_report_to_duplicate = {'livereport_name': 'RPE Selenium Test LR', 'livereport_id': '2302'}


@pytest.mark.k8s_defect(reason='SS-42624: Fails to freeze 5 tiles to overflow the viewport')
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_freeze_unfreeze(selenium):
    """
    Test for freeze and Unfreeze tiles.
    1. Freeze any tile, Verify its frozen state and is in first position
    2. Unfreeze tile and verify tile retained its original position
    3. Sort on ID column and verify frozen tile position is not changed with respect to sorting
    4. Freeze multiple tiles and switch to grid view to verify 'too many frozen rows' bacon bar
    5. Click on 'Unfreeze all rows' and verify the baconbar is gone

    :param selenium: Selenium Webdriver
    """
    # switch to tile view
    switch_to_tile_view(selenium)

    # ----- Freeze any tile, Verify its frozen state and is in first position ----- #
    tile = 'V039485'
    tile_position_before_freeze = 3

    click_tile_context_menu_item(selenium, tile, 'Freeze')
    wait.until_extjs_loading_mask_not_visible(selenium)
    # Verify tile is in freeze state
    verify_is_visible(selenium, FROZEN_TILE.format(tile))
    # verify position of frozen tile
    assert get_the_position_of_tile_in_tile_view(selenium, tile) == 1, \
        "Frozen tile with ID: {} is not at the first position in the tile view".format(tile)

    # ----- Unfreeze tile and verify tile retained its original position ----- #
    click_tile_context_menu_item(selenium, tile, 'Unfreeze')
    wait.until_extjs_loading_mask_not_visible(selenium)
    # verify tile is in unfreeze state
    verify_is_not_visible(selenium, FROZEN_TILE.format(tile))
    # verify tile position is retained after unfreeze
    assert get_the_position_of_tile_in_tile_view(selenium, tile) == tile_position_before_freeze, \
        "Tile with ID: {} didn't retain it's original position after unfreeze".format(tile)

    # Freeze tile
    tile_to_verify_position_after_sorting = 'V041630'
    click_tile_context_menu_item(selenium, tile_to_verify_position_after_sorting, 'Freeze')
    wait.until_extjs_loading_mask_not_visible(selenium)
    # ----- Sort on ID column and verify frozen tile position is not changed with respect to sorting ----- #
    sort_tile_by(selenium, 'ID')
    assert get_the_position_of_tile_in_tile_view(selenium, tile_to_verify_position_after_sorting) == 1, \
        "Frozen tile with ID: {} is not at the first position in the tile view after sorting".format(
            tile_to_verify_position_after_sorting)

    # ----- Freeze multiple tiles & switch to grid view to verify 'too many frozen rows' butterbar ----- #
    tiles_to_freeze = ['V039485', 'V041630', 'V036300', 'V038027', 'V040929', 'V041660']
    select_multiple_tiles(selenium, tiles_to_freeze)
    click_tile_context_menu_item(selenium, tiles_to_freeze[5], 'Freeze')
    wait.until_extjs_loading_mask_not_visible(selenium)
    # Switch to grid view
    switch_to_grid_view(selenium)
    # Verify 'too many frozen rows' butterbar is visible
    check_for_baconbar(selenium,
                       notification_text='There are too many frozen rows to enable scrolling\n[Unfreeze all rows]',
                       visible=True)
    # Click 'Unfreeze all rows' to unfreeze
    dom.click_element(selenium, GRID_ERROR_NOTIFICATION_LINK, text="Unfreeze all rows")
    # Verify 'too many frozen rows' butterbar is gone
    check_for_baconbar(selenium,
                       notification_text='There are too many frozen rows to enable scrolling\n[Unfreeze all rows]',
                       visible=False)
