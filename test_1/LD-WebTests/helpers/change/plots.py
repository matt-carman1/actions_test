"""
State changes made to plots.
"""
import time

from selenium.webdriver.common.by import By

from helpers.change.actions_pane import open_visualize_panel
from helpers.selection.modal import OK_BUTTON
from helpers.selection.plots import ADVANCED_OPTIONS_BUTTON, BIN_COUNT_BUTTON, \
    CUSTOM_BINNING_RULE_TYPE_LABEL, GADGET_TAB_NUMBER, \
    HEATMAP_COLUMN_PICKER, HEATMAP_COLUMN_PICKER_SELECTED_ITEM_COLOR_LINK, \
    HEATMAP_COLUMN_PICKER_UNSELECTED_ITEM_CHECKBOX, NUMERIC_RULE_MAX_BOX, NUMERIC_RULE_MIN_BOX, OPTIONS_MODE_BASIC, \
    PLOT_OPTIONS_DIALOG_CLOSE_BUTTON, PLOT_OPTIONS_PANEL, PLOT_OPTIONS_TAB, PLOT_OPTIONS_TAB_ACTIVE, \
    PLOT_OPTIONS_TAB_NAME_TOOLTIP, SPG_BIN_HEADER, SPG_BIN_OPTIONS, TOOLTIP_MODE_RADIO, VISUALIZATION_BOX, \
    VISUALIZATION_HISTOGRAM, VISUALIZATION_PIE, VISUALIZATION_RADAR, VISUALIZATION_SCATTER, EQUAL_BINNING_INPUT, \
    SPG_ADD_BIN_RULE, RULE_NAME, ADD_OVERLAY_BUTTON, OVERLAY_OPTION, PLOT_OPTIONS_STYLE_NTH_CHILD_SHAPE, \
    SELECT_SHAPE_BY, PLOT_OPTIONS_SHAPE_SELECTION_BUTTON
from helpers.selection.visualize import VISUALIZE_TAB, VISUALIZER_ACTIVE_TAB_TITLE_BAR
from helpers.verification.grid import check_for_butterbar
from library import dom, ensure, wait, utils
from library.dom import press_enter_key


def switch_gadget_tab(selenium, index):
    """
    Switches to the indexed gadget tab (starting from 1, nth-child selector).

    :param selenium: Webdriver
    :param index: The index for the gadget tab
    :type index: int
    :return:
    """
    selector = GADGET_TAB_NUMBER.format(index)
    dom.click_element(selenium, selector)


def open_advanced_options_panel(selenium, plot_tab_name=None):
    """
    Opens the advanced options panel and waits for it to appear.
    Also selects the tab if plot_tab_name is specified

    :param selenium: Webdriver
    :param plot_tab_name: str Name of the options tab to be selected
    """
    dom.click_element(selenium, ADVANCED_OPTIONS_BUTTON)
    wait.until_visible(selenium, PLOT_OPTIONS_PANEL)

    change_advanced_options_panel_tab(selenium, plot_tab_name)


def change_advanced_options_panel_tab(selenium, plot_tab_name):
    """
    Sets the active tab in the advanced options panel dialog

    :param selenium: Webdriver
    :param plot_tab_name: str Name of the tab which should be made active
    """
    if plot_tab_name is None:
        return

    dom.click_element(selenium, PLOT_OPTIONS_TAB, text=plot_tab_name)
    wait.until_visible(selenium, PLOT_OPTIONS_TAB_ACTIVE, text=plot_tab_name)


def close_advanced_options_panel(selenium):
    """
    Close the advanced options panel and waits for it to disappear.

    :param selenium: Webdriver
    """
    dom.click_element(selenium, PLOT_OPTIONS_DIALOG_CLOSE_BUTTON)
    wait.until_visible(selenium, OPTIONS_MODE_BASIC)


def add_scatterplot(driver):
    """
    Create a new Scatterplot

    :param driver: selenium webdriver
    :return: str, name of the scatter plot tab created
    """
    # if there are too many tabs, the expected VISUALIZE_TAB will not be visible.
    ensure.element_visible(driver, VISUALIZE_TAB, VISUALIZATION_SCATTER, action_selector_text='VISUALIZE +')
    dom.click_element(driver, VISUALIZATION_SCATTER)
    check_for_butterbar(driver, notification_text="Please wait while the plot is being created")
    check_for_butterbar(driver, notification_text="Please wait while the plot is being created", visible=False)
    return dom.get_elements(driver, VISUALIZE_TAB)[1].text


