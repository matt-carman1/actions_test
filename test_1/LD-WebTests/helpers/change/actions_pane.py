"""
Functions in this module click and toggle buttons that are in the
action panel of an opened Live Report.
"""
from helpers.change.grid_column_menu import scroll_to_column_header
from helpers.extraction.grid import db_column_id
from helpers.selection.actions_pane import (ADD_COMPOUND_BUTTON, ADD_DATA_BUTTON, FILTER_BUTTON, TOOLS_BUTTON,
                                            VISUALIZE_BUTTON, COMMENTS_BUTTON, TOOLS_PANE, TOOLS_PANE_TOOL,
                                            TOOLS_PANE_TAB, REPORT_LEVEL_PICKER, REPORT_LEVEL_PICKLIST_WRAPPER,
                                            REPORT_LEVEL_PICKLIST_OPTIONS, REPORT_LEVEL_PICKER_SELECTED_VALUE)
from helpers.selection.add_compound_panel import (COMPOUNDS_PANE_TAB_PICKER, COMPOUNDS_PANE_ACTIVE_TAB,
                                                  COMPOUNDS_PANE_TAB)
from helpers.selection.column_tree import COLUMN_TREE_PICKER
from helpers.selection.comments import COMMENTS_TEXTBOX
from helpers.selection.filter_actions import FILTERS_PANELS
from helpers.selection.grid import GRID_COMPOUND_ID_CELLS, GRID_EXPAND_BUTTON_, GRID_ROW_COLUMN_
from helpers.selection.notifications import NOTIFICATIONS_FLAG, NOTIFICATIONS_PANEL
from helpers.selection.sar_analysis import SAR_PANELS
from helpers.selection.visualize import VISUALIZE_TITLE_BAR
from library import dom, simulate, wait, ensure


def open_add_compounds_panel(driver):
    """
    Opens the "Add Compounds" action panel

    :param driver: Selenium Webdriver
    """
    ensure.element_visible(driver,
                           action_selector=ADD_COMPOUND_BUTTON,
                           expected_visible_selector=COMPOUNDS_PANE_TAB_PICKER)


def close_add_compounds_panel(driver):
    """
    Closes the "Add Compounds" action panel

    :param driver: Selenium Webdriver
    """
    ensure.element_not_visible(driver,
                               action_selector=ADD_COMPOUND_BUTTON,
                               expected_not_visible_selector=COMPOUNDS_PANE_TAB_PICKER)


def open_advanced_search(driver):
    """
    Opens the Advanced Search Panel. Assumes open_add_compounds_panel(selenium) has been called

    :param driver: Selenium Webdriver
    """
    open_compounds_pane_tab(driver, 'Advanced')


def open_file_import_panel(driver):
    """
    Opens the Import Panel. Assumes open_add_compounds_panel(selenium) has been called

    :param driver: Selenium Webdriver
    """
    open_compounds_pane_tab(driver, 'Import')


def open_compound_search_panel(driver):
    """
    Opens the Search Tab. Assumes open_add_compounds_panel(selenium) has been called

    :param driver: Selenium Webdriver
    """
    open_compounds_pane_tab(driver, 'Search')


def open_compound_design_panel(driver):
    """
    Opens the Design Tab. Assumes open_add_compounds_panel(selenium) has been called

    :param driver: Selenium Webdriver
    """
    open_compounds_pane_tab(driver, 'Design')


def open_enumeration_panel(driver):
    """
    Opens the Enumeration Tab. Assumes open_add_compounds_panel(selenium) has been called

    :param driver: Selenium Webdriver
    """
    open_compounds_pane_tab(driver, 'Enumerate')


def open_compounds_pane_tab(driver, tab):
    """
    Opens the tab in compounds pane according to the passed in the tab

    :param driver: Selenium Webdriver
    :param tab: The name of the tab to be opened
    :return:
    """
    ensure.element_visible(driver, COMPOUNDS_PANE_TAB, COMPOUNDS_PANE_ACTIVE_TAB, tab, tab)


def open_add_data_panel(driver):
    """
    Opens the "Add Data" action panel

    :param driver: Selenium Webdriver
    """
    ensure.element_visible(driver, action_selector=ADD_DATA_BUTTON, expected_visible_selector=COLUMN_TREE_PICKER)


def close_add_data_panel(driver):
    """
    Closes the "Add Data" action panel

    :param driver: Selenium Webdriver
    """
    ensure.element_not_visible(driver,
                               action_selector=ADD_DATA_BUTTON,
                               expected_not_visible_selector=COLUMN_TREE_PICKER)


def open_filter_panel(driver):
    """
    Opens the "Filter Compounds" action panel

    :param driver: Selenium Webdriver
    """
    filter_button = dom.get_element(driver, FILTER_BUTTON)
    simulate.hover(driver, filter_button)

    ensure.element_visible(driver, action_selector=FILTER_BUTTON, expected_visible_selector=FILTERS_PANELS)


def close_filter_panel(driver):
    """
    Closes the "Filter Compounds" action panel

    :param driver: Selenium Webdriver
    """
    ensure.element_not_visible(driver, action_selector=FILTER_BUTTON, expected_not_visible_selector=FILTERS_PANELS)


