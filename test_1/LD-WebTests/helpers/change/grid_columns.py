from helpers.change.grid_row_actions import scroll_to_row
from helpers.extraction import grid
from helpers.selection.grid import GRID_ROWS_CONTAINER, GRID_HEADER_SELECTOR_, GRID_FIXED_COLUMN_GROUP, GRID_ROW_ID_, \
    GRID_HEADER_CELL, GRID_CELL_COLUMN_ID_, GRID_ROW_CHECKBOX_, GRID_ALL_ROWS_CHECKBOX,\
    GRID_COLUMN_HEADER_REORDER_CONTAINER
from helpers.selection.modal import MODAL_DIALOG_BODY
from library import dom, simulate, wait
from library.dom import DEFAULT_TIMEOUT
from library.scroll import wheel_to_leftmost, scroll_until_visible
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time


def scroll_to_column_header(driver, column_name, custom_timeout=DEFAULT_TIMEOUT):
    """
    Scroll the grid horizontally until a column with the given name is visible on the screen

    :param driver: selenium webdriver
    :param column_name: name of the column to be visible
    :return: the column header cell for that column
    :param custom_timeout: time for which to look for the column with the given name. Defaults to 60seconds
    :return: element, the column header cell for that column
    :rtype: element
    """
    header_selector = GRID_HEADER_SELECTOR_.format(column_name)

    row_container = dom.get_element(driver, GRID_ROWS_CONTAINER)
    amount_to_scroll = _determine_horizontal_amount_to_scroll(row_container)

    wheel_to_leftmost(driver, row_container)
    # NOTE (pradeep): Wait for the row container to be scrolled before verifying values below
    wait.until_grid_is_scrolled_to_leftmost(driver)

    column_header = scroll_until_visible(driver,
                                         row_container,
                                         header_selector,
                                         delta_px=amount_to_scroll,
                                         horizontal=True,
                                         message='Unable to find the column with name "{}"'.format(column_name),
                                         timeout=custom_timeout)
    return column_header


def _determine_horizontal_amount_to_scroll(row_container):
    # It's safe to request the first item from the result of a call to
    # get_elements because the function will raise an error if no elements are
    # found that match the selector.
    fixed_cell_group_wrapper = dom.get_elements(row_container, GRID_FIXED_COLUMN_GROUP)[0]
    grid_width = row_container.size.get('width')
    fixed_cells_width = fixed_cell_group_wrapper.size.get('width')
    unfixed_width = grid_width - fixed_cells_width

    # TODO this arbitrary number should be width of last visible column
    return unfixed_width - 100


def copy_grid_column_contents(driver, column_name):
    """
        Function to copy and paste grid contents to filter

        :param driver: selenium webdriver
        :param column_name: name of header to copy
        """
    column_element = scroll_to_column_header(driver, column_name)

    # Copy all contents in column
    simulate.click(driver, column_element)

    # Recursively copy while the "try again" modal is showing
    done = False
    while not done:
        dom.copy(driver)

        # if copy dialog comes up, send copy call again
        bb_dialog = dom.get_element(driver,
                                    MODAL_DIALOG_BODY,
                                    text="Data loaded. Please hit CTRL+C again "
                                    "to copy.",
                                    timeout=3,
                                    dont_raise=True)

        done = not bb_dialog


def get_cell(driver, compound_id, column_title):
    """
    Returns element for cell given grid row number and column title.

    If two column titles are the same, this might break, but using the title of a column is more user friendly than
    using the ID.

    :param driver: selenium WebDriver
    :param compound_id: <str>, compound ID to identify row
    :param column_title: <str>, cell that column falls under
    :return: cell WebElement
    """
    scroll_to_row(driver, structure_id=compound_id)
    scroll_to_column_header(driver, column_name=column_title)
    row = dom.get_element(driver, GRID_ROW_ID_.format(compound_id))
    column_id = grid.db_column_id(driver, column_title)
    return dom.get_element(row, GRID_CELL_COLUMN_ID_.format(column_id))


def click_compound_row(driver, entity_id='all'):
    """
    Click the checkbox that selects the entire row in LR for a Compound ID.
    Will select all compounds in LR if no entity ID is entered.

    :param driver: webdriver
    :param entity_id: str, Compound ID from ID column.
                           If not specified function will select all compounds
    """
    checkbox_selector = GRID_ALL_ROWS_CHECKBOX \
        if entity_id == 'all' \
        else GRID_ROW_CHECKBOX_.format(entity_id)

    dom.click_element(driver, checkbox_selector)


def select_multiple_columns(driver, *columns_to_select):
    """
    Selects a column, press control and then clicks on other column header to be selected.
    :param driver: Selenium webdriver
    :param columns_to_select: name of column(s) to be selected
    :return:
    """
    control_key = dom.get_ctrl_key()

    # # Selecting the first column
    # scroll_to_column_header(driver, list_of_columns_to_select[0])
    # dom.click_element(driver, GRID_HEADER_CELL, text=list_of_columns_to_select[0], exact_text_match=True)

    for column in columns_to_select:
        scroll_to_column_header(driver, column)
        column_element = dom.get_element(driver, GRID_HEADER_CELL, text=column, exact_text_match=True)
        ActionChains(driver).key_down(control_key).click(column_element).key_up(control_key).perform()


def select_multiple_contiguous_columns(driver, start_column, end_column):
    """
    Select a column, hold shift and select the last column. This would result in selecting multiple contiguous columns.

    :param driver: Selenium Webdriver
    :param start_column: str, signifies the first column to be selected in the range of columns.
    :param end_column: str, signifies the end of range of columns(last column) to be selected.
    :return:
    """
    scroll_to_column_header(driver, start_column)

    dom.click_element(driver, GRID_HEADER_CELL, text=start_column, exact_text_match=True)

    # end_column_element = dom.get_element(driver, GRID_HEADER_CELL, text=end_column, exact_text_match=True)
    end_column_element = scroll_to_column_header(driver, end_column)

    ActionChains(driver).key_down(Keys.SHIFT).click(end_column_element).key_up(Keys.SHIFT).perform()


def drag_and_drop_columns_in_grid(driver, source_column_name, dest_column_name):
    """
    Function to drag and drop columns on the grid
    Note: This function works only if both source_column and dest_column are within viewport range
          As if the dest_column present past the viewport then the element won't be fetched by get_element

    :param driver: Selenium Webdriver
    :param source_column_name: str, Drag target column name
    :param dest_column_name: str, Drop target column name
    """

    def get_column_reorder_elem(driver_, column_name):
        column_elem = dom.get_element(driver_, GRID_HEADER_SELECTOR_.format(column_name))
        parent_elem = dom.get_parent_element(column_elem)
        ancestor_elem = dom.get_parent_element(parent_elem)
        reorder_elem = dom.get_element(ancestor_elem, GRID_COLUMN_HEADER_REORDER_CONTAINER, must_be_visible=False)
        return reorder_elem

    action = ActionChains(driver)
    action.click_and_hold(get_column_reorder_elem(driver, source_column_name))\
        .move_to_element(get_column_reorder_elem(driver, dest_column_name)).release().perform()
