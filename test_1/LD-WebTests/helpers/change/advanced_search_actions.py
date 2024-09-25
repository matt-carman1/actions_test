from helpers.change import autosuggest_actions, range_actions
from helpers.change.columns_action import add_column_by_expanding_nodes, \
    search_and_selecting_column_in_columns_tree
from helpers.change.live_report_picker import open_live_report
from helpers.change.sketcher import import_structure_into_sketcher
from helpers.verification.maestro import verify_molv_from_maestro_equals
from helpers.change.actions_pane import open_add_compounds_panel, open_advanced_search
from helpers.selection.advanced_search import ADVANCED_SEARCH_TEXTBOX, ADV_QUERY_BOX_WIDGET, ADV_QUERY_PANEL_HEADER, \
    ALL_IDS_LINK, BOTTOM_OPTIONS_LINKS, CLEAR_ADVANCED_QUERY_BUTTON, CLEAR_ADVANCED_QUERY_DIALOG_TITLE, \
    COMPOUND_STRUCTURE_LINK, INACTIVE_MODE_BUTTON, SIMILARITY_VALUE_INPUT, PRESENCE_IN_LR_DROPDOWN_OPTIONS, \
    PRESENCE_IN_LR_DROPDOWN, QUERY_RANGE_LOWER_VALUE_INPUT, \
    QUERY_RANGE_UPPER_VALUE_INPUT, SEARCH_AND_ADD_COMPOUNDS_BUTTON, ADV_QUERY_COG_ICON, ADVANCED_SEARCH_TYPE, \
    ADVANCED_SEARCH_VIEW_MENU, COMPLEX_ADV_QUERY_PANEL
from helpers.selection.general import HEADER_NAME, STRUCTURE_IMAGE
from helpers.selection.modal import MODAL_DIALOG_HEADER
from helpers.selection.add_compound_panel import COMPOUNDS_PANE_ACTIVE_TAB
from helpers.selection.general import MENU_ITEM
from helpers.selection.sketcher import ADVANCED_SEARCH_SKETCHER_IFRAME
from library import base, dom, ensure, wait, simulate
from library.dom import LiveDesignRetryException


def get_query(driver, query_name):
    """
    Gets the advanced query element by the given query name

    :param driver: webdriver
    :param query_name: str, name of the query
    :return: query panel element
    """
    # wait for query to appear
    wait.until_visible(driver, HEADER_NAME, text=query_name)

    # get list of queries
    query_list = dom.get_elements(driver, ADV_QUERY_BOX_WIDGET)

    # if query matches given name, then return the element
    for query in query_list:
        header_name = dom.get_element(query, ADV_QUERY_PANEL_HEADER)
        if header_name.text == query_name:
            return query

    # we didn't get the query panel element, so throw an error
    raise RuntimeError("Cannot find query '{}'".format(query_name))


def add_query(driver, query_name, display_name=None, text_search=True):
    """
    Adds an advanced query either by:
    1. searching the D&C (default) OR
    2. clicking on a query link

    :param driver: webdriver
    :param query_name: str, query name to add
    :param display_name: str, the name displayed after a query is selected, defaults to None
    :param text_search: boolean, True to search for query in D&C tree (default if not set)
                                    OR
                                 False to click on a query link
    :return: None
    """
    text_query = str(query_name)

    if text_search:
        search_and_selecting_column_in_columns_tree(driver, text_query, ADVANCED_SEARCH_TEXTBOX)
        if display_name:
            query_name = "{}".format(display_name)

        wait.until_visible(driver, HEADER_NAME, text=query_name)

    else:
        # clicks on the textbox to activate the column selector, this is
        # required because the column selector displays the bottom options
        dom.click_element(driver, ADVANCED_SEARCH_TEXTBOX)

        # find query link matching given name and click it
        dom.click_element(driver, BOTTOM_OPTIONS_LINKS, text=query_name)


def add_column_with_multiple_endpoints(driver, column_name, endpoint_name=None):
    # type in search term to textbox
    dom.set_element_value(driver, ADVANCED_SEARCH_TEXTBOX, str(column_name))
    # clicks the item in the D&C Tree
    add_column_by_expanding_nodes(driver, [endpoint_name])
    query_name = column_name + ' (' + endpoint_name + ')'
    wait.until_visible(driver, HEADER_NAME, text=query_name)


def add_query_compound_structure(driver, molv3):
    """
    Adds a Compound Structure advanced search query

    :param driver: webdriver
    :param molv3: str, molv3 string to query
    :return: None
    """
    # Add compound query
    add_query(driver, COMPOUND_STRUCTURE_LINK, text_search=False)

    # import structure molv3 or SMILES into sketcher
    import_structure_into_sketcher(driver, molv3, sketcher_iframe_selector=ADVANCED_SEARCH_SKETCHER_IFRAME)

    # presses the OK button to add the compound structure
    base.click_ok(driver)

    wait.until_visible(driver, ADV_QUERY_PANEL_HEADER, text='Compound Structure')

    # wait for the structure to appear (There is a slight delay for the structure image to appear once 'OK' is
    # clicked on the sketcher, which causes the test to fail occasionally)
    def _image_not_pending(img_element):
        if img_element.get_attribute('src').endswith('pending_structure.png'):
            raise LiveDesignRetryException('structure image is pending placeholder; compound image expected')

    dom.get_element(driver, STRUCTURE_IMAGE, action_callback=_image_not_pending)


