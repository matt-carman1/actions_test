from helpers.change.tile_view import open_tile_menu
from helpers.selection.general import OPENED_MENU_ITEMS
from helpers.selection.tile_view import TILE_VIEW_HEADER, TILE_HEADER, SELECTED_TILE_HEADER
from helpers.verification.element import verify_is_visible
from library import simulate, dom


def verify_tile_menu_items(driver, tile_id, *menu_items):
    """
    Verify tile menu items.

    :param driver: Selenium Webdriver
    :param tile_id: str, ID of the any tile which is selected
    :param menu_items: str, menu item name(s) which needs to be verified
    """
    # Open tile menu
    open_tile_menu(driver, tile_id)

    # verify whether menu item visible
    for menu_item in menu_items:
        verify_is_visible(driver, selector=OPENED_MENU_ITEMS, selector_text=menu_item)

    # clicking header to close the tile menu
    dom.click_element(driver, TILE_VIEW_HEADER)


def verify_selected_tile_ids(driver, *expected_selected_ids):
    """
    Verify Selected tile ids which are in visible range.

    :param driver: Selenium webdriver
    :param expected_selected_ids: str, expected selected tile id(s)
    """
    selected_tile_elems = dom.get_elements(driver, selector=SELECTED_TILE_HEADER, dont_raise=True, timeout=5)
    selected_tile_ids = [elem.text for elem in selected_tile_elems]
    assert set(selected_tile_ids) == set(expected_selected_ids), 'Actual tile ids:{}, Expected tile ids:{}'.format(
        selected_tile_ids, expected_selected_ids)
