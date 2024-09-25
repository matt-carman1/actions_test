"""
Verifications that specific application features are enabled or disabled.
"""
from helpers.change.menus import open_submenu
from helpers.selection.actions_pane import TOOLS_PANE_TOOL
from helpers.selection.add_compound_panel import SEARCH_AND_ADD_COMPOUNDS_BUTTON, COMPOUNDS_PANE_TAB, \
    IMPORT_FILE_BUTTON, ADD_IDEA_TO_LIVE_REPORT_BUTTON
from helpers.selection.grid import GRID_MENU_ITEM_DISABLED, GRID_MENU_ITEM_NOT_DISABLED
from helpers.verification import element
from helpers.verification.element import verify_is_not_visible, verify_element_click_does_nothing, verify_is_visible
from helpers.change.actions_pane import open_tools_pane
from helpers.change.live_report_menu import open_live_report_menu
from helpers.selection.sketcher import ADD_SAR_BUTTON
from helpers.selection.grid_menus import SUB_MENU_ITEM
from helpers.selection.general import MENU_ITEM
from helpers.selection.modal import MODAL_DIALOG_HEADER, WINDOW_HEADER_TEXT_DEFAULT
from library import simulate, dom


def verify_compound_design_tab_is_disabled(driver):
    """
    Checks that the Compounds Panel Design tab is disabled. Generally it is the case for Device LiveReports.

    :param driver: Selenium Webdriver
    """

    def check_click_failed():
        verify_is_not_visible(driver, ADD_IDEA_TO_LIVE_REPORT_BUTTON, selector_text='Add Idea to LiveReport')

    verify_element_click_does_nothing(driver,
                                      COMPOUNDS_PANE_TAB,
                                      selector_text='Design',
                                      ensure_click_failed_callback=check_click_failed)


def verify_compound_design_tab_is_enabled(driver):
    """
    Checks that the Compounds Panel Design tab is enabled.

    :param driver: Selenium Webdriver
     """

    def click_and_check_succeeded(element):
        simulate.click(driver, element)
        verify_is_visible(driver,
                          ADD_IDEA_TO_LIVE_REPORT_BUTTON,
                          selector_text='Add Idea to LiveReport',
                          exact_selector_text_match=True)

    dom.get_element(driver, COMPOUNDS_PANE_TAB, text='Design', action_callback=click_and_check_succeeded, timeout=2)


def verify_structure_search_is_disabled(driver):
    """
    Checks that the Compounds Panel Search tab has Structure search disabled. Generally it is the case for Device
    LiveReports.

    :param driver: Selenium Webdriver
    """

    def check_click_failed():
        verify_is_not_visible(driver, SEARCH_AND_ADD_COMPOUNDS_BUTTON, selector_text='Search and Add Compounds')

    dom.click_element(driver, COMPOUNDS_PANE_TAB, text='Search')
    verify_element_click_does_nothing(driver,
                                      '.compounds-design-pane .sub-tab',
                                      selector_text="Structure",
                                      ensure_click_failed_callback=check_click_failed)


def verify_structure_search_is_enabled(driver):
    """
    Checks that the Compounds Panel Search tab has Structure search enabled.

    :param driver: Selenium Webdriver
    """
    search_button = dom.get_element(driver,
                                    SEARCH_AND_ADD_COMPOUNDS_BUTTON,
                                    text='Search and Add Compounds',
                                    dont_raise=True,
                                    timeout=2)

    if not search_button:

        def click_and_check_succeeded(element):
            simulate.click(driver, element)
            dom.click_element(driver, '.compounds-design-pane .sub-tab', text="Structure")
            verify_is_visible(driver, SEARCH_AND_ADD_COMPOUNDS_BUTTON, selector_text='Search and Add Compound')

        dom.get_element(driver, COMPOUNDS_PANE_TAB, text='Search', action_callback=click_and_check_succeeded, timeout=2)


def verify_import_from_file_is_disabled(driver):
    """
    Checks that the Compounds Panel Import tab is disabled. Generally it is the case for Device LiveReports.

    :param driver: Selenium Webdriver
    """

    def check_click_failed():
        verify_is_not_visible(driver, IMPORT_FILE_BUTTON, selector_text='Import File')

    verify_element_click_does_nothing(driver,
                                      COMPOUNDS_PANE_TAB,
                                      selector_text='Import',
                                      ensure_click_failed_callback=check_click_failed)


