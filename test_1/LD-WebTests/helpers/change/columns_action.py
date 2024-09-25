"""
Changes to the page made through the "Add Columns" action panel
"""
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from helpers.change.actions_pane import open_add_data_panel
from helpers.change.columns_management_ui import search_in_col_mgmt_ui
from helpers.change.data_and_columns_tree import scroll_column_tree_to_top
from helpers.change.grid_column_menu import click_column_menu_item
from helpers.selection.column_tree import COLUMN_TREE_PICKER_NODE_TEXT_AREA, COLUMN_TREE_PICKER_SEARCH, \
    PARAMETERIZED_MODEL_DIALOG, COLUMN_FOLDER_MULTI_SELECT, COLUMN_TREE_PICKER_NODE_ICON_AREA, \
    COLUMN_TREE_PICKER_TEXT_NODE, COLUMN_TREE_PICKER_ADD_NODE_BUTTON, LIVEREPORT_VISIBLE_COLUMN_LABEL, \
    COLUMN_FOLDER_TEXT_AREA
from helpers.selection.general import COMPONENTS_TEXT_INPUT_BOX
from helpers.selection.modal import MODAL_DIALOG_HEADER
from helpers.verification.element import verify_is_visible
from helpers.verification.grid import check_for_butterbar
from library import dom, base, simulate
from library.utils import make_unique_name


def search_and_selecting_column_in_columns_tree(driver, column_name, picker_search_selector):
    """
    This will search the column in D&C tree and clicks + button for the column.

    :param driver: Selenium webdriver
    :param column_name: str, column name which needs to be search and select
    :param picker_search_selector: str, Selector for the input text box, this selector is different for advanced search
    and column tree. COLUMN_TREE_PICKER_SEARCH is for column tree and ADVANCED_SEARCH_TEXTBOX is for advanced search.
    """
    dom.set_element_value(driver, picker_search_selector, column_name)
    column_tree_node_text_area = dom.get_element(driver,
                                                 COLUMN_TREE_PICKER_NODE_TEXT_AREA,
                                                 column_name,
                                                 dont_raise=True,
                                                 must_be_visible=True,
                                                 exact_text_match=True)
    if not column_tree_node_text_area:
        # uses JS to address the scenario in which the name is longer than the width of the d/c tree
        column_tree_node_text_area = driver.execute_script(
            """
            var elems = document.querySelectorAll(arguments[0])
            var element_name = arguments[1];
            for (var i = 0; i < elems.length; i++) {
                if (elems[i].innerText == element_name) {
                    return elems[i];
                }
            };
            throw "Can not find column: " + element_name;
            """, COLUMN_TREE_PICKER_NODE_TEXT_AREA, column_name)
    simulate.hover(column_tree_node_text_area)
    dom.click_element(column_tree_node_text_area, COLUMN_TREE_PICKER_ADD_NODE_BUTTON)


def add_column_by_name(driver, column_name):
    """
    Gets elements in the D/C tree and clicks the element with text that matches provided name.

    :param driver: webdriver
    :param column_name: str, name of the element that needs to be added
    :return: None
    """
    search_and_selecting_column_in_columns_tree(driver, column_name, COLUMN_TREE_PICKER_SEARCH)

    modal = dom.get_element(driver, PARAMETERIZED_MODEL_DIALOG, dont_raise=True, timeout=3)
    added_column_name = column_name
    if modal:
        # this logic is for parametrized model dialog.
        added_column_name = make_unique_name(column_name)
        base.set_input_text(modal, column_name, character_delay=0.1)
        base.click_ok(modal)

    check_for_butterbar(driver, 'Adding columns to LiveReport', visible=False)

    return added_column_name


