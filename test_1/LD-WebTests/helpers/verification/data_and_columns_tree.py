from helpers.change.actions_pane import open_add_data_panel, close_add_data_panel
from helpers.change.data_and_columns_tree import clear_column_tree_search, search_column_tree
from helpers.selection.column_tree import (COLUMN_TREE_SEARCH_BOX, COLUMN_TREE_PICKER_NODE_TEXT_AREA,
                                           INVALID_SEARCH_RESULT, COLUMNS_TREE_LIVEREPORT_TAB,
                                           LIVEREPORT_CHECKED_COLUMNS, LIVEREPORT_COLUMN_CHECKBOX_LABEL,
                                           LIVEREPORT_COLUMN_CONTAINER_ID_, LIVEREPORT_COLUMN_LABEL_HIGHLIGHT,
                                           COLUMN_TREE_SEARCH_HIGHLIGHTED, LIVEREPORT_COLUMN_MANAGER_BUTTON)
from helpers.verification.element import verify_is_not_visible, verify_is_visible
from library.eventually import eventually_equal
from library.wait import until_condition_met
from library import dom


def verify_no_column_exists_in_column_tree(driver, column_name_to_search):
    """
    Verify that there exist no column with the given column name.
    :param driver: Selenium Webdriver
    :param column_name_to_search: str, Column Name to search for
    :return:
    """
    open_add_data_panel(driver)
    dom.set_element_value(driver, COLUMN_TREE_SEARCH_BOX, column_name_to_search)

    def callback(element):
        assert element.get_attribute('textContent') == "No columns match your search term."

    invalid_search_result = dom.get_element(driver,
                                            INVALID_SEARCH_RESULT,
                                            dont_raise=True,
                                            timeout=3,
                                            action_callback=callback)
    if not invalid_search_result:
        verify_is_not_visible(driver, selector=COLUMN_TREE_PICKER_NODE_TEXT_AREA, selector_text=column_name_to_search)

    clear_column_tree_search(driver)
    close_add_data_panel(driver)


def verify_column_exists_in_column_tree(driver, column_name, search_retries=1):
    """
    Verify whether column present in D&C tree. This would fail if there exists multiple columns
    with exactly same name.
    :param driver: Selenium webdriver
    :param column_name: str, name of the column
    :param search_retries: number of times to retry the search if the column is not found
    in column tree search results. Can be set to greater than 1 to retry the search multiple
    times when we want to check the presence of a column in column tree immediately
    after creating it.
    :return:
    """
    open_add_data_panel(driver)
    verify_column_visible_in_column_tree_by_searching(driver, column_name, search_retries)
    clear_column_tree_search(driver)
    close_add_data_panel(driver)


def verify_column_visible_in_column_tree_by_searching(driver, column_name, retries=1):
    """
    Verify whether column eventually becomes visible in column tree by repeating the search multiple times
    while the column is not found in search results. This would fail if there exists multiple columns
    with exactly same name.
    :param driver: Selenium webdriver
    :param column_name: str, name of the column
    :param retries: number of times to retry the search if the column is not found in column tree search results.
    Can be set to greater than 1 to retry the search multiple times when we want to check the presence of a
    column in column tree immediately after creating it.
    :return:
    """

    def search_and_check_column_visible_in_column_tree():
        search_column_tree(driver, column_name)
        visible = verify_is_visible(driver,
                                    selector=COLUMN_TREE_PICKER_NODE_TEXT_AREA,
                                    selector_text=column_name,
                                    exact_selector_text_match=True,
                                    dont_raise=True)
        assert visible

    until_condition_met(search_and_check_column_visible_in_column_tree, retries)


