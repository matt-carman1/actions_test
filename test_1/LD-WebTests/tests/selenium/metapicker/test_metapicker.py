import pytest

from helpers.change.live_report_picker import search_for_live_report, open_lr_by_double_click, \
    open_live_report, open_metapicker, create_and_open_live_report, select_multiple_live_reports, \
    move_selected_live_report_to_folder, delete_selected_live_report_via_metapicker
from helpers.selection.live_report_picker import REPORT_PICKER
from helpers.verification.live_report_picker import verify_green_dot, verify_live_report_tab_present
from library import dom
from library.base import click_ok
from library.eventually import eventually_equal


@pytest.mark.smoke
@pytest.mark.usefixtures("open_project")
def test_metapicker(selenium):
    """
    Tests metapicker functionality:
    1. To open Live Report(s):
        a) By selecting the LR and clicking OK button on the Metapicker
        b) By double clicking the LR.
    2. Check for green dot on the currently open LR(s).
    3. Search for LR in a folder.

    :param selenium: Webdriver
    """

    # Existing live reports
    lr_name = '50 Compounds 10 Assays'
    lr_name_02 = '5 Compounds 4 Assays'

    open_live_report(selenium, name=lr_name)
    # verify first LR tab present
    verify_live_report_tab_present(selenium, lr_name)

    # Open an LR via double click #
    open_lr_by_double_click(selenium, lr_name_02, exact_text_match=True)

    # verify first LR tab present
    verify_live_report_tab_present(selenium, lr_name)
    # verify second LR tab present
    verify_live_report_tab_present(selenium, lr_name_02)

    # ----- Verify that green dot is visible on open LRs ----- #
    open_metapicker(selenium)
    dom.click_element(selenium, 'a', 'All LiveReports')
    verify_green_dot(selenium, lr_name)
    verify_green_dot(selenium, lr_name_02)

    # ----- Search for a LR in JS Testing Home Folder ----- #
    returned_lr = search_for_live_report(selenium, name=lr_name, directory="JS Testing Home")
    # verify that live report is correct
    assert dom.get_element(returned_lr, '.title', text=lr_name)


# @pytest.mark.app_defect(reason="SS-31732: Test failing on 8.10. and master due to StaleElement")
@pytest.mark.smoke
@pytest.mark.usefixtures("open_project")
def test_open_move_delete_multiple_live_reports_via_metapicker(selenium):
    """
    Tests opening, moving and deleting multiple LiveReports through metapicker.
    :param selenium: Webdriver
    :return:
    """

    # Create new Live Reports from "+" button
    lr_name_01 = create_and_open_live_report(selenium, 'test_1')
    lr_name_02 = create_and_open_live_report(selenium, 'test_2')
    lr_name_03 = create_and_open_live_report(selenium, 'test_3')

    # Open multiple LRs by highlighting and clicking.
    select_multiple_live_reports(selenium, ['Radar', 'Presence in LR'])
    click_ok(selenium)

    # Verify LR tabs present
    verify_live_report_tab_present(selenium, 'Radar')
    verify_live_report_tab_present(selenium, 'Presence in LR')

    # Move multiple LRs to a folder
    select_multiple_live_reports(selenium, [lr_name_01, lr_name_02, lr_name_03])
    move_selected_live_report_to_folder(selenium, 'MPO')

    # Verifying LiveReport folder
    livereports = [lr_name_01, lr_name_02, lr_name_03]
    verify_livereports_present(selenium, expected_livereport_names_list=livereports, directory='MPO')

    # Delete multiple LRs
    select_multiple_live_reports(selenium, [lr_name_01, lr_name_02, lr_name_03])
    delete_selected_live_report_via_metapicker(selenium)

    # Verify that LRs have been deleted
    verify_livereports_not_present(selenium, unexpected_livereport_names_list=livereports)


def verify_livereports_present(driver, expected_livereport_names_list, directory="All LiveReports"):
    """
    Get the list of all the LRs in the metapicker and checks for the expected LiveReport names in that list.

    :param driver: Selenium Webdriver
    :param expected_livereport_names_list: list, Names of the expected LiveReport(s)
    :param directory: str, LR Metapicker directory
    """

    # Open LR metapicker and navigate to the desired metapicker directory/folder
    picker = dom.get_element(driver, REPORT_PICKER)
    dom.click_element(picker, 'a', directory)

    def get_missing_live_reports(driver):
        # Get the list of all the LiveReports
        livereports_list = dom.get_elements(driver, '.report-list li .report-list-column.title .title-text')
        livereport_names_list = [element.text for element in livereports_list]
        return set(expected_livereport_names_list) - set(livereport_names_list)

    assert eventually_equal(driver, get_missing_live_reports, set(), timeout=3), \
        f"LiveReport {get_missing_live_reports(driver)} is not showing up in the metapicker when it should be."


def verify_livereports_not_present(driver, unexpected_livereport_names_list, directory="All LiveReports"):
    """
    Get the list of all the LRs in the metapicker and checks for the absence of LiveReport names in that list.

    :param driver: Selenium Webdriver
    :param unexpected_livereport_names_list: list, Names of the unexpected LiveReport(s)
    :param directory: str, LR Metapicker directory
    """

    # Open LR metapicker and navigate to the desired metapicker directory/folder
    picker = dom.get_element(driver, REPORT_PICKER)
    dom.click_element(picker, 'a', directory)

    def get_unexpected_live_reports(driver):
        # Get the list of all the LiveReports
        livereports_list = dom.get_elements(driver, '.report-list li .report-list-column.title .title-text')
        livereport_names_list = [element.text for element in livereports_list]
        return set(unexpected_livereport_names_list).intersection(set(livereport_names_list))

    assert eventually_equal(driver, get_unexpected_live_reports, set(), timeout=10), \
        f"LiveReport {get_unexpected_live_reports(driver)} is showing up in the metapicker when it shouldn't be."
