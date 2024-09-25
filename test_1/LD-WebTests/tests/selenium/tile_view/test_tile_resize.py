import pytest

from helpers.change.actions_pane import open_add_data_panel, close_add_data_panel
from helpers.change.columns_action import add_column_by_name
from helpers.change.grid import switch_to_grid_view
from helpers.change.tile_view import switch_to_tile_view, show_column, hide_column, increase_tile_size
from helpers.selection.general import MENU_ITEM
from helpers.selection.tile_view import TILE_VIEW_TILE, TILE_VIEW_COLUMN
from helpers.verification import element
from library import dom, wait

from library.simulate import right_click

# Set name of LiveReport that will be duplicated
live_report_to_duplicate = {'livereport_name': '4 Compounds 3 Formulas', 'livereport_id': '890'}


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_tile_resize(selenium):
    """
    NOTE: Tile height is dependent on viewport size, so expected height values are according to 1366 x 768 (jenkins)
    NOTE: Browsers have different heights for default elements such as button bars. This results in a slightly
          different tile height across browsers: for example, FF is showing 1px more than Chrome.
    """
    # Open tile view
    switch_to_tile_view(selenium)

    # Get the tile
    tile = _get_tile(selenium)
    wait.until_visible(tile, TILE_VIEW_COLUMN, 'Lot Scientist')

    base_low = 276
    base_high = 338

    # Get initial tile height
    tile_height = int(tile.size.get('height'))
    assert base_low <= tile_height <= base_high

    # Open tile column context menu
    column = dom.get_element(tile, TILE_VIEW_COLUMN, 'Lot Scientist')
    right_click(column)

    # Hide the column
    dom.click_element(selenium, MENU_ITEM, 'Hide Property')
    element.verify_is_not_visible(tile, TILE_VIEW_COLUMN, 'Lot Scientist')

    # Get new tile height. Should be less than initial height.
    tile_height = int(tile.size.get('height'))
    difference = -31
    assert base_low + difference <= tile_height <= base_high + difference

    # Add an image column
    open_add_data_panel(selenium)
    image_column = '[Image] Sample - 2 (Icon)'
    add_column_by_name(selenium, image_column)
    close_add_data_panel(selenium)

    # Show the image column
    show_column(selenium, image_column)

    # the tile may have been refreshed in the DOM, get it again
    tile = _get_tile(selenium)

    # Verify the image column is visible, then check the tile height
    element.verify_is_visible(tile, TILE_VIEW_COLUMN, image_column)
    # Image column is 2px higher than regular columns
    tile_height = int(tile.size.get('height'))
    # For some reason, headless mode produces 2px lower here, so the lower range is wider here.
    difference = 11
    assert base_low + difference <= tile_height <= base_high + difference

    # Hide the image column and check for the tile height
    hide_column(selenium, image_column)

    # the tile may have been refreshed in the DOM, get it again
    tile = _get_tile(selenium)
    element.verify_is_not_visible(tile, TILE_VIEW_COLUMN, image_column)
    tile_height = int(tile.size.get('height'))
    difference = -31
    assert base_low + difference <= tile_height <= base_high + difference

    # Increase the size of the tiles
    # This should bring the tile height back to about the original size
    increase_tile_size(selenium)

    # Get the new tile height to compare later
    tile_height = int(tile.size.get('height'))
    difference = 0
    assert base_low + difference <= tile_height <= base_high + difference

    # Switch to grid view, then switch back to tile view
    switch_to_grid_view(selenium)
    switch_to_tile_view(selenium)

    # Get the tile again, since the element was destroyed when we switched views
    tile = _get_tile(selenium)

    # Make sure the tile height remains at the same increased size
    tile_height_after_switching = int(tile.size.get('height'))
    assert tile_height == tile_height_after_switching


def _get_tile(driver):
    """
    Get the tile from the DOM. Extracted since we do it more than three times in the test

    :param driver: webdriver
    :return: tile element
    """
    return dom.get_element(driver, TILE_VIEW_TILE, 'V035624')
