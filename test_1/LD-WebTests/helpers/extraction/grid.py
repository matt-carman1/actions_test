"""
Extract data as strings from the grid.
"""
import re

from selenium.webdriver.common.by import By

from helpers.change.grid_column_menu import toggle_show_smiles
from helpers.change.grid_columns import scroll_to_column_header
from helpers.selection.grid import GRID_ROWS_CONTAINER, GRID_ROW, GRID_ROW_SELECTION_CELL, \
    GRID_CELL_COLUMN_ID_, GRID_FOOTER_ROW_ALL_COUNT, GRID_FOOTER_ROW_HIDDEN_COUNT, GRID_FOOTER_ROW_FILTERED_COUNT, \
    GRID_FOOTER_ROW_SELECTED_COUNT, GRID_FOOTER_COLUMN_ALL_COUNT, GRID_FOOTER_COLUMN_HIDDEN_COUNT, \
    GRID_COMPOUND_ID_CELLS, GRID_CELL_ASSAY_SUBCELL, GRID_HEADER_SELECTOR_, GRID_COLUMN_MENU_OPEN, GRID_PENDING_CELLS_IN_COLUMN,\
    GRID_FOOTER_ROW_DISPLAYED_COUNT
from helpers.selection.sar_analysis import SAR_IMAGE
from library import dom, style, wait
from library.scroll import wheel_to_top, wheel_element, element_is_scrolled_to_bottom
from library.utils import get_first_int, element_is_vertically_within_parent


def find_column_subcell_contents(driver, column_name, get_info_from_subcell=None):
    """
    Get the contents of a given, named column, as a list of lists of strings.
    Each subcell is separated

    NOTE: Calling this function will cause the grid to be scrolled both horizontally and vertically: Firstly to find the
    column, and then to scroll through all rows to extract the relevant values.

    :param driver: selenium webdriver
    :param column_name: str, Column name for which the contents needs to be extracted.
    :param get_info_from_subcell: optional function that is used to extract data from a cell. If not supplied, we will
                                  get the text representation. NOTE: This is ignored for Compound Structure Column.
    :return: list, List of strings.
    """

    if not get_info_from_subcell:

        def default_get_info_from_subcell(subcell):
            return subcell.text

        get_info_from_subcell = default_get_info_from_subcell

    def get_all_subcell_info_in_cell(cell):
        subcells = dom.get_elements(cell, GRID_CELL_ASSAY_SUBCELL)
        return [get_info_from_subcell(subcell) for subcell in subcells]

    return find_column_contents(driver, column_name, get_all_subcell_info_in_cell)


def find_column_contents(driver, column_name, get_info_from_cell=None):
    """
    Get the contents of a given, named column, as a list of strings.

    NOTE: Calling this function will cause the grid to be scrolled both
    horizontally and vertically: Firstly to find the column, and then to scroll
    through all rows to extract the relevant values.

    :param driver: selenium webdriver
    :param column_name: str, Column name for which the contents needs to be extracted.
    :param get_info_from_cell: optional function that is used to extract data from a cell. If not supplied, we will get
                               the text representation. NOTE: This is ignored for Compound Structure Column.
    :return: list, List of strings.
    """
    if column_name == 'Compound Structure':
        column_contents = _find_smiles_contents(driver)
    else:
        column_contents = _find_cell_contents(driver, column_name, get_info_from_cell)

    return column_contents


def get_grid_metadata(driver):
    """
    Get grid metadata that is displayed in the grid footer. This includes
    filtered count, hidden rows, total row count, selected rows,
    total column count, hidden columns etc.

    :param driver: selenium webdriver
    :return:
    """

    selectors = {
        'row_all_count': GRID_FOOTER_ROW_ALL_COUNT,
        'row_displayed_count': GRID_FOOTER_ROW_DISPLAYED_COUNT,
        'row_hidden_count': GRID_FOOTER_ROW_HIDDEN_COUNT,
        'row_filtered_count': GRID_FOOTER_ROW_FILTERED_COUNT,
        'row_selected_count': GRID_FOOTER_ROW_SELECTED_COUNT,
        'column_all_count': GRID_FOOTER_COLUMN_ALL_COUNT,
        'column_hidden_count': GRID_FOOTER_COLUMN_HIDDEN_COUNT,
    }
    result = {}

    for (key, selector) in selectors.items():
        elements = driver.find_elements(By.CSS_SELECTOR, selector)
        if elements:
            result[key] = elements[0].text

    filtered_count = result.get('row_filtered_count')
    all_row_count = result.get('row_all_count')

    result['row_visible_count'] = filtered_count if filtered_count else \
        all_row_count

    return result


