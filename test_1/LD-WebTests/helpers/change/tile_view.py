from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from helpers.change.menus import click_submenu_option
from helpers.selection.general import OPENED_MENU_ITEMS, MENU_ITEM
from helpers.selection.grid import GRID_ROW_MENU
from helpers.selection.tile_view import TILE_ICON, TILE_ICON_ACTIVE, AVAILABLE_COLUMNS_ITEM, SHOW_BUTTON, \
    DISPLAYED_COLUMNS_ITEM, CONFIGURE_TILES, HIDE_BUTTON, AVAILABLE_COLUMNS_ITEM_NOT_DISPLAYED, TILE_VIEW_TILE, \
    INCREASE_TILE_SIZE, TILE_VIEW_DIV, TILE_HEADER, TILE_FIELD_NAME_, TILE_CONTAINER, TILE_VIEW_SELECTION_CHECKBOX, \
    TILE_VIEW_HEADER
from helpers.verification import element
from library import ensure, dom, wait, simulate
from library.base import click_ok
from library.dom import LiveDesignWebException
from library.scroll import scroll_until_visible

ASC = 'Ascending'
DESC = 'Descending'


def switch_to_tile_view(driver,):
    """
    Opens tile view.

    :param driver: selenium webdriver
    """
    ensure.element_visible(driver, action_selector=TILE_ICON, expected_visible_selector=TILE_ICON_ACTIVE)
    wait.until_visible(driver, TILE_VIEW_HEADER)


def show_column(driver, column):
    """
    Displays a column in tile view via the Configure Tiles dialog.

    :param driver: selenium webdriver
    :param column: the column (property) to display
    """
    dom.click_element(driver, CONFIGURE_TILES)
    dom.click_element(driver, AVAILABLE_COLUMNS_ITEM, column)
    dom.click_element(driver, SHOW_BUTTON)
    element.verify_is_visible(driver, DISPLAYED_COLUMNS_ITEM, column)
    click_ok(driver)


def hide_column(driver, column):
    """
    Hides a column in tile view via the Configure Tiles dialog.

    :param driver: selenium webdriver
    :param column: the column (property) to hide
    """
    dom.click_element(driver, CONFIGURE_TILES)
    dom.click_element(driver, DISPLAYED_COLUMNS_ITEM, column)
    dom.click_element(driver, HIDE_BUTTON)
    element.verify_is_visible(driver, AVAILABLE_COLUMNS_ITEM_NOT_DISPLAYED, column)
    click_ok(driver)


def increase_tile_size(driver):
    """
    Increases the tile size by clicking the icon once,
    then waiting until the first tile's height has changed.

    :param driver: selenium webdriver
    """
    tile = dom.get_elements(driver, TILE_VIEW_TILE)[0]
    tile_height_before = int(tile.size.get('height'))
    dom.click_element(driver, INCREASE_TILE_SIZE)

    # Callback to wait until the height has changed before moving on
    def is_height_changed(el):
        tile_height_after = el.size.get('height')
        return tile_height_before != tile_height_after

    dom.wait_until(tile, is_height_changed)


def sort_tile_by(driver, column_name, sort_ascending=True):
    """
    Will sort the tiles based on column name

    :param driver: Selenium webdriver
    :param column_name: str, Column name which need to be sorted
    :param sort_ascending: boolean, True for sort ascending, False otherwise
    """
    direction = ASC if sort_ascending else DESC
    # getting first tile ID to select property
    tile_id = dom.get_elements(driver, TILE_HEADER)[0].text
    # selecting property menu item
    click_property_menu_item(driver, tile_id, column_name, direction, 'Sort')
    wait.until_loading_mask_not_visible(driver)


def click_property_menu_item(driver, tile_id, column_name, menu_item_name, submenu_name=None):
    """
    Will click menu item for the specified property(column name)

    :param driver: Selenium webdriver
    :param tile_id: str, ID of tile for which the property item to be selected
    :param column_name: str, column name or property name
    :param menu_item_name: str, menu item name which need to be clicked
    """
    scroll_to_property_header(driver, tile_id, column_name)
    property_element = dom.get_element(driver,
                                       TILE_FIELD_NAME_.format(tile_id),
                                       text=column_name,
                                       exact_text_match=True)
    simulate.right_click(property_element)
    wait.until_visible(driver, OPENED_MENU_ITEMS)
    if submenu_name:
        click_submenu_option(driver, submenu_name, menu_item_name, exact_text_match=True)
    else:
        dom.click_element(driver, OPENED_MENU_ITEMS, text=menu_item_name)


def scroll_to_property_header(driver, tile_id, column_name):
    """
    Scrolls the cursor to the property header.

    :param driver: Selenium webdriver
    :param tile_id: str, ID of the tile
    :param column_name: str, column name or property name
    """
    tile_container = dom.get_element(driver, TILE_CONTAINER)
    # taking tile view scrollable item height
    scroll_distance_str = dom.get_element(driver, TILE_VIEW_DIV).value_of_css_property('height')
    # converting the string to to int, ex: 412px to 412
    scroll_distance = int(scroll_distance_str[:-2])

    scroll_until_visible(driver,
                         tile_container,
                         selector=TILE_FIELD_NAME_.format(tile_id),
                         text=column_name,
                         delta_px=scroll_distance)