def open_sar_panel(driver):
    """
    Opens the "SAR Analysis" action panel

    :param driver: Selenium Webdriver
    """
    ensure.element_visible(driver, action_selector=TOOLS_BUTTON, expected_visible_selector=TOOLS_PANE)
    ensure.element_visible(driver,
                           action_selector=TOOLS_PANE_TOOL,
                           action_selector_text='R-Group decomposition',
                           expected_visible_selector=SAR_PANELS)


def open_tools_pane(driver):
    """
    Opens the Tools action panel

    :param driver: Selenium Webdriver
    """
    ensure.element_visible(driver, action_selector=TOOLS_BUTTON, expected_visible_selector=TOOLS_PANE)
    ensure.element_not_visible(driver,
                               action_selector=TOOLS_PANE_TAB,
                               action_selector_text='Tools',
                               expected_not_visible_selector=SAR_PANELS)


def close_sar_panel(driver):
    """
    Closes the "SAR Analysis" action panel

    :param driver: Selenium Webdriver
    """
    ensure.element_not_visible(driver, action_selector=TOOLS_BUTTON, expected_not_visible_selector=SAR_PANELS)


def open_visualize_panel(driver):
    """
    Opens the "Visualize" action panel

    :param driver: Selenium Webdriver
    """
    ensure.element_visible(driver, action_selector=VISUALIZE_BUTTON, expected_visible_selector=VISUALIZE_TITLE_BAR)


def close_visualize_panel(driver):
    """
    Closes the "Visualize" action panel

    :param driver: Selenium Webdriver
    """
    ensure.element_not_visible(driver,
                               action_selector=VISUALIZE_BUTTON,
                               expected_not_visible_selector=VISUALIZE_TITLE_BAR)


def open_comments_panel(driver):
    """
    Opens the "Comments" action panel

    :param driver: Selenium Webdriver
    """
    ensure.element_visible(driver, action_selector=COMMENTS_BUTTON, expected_visible_selector=COMMENTS_TEXTBOX)


def close_comments_panel(driver):
    """
    Closes the "Comments" action panel

    :param driver: Selenium Webdriver
    """
    ensure.element_not_visible(driver, action_selector=COMMENTS_BUTTON, expected_not_visible_selector=COMMENTS_TEXTBOX)


def open_notification_panel(driver):
    """
    Opens Notifications Panel.

    :param driver: Selenium Webdriver
    """
    ensure.element_visible(driver, action_selector=NOTIFICATIONS_FLAG, expected_visible_selector=NOTIFICATIONS_PANEL)


def close_notification_panel(driver):
    """
    Close Notifications Panel.

    :param driver: Selenium Webdriver
    """
    ensure.element_not_visible(driver,
                               action_selector=NOTIFICATIONS_FLAG,
                               expected_not_visible_selector=NOTIFICATIONS_PANEL)


def toggle_lr_mode(driver, row_per_mode='Compound'):
    """
    Toggles LiveReport mode to Compound, Compound Lot, Compound Salt,
    Compound Lot Salt. This cannot be used to toggle to RPE mode or pose mode as
    those are grid functions. However, we could use this script to toggle
    from RPE/Pose mode to other modes once the LR is in RPE/Pose mode

    :param driver: Selenium Webdriver
    :param row_per_mode: str, Live Report modes such as Compound, Compound Lot,
                         Compound Salt, Compound Lot Salt to which the LR
                         needs to be switched.
    :return: None
    """
    dom.click_element(driver, REPORT_LEVEL_PICKER)
    wait.until_visible(driver, REPORT_LEVEL_PICKLIST_WRAPPER)
    report_levels = dom.get_elements(driver, REPORT_LEVEL_PICKLIST_OPTIONS)

    for option in report_levels:
        if option.text == row_per_mode:
            option.click()
            wait.until_loading_mask_not_visible(driver)
            wait.until_visible(driver, REPORT_LEVEL_PICKER_SELECTED_VALUE, text=row_per_mode)
            break


def click_expand_row(driver, column_name):
    """
    Expands a RPE column using the first row seen in the LiveReport.
    Will fail if column is not in view.

    :param driver: Webdriver
    :param column_name: str, column name. Do not include units in the name,
                        for example, to expand column name
                        "PK_IV_RAT (AUC) Prot 2 [uM]", set
                        column_name = "PK_IV_RAT (AUC) Prot 2"
    :return: None
    """

    # Added this to scroll to the column if it is not in the current screen view
    scroll_to_column_header(driver, column_name)

    id_number = db_column_id(driver, column_name)
    compound_ids = [element.text for element in dom.get_elements(driver, GRID_COMPOUND_ID_CELLS)]
    # replace all spaces in the ID with a period to avoid element not found error
    compound_ids[0] = compound_ids[0].replace(' ', '.')
    # hover over first compound & column to show View Experiment
    first_compound = dom.get_element(driver, GRID_ROW_COLUMN_.format(compound_ids[0], id_number))
    simulate.hover(driver, first_compound)

    dom.click_element(driver, GRID_EXPAND_BUTTON_.format(compound_ids[0], id_number))

    # prevent flakiness by waiting for LR to change mode before ending function
    # (loading mask disappears)
    wait.until_loading_mask_not_visible(driver)

    # confirming that LR is in Experiment mode
    lr_mode = dom.get_element(driver, REPORT_LEVEL_PICKER_SELECTED_VALUE).text
    assert lr_mode == 'Experiment', \
        "LiveReport is in Row per {}, expected Experiment".format(lr_mode)
