from helpers.change import actions_pane
from helpers.change.compound_actions import search_and_add_compounds_by_pasting_id
from helpers.selection.add_compound_panel import ADD_IDEA_TO_LIVE_REPORT_BUTTON, SEARCH_AND_ADD_COMPOUNDS_BUTTON, \
    ADD_IDEA_TAB, SUBSTRUCTURE_TAB, SIMILARITY_TAB

from library import dom, wait
from helpers.selection.add_compound_panel import COMPOUND_SEARCH_BY_ID_TEXTAREA, COMPOUND_SEARCH_BUTTON, \
    COMPOUND_SEARCH_SUB_TAB, COMPOUND_SEARCH_SUB_TAB_ACTIVE, MAX_RESULTS_INPUT, MAX_RESULTS_DIALOG, GEAR_BUTTON_DOWN, \
    GEAR_BUTTON_UP
from helpers.change.sketcher import import_structure_into_sketcher
from helpers.verification.maestro import verify_molv_from_maestro_equals
from helpers.verification.element import verify_is_visible
from library.scroll import scroll_element_by


def add_compound_by_molv_to_active_lr(driver,
                                      molv3,
                                      mode=ADD_IDEA_TAB,
                                      max_results=None,
                                      scroll_required_for_max_results=False):
    """
    Encapsulate the flow of actions to add a compound to the active live report
    by molv3 string.

    :param driver: webdriver
    :param mode: str, ADD_IDEA_TAB, SIMILARITY_TAB, SUBSTRUCTURE_TAB, or EXACT_TAB
    :param molv3: str, MOLV3 compound representation
    :param max_results: maximum number of results to be returned
    :param scroll_required_for_max_results: boolean, Whether we need to scroll in the Compounds Panel to reach the gear icon for max
                            results.
    """

    if mode == ADD_IDEA_TAB:
        actions_pane.open_compound_design_panel(driver)
    else:
        actions_pane.open_compound_search_panel(driver)
        if mode == SIMILARITY_TAB:
            dom.click_element(driver, COMPOUND_SEARCH_SUB_TAB, text='Similarity', exact_text_match=True)
            wait.until_visible(driver, COMPOUND_SEARCH_SUB_TAB_ACTIVE, text='Similarity')
        elif mode == SUBSTRUCTURE_TAB:
            dom.click_element(driver, COMPOUND_SEARCH_SUB_TAB, text='Substructure', exact_text_match=True)
            wait.until_visible(driver, COMPOUND_SEARCH_SUB_TAB_ACTIVE, text='Substructure')
        else:
            dom.click_element(driver, COMPOUND_SEARCH_SUB_TAB, text='Exact Match', exact_text_match=True)
            wait.until_visible(driver, COMPOUND_SEARCH_SUB_TAB_ACTIVE, text='Exact Match')

    # Adds molv3 string to sketcher
    import_structure_into_sketcher(driver, molv3)
    # Calculating the atoms and bonds of the original mol block
    atoms_bond_count = molv3.split('\n')[5].split()[3:5]
    verify_molv_from_maestro_equals(driver, atoms_bond_count)

    # Sets max results if specified
    if max_results:
        max_results_on_search(driver, max_result=max_results, scroll_required=scroll_required_for_max_results)

    # Clicks the add to LR button
    add_button = ADD_IDEA_TO_LIVE_REPORT_BUTTON if mode == ADD_IDEA_TAB else SEARCH_AND_ADD_COMPOUNDS_BUTTON
    dom.click_element(driver, add_button)


def search_by_id(driver, ids):
    """
    Search the compounds in the database by id(s)

    :param driver: Selenium Webdriver
    :param ids: <str> id to search
    """
    open_search_by_id_tab(driver)
    # We manually clear the text-area otherwise we get a staleStateException if we rely on set_element_value to clear
    # the existing values
    search_by_id_textarea = dom.get_element(driver, COMPOUND_SEARCH_BY_ID_TEXTAREA)
    search_by_id_textarea.clear()
    dom.set_element_value(driver, COMPOUND_SEARCH_BY_ID_TEXTAREA, ids, clear_existing_value=False, character_delay=0.1)
    dom.click_element(driver, COMPOUND_SEARCH_BUTTON)


def max_results_on_search(driver, max_result, scroll_required=False):
    """
    Method to tweak the max results of a search.
    Note ability to tweak with the Compounds/R-groups have not been added yet.

    :param driver: Selenium webdriver
    :param max_result: int, The max results to be searched for
    :param scroll_required: boolean, Whether we need to scroll in the Compounds Panel to reach the gear icon for max
                            results.
    """
    if scroll_required:
        scroll_ele = dom.get_element(driver, '#compounds-pane-container .active-tab-content', timeout=10)
        scroll_element_by(driver, scrollable_element=scroll_ele, vertical_px=100)

    dom.click_element(driver, GEAR_BUTTON_DOWN)
    verify_is_visible(driver, MAX_RESULTS_DIALOG)
    dom.set_element_value(driver, MAX_RESULTS_INPUT, max_result)
    dom.click_element(driver, GEAR_BUTTON_UP)


def open_search_by_id_tab(driver):
    """
    Opens Compounds Panel and then opens search by ID tab.
    :param driver: Selenium Webdriver
    """
    actions_pane.open_add_compounds_panel(driver)
    actions_pane.open_compound_search_panel(driver)
    dom.click_element(driver, COMPOUND_SEARCH_SUB_TAB, text='ID', exact_text_match=True)
    wait.until_visible(driver, COMPOUND_SEARCH_SUB_TAB_ACTIVE, text='ID')
    wait.until_visible(driver, COMPOUND_SEARCH_BY_ID_TEXTAREA)


def open_search_add_compound_by_id(selenium, seperated_symbol, actual_input):
    """
    1. Open the add compounds panel
    2. Search compounds with copy and pasting compound IDs in the compound-ID search textarea.
    3. Clicking the appropriate radio buttons depending on the compound ID string pasted, for example: Semicolon,\
       Comma,None, White space
    4. Adding the compounds to the LR
    param seperated_symbol: seperated symbol from parametrize data
    param actual_input: Actual compounds from parametrize data as a string
    """

    # Opening the compounds panel and searching for the ID tab
    open_search_by_id_tab(selenium)
    # Adding the semicolon separated compound IDs
    search_and_add_compounds_by_pasting_id(selenium, seperated_symbol, actual_input)