def add_column_by_expanding_nodes(driver, nodes):
    """
    This will add the column to the LiveReport using double click by expanding all given nodes
    :param driver: selenium driver
    :param nodes: list of all nodes including the column has to be selected
    :return:
    """

    for column_name in nodes[:-1]:
        element = dom.get_element(driver, COLUMN_FOLDER_MULTI_SELECT, column_name, exact_text_match=True)
        dom.click_element(element, COLUMN_TREE_PICKER_NODE_ICON_AREA)

    element = dom.get_element(driver, COLUMN_TREE_PICKER_NODE_TEXT_AREA, text=nodes[-1], exact_text_match=True)
    simulate.double_click(element)


def select_multiple_columns_in_column_tree(driver, column_dict, is_section=True):
    """
    Selecting multiple columns sequentially using Ctrl+click, This won't work, If column not there in visible range.

    :param driver: Selenium Webdriver
    :param column_dict: dictionary,
        keys: parent folders(included section),
        values: dictionary(which has parent folders as keys and list of columns as values) or List of columns.
        format: {section1:{parent_fol1:{parent_fol2:[col1, col2, ..]}}, section2: {parent_fol3: [col3, col4, ..]}}
    :param is_section: boolean,
        True if keys of column_dict are sections like 'Computational Models',
        False otherwise(for parent columns)
    """
    for section in column_dict:
        section_iterator = {section: column_dict[section]}
        # expand column tree nodes and return the columns to select
        columns_to_be_selected = expand_column_tree_nodes(driver, section_iterator, is_section)
        # selecting columns using Ctrl+Click
        select_multiple_columns_by_ctrl_click(driver, columns_to_be_selected)
        # Closing opened section
        if is_section:
            scroll_column_tree_to_top(driver)
            dom.click_element(driver, COLUMN_TREE_PICKER_TEXT_NODE, text=section, exact_text_match=True)


def select_multiple_contiguous_columns_in_column_tree(driver, column_dict, is_section=True):
    """
    Selecting multiple columns sequentially using shift+click, This won't work if the column is not in the visible range

    :param driver: Selenium webdriver
    :param column_dict: dictionary,
        keys: parent folders(included section),
        values: dictionary(which has parent folders as keys and list of columns as values) or List of columns.
        format: {section:{parent_col1:{parent_col2:[start_column, end_column]}}}
    :param is_section: boolean,
        True if keys of column_dict are sections like 'Computational Models',
        False otherwise(for parent columns)
    """
    for section in column_dict:
        section_iterator = {section: column_dict[section]}
        # expand column tree nodes and return the columns to select
        columns_to_be_selected = expand_column_tree_nodes(driver, section_iterator, is_section)
        # selecting columns using Shift+Click
        select_multiple_columns_by_shift_click(driver, columns_to_be_selected)
        # Closing opened section
        if is_section:
            scroll_column_tree_to_top(driver)
            dom.click_element(driver, COLUMN_TREE_PICKER_TEXT_NODE, text=section, exact_text_match=True)


def rename_grouped_column(driver, column_name, new_column_name):
    """
    Renames grouped column.

    :param driver: Selenium webdriver
    :param column_name: str, grouped column which for which you want to rename
    :param new_column_name: str, new column name
    """
    click_column_menu_item(driver, column_name, "Rename Group…")
    # check for Rename Group dialog box
    verify_is_visible(driver, MODAL_DIALOG_HEADER, selector_text="Rename Group '{}'".format(column_name))
    # set new column name as input
    dom.set_element_value(driver, COMPONENTS_TEXT_INPUT_BOX, value=new_column_name)
    base.click_ok(driver)


def search_in_columns_tree(driver, search_term):
    """
    Searches in Data & Columns Tree searchbox
    :param driver: Selenium webdriver
    :param search_term: str, Search query that is passed in the search box
    """
    open_add_data_panel(driver)
    dom.set_element_value(driver, selector=COLUMN_TREE_PICKER_SEARCH, value=search_term)