def get_grid_render_count_map(driver):
    """
    Returns the grid render count map (see GridCell.jsx)

    :param driver: Webdriver
    :return: The grid render count map
    :rtype: dict
    """
    return driver.execute_script('return bb.perfMetrics.GridCellRenderCountMap;')


def get_row_entity_id(driver, visible_row_index):
    """
    Returns the entity id for nth row currently visible
    (where n is the provided index)

    :param driver: Webdriver
    :param visible_row_index: str
    :return: the Compound ID from ID column
    :rtype: str
    """
    row_container = dom.get_element(driver, GRID_ROWS_CONTAINER)
    id_elements = dom.get_elements(row_container, GRID_COMPOUND_ID_CELLS)
    visible_ids = [element for element in id_elements if element_is_vertically_within_parent(row_container, element)]
    id_element = visible_ids[visible_row_index]
    if not id_element:
        raise ValueError('No element found for the given visible_row_index')
    return id_element.text


def _find_smiles_contents(driver):
    """
    Get the SMILES content, as a list of strings, from the grid.

    In order to get the smiles from the grid, we need to switch compound display
    to SMILES, then get the data, then switch back to compound image.

    :param driver: selenium webdriver
    :return: smiles string for compounds in the live report
    :rtype: List[str]
    """

    column_name = 'Compound Structure'
    toggle_show_smiles(driver)

    smiles = _find_cell_contents(driver, column_name)

    toggle_show_smiles(driver)
    return smiles


def _find_cell_contents(driver, column_name, get_info_from_cell=None):
    """
    Get the string contents of cells for a given, named column.

    This function both scrolls the grid and extracts the data.

    :param driver: selenium webdriver
    :param column_name:
    :param get_info_from_cell: optional function that is used to extract data from a cell. If not supplied, we will get
                               the text representation. NOTE: This is ignored for Compound Structure Column.
                               For e.g. refer to verify_column_color helper where we are using this to get the color
                               from each cell in a column rather than text.
    :return: found cell contents
    :rtype: List[str]
    """
    # NOTE: Scrolls horizontally
    column_header = scroll_to_column_header(driver, column_name)
    wait_until_cells_are_loaded(driver, column_name)

    grid_metadata = get_grid_metadata(driver)
    expected_rows = get_first_int(grid_metadata['row_visible_count'])

    found_cells = {}
    row_container = dom.get_element(driver, GRID_ROWS_CONTAINER)

    # NOTE: Scrolls vertically
    wheel_to_top(driver, row_container)

    while True:
        rows = dom.get_elements(row_container, GRID_ROW)
        visible_rows = [row for row in rows if element_is_vertically_within_parent(row_container, row)]

        for row in visible_rows:
            text_idx = dom.get_element(row, GRID_ROW_SELECTION_CELL).text
            if text_idx:
                # Subtract 1 because rows are 1-indexed, arrays are 0-indexed.
                idx = int(text_idx) - 1
                cell = _find_cell(row, column_header)
                value = get_info_from_cell(cell) if get_info_from_cell else cell.text

                if found_cells.get('idx') and found_cells[idx] != value:
                    raise Exception('For row {}, got conflicting data {} and now {}'.format(
                        text_idx, found_cells[idx], value))

                if not found_cells.get('idx'):
                    found_cells[idx] = value
                else:
                    print('found {} again with {}'.format(text_idx, value))

        if expected_rows == len(found_cells) \
                or element_is_scrolled_to_bottom(row_container):
            break

        scroll_distance = calculate_scroll_distance(visible_rows)

        # NOTE: Scrolls vertically
        wheel_element(driver, row_container, scroll_distance)

    # NOTE: Scrolls vertically
    wheel_to_top(driver, row_container)

    return [found_cells[idx] for idx in sorted(found_cells.keys())]


