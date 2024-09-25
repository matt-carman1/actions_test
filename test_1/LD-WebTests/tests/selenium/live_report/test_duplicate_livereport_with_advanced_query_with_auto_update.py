import pytest

from helpers.change.actions_pane import open_advanced_search, open_add_compounds_panel
from helpers.change.advanced_search_actions import add_query, get_query, add_query_presence_in_live_report
from helpers.change.autosuggest_actions import set_autosuggest_items
from helpers.flows.live_report_management import copy_active_live_report
from helpers.selection.advanced_search import AUTO_UPDATE_CHECKBOX, SEARCH_AND_ADD_COMPOUNDS_BUTTON, \
    ADV_QUERY_STOP_SEARCH, QUERY_HEADERS, AUTO_UPDATE_CHECKED
from helpers.verification.grid import verify_is_visible
from library import dom, wait


@pytest.mark.smoke
def test_duplicate_livereport_with_advanced_query_with_auto_update(selenium, new_live_report, open_livereport):
    """
    This test confirms successful LiveReport duplication of an auto-updating advanced query search containing the
    following query types:

    1. text
    2. ranged
    3. "Presence in LiveReport"
    """
    # Open the Compounds Panel & then the advanced search panel
    open_add_compounds_panel(selenium)
    open_advanced_search(selenium)

    ### ADD TEXT QUERY ###
    add_query(selenium, "Lot Scientist")
    # Set value "(defined)" in text query
    lot_scientist_query = get_query(selenium, "Lot Scientist")
    # select_query_checkbox_item(lot_scientist_query, "(defined)")
    set_autosuggest_items(lot_scientist_query, ["(defined)"])

    ### ADD RANGED QUERY ###
    add_query(selenium, "Random integer (Result)")

    ### ADD "PRESENCE IN LIVEREPORT" QUERY ###
    # Add Presence in LR and set LR name
    add_query_presence_in_live_report(selenium, name="Presence in LR")

    ### AUTO_UPDATE SEARCH ###
    # Enable auto-update results
    dom.click_element(selenium, AUTO_UPDATE_CHECKBOX)
    verify_is_visible(selenium, AUTO_UPDATE_CHECKED)

    # Click "Search for Compounds" button
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)

    ### DUPLICATE CURRENT LR ###
    copy_active_live_report(selenium, livereport_name=new_live_report, new_name="adv_queries_duplicated")
    wait.until_live_report_loading_mask_not_visible(selenium)

    ### TEST PASSING CRITERIA ###
    # Confirm LR is in auto-update result mode
    wait.until_visible(selenium, ADV_QUERY_STOP_SEARCH)
    # Confirm Advanced Search queries are duplicated
    actual_present_queries = {query.text for query in dom.get_elements(selenium, QUERY_HEADERS)}
    expected_present_queries = {"Lot Scientist", "Presence in LiveReport", "Random integer (Result)"}
    assert expected_present_queries == actual_present_queries, \
        "Expected list of queries, `{}` not found in actual list of queries `{}`".format(
            actual_present_queries, expected_present_queries)
