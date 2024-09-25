from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from helpers.change.grid_columns import select_multiple_columns, select_multiple_contiguous_columns
from helpers.change.grid_row_actions import choose_row_selection_type
from helpers.change.sketcher import import_structure_into_sketcher
from helpers.extraction import paths
from helpers.selection.grid import ROW_RATIONALE_CELL, ROW_RATIONALE_CELL_EDIT_BUTTON, Footer
from helpers.selection.modal import MODAL_DIALOG_BODY_INPUT
from helpers.selection.rationale import RATIONALE_TEXTAREA, RATIONALE_SAVE
from helpers.selection.sketcher import CUSTOM_ALIGNMENT_SKETCHER_IFRAME
from helpers.verification.grid import verify_footer_values, verify_column_contents
from library import dom, base, simulate
from helpers.change.grid_column_menu import open_group_column_dialog, click_column_menu_item, open_set_alignment_dialog, \
    toggle_cell_aggregation
from library.dom import set_element_value, click_element


def group_columns_selectively(driver, group_name, *columns_to_group):
    """
    Selects multiple column as per the choice and group them.

    :param driver: Selenium Webdriver
    :param group_name: str, name of the column group
    :param columns_to_group: name of column(s) to be grouped
    :return:
    """
    # Select multiple columns
    select_multiple_columns(driver, *columns_to_group)

    # Open the column context menu and group columns
    open_group_column_dialog(driver, columns_to_group[-1])
    dom.set_element_value(driver, MODAL_DIALOG_BODY_INPUT, value=group_name)
    base.click_ok(driver)


def group_columns_in_bulk(driver, start_column_name, end_column_name, group_name):
    """
    Select multiple adjacent columns and groups them.

    :param driver: Selenium Webdriver
    :param start_column_name: str, signifies the first column to be selected in the range of columns.
    :param end_column_name: str, signifies the end of range of columns(last column) to be selected and then grouped
    :param group_name: str, name of the column group
    :return:
    """

    # Select multiple columns
    select_multiple_contiguous_columns(driver, start_column_name, end_column_name)

    # Open the column context menu and group columns
    open_group_column_dialog(driver, end_column_name)
    dom.set_element_value(driver, MODAL_DIALOG_BODY_INPUT, value=group_name)
    base.click_ok(driver)


def hide_columns_selectively(driver, *columns_to_hide):
    """
    Selects multiple columns using the ctrl/cmd key and hides them.
    Clicks on the first column to get to the context menu.

    :param driver: Selenium Webdriver
    :param columns_to_hide: name(s) of column(s) to be hidden
    :return:
    """
    # Select multiple columns
    select_multiple_columns(driver, *columns_to_hide)

    # Open the column context menu and hide the columns
    click_column_menu_item(driver, columns_to_hide[0], column_option_name='Hide', exact_text_match=True)


def hide_columns_contiguously(driver, first, last):
    """
    Selects multiple contiguous columns using the shift key and hides them.

    :param driver: Selenium Webdriver
    :param first: name of the first column in the contiguous selection
    :param last: name of the last column in the contiguous selection
    """
    # Select multiple columns
    select_multiple_contiguous_columns(driver, first, last)

    # Open the column context menu and hide the columns
    click_column_menu_item(driver, last, column_option_name='Hide', exact_text_match=True)


def set_custom_alignment(driver, mrv_file):
    """
    Open the Set Alignment dialog and import the custom mrv into the sketcher. Then click OK.

    :param driver: Selenium Webdriver
    :param mrv_file: str, Mrv file of the core structure to align the LR's compounds to
    :return:
    """
    # Open the Compound Structure's column context menu and select Set Alignment
    open_set_alignment_dialog(driver)

    # Get the mrv string
    path_to_mrv = paths.get_resource_path(mrv_file)
    with open(path_to_mrv, 'r') as file:
        mrv = file.read().replace('\n', '')

    # Import the mrv into the sketcher
    import_structure_into_sketcher(driver, mrv, sketcher_iframe_selector=CUSTOM_ALIGNMENT_SKETCHER_IFRAME)
    base.click_ok(driver)


def toggle_cell_aggregation_and_verify_column_content(driver,
                                                      initial_column_name,
                                                      aggregation_option,
                                                      results,
                                                      column_name_after_toggle=None):
    """
    Utility function to toggle the cell aggregation mode of a column and thereafter verify the column contents.

    :param driver: Webdriver
    :param initial_column_name: str, Name of the column for which the function will perform the actions
    :param aggregation_option: str, Cell aggregation mode, to be shuffled to
    :param results: list, string values expected in the column under consideration
    :param column_name_after_toggle: str, New name of the column after toggling
    :return:
    """
    toggle_cell_aggregation(driver, initial_column_name, aggregation_option)

    if column_name_after_toggle:
        verify_column_contents(driver, column_name_after_toggle, results)
    else:
        verify_column_contents(driver, initial_column_name, results)


def choose_row_selection_type_and_verify_footer(driver, checkbox_item_name, all_rows_count, selected_count):
    """
    Selects the row selection and verify footer values based on selection

    :param driver: Selenium webdriver
    :param checkbox_item_name: str, Checkbox item name "All", "Inverted" or "None"
    :param all_rows_count: int, all compounds count
    :param selected_count: int, selected compounds count
    """
    choose_row_selection_type(driver, checkbox_item_name)
    # verification of all compounds selection
    verify_footer_values(
        driver, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(all_rows_count),
            Footer.ROW_SELECTED_COUNT_KEY: Footer.ROW_SELECTED_COUNT_VALUE.format(selected_count)
        })


def select_grid_cells_with_navigation_keys(driver, *args):
    """
    Select multiple grid cells while traversing those cells using navigation keys (UP, DOWN, LEFT, RIGHT)
    This method holds down Shift key & then uses navigation keys to select grid cells, then releases Shift key
    Usage example: (selenium, Keys.RIGHT*3, Keys.DOWN*3), nav keys must be in UPPERCASE
    :param driver: selenium webdriver
    :param args: tuple, navigation keys and number of keystrokes for each key
    """
    ActionChains(driver).key_down(Keys.SHIFT).perform()
    for value in args:
        dom.press_keys(driver, value)
    ActionChains(driver).key_up(Keys.SHIFT)


def edit_rationale_in_grid_view(driver, rationale_text, compound_id):
    """
    Edits rationale in grid view for a given compound

    :param driver: selenium webdriver
    :param rationale_text: text input for rationale
    :param compound_id: compound id to edit/add rationale for
    """
    simulate.hover(driver, dom.get_element(driver, ROW_RATIONALE_CELL.format(compound_id)))
    simulate.click(driver, dom.get_element(driver, ROW_RATIONALE_CELL_EDIT_BUTTON.format(compound_id)))
    set_element_value(driver, RATIONALE_TEXTAREA, rationale_text)
    click_element(driver, RATIONALE_SAVE)
