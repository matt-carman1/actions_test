import pytest

from helpers.change.actions_pane import open_advanced_search, open_add_compounds_panel
from helpers.change.advanced_search_actions import add_query_presence_in_live_report, get_query, add_query, \
     set_query_range
from helpers.change.live_report_picker import search_for_live_report
from helpers.selection.advanced_search import PRESENCE_IN_LR_DROPDOWN_OPTIONS, SEARCH_AND_ADD_COMPOUNDS_BUTTON, \
    PRESENCE_IN_LR_DROPDOWN, PRESENCE_IN_LR_DROPDOWN_TITLE
from helpers.selection.grid import Footer
from helpers.selection.live_report_picker import REPORT_LIST_ROW, METAPICKER_FOLDER_LIST_ITEM
from helpers.selection.modal import MODAL_DIALOG_HEADER
from helpers.verification.grid import verify_footer_values, verify_column_contents, check_for_butterbar, \
    verify_is_visible
from library import dom, wait, base


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures('new_live_report')
def test_adv_query_presence_in_live_report(selenium):
    """
    Test for create advanced search on presence in live report query
    1. Add one LR to presence in LR query
    2. Add an assay column
    3. Search for Compounds and verify.
    4. Add a second LR by following the steps one by one (without the helper).
    5. Delete the old assay column and add a new assay column.
    6. Search for compounds and verify.


    :param selenium: Selenium webdriver
    """
    assay_column = 'G1 (undefined)'

    # open advanced search panel
    open_add_compounds_panel(selenium)
    open_advanced_search(selenium)

    # ----- Advanced search with presence in LR query ----- #
    add_query_presence_in_live_report(selenium, '11k and 30 Columns')
    verify_is_visible(selenium, PRESENCE_IN_LR_DROPDOWN_TITLE, selector_text='11k and 30 Columns')

    # adding an assay column
    add_query(selenium, assay_column)
    condition_box = get_query(selenium, assay_column)
    set_query_range(condition_box, upper_limit=10)
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)
    check_for_butterbar(selenium, notification_text='Searching for compounds...', visible=True)
    check_for_butterbar(selenium, notification_text='Searching for compounds...', visible=False)

    # Verify footer values and compound ids in grid
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(2),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(6)
        })
    verify_column_contents(selenium, 'ID', ['CRA-035438', 'CRA-035452'])

    # Adding another LR to the presence in LR query
    presence_in_live_report = get_query(selenium, "Presence in LiveReport")
    dom.click_element(presence_in_live_report, PRESENCE_IN_LR_DROPDOWN)
    dom.click_element(selenium, PRESENCE_IN_LR_DROPDOWN_OPTIONS, text='Choose LiveReport...')
    wait.until_visible(selenium, MODAL_DIALOG_HEADER, text='Manage LiveReports')

    # find and select LiveReport from metapicker
    verify_is_visible(selenium, METAPICKER_FOLDER_LIST_ITEM, selector_text='Shared with me')
    search_for_live_report(selenium, name='(Global) 20 Compounds 3 Assays', directory='Shared with me')
    dom.click_element(selenium, REPORT_LIST_ROW, text='(Global) 20 Compounds 3 Assays')
    base.click_ok(selenium)
    verify_is_visible(selenium,
                      PRESENCE_IN_LR_DROPDOWN_TITLE,
                      selector_text='(Global) 20 Compounds 3 Assays, '
                      '11k and 30 Columns')

    # searching for compounds present in the new LR
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)

    # Verification of the butterbar message
    check_for_butterbar(selenium, notification_text='Searching for compounds...', visible=True)
    check_for_butterbar(selenium, notification_text='Searching for compounds...', visible=False)

    # Verification of the compounds returned
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(4),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(6)
        })
    verify_column_contents(selenium, 'ID', ['CRA-035424', 'CRA-035432', 'CRA-035438', 'CRA-035452'])
