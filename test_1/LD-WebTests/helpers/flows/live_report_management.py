from library import dom, base, wait
from library.utils import make_unique_name
from library.select import select_option_by_text

from helpers.selection.live_report_tab import TAB, TAB_ACTIVE
from helpers.change.live_report_menu import close_live_report, click_live_report_menu_item, switch_to_live_report
from helpers.selection.modal import (DUPLICATE_LR_FOLDER_DROPDOWN, DUPLICATE_LR_RADIO_BUTTON_LABEL,
                                     DUPLICATE_LR_RADIO_GROUP_LABEL, MODAL_LR_COLUMN_LABEL, MODAL_DIALOG,
                                     MODAL_TITLE_FIELD_INPUT)
from helpers.verification.grid import check_for_butterbar


def duplicate_livereport(driver,
                         livereport_name,
                         duplicate_lr_name=None,
                         folder='JS Testing Home',
                         selected_compounds='All',
                         selected_columns=['All']):
    """
    Duplicates the complete LiveReport or it's subset by selecting certain rows and columns. Make sure to open the
    LiveReport before calling this helper.

    To create tests that begin with duplicating a LiveReport, use fixture duplicate_live_report in conftest.py instead

    :param driver: Selenium Webdriver
    :param livereport_name: str, LiveReport to be duplicated
    :param duplicate_lr_name: str, name to be set for duplicate LiveReport
    :param folder: str, name of the folder under which the LiveReport has to be placed
    :param selected_compounds: str, 'All' for all the compounds in the LR or number of Columns selected.
    :param selected_columns: list, ['All'] for all the columns or the list of column names to be selected
    :return: str, duplicated LR name
    """

    duplicate_name = copy_active_live_report(driver,
                                             livereport_name=livereport_name,
                                             new_name=duplicate_lr_name,
                                             folder_name=folder,
                                             compounds=selected_compounds,
                                             columns=selected_columns)

    # Wait until the LR is loaded otherwise it will mess with closing the old LR
    check_for_butterbar(driver, 'Duplicating LiveReport', visible=False)
    close_live_report(driver, livereport_name)

    # If other LRs are open, need to switch Tabs so it's active
    switch_to_live_report(driver, duplicate_name)
    wait.until_visible(driver, TAB_ACTIVE, duplicate_name)
    return duplicate_name


def copy_active_live_report(driver,
                            livereport_name,
                            new_name=None,
                            folder_name='JS Testing Home',
                            compounds='All',
                            columns=['All'],
                            wait_until_visible=True):
    """
    Make a copy of the currently active Live Report. Inputs to compounds and columns argument would duplicate the LR
    with specific compounds and columns.

    :param driver: selenium webdriver
    :param livereport_name: str, the name of the Live Report that will be copied
    :param new_name: str, the name of the new Live Report. This is optional.
    :param folder_name: str, name of the folder under which the LiveReport has to be placed.
    :param compounds: str, number of compound selected. Use "All" if each one of them is selected for duplicating.
    :param columns: list, list of columns to be selected for copying or ['All'] for all the columns
    :param wait_until_visible: Wait till the LR tab is visible. Defaults to True.
    :return: the name of the new Live Report
    """
    new_name = make_unique_name(new_name if new_name else livereport_name)

    # Opening the duplicate LR dialog
    click_live_report_menu_item(driver, livereport_name, 'Duplicate...')

    modal = dom.get_element(driver, MODAL_DIALOG)

    # Setting LiveReport name
    dom.set_element_value(modal, MODAL_TITLE_FIELD_INPUT, value=new_name)

    # Setting LiveReport folder
    select_option_by_text(driver, DUPLICATE_LR_FOLDER_DROPDOWN, option_text=folder_name)

    # Selecting Radio button for Compounds based on the variable whether it is "All" or "Currently Selected"
    if compounds != 'All':
        compounds = "Currently Selected ({})".format(len(compounds))
    radio_label = dom.get_element(driver, DUPLICATE_LR_RADIO_GROUP_LABEL, text="Compounds:")
    radio_group = dom.get_parent_element(radio_label)
    dom.click_element(radio_group, DUPLICATE_LR_RADIO_BUTTON_LABEL, text=compounds)

    # Selecting the Columns to be copied if it is not 'All'
    if columns != ['All']:
        dom.click_element(driver, DUPLICATE_LR_RADIO_BUTTON_LABEL, text='Choose Subset')
        for column in columns:
            dom.click_element(driver, MODAL_LR_COLUMN_LABEL, text=column)
    else:
        radio_label = dom.get_element(driver, DUPLICATE_LR_RADIO_GROUP_LABEL, text="Columns:")
        radio_group = dom.get_parent_element(radio_label)
        dom.click_element(radio_group, DUPLICATE_LR_RADIO_BUTTON_LABEL, text=columns[0])

    base.click_ok(modal)

    # in some cases we may not want to wait--test_duplicate_large_lr we want to immediately test for the presence of
    # the butter bar.
    if wait_until_visible:
        wait.until_visible(driver, TAB, new_name)

    return new_name
