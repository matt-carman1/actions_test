import time

import pytest

from helpers.change.tile_view import switch_to_tile_view, select_multiple_tiles
from helpers.selection.tile_view import TILE_HEADER
from helpers.verification.tile_view import verify_tile_menu_items, verify_selected_tile_ids
from library import dom

live_report_to_duplicate = {'livereport_name': 'Test Reactants - Halides', 'livereport_id': '2554'}


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_tile_context_menu_items(selenium):
    """
    Test for verify tile context menu items.

    1. Select a tile and verify tile context menu items
    2. Select Multiple Non-contiguous tiles and verify context menu items
    3. Select Contiguous tiles and verify context menu items

    :param selenium: Selenium WebDriver
    """
    switch_to_tile_view(selenium)
    # ------- Select a tile and verify tile context menu items ------- #
    # select tile
    dom.click_element(selenium, TILE_HEADER, text='V055824', exact_text_match=True)
    verify_selected_tile_ids(selenium, 'V055824')
    # verify tile context menu items for single compound
    verify_tile_menu_items(selenium, 'V055824', 'V055824 SELECTED', 'Use in', 'Filter to selected', 'Set alignment...',
                           'Comment', 'Hide', 'Freeze', 'Remove', 'Copy to', 'Export as')

    # ------- Select Multiple Non-contiguous tiles and verify context menu items ------- #
    # selecting 3rd tile to make non contiguous tile selection
    select_multiple_tiles(selenium, ['V055826'])
    time.sleep(1)
    verify_selected_tile_ids(selenium, 'V055824', 'V055826')
    # verify tile context menu items for multiple non-contiguous compounds selection
    verify_tile_menu_items(selenium, 'V055826', '2 COMPOUNDS SELECTED', 'Filter to selected', 'Comment', 'Hide',
                           'Freeze', 'Remove', 'Copy to', 'Export as')

    # ------- Select Contiguous tiles and verify tile context menu items ------- #
    # selecting 2nd tile to make contiguous selection
    select_multiple_tiles(selenium, ['V055825'])
    time.sleep(1)
    verify_selected_tile_ids(selenium, 'V055824', 'V055825', 'V055826')
    # verify tile context menu items for multiple contiguous compounds selection
    verify_tile_menu_items(selenium, 'V055824', '3 COMPOUNDS SELECTED', 'Filter to selected', 'Comment', 'Hide',
                           'Freeze', 'Remove', 'Copy to', 'Export as')