def add_histogram_plot(driver):
    """
    Create a new Histogram plot

    :param driver: selenium webdriver
    :return: str, name of the histogram plot tab created
    """
    # if there are too many tabs, the expected VISUALIZE_TAB will not be visible.
    ensure.element_visible(driver, VISUALIZE_TAB, VISUALIZATION_HISTOGRAM, action_selector_text='VISUALIZE +')
    dom.click_element(driver, VISUALIZATION_HISTOGRAM)
    return dom.get_elements(driver, VISUALIZE_TAB)[1].text


def add_radar_plot(driver):
    """
    Create a new Radar plot

    :param driver: selenium webdriver
    :return: str, name of the radar plot tab created
    """
    # if there are too many tabs, the expected VISUALIZE_TAB will not be visible.
    ensure.element_visible(driver, VISUALIZE_TAB, VISUALIZATION_RADAR, action_selector_text='VISUALIZE +')
    dom.click_element(driver, VISUALIZATION_RADAR)
    return dom.get_elements(driver, VISUALIZE_TAB)[1].text


def add_box_plot(driver):
    """
    Create a new Box plot

    :param driver: selenium webdriver
    :return: str, name of the box plot tab created
    """
    # if there are too many tabs, the expected VISUALIZE_TAB will not be visible.
    ensure.element_visible(driver, VISUALIZE_TAB, VISUALIZATION_BOX, action_selector_text='VISUALIZE +')
    dom.click_element(driver, VISUALIZATION_BOX)
    return dom.get_element(driver, VISUALIZER_ACTIVE_TAB_TITLE_BAR).text


def add_pie_plot(driver):
    """
    Create a new Pie plot

    :param driver: selenium webdriver
    :return: str, name of the pie plot created
    """
    # if there are too many tabs, the expected VISUALIZE_TAB will not be visible.
    ensure.element_visible(driver, VISUALIZE_TAB, VISUALIZATION_PIE, action_selector_text='VISUALIZE +')
    dom.click_element(driver, VISUALIZATION_PIE)
    return dom.get_elements(driver, VISUALIZE_TAB)[1].text


def add_heatmap_column(selenium, column_name):
    """
    Adds a column to the heatmap.

    :param selenium: Webdriver
    :param column_name: The name for column to add.
    :type column_name: str
    :return:
    """
    dom.click_element(selenium, HEATMAP_COLUMN_PICKER)
    wait.until_visible(selenium, '.multiselect-picklist')
    selector = HEATMAP_COLUMN_PICKER_UNSELECTED_ITEM_CHECKBOX.format(column_name)
    dom.click_element(selenium, selector)
    # Click somewhere else to close the popup menu.
    dom.click_element(selenium, 'body')


def color_heatmap_column(selenium, column_name):
    """
    Sets coloring on the heatmap column.

    :param selenium: Webdriver
    :param column_name: The name for the column.
    :type column_name: str
    :return:
    """
    dom.click_element(selenium, HEATMAP_COLUMN_PICKER)
    wait.until_visible(selenium, '.multiselect-picklist')
    selector = HEATMAP_COLUMN_PICKER_SELECTED_ITEM_COLOR_LINK.format(column_name)
    dom.click_element(selenium, selector)
    dom.click_element(selenium, OK_BUTTON)


def set_tooltip_mode(selenium, mode):
    """
    Opens the advanced option panel, sets the tooltip mode and closes the advanced options panel.

    :param selenium: Webdriver
    :param mode: The tooltip mode, this should be one of 'none', 'normal', 'docked'.
    :type mode: str
    :return:
    """
    open_advanced_options_panel(selenium, PLOT_OPTIONS_TAB_NAME_TOOLTIP)
    dom.click_element(selenium, TOOLTIP_MODE_RADIO.format(mode), must_be_visible=False)
    close_advanced_options_panel(selenium)

    wait.until_visible(selenium, OPTIONS_MODE_BASIC)


def show_bin_options(selenium):
    """
    Opens the binning options menu for plots that have that capability.

    :param selenium: Webdriver
    """
    dom.click_element(selenium, SPG_BIN_HEADER)
    wait.until_visible(selenium, SPG_BIN_OPTIONS)


def hide_bin_options(selenium):
    """
    Closes the binning options menu for plots that have that capability.

    :param selenium: Webdriver
    """
    dom.click_element(selenium, SPG_BIN_HEADER)
    wait.until_not_visible(selenium, SPG_BIN_OPTIONS)


def set_active_custom_binning_rule_type(selenium, rule_type):
    """
    Sets the active binning rule type, assumes the binning options menu is open and the custom binning option has been
    selected.

    :param selenium: Webdriver
    :param rule_type: Either 'value' (for categorical columns) or 'numeric_range' for numeric columns
    :type rule_type: str
    """

    selector = CUSTOM_BINNING_RULE_TYPE_LABEL.format(rule_type)
    dom.click_element(selenium, selector)
    wait.until_visible(selenium, selector + '.active')


