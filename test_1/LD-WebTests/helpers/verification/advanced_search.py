from helpers.selection.column_tree import COLUMN_TREE_SEARCH_HIGHLIGHTED, COLUMN_TREE_PICKER_TOOLTIP_HEADER_TEXT, \
    COLUMN_TREE_PICKER_TOOLTIP_BODY_TEXT
from library import dom, simulate
from library.eventually import eventually_equal
from helpers.selection.actions_pane import ADD_COMPOUND_BUTTON
from helpers.selection.advanced_search import ADVANCED_SEARCH_ACTIVE_CLASS, ADV_QUERY_PANEL_HEADER, \
    ADVANCED_SEARCH_TEXTBOX
from helpers.verification.element import verify_is_visible


def verify_active_search_callout(driver, expected_compound_count):
    """
    Verifies the callout on the compound drawer button is pulsating
    and displays the correct value while an auto update advanced search is active

    :param driver: webdriver
    :param expected_compound_count: int, The number which should be displayed on the callout
    :return: None
    """

    assert eventually_equal(driver, _get_callout_count, expected_compound_count), \
        "Expected the compound callout count to be {}".format(expected_compound_count)

    verify_is_visible(driver, ADVANCED_SEARCH_ACTIVE_CLASS)


def _get_callout_count(driver):
    compound_button = dom.get_element(driver, ADD_COMPOUND_BUTTON)
    return int(compound_button.get_attribute('data-callout'))


def verify_added_columns_in_advanced_query_panel(driver, expected_column_names):
    """
    Verify columns which are in visible range in advanced search query panel.

    :param driver: Selenium Webdriver
    :param expected_column_names: list, list of expected column names in advanced search query panel
    """
    widget_elems = dom.get_elements(driver, ADV_QUERY_PANEL_HEADER, dont_raise=True)
    column_names = [widget.text for widget in widget_elems]
    assert column_names == expected_column_names, 'Actual column names:{}, expected column names:{}'.format(
        column_names, expected_column_names)


def verify_column_searched_tooltip_in_advanced_query(driver, search_term, tooltip_body=False, tooltip_body_text=''):
    """
    Searches for column in Advanced Search panel
    Hovers over the column name to verify its name & description from the tooltip
    :param driver: selenium webdriver
    :param search_term: str, column name to search
    :param tooltip_body: bool, True if tooltip contains a description text, by default False
    :param tooltip_body_text: str, tooltip description text
    """
    dom.set_element_value(driver, ADVANCED_SEARCH_TEXTBOX, search_term)
    # Column names having multiple words show highlight markup tag separately on them, adding (") to column name
    # highlights the whole name as a single tag but fails in verification step so removing (")
    search_hit = search_term.replace('"', '')
    simulate.hover(driver, dom.get_element(driver, COLUMN_TREE_SEARCH_HIGHLIGHTED, text=search_hit))
    verify_is_visible(driver,
                      COLUMN_TREE_PICKER_TOOLTIP_HEADER_TEXT,
                      selector_text=search_hit,
                      exact_selector_text_match=True)
    if tooltip_body:
        verify_is_visible(driver,
                          COLUMN_TREE_PICKER_TOOLTIP_BODY_TEXT,
                          selector_text=tooltip_body_text,
                          exact_selector_text_match=True)