def toggle_tile_selection(driver, tile_id):
    """
    Deselects already selected tile or add tile to the selection.

    :param driver: Selenium webdriver
    :param tile_id: str, ID of the selected tile which needs to be deselect
    """
    control_key = dom.get_ctrl_key()
    tile_element = dom.get_element(driver, TILE_HEADER, text=tile_id, exact_text_match=True)
    ActionChains(driver).key_down(control_key).click(tile_element).key_up(control_key).perform()


def select_multiple_tiles(driver, tiles_to_select):
    """
    Selects a tile, press control and then clicks on other column header to be selected.

    :param driver: Selenium webdriver
    :param tiles_to_select: IDs of tile(s) to be selected
    """
    control_key = dom.get_ctrl_key()

    for tile in tiles_to_select:
        scroll_to_tile(driver, tile)
        tile_element = dom.get_element(driver, TILE_HEADER, text=tile, exact_text_match=True)
        ActionChains(driver).key_down(control_key).click(tile_element).key_up(control_key).perform()


def scroll_to_tile(driver, tile_id):
    """
    Scroll the grid vertically until a tile with the given ID is visible on the screen.

    :param driver: selenium webdriver
    :param tile_id: str, structure ID
    :return: the tile ID cell
    :rtype: element
    """
    # find the amount to scroll
    # taking tile view scrollable item height
    scroll_distance_str = dom.get_element(driver, TILE_VIEW_DIV).value_of_css_property('height')
    # converting the string to to int, ex: 412px to 412
    amount_to_scroll = int(scroll_distance_str[:-2])

    # scroll to the tile containing the structure id
    tile_container = dom.get_element(driver, TILE_VIEW_DIV)
    tile_id_tile = scroll_until_visible(driver, tile_container, TILE_HEADER, text=tile_id, delta_px=amount_to_scroll)

    return tile_id_tile


def hide_multiple_contiguous_columns_in_tile_view(driver, start_column, end_column):
    """
    Hides multiple columns contiguously using shift key in tile view via the Configure Tiles dialog.

    :param driver: selenium webdriver
    :param start_column: str, first column in contiguous column.
    :param end_column: str, the last column in contiguous columns
    """
    dom.click_element(driver, CONFIGURE_TILES)

    # clicking first column
    dom.click_element(driver, DISPLAYED_COLUMNS_ITEM, start_column)
    # shift+end column click
    end_column_element = dom.get_element(driver, DISPLAYED_COLUMNS_ITEM, end_column)
    ActionChains(driver).key_down(Keys.SHIFT).click(end_column_element).key_up(Keys.SHIFT).perform()

    # click hide button
    dom.click_element(driver, HIDE_BUTTON)

    click_ok(driver)


def check_select_all_tiles_checkbox(driver):
    """
    click select all tiles checkbox

    :param driver: Selenium Webdriver
    """
    dom.click_element(driver, TILE_VIEW_SELECTION_CHECKBOX)


def open_tile_menu(driver, tile_id):
    """
    Right clicks on tile to open tile menu.

    :param driver: Selenium webdriver
    :param tile_id: str, ID of the tile here tile ID is compound entity ID
    """
    tile_element = dom.get_element(driver, TILE_HEADER, text=tile_id, exact_text_match=True)
    simulate.right_click(tile_element)
    wait.until_visible(driver, GRID_ROW_MENU)


def click_tile_context_menu_item(driver, tile_id, option_to_select, submenu_name=None, exact_text_match=False):
    """
    1. Right clicks on a tile.
    2. Selects, or hover over (if submenu_name is provided), an option from the context menu
    3. Clicks a submenu item

    :param driver: Selenium WebDriver
    :param tile_id: str, ID of the tile to right click
    :param option_to_select: str, The option to select from the right click dropdown
    :param submenu_name: str, column menu item's sub menu label
    :param exact_text_match: bool, Whether text match should be exact or not. Disabled by default.
    """
    open_tile_menu(driver, tile_id)
    if submenu_name:
        click_submenu_option(driver, option_to_select, submenu_name, exact_text_match)
    else:
        dom.click_element(driver, MENU_ITEM, option_to_select)


def select_tiles_and_click_context_menu_item(driver, list_of_tile_ids, option_to_select=None):
    """
    This method performs three actions:
    1. Select tiles.
    2. Right click to bring up tile submenu.
    3. Select an option from the context menu.

    :param driver: Selenium WebDriver
    :param list_of_tile_ids: list, List of entity ids(tiles) to be selected
    :param option_to_select: str, The option to select from the right click dropdown
    """
    select_multiple_tiles(driver, list_of_tile_ids)
    click_tile_context_menu_item(driver, list_of_tile_ids[-1], option_to_select)


def get_the_position_of_tile_in_tile_view(driver, tile_id):
    """
    Gets the position of tile in tile view. This will work only for the tiles which are in visible range

    :param driver: Selenium webdriver
    :param tile_id: str, ID of the which needs to be verified
    :return int, Returns the position of the tile in tile view
    """
    tile_headers = dom.get_elements(driver, TILE_HEADER)
    for position, tile in enumerate(tile_headers):
        if tile.text == tile_id:
            return position + 1

    raise LiveDesignWebException('There is no tile found with ID : {}'.format(tile_id))