def search_and_select_column_from_columns_mgmt_ui(driver, search_term):
    """
    Search, verify and click on column in column management UI
    :param driver: Selenium webdriver
    :param search_term: text for searching
    """
    search_in_col_mgmt_ui(driver, search_term)
    verify_is_visible(driver, LIVEREPORT_VISIBLE_COLUMN_LABEL, selector_text=search_term)
    dom.click_element(driver, LIVEREPORT_VISIBLE_COLUMN_LABEL, text=search_term)


def select_multiple_columns_by_ctrl_click(driver, column_list):
    """
    Selects multiple columns by pressing down Control(Win)/Command(Mac) key

    :param driver: Selenium webdriver
    :param column_list: List of columns to be selected
    """
    control_key = dom.get_ctrl_key()
    for column in column_list:
        column_element = dom.get_element(driver, COLUMN_TREE_PICKER_NODE_TEXT_AREA, text=column, exact_text_match=True)
        ActionChains(driver).key_down(control_key).click(column_element).key_up(control_key).perform()


def select_multiple_columns_by_shift_click(driver, column_list):
    """
    Selects multiple columns by pressing down Shift key

    :param driver: Selenium webdriver
    :param column_list: List of first and last column to be selected, so it selects
                        all the columns in between including these two
    """
    dom.click_element(driver, COLUMN_TREE_PICKER_NODE_TEXT_AREA, text=column_list[0], exact_text_match=True)
    end_column_element = dom.get_element(driver,
                                         COLUMN_TREE_PICKER_NODE_TEXT_AREA,
                                         text=column_list[1],
                                         exact_text_match=True)
    ActionChains(driver).key_down(Keys.SHIFT).click(end_column_element).key_up(Keys.SHIFT).perform()


def expand_column_tree_nodes(driver, column_dict, is_section):
    """
    Expands column tree nodes as the path is given in column_dict and returns list of columns

    :param driver: Selenium webdriver
    :param column_dict: dictionary, columns within a single section
        keys: parent folders(included section),
        values: dictionary(which has parent folders as keys and list of columns as values) or List of columns.
        format: {section:{parent_fol1:{parent_fol2:[col1, col2, ..]}}}
    :param is_section: boolean,
        True if key of column_dict is section like 'Computational Models',
        False otherwise(for parent columns)
    :return: List of columns
    :rtype: List[str]
    """
    for section in column_dict:
        column_list = column_dict[section]

        if is_section:
            # opening the section in D&C tree
            dom.click_element(driver, COLUMN_TREE_PICKER_TEXT_NODE, text=section, exact_text_match=True)
        else:
            # expanding parent folder
            element = dom.get_element(driver, COLUMN_FOLDER_MULTI_SELECT, text=section, exact_text_match=True)
            dom.click_element(element, COLUMN_TREE_PICKER_NODE_ICON_AREA)

        if isinstance(column_list, dict):
            # expanding folders/sub-folders recursively
            column_list = expand_column_tree_nodes(driver, column_list, is_section=False)
        else:
            # return list of columns
            return column_list
        return column_list


def clear_column_selection(driver):
    """
    Clears any selected node from columns tree by selecting a separate node and then de-selecting it

    :param driver: Selenium webdriver
    """
    scroll_column_tree_to_top(driver)
    # expands the section
    dom.click_element(driver, COLUMN_TREE_PICKER_TEXT_NODE, text='Computed Properties', exact_text_match=True)
    # selects a node
    column_element = dom.get_element(driver,
                                     selector=COLUMN_TREE_PICKER_NODE_TEXT_AREA,
                                     text='Chemaxon LibMCS',
                                     exact_text_match=True)
    dom.click_element(column_element, selector=COLUMN_FOLDER_TEXT_AREA, text='Chemaxon LibMCS', exact_text_match=True)
    # deselects the node
    control_key = dom.get_ctrl_key()
    ActionChains(driver).key_down(control_key).click(column_element).key_up(control_key).perform()
    # collapses the open section
    dom.click_element(driver, COLUMN_TREE_PICKER_TEXT_NODE, text='Computed Properties', exact_text_match=True)