def verify_import_from_file_is_enabled(driver):
    """
    Checks that the Compounds Panel Import tab is enabled.

    :param driver: Selenium Webdriver
    """

    def click_and_check_succeeded(element):
        simulate.click(driver, element)
        verify_is_visible(driver, IMPORT_FILE_BUTTON, selector_text='Import File')

    dom.get_element(driver, COMPOUNDS_PANE_TAB, text='Import', action_callback=click_and_check_succeeded, timeout=2)


def verify_sar_button_is_disabled(driver):
    """
    Checks that the SAR button is disabled. Generally it is the case for Device LiveReports or Read-Only LiveReports.

    :param driver: Selenium Webdriver
    """

    def check_click_failed():
        verify_is_not_visible(driver, ADD_SAR_BUTTON)

    open_tools_pane(driver)
    verify_element_click_does_nothing(driver,
                                      TOOLS_PANE_TOOL,
                                      selector_text='R-Group decomposition',
                                      ensure_click_failed_callback=check_click_failed)


def verify_sar_button_is_enabled(driver):
    """
    Checks that the SAR button is enabled.

    :param driver: Selenium Webdriver
    """

    def click_and_check_succeeded(element):
        simulate.click(driver, element)
        verify_is_visible(driver, ADD_SAR_BUTTON)

    open_tools_pane(driver)
    dom.get_element(driver,
                    TOOLS_PANE_TOOL,
                    text='R-Group decomposition',
                    exact_text_match=True,
                    action_callback=click_and_check_succeeded,
                    timeout=2)


def verify_live_report_menu_option_is_disabled(driver, live_report_name, item_name, dialog_header_text):
    """
    Verifies that the livereport menu option is disabled.

    :param driver: Selenium Webdriver
    :param live_report_name: str, name of the LiveReport.
    :param item_name: str, LiveReport dropdown menu item which should be disabled.
    :param dialog_header_text: str, The header of the dialog
    :return:
    """

    open_live_report_menu(driver, live_report_name)

    def check_click_failed():
        verify_is_not_visible(driver, MODAL_DIALOG_HEADER, selector_text=dialog_header_text)

    verify_element_click_does_nothing(driver,
                                      MENU_ITEM,
                                      selector_text=item_name,
                                      ensure_click_failed_callback=check_click_failed)


def verify_live_report_submenu_option_is_disabled(driver,
                                                  live_report_name,
                                                  item_name,
                                                  submenu_option,
                                                  submenu_dialog_header_text,
                                                  exact_text_match=False):
    """
    Verifies that the livereport submenu option is disabled.

    :param driver: Selenium Webdriver
    :param live_report_name: str, name of the LiveReport.
    :param item_name: str, LiveReport dropdown menu item
    :param submenu_option: str, dropdown submenu item
    :param submenu_dialog_header_text: str, text of submenu dialog
    :param exact_text_match: bool, Whether text match should be exact or not, Disabled by default.
    :return:
    """

    open_live_report_menu(driver, live_report_name)

    open_submenu(driver, item_name, exact_text_match=exact_text_match)

    # make sure that clicking on the submenu option doesn't open the submenu panel
    def check_click_failed():
        verify_is_not_visible(driver, WINDOW_HEADER_TEXT_DEFAULT, selector_text=submenu_dialog_header_text)

    verify_element_click_does_nothing(driver,
                                      SUB_MENU_ITEM,
                                      selector_text=submenu_option,
                                      ensure_click_failed_callback=check_click_failed)


def verify_menu_items_are_disabled(driver, *disabled_items):
    """
    Verifies that the chosen grid menu items (row or column) are disabled.

    :param driver: Selenium Webdriver
    :param disabled_items: str of disabled menu items
    """
    # Verify each item is disabled
    for item in disabled_items:
        element.verify_is_visible(driver, GRID_MENU_ITEM_DISABLED, item)


def verify_menu_items_are_not_disabled(driver, *not_disabled_items):
    """
    Verifies that the chosen grid menu items (row or column) are not disabled.

    :param driver: Selenium Webdriver
    :param not_disabled_items: str of disabled menu items
    """
    # Verify each item is disabled
    for item in not_disabled_items:
        element.verify_is_visible(driver, GRID_MENU_ITEM_NOT_DISABLED, item)


def verify_menu_items_are_not_visible(driver, *not_visible_items):
    """
    Verifies that the chosen grid menu items are not visible

    :param driver: Selenium Webdriver
    :param not_visible_items: str of not visible menu items
    """
    # Verify each item is not visible
    for item in not_visible_items:
        element.verify_is_not_visible(driver, GRID_MENU_ITEM_NOT_DISABLED, item)
