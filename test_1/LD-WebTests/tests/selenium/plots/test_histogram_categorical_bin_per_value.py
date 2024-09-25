import pytest
from selenium.webdriver.support.ui import Select

from helpers.change.actions_pane import open_add_compounds_panel, open_visualize_panel
from helpers.change.freeform_column_action import create_ffc, edit_ffc_cell
from helpers.selection.plots import CHART_AXIS_TITLE, CHART_XAXIS_LABEL, HIST_BAR_01, HIST_BAR_02, HIST_BAR_03, \
    ONE_PER_VALUE_BINNING_BUTTON, SPG_BIN_HEADER, SPG_BIN_OPTIONS, VISUALIZATION_HISTOGRAM
from library import dom, simulate, wait

live_report_to_duplicate = {'livereport_name': 'Plots test LR', 'livereport_id': '2598'}


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_histogram_categorical_bin_per_value(selenium):
    """
    Test categorical bin per value histogram creation.

    :param selenium: selenium Webdriver
    """

    # ----- LR Setup ----- #
    # Create a new FFC through button in D&C tree
    description = 'This is a simple text free form column.'
    open_add_compounds_panel(selenium)
    create_ffc(selenium, 'FFC Name 01', description)

    # Add FFC values
    edit_ffc_cell(selenium, 'FFC Name 01', 'V035752', 'A Bin')
    edit_ffc_cell(selenium, 'FFC Name 01', 'V038399', 'B Bin')
    edit_ffc_cell(selenium, 'FFC Name 01', 'V041170', 'B Bin')
    edit_ffc_cell(selenium, 'FFC Name 01', 'V041471', 'B Bin')
    edit_ffc_cell(selenium, 'FFC Name 01', 'V044401', 'C Bin')

    # ----- Create Histogram new plot ----- #
    open_visualize_panel(selenium)
    dom.click_element(selenium, VISUALIZATION_HISTOGRAM)

    # Select categorical column as axis
    select = Select(dom.get_element(selenium, '#spg-x-axis-select'))
    select.select_by_visible_text('FFC Name 01')

    # Select One Bin Per Value (This is the default so it's not strictly
    # necessary. But it seems worth figuring out how to click the radio
    # buttons.)
    dom.click_element(selenium, SPG_BIN_HEADER)
    wait.until_visible(selenium, SPG_BIN_OPTIONS)
    dom.click_element(selenium, ONE_PER_VALUE_BINNING_BUTTON)

    # Close bin options (when open, a transparent mask covers the plot to capture clicks)
    dom.click_element(selenium, SPG_BIN_HEADER)

    # ----- Verify Plot ----- #
    # Verify x axis label
    dom.get_element(selenium, CHART_AXIS_TITLE, text='FFC Name 01')

    # Verify bins along x axis are as expected
    dom.get_element(selenium, CHART_XAXIS_LABEL, text='A Bin')
    dom.get_element(selenium, CHART_XAXIS_LABEL, text='B Bin')
    dom.get_element(selenium, CHART_XAXIS_LABEL, text='C Bin')

    # Hover over the first histogram bar
    hist_bar_01 = dom.get_element(selenium, HIST_BAR_01)
    simulate.hover(selenium, hist_bar_01)
    wait.until_visible(selenium, '.category-name', 'A Bin')
    # Verify popup information
    assert dom.get_element(selenium, '.category-name').text == 'A Bin'
    assert dom.get_element(selenium, '.bin-count').text == '1'

    # Hover over the second histogram bar
    hist_bar_02 = dom.get_element(selenium, HIST_BAR_02)
    simulate.hover(selenium, hist_bar_02)
    wait.until_visible(selenium, '.category-name', 'B Bin')
    # Verify popup information
    assert dom.get_element(selenium, '.category-name').text == 'B Bin'
    assert dom.get_element(selenium, '.bin-count').text == '3'

    # Hover over the third histogram bar
    hist_bar_03 = dom.get_element(selenium, HIST_BAR_03)
    simulate.hover(selenium, hist_bar_03)
    wait.until_visible(selenium, '.category-name', 'C Bin')
    # Verify popup information
    assert dom.get_element(selenium, '.category-name').text == 'C Bin'
    assert dom.get_element(selenium, '.bin-count').text == '1'