def set_bin_range(selenium, index, low=None, high=None):
    """
    Sets the bin range for the indexed numeric bin (starting from 1, nth-child selector) on the binning options menu.
    The binning options menu needs to be open.

    :param selenium: Webdriver
    :param index: the nth child selector for the bin range
    :type index: int
    :param low: the min value
    :type low: int
    :param high: the max value
    :type high: int
    """
    if low is None:
        low = ''
    if high is None:
        high = ''
    dom.set_element_value(selenium, NUMERIC_RULE_MIN_BOX.format(index), low, clear_existing_value=True, timeout=0.5)
    dom.click_element(selenium, NUMERIC_RULE_MAX_BOX.format(index))
    time.sleep(0.5)
    dom.set_element_value(selenium, NUMERIC_RULE_MAX_BOX.format(index), high, clear_existing_value=True, timeout=0.5)


def set_equal_bin_count(selenium, bin_count):
    """
    Will set equal bin count input value. To use this method, bin options window should be opened.

    :param selenium: selenium webdriver
    :param bin_count: int, Count which needs to be placed in equal bin count input box
    """
    show_bin_options(selenium)
    dom.click_element(selenium, BIN_COUNT_BUTTON)
    dom.set_element_value(selenium, EQUAL_BINNING_INPUT, value=bin_count)
    hide_bin_options(selenium)


def add_custom_bin_rule(driver, min_value, max_value, index):
    """
    Adds rule in custom bin selection

    :param driver: Selenium webdriver
    :param min_value: int, minimum value set to bin rule
    :param max_value: int, maximum value set to bin rule
    :param index: int, rule number
    """
    # clicking on Add Rule button
    dom.click_element(driver, SPG_ADD_BIN_RULE)

    wait.until_visible(driver, RULE_NAME.format(index))
    set_bin_range(driver, index, min_value, max_value)
    time.sleep(0.5)
    wait.sleep_if_k8s(1)
    # Here using a trick to press enter on max input box to apply the change in plot
    max_elem = dom.get_element(driver, NUMERIC_RULE_MAX_BOX.format(index))
    press_enter_key(utils.get_driver_from_element(max_elem))

    hide_bin_options(driver)


def set_style_overlays(selenium, overlay_position):
    """
    Opens the advanced option panel, goes to Style tab and sets the Overlays, and closes the advanced options panel.

    :param selenium: Webdriver
    :param overlay_position: The overlays, this should be one of positions of overlays, 1, 'Binding Efficiency Index',
        2, 'Custom Line', 3, 'Error Bands', 4, 'Horizontal Lines', 5, 'Ligand Efficiency', 6, 'Ligand Efficiency Dependent
        Lipophilicity', 7, 'Ligand Lipophilic Efficiency', 8, 'Regression Line', 9, 'Selectivity', 10, 'Size Independent
        Ligand Efficiency', 11, 'Surface Binding Efficiency', 12, 'Vertical Lines'
    :type overlay_position: str
    :return:
    """

    dom.click_element(selenium, ADD_OVERLAY_BUTTON, must_be_visible=True)
    dom.click_element(selenium, OVERLAY_OPTION.format(overlay_position))
    dom.click_element(selenium, OK_BUTTON)

    wait.until_visible(selenium, OPTIONS_MODE_BASIC)


def open_a_new_scatter_plot(selenium):
    """
    Function to create new scatterplot

    :param selenium: selenium Webdriver
    """
    open_visualize_panel(selenium)
    dom.click_element(selenium, VISUALIZATION_SCATTER)
    wait.until_visible(selenium, VISUALIZER_ACTIVE_TAB_TITLE_BAR)


def default_shape_selection_on_style_tab(selenium, data_shape):
    """
    Function to select default shape on style tab

    :param selenium: selenium Webdriver
    :data_shape: select shapes(like circle, diamond, right-triangle...etc)
    :type data_shape: str
    """
    dom.click_element(selenium, PLOT_OPTIONS_SHAPE_SELECTION_BUTTON, selector_type=By.XPATH)
    shape_selector = SELECT_SHAPE_BY.format(data_shape)
    dom.click_element(selenium, shape_selector)


def add_rule_nth_child_shape_selection(selenium, data_shape):
    """
    Function to select the shape on nth child of add rule

    :param selenium: selenium Webdriver
    :data_shape: select shapes(like circle, diamond, right-triangle...etc)
    :type data_shape: str
    """
    # Go to Nth child or last rule
    dom.click_element(selenium, PLOT_OPTIONS_STYLE_NTH_CHILD_SHAPE)
    shape_selector = SELECT_SHAPE_BY.format(data_shape)
    dom.click_element(selenium, shape_selector)