def verify_visible_columns_from_column_mgmt_ui(selenium, expected_column_names):
    """
    Verifying visible columns in LR by using checked columns in column management UI, opening and closing D&C Tree is
    not included in helper
    :param selenium: selenium webdriver
    :param expected_column_names: list, List of column names which are there in LR
    :return:
    """
    # Navigating to LiveReport tab in D&C tree
    dom.click_element(selenium, COLUMNS_TREE_LIVEREPORT_TAB)

    def get_visible_columns_list(driver_):
        tree_ui_column_elements = dom.get_elements(driver_, LIVEREPORT_CHECKED_COLUMNS)
        observed_columns_in_tree_ui = [element.text for element in tree_ui_column_elements]
        return sorted(observed_columns_in_tree_ui)

    # verifying the actual columns names with expected column names
    assert eventually_equal(selenium, get_visible_columns_list, sorted(expected_column_names)), \
        "Expected following column labels order in the Columns Management UI {} but got {}.".format(
            sorted(expected_column_names), get_visible_columns_list(selenium))


def verify_columns_in_column_mgmt_ui(driver, expected_columns):
    """
    Verify the column names in the Column Management UI.
    :param driver: Selenium Webdriver
    :param expected_columns: list, expected column names Order of the columns is important starting from top to bottom.
    """

    def get_columns_list(driver_):
        tree_ui_column_elements = dom.get_elements(driver_, LIVEREPORT_COLUMN_CHECKBOX_LABEL)
        observed_columns_in_tree_ui = [element.text for element in tree_ui_column_elements]
        return observed_columns_in_tree_ui

    assert eventually_equal(driver, get_columns_list, expected_columns), \
        "Expected following column labels order in the Columns Management UI{} but got {}.".format(
            expected_columns, get_columns_list(driver))


def verify_grouped_columns_in_column_mgmt_ui(driver, expected_grouped_columns_list, group_name):
    """
    Verify the grouped column names in the Columns Management UI (LiveReport Tab under D&C Tree).
    :param driver: Selenium Webdriver
    :param expected_grouped_columns_list: list, expected column names in the column group in the Column Management UI
                                          from the top to bottom. Order of the column names is important too.
    :param group_name: str, name of the group
    """

    def get_group_columns_from_column_mgmt_ui(driver_):
        group_element = dom.get_element(driver_,
                                        LIVEREPORT_COLUMN_CONTAINER_ID_.format('columnGroup_'),
                                        text=group_name)
        group_parent_div = dom.get_parent_element(group_element)
        observed_grouped_columns_in_tree_ui = group_parent_div.text.split("\n")[1:]
        return observed_grouped_columns_in_tree_ui

    assert eventually_equal(driver, get_group_columns_from_column_mgmt_ui, expected_grouped_columns_list), \
        "Expected following column names to be frozen {}".format(expected_grouped_columns_list)


def verify_highlighted_column_names(driver, expected_highlighted_column_names, columns_tree=True, only_expected=True):
    """
    Validates the column label which contains the text highlighted using <mark> tag or not.

    :param driver: Selenium Webdriver
    :param expected_highlighted_column_names: list, list of expected columns
                                              or use an empty list if there are no expected highlighted columns
    :param columns_tree: bool, The view where verification takes place, by default it's columns tree view
                        False reverts to column management ui view
    :param only_expected: bool, True if only expected columns should be highlighted, False if others are permitted
    """
    if columns_tree:
        element = COLUMN_TREE_SEARCH_HIGHLIGHTED
    else:
        element = LIVEREPORT_COLUMN_LABEL_HIGHLIGHT
    highlighted_column_names = [
        dom.get_parent_element(elem).text for elem in dom.get_elements(driver, element, timeout=3, dont_raise=True)
    ]

    if only_expected:
        assert set(highlighted_column_names) == set(expected_highlighted_column_names)
    else:
        assert set(expected_highlighted_column_names).issubset(
            set(highlighted_column_names)
        ), f'Expected {expected_highlighted_column_names} to be a subset of actual columns ({highlighted_column_names})'


def verify_click_column_via_col_tree(driver, selector_text):
    """
    Verify the selector_text on livereport_column_manager and click on it.
    :param driver: Selenium Webdriver
    :param selector_text: str, text that may be visible on UI regarding the selector
    """
    verify_is_visible(driver, LIVEREPORT_COLUMN_MANAGER_BUTTON, selector_text=selector_text)
    dom.click_element(driver, LIVEREPORT_COLUMN_MANAGER_BUTTON, text=selector_text)