def set_similarity_percent_for_structure_search(driver, tanimoto_score_threshold):
    """
    Sets a new tanimoto score threshold value for the Compound Structure advanced search query.

    :param driver: webdriver
    :param tanimoto_score_threshold: number, sets the similarity field to a number
    :return: None
    """
    # prevents an auto-update tooltip element from covering the similarity threshold input field
    search_button = dom.get_element(driver, SEARCH_AND_ADD_COMPOUNDS_BUTTON)
    simulate.hover(driver, search_button)

    ensure.element_visible(driver,
                           expected_visible_selector=SIMILARITY_VALUE_INPUT,
                           action_selector=INACTIVE_MODE_BUTTON)
    wait.until_visible(driver, SIMILARITY_VALUE_INPUT)
    dom.set_element_value(driver, SIMILARITY_VALUE_INPUT, str(tanimoto_score_threshold))
    # this extra click in necessary for the values to synced in the query, without this click the query just runs
    # with the old value
    dom.click_element(driver, COMPOUNDS_PANE_ACTIVE_TAB)


def add_query_all_id(driver, id_list):
    """
    Adds a All Ids advanced search query and
    populates given entries.

    :param driver: webdriver
    :param id_list: list of IDs to be added to the query
    :return: None
    """

    # Add All Ids query
    add_query(driver, ALL_IDS_LINK, text_search=False)
    query_box = get_query(driver, ALL_IDS_LINK)

    # Add items from id_list into the query
    autosuggest_actions.set_autosuggest_items(query_box, id_list)


def remove_all_search_conditions(driver):
    """
    Removes all the search conditions

    :param driver: webdriver
    :return: None
    """
    dom.click_element(driver, CLEAR_ADVANCED_QUERY_BUTTON)
    wait.until_visible(driver, MODAL_DIALOG_HEADER, text=CLEAR_ADVANCED_QUERY_DIALOG_TITLE)
    base.click_ok(driver)


def add_query_presence_in_live_report(driver, name):
    """
    Adds query "Presence in LiveReport" to the advance search panel. Will set the query to the name, if specified

    :param driver: webdriver
    :param name: str, LiveReport name
    """
    # Add query to advanced search panel
    add_query(driver, "Presence in LiveReport", text_search=False)

    # Set LiveReport
    presence_in_live_report = get_query(driver, "Presence in LiveReport")
    wait.until_visible(presence_in_live_report, PRESENCE_IN_LR_DROPDOWN)
    dom.click_element(presence_in_live_report, PRESENCE_IN_LR_DROPDOWN)

    # Click on the 'Choose LiveReport...' link
    wait.until_visible(driver, PRESENCE_IN_LR_DROPDOWN_OPTIONS)
    dom.click_element(driver, PRESENCE_IN_LR_DROPDOWN_OPTIONS, text='Choose LiveReport...')
    wait.until_visible(driver, MODAL_DIALOG_HEADER)

    # find and select LiveReport
    open_live_report(driver, name=name)


def set_query_range(query_element, lower_limit=None, upper_limit=None):
    """
    Adjust a query condition's range based on upper and lower limit

    NOTE: This is similar to the filter_actions.set_filter_range,
    but unlike that function this doesn't reset the condition before setting the values

    :param query_element: query condition element to work on
    :param lower_limit: lower range limit value
    :param upper_limit: upper range limit value
    """

    if lower_limit is not None:
        range_actions.set_range_limit_value(query_element, QUERY_RANGE_LOWER_VALUE_INPUT, lower_limit)

    simulate.click(query_element)

    if upper_limit is not None:
        range_actions.set_range_limit_value(query_element, QUERY_RANGE_UPPER_VALUE_INPUT, upper_limit)

    simulate.click(query_element)


def choose_adv_query_options(driver, query_name, option_to_choose=None):
    """
    Choosing the option from the AdvQuery cog menu
    :param driver: Selenium webdriver
    :param query_name: the name of the query
    :param option_to_choose: The option to choose from the cog menu
    """
    query = get_query(driver, query_name)
    dom.click_element(query, ADV_QUERY_COG_ICON)
    wait.until_visible(query, ADV_QUERY_COG_ICON)
    dom.click_element(query, MENU_ITEM, text=option_to_choose)


def open_complex_advanced_search_panel(driver):
    """
    Opening the Advanced Search panel and switching to Complex view mode
    :param driver: Selenium webdriver
    """
    # Open the Compounds Panel
    open_add_compounds_panel(driver)
    open_advanced_search(driver)

    # Switching to complex view
    dom.click_element(driver, ADVANCED_SEARCH_TYPE, text='Simple')
    dom.click_element(driver, ADVANCED_SEARCH_VIEW_MENU, text='Complex')
    wait.until_visible(driver, COMPLEX_ADV_QUERY_PANEL)
