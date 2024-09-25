from helpers.change.menus import click_submenu_option
from helpers.selection.general import MENU_ITEM
from library import dom, wait
from helpers.selection.grid import GRID_ROW_CHECKBOX_, GRID_ALL_ROWS_CHECKBOX, GRID_ROW_MENU, \
    ROW_SELECTION_CHECKBOX_DROPDOWN, ROW_SELECTION_MENU, GRID_ROWS_CONTAINER, GRID_ROW_ID_
from library.scroll import scroll_until_visible
from library.simulate import right_click, hover
from library.dom import LiveDesignWebException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def hover_row(driver, entity_id):
    """
    Use this method to hover a visible row in the LR

    :param driver: Selenium Webdriver
    :param entity_id: str, Compound ID from ID column
    """
    element = dom.get_element(driver, GRID_ROW_CHECKBOX_.format(entity_id))
    hover(driver, element)


def select_all_rows(driver):
    """
    Clicks on the checkbox that selects the entire row in LR

    :param driver: Selenium Webdriver
    """
    dom.click_element(driver, GRID_ALL_ROWS_CHECKBOX)


def select_row(driver, entity_id):
    """
    Use this method to select any particular row/Compound in the LR, for example:
    select_row(driver, entity_id = 'CHEMBL1000')

    :param driver: Selenium Webdriver
    :param entity_id: str, Compound ID from ID column
                        If not specified function will select all compounds
    """
    dom.click_element(driver, GRID_ROW_CHECKBOX_.format(entity_id))


def select_rows(driver, list_of_entity_ids):
    """
    Use this method to select a list of rows/Compounds in the LR, for example:
    select rows(driver, list_of_entity_ids = ['CHEMBL1000','CHEMBL1001', 'CHEMBL1002']

    :param driver: Selenium Webdriver
    :param list_of_entity_ids: List of entity ids to select

    """

    if isinstance(list_of_entity_ids, str):
        raise LiveDesignWebException("Use select_row method for single entity values")
    for id in list_of_entity_ids:
        select_row(driver, id)


def open_row_menu(driver, entity_id):
    """
    Right clicks compound row menu.
    :param driver:
    :param entity_id:
    :return:
    """
    row_element = dom.get_element(driver, GRID_ROW_CHECKBOX_.format(entity_id))
    right_click(row_element)
    wait.until_visible(driver, GRID_ROW_MENU)


def pick_row_context_menu_item(driver, entity_id, option_to_select, submenu_name=None, exact_text_match=False):
    """
    1. Right clicks a compound row.
    2. Selects, or hover over (if submenu_name is provided), an option from the context menu
    3. Clicks a submenu item

    :param driver: Selenium WebDriver
    :param entity_id: entity_id to right click
    :param option_to_select: str, The option to select from the right click dropdown
    :param submenu_name: str, column menu item's sub menu label
    :param exact_text_match: bool, Whether text match should be exact or not. Disabled by default.
    """
    open_row_menu(driver, entity_id)
    if submenu_name:
        click_submenu_option(driver, option_to_select, submenu_name, exact_text_match)
    else:
        dom.click_element(driver, MENU_ITEM, option_to_select)
    # (ext_dfuzr_moore) After the menu option is clicked, we need to move the mouse
    # elsewhere, otherwise it will hover over compound images and trigger the zoom
    # preview. This obscures various elements and can cause false test failures, for
    # example when attempting to verify the LR footer values which are now covered.
    title = dom.get_element(driver, '#project-title', must_be_visible=False, must_be_clickable=False)
    hover(driver, title)


def select_rows_and_pick_context_menu_item(driver, list_of_entity_ids, option_to_select=None):
    """
    This method performs three actions:
    1. Select compound row(s)
    2. Right click to bring up row submenu
    3. Select an option from the context menu.

    :param driver: Selenium WebDriver
    :param list_of_entity_ids: List of entity ids to be selected
    :param option_to_select: str, The option to select from the right click dropdown

    """
    select_rows(driver, list_of_entity_ids)
    pick_row_context_menu_item(driver, list_of_entity_ids[0], option_to_select)


def select_multiple_rows(driver, *rows_to_select):
    """
    Selects multiple rows by IDs using checkbox.

    :param driver: Selenium webdriver
    :param rows_to_select: name of row(s) to be selected
    """
    for row in rows_to_select:
        scroll_to_row(driver, row)
        dom.click_element(driver, GRID_ROW_CHECKBOX_.format(row))


def select_multiple_continuous_rows(driver, start_row, end_row):
    """
    Select a column, hold shift and select the last column. This would result in selecting multiple continuous columns.

    :param driver: Selenium Webdriver
    :param start_row: str, signifies the first row to be selected in the range of columns.
    :param end_row: str, signifies the end of range of row(last row) to be selected.
    """
    scroll_to_row(driver, start_row)
    select_row(driver, start_row)

    scroll_to_row(driver, end_row)
    end_row_element = dom.get_element(driver, GRID_ROW_CHECKBOX_.format(end_row))

    ActionChains(driver).key_down(Keys.SHIFT).click(end_row_element).key_up(Keys.SHIFT).perform()


def choose_row_selection_type(driver, row_selection_type=None):
    """
    Opens row selection drop down and click the selection type item. This will work both for Spreadsheet and Tile view.

    :param driver: selenium webdriver
    :param row_selection_type: str, row selection type, "All", "Inverted" "None"
    """
    dom.click_element(driver, ROW_SELECTION_CHECKBOX_DROPDOWN)
    selection_menu_elem = dom.get_element(driver, ROW_SELECTION_MENU)
    dom.click_element(selection_menu_elem, MENU_ITEM, text=row_selection_type)


def scroll_to_row(driver, structure_id):
    """
    Scroll the grid vertically until a row with the given ID is visible on the screen.

    :param driver: selenium webdriver
    :param structure_id: structure ID
    :return: the row ID cell
    :rtype: element
    """
    # find the amount to scroll
    cell_image = dom.get_element(driver, '.grid-image-cell', require_single_matching_element=False)
    single_row_height = int(cell_image.size.get('height'))
    row_container = dom.get_element(driver, GRID_ROWS_CONTAINER)
    full_grid_height = row_container.size.get('height')
    amount_to_scroll = full_grid_height - single_row_height

    # scroll to the row containing the structure id
    row_selector = GRID_ROW_ID_.format(structure_id)
    row_container = dom.get_element(driver, GRID_ROWS_CONTAINER)
    row_id_cell = scroll_until_visible(driver, row_container, row_selector, delta_px=amount_to_scroll)

    return row_id_cell
