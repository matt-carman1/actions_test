from helpers.change.live_report_menu import open_live_report_menu
from helpers.selection.general import MENU_ITEM
from helpers.selection.live_report_picker import REPORT_SEARCH_CROSS_MARK, REPORT_OPEN, REPORT_READ_ONLY, \
    METAPICKER_FOLDER_DROP_TARGET, METAPICKER_FOLDER_ACTIVE, REPORT_LIST_CONTAINER
from helpers.change.live_report_picker import search_for_live_report
from helpers.selection.modal import COPY_LR_TO_PROJECT_LIST, OK_BUTTON, MODAL_CANCEL_BUTTON
from helpers.verification.element import verify_is_visible
from library import dom, wait
from helpers.selection.live_report_tab import TAB, PRIVATE_ICON, TAB_ACTIVE
from library.select import select_option_by_text


def verify_sorted_metapicker_column(driver, selector, metapicker_column, expected_sort):
    """
    Check whether the sorted order is correct in Metapicker.

    :param driver: Webdriver
    :param selector: CSS selector for the column (i.e. '.report-list-column.alias',
    '.report-list-column.title', etc)
    :param metapicker_column: Metapicker column (i.e. 'Name', 'ID', 'Last Edited', etc.) for which
    the sort needs to be verified
    :param expected_sort: list, Expected sort order values
    :return:
    """

    # Excluding the first element, as it represents the headers
    elements = dom.get_elements(driver, selector)[1:]
    observed_sort = [element.text for element in elements]

    assert observed_sort == expected_sort, "{} appears not sorted. \nActual List: {} " \
                                           "\nExpected List: {}".format(metapicker_column,
                                                                        observed_sort,
                                                                        expected_sort)


def verify_green_dot(driver, live_report_name):
    """
    Verify that open livereport has green dot next to it.

    :param driver: webdriver
    :param live_report_name: name of open livereport
    """
    element = dom.get_element(driver, REPORT_OPEN, text=live_report_name, dont_raise=True)
    assert element, "Cannot find element for lr: {}".format(live_report_name)


def verify_live_report_tab_present(driver, live_report_name):
    """
    Verify that livereport is open and tab is present.

    :param driver: webdriver
    :param live_report_name: name of open livereport
    """
    assert dom.get_element(driver, TAB, text=live_report_name,
                           dont_raise=True), "Could not find LR: {}".format(live_report_name)


def verify_read_only_lock(driver, live_report_name):
    """
    Verify that open livereport has green dot next to it.

    :param driver: webdriver
    :param live_report_name: name of open livereport
    """
    element = dom.get_element(driver, REPORT_READ_ONLY, text=live_report_name, dont_raise=True)
    assert element, "Cannot find element for lr: {}".format(live_report_name)


def verify_live_report_not_present(driver, live_report_name, folder_name='All LiveReports'):
    """
    Search in the metapicker to check that a given LiveReport is not present.

    :param driver: Selenium Webdriver
    :param live_report_name: LiveReport to be verified for deletion.
    :param folder_name: str, metapicker folder where we would want to look for the given livereport
    :return:
    """

    live_report_element = search_for_live_report(driver, name=live_report_name, directory=folder_name)

    assert not live_report_element, \
        "LiveReport with name {} found in the Folder {}".format(live_report_name, folder_name)

    # Clearing the LiveReport search input
    dom.click_element(driver, REPORT_SEARCH_CROSS_MARK)


# Nitin found a faster alternative to this. Commenting so that it shows in the CR.
def verify_live_report_present(driver, live_report_name, folder_name='All LiveReports'):
    """
    Search in the metapicker to check that a given LiveReport is not present
    :param driver: Webdriver
    :param live_report_name: str, LiveReport name
    :param folder_name: str, metapicker folder where we would want to look for the given livereport
    :return:
    """

    live_report_element = search_for_live_report(driver, name=live_report_name, directory=folder_name)
    assert live_report_element, "No LiveReport with name {} found in the Folder {}".format(
        live_report_name, folder_name)

    # Clearing the LiveReport search input
    dom.click_element(driver, REPORT_SEARCH_CROSS_MARK)


def verify_private_icon_on_live_report(driver, live_report_name):
    """
    Verify that the converted LR has private icon on the tab

    :param driver: Webdriver
    :param live_report_name: name of the open livereport
    :return:
    """

    live_report_element = dom.get_element(driver, TAB, text=live_report_name)
    assert dom.get_element(live_report_element, PRIVATE_ICON, dont_raise=False,
                           timeout=10), "{} is not a private LR".format(live_report_name)


def verify_count_of_live_report_per_folder(driver, expected_folder_lr):
    """
    Verify the count of live report
    :param driver: Webdriver
    :param expected_folder_lr: Dictionary containing expected values
    :return:
    """

    for (folder_name, expected_value) in expected_folder_lr.items():
        dom.click_element(driver, selector=METAPICKER_FOLDER_DROP_TARGET, text=folder_name)
        verify_is_visible(driver, selector=METAPICKER_FOLDER_ACTIVE, selector_text=folder_name)
        assert len(dom.get_elements(driver, selector=REPORT_LIST_CONTAINER)) - 1 == expected_value


def verify_lr_copy_project_option(selenium, live_report_name):
    """
    Function to verify "Copy to Project..." option and copy livereport to other project.
    1. Open live report menu
    2. Verifying "Copy to Project..." option.
    3. Click on "Copy to Project..." option.
    4. Copy to other project.
    5. Verifying the copied live_report in Livereport picker search.
    6. Logout.

    :param selenium: Selenium Webdriver
    :param live_report_name: livereport name
    """
    wait.until_visible(selenium, TAB_ACTIVE)
    open_live_report_menu(selenium, live_report_name)
    if verify_is_visible(selenium, selector=MENU_ITEM, selector_text='Copy to Project...'):
        dom.click_element(selenium, selector=MENU_ITEM, text='Copy to Project...')
        select_option_by_text(selenium, COPY_LR_TO_PROJECT_LIST, option_text='Project B')
        dom.click_element(selenium, OK_BUTTON)
        verify_live_report_present(selenium, live_report_name)
        dom.click_element(selenium, MODAL_CANCEL_BUTTON)