def db_column_id(driver, column_name):
    """
    For the given column name, returns the database id number from the dom, which is the ld_addable_column.id

    :param driver: webdriver
    :param column_name: str, column name, such as "PK_IV_RAT (AUC) Prot 2" (not including the units in square brackets)
    :return: str, id for the given column name, for example "-123" but we return "123"
    """

    column_header = dom.get_element(driver, GRID_HEADER_SELECTOR_.format(column_name))
    column_id = column_header.get_attribute("id")[1:]
    return column_id


def _find_cell(row, column_header):
    """
    For a given row in the grid, find the cell contents in a given column.

    NOTE: If the cell is not scrolled into view, this will fail.

    :param row:
    :param column_header:
    :return: element
    """
    column_id = column_header.get_attribute('id')[1:]
    cell_selector = GRID_CELL_COLUMN_ID_.format(column_id)

    cell = dom.get_element(row, cell_selector)
    return cell


def _get_number_from_footer_text(string):
    """
    All footer information is presented like "50 Compound", "6 Filtered".
    This function extracts the leading numerals
    and parses into an integer.

    :param string: e.g. "50 Compounds"
    :return: the number part of the string
    :rtype: int
    """
    pattern = re.compile('^(\\d+) ')
    match = pattern.match(string)
    string_value = match.group(0)
    return int(string_value)


def calculate_scroll_distance(visible_rows):
    """
    Provide a reasonable guess for how much to scroll the page, given how many
    rows are visible and how much space they take up.

    :param visible_rows:
    :return: amount to scroll in px
    :rtype: int
    """
    if not visible_rows:
        raise ValueError('Falsy visible_rows passed to _calculate_scroll_distance')

    a_row = visible_rows[0]
    height_of_a_row = a_row.size.get('height')

    if len(visible_rows) == 1:
        return height_of_a_row

    # Rows are not provided in any particular order, so sort by y pos.
    sorted_px = sorted([row.location.get('y') for row in visible_rows])
    first_to_last_px = sorted_px[-1] - sorted_px[0]

    return first_to_last_px + height_of_a_row


def get_color_tuple(child_selector, cell):
    """
    Extract the color from a given cell as an rgba tuple.

    NOTE: If the browser returns the color as an rgb value, e.g. rgb(2, 255, 0), then an alpha channel value of
    1 is assumed and appended to the end of the tuple to give (2, 255, 0, 1).

    :param child_selector: selector to find child item that has color data
    :param cell: selenium element representing a cell in the DOM
    :return: tuple of integers, e.g. (2, 255, 0, 1)
    """
    child_cell = dom.get_element(cell, child_selector, must_be_visible=False)

    actual_color_string = style.get_css_value(child_cell, css_property_name='background-color')
    try:
        rgb_array = [int(val) for val in re.findall(r'\d+(?:\.\d+)?', actual_color_string)]
    except ValueError as e:
        print(e)
        print('alpha channel value is a decimal,we may need to IMPROVE this helper.')

    # Some of the browsers return the color as rgb value, so defaulting the alpha channel value as 1.
    if len(rgb_array) == 3:
        rgb_array.append(1)
    return tuple(rgb_array)


def get_image_status(element):
    """
    Callback function that returns True/False depending on whether an image element exists.
    :param element: webdriver element.
    :return: bool, True if an image exists, else False
    """
    image = dom.get_element(element, SAR_IMAGE, timeout=10, dont_raise=True)
    return bool(image)


def wait_until_cells_are_loaded(driver, column_title: str, custom_timeout: int = None):
    # breakpoint()
    """
    Waits until all the cells under the given column are not in a pending state.

    :param driver: selenium webdriver
    :param column_title: <str>, name of the column
    :param custom_timeout: <seconds>, wait time for the cells to load
    """
    column_id = db_column_id(driver, column_title)
    if custom_timeout:
        wait.until_not_visible(driver, GRID_PENDING_CELLS_IN_COLUMN.format(column_id), timeout=custom_timeout)
    else:
        wait.until_not_visible(driver, GRID_PENDING_CELLS_IN_COLUMN.format(column_id))