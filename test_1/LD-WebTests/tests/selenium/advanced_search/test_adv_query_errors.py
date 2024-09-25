import pytest

from helpers.change.advanced_search_actions import add_query, get_query, set_query_range, \
    add_query_presence_in_live_report
from helpers.change.actions_pane import open_add_compounds_panel, open_advanced_search
from helpers.selection.advanced_search import ADV_QUERY_INVERT, CLEAR_ADVANCED_QUERY_BUTTON, \
    DISABLED_SEARCH_AND_ADD_COMPOUNDS_BUTTON, ADV_QUERY_WARNING, PRESENCE_IN_LR_DROPDOWN_TITLE, \
    SEARCH_AND_ADD_COMPOUNDS_BUTTON
from helpers.selection.modal import MODAL_DIALOG_HEADER, MODAL_DIALOG_BODY
from helpers.verification.grid import verify_is_visible
from library import dom, base


@pytest.mark.k8s_defect(reason="SS-42606: Invalid search not shown when range set too quickly")
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_adv_query_errors(selenium):
    """
    Selenium test for validating errors in the adv query feature:
    1. Validate that an invalid range search will throw an error.
    2. Validation of the error message.
    3. Validate that an inverted "Presence in adv search" query throws an error.
    4. Validation of the error message.

    :param selenium: Selenium Webdriver
    """

    # Define test variables required throughout the test
    column_name = 'CMET-TRFRET (Ki)'
    lr_name = "11k and 30 Columns"

    # Open the Advanced Query Tab
    open_add_compounds_panel(selenium)
    open_advanced_search(selenium)

    # Add range query and Clear report on search
    add_query(selenium, column_name)

    # ----- Validate that an invalid range search will throw an error ---- #
    condition_box = get_query(selenium, column_name)
    set_query_range(condition_box, lower_limit=10, upper_limit=3)

    # Validation of the error messages
    error_header_text = "Invalid Search"
    error_message_body = "CMET-TRFRET (Ki): The value entered is not valid. Reverting to previous values."
    verify_is_visible(selenium, MODAL_DIALOG_HEADER, selector_text=error_header_text)
    verify_is_visible(selenium, MODAL_DIALOG_BODY, selector_text=error_message_body)
    base.click_ok(selenium)

    # ----- Validate that an inverted "Presence in adv search" query throws an error ----- #
    dom.click_element(selenium, CLEAR_ADVANCED_QUERY_BUTTON)
    base.click_ok(selenium)
    add_query_presence_in_live_report(selenium, lr_name)
    verify_is_visible(selenium, PRESENCE_IN_LR_DROPDOWN_TITLE, selector_text='11k and 30 Columns')
    dom.click_element(selenium, ADV_QUERY_INVERT)

    # Validation of the error messages
    warning_message = "Cannot run Advanced Search with only an inverted presence in LiveReport condition. " \
                      "This type of inverted condition can only be used to filter out compounds retrieved by " \
                      "additional query conditions."
    verify_is_visible(selenium, DISABLED_SEARCH_AND_ADD_COMPOUNDS_BUTTON, selector_text="Search and Add Compounds")
    verify_is_visible(selenium, ADV_QUERY_WARNING, selector_text=warning_message)

    # Inverting the inverted search and ensuring that the Search button is now active
    dom.click_element(selenium, ADV_QUERY_INVERT)
    verify_is_visible(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)
