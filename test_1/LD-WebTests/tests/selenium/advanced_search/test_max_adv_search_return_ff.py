import pytest

from helpers.change.actions_pane import open_add_compounds_panel, open_advanced_search
from helpers.change.advanced_search_actions import add_query, get_query, set_query_range, range_actions
from helpers.selection.advanced_search import SEARCH_AND_ADD_COMPOUNDS_BUTTON, CLEAR_REPORT_CHECKED, \
    CLEAR_REPORT_CHECKBOX, QUERY_RANGE_UPPER_AUTO_BUTTON, QUERY_RANGE_UPPER_BOX
from helpers.selection.grid import Footer
from helpers.verification.element import verify_is_visible
from helpers.verification.grid import verify_footer_values, check_for_butterbar
from library import dom, base

# This is an FF which restricts the maximum number of compounds returned by an Advanced Search query.
LD_PROPERTIES = {'MAX_ADVANCED_SEARCH_RETURN': 5}


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
@pytest.mark.usefixtures('customized_server_config')
def test_max_adv_search_return_ff(selenium):
    """
    This will check whether the FF MAX_ADVANCED_SEARCH_RETURN FF is working as expected.

    1. Adding same number of rows/compounds as set by the FF and subsequent verification.
    2. Adding more number of rows/compounds than what's set in by the FF and subsequent verification.
    3. Adding lesser number of compounds as set of FF and subsequent verification.
    :param selenium: Selenium Webdriver
    """
    column_name = "CMET-TRFRET (Ki)"
    # Open advanced search panel
    open_add_compounds_panel(selenium)
    open_advanced_search(selenium)

    # Adding the assay query upon which searches will be performed.
    add_query(selenium, column_name)

    # ----- Adding same number of rows/compounds as set by the FF and subsequent verification ----- #
    # Update range upper limit such that exactly five compounds are returned and subsequent searching.
    condition_box = get_query(selenium, column_name)
    set_query_range(condition_box, upper_limit=0.004)
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)

    # Verification that exactly 5 compounds are returned.
    check_for_butterbar(selenium, notification_text='Searching for compounds...', visible=True)
    check_for_butterbar(selenium, notification_text='Searching for compounds...', visible=False)
    verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(5)})

    # Resetting the range to the default values - which would otherwise return 273 rows/compounds.
    range_actions.set_range_to_auto_or_infinity(selenium,
                                                condition_box,
                                                QUERY_RANGE_UPPER_AUTO_BUTTON,
                                                hover_element_selector=QUERY_RANGE_UPPER_BOX)
    dom.click_element(selenium, CLEAR_REPORT_CHECKBOX)
    verify_is_visible(selenium, CLEAR_REPORT_CHECKED)
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)
    base.click_ok(selenium)

    # Verification that five compounds are still returned.
    check_for_butterbar(selenium, notification_text='Removing all and Searching for compounds...', visible=True)
    check_for_butterbar(selenium, notification_text='Removing all and Searching for compounds...', visible=False)
    verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(5)})

    # ----- Adding lesser number of compounds as set of FF and subsequent verification ----- #
    condition_box = get_query(selenium, column_name)
    set_query_range(condition_box, upper_limit=0.003)
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)
    base.click_ok(selenium)

    # Verification that exactly 4 compounds are returned.
    check_for_butterbar(selenium, notification_text='Removing all and Searching for compounds...', visible=True)
    check_for_butterbar(selenium, notification_text='Removing all and Searching for compounds...', visible=False)
    verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(4)})
