import pytest

from helpers.change.actions_pane import open_visualize_panel
from helpers.change.plots import add_box_plot
from helpers.selection.plots import Y_AXIS_SELECT, X_AXIS_SELECT, CHART_XAXIS_LABEL, \
    CHART_YAXIS_LABEL, BOX_PLOT_POINT, CHART_XAXIS_TITLE, CHART_YAXIS_TITLE, BOX_PLOT_BOX_POINT
from helpers.selection.visualize import VISUALIZER_ACTIVE_TAB_TITLE_BAR
from helpers.verification.element import verify_is_visible
from helpers.verification.plots import verify_plot_tootip
from library import dom
from library.select import select_option_by_text
from helpers.verification import plots

live_report_to_duplicate = {'livereport_name': 'Boxplot Data', 'livereport_id': '888'}


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures('duplicate_live_report')
@pytest.mark.app_defect(
    reason="SS-40507: Plots tooltip is not getting removed when we move the focus out from the tooltip")
def test_box_plot(selenium):
    """
    Test box plot

    :param selenium: Selenium Webdriver
    """
    set_viewport_size(driver=selenium, width=1366, height=768)
    # create box plot
    open_visualize_panel(selenium)
    add_box_plot(selenium)

    # select axes
    select_option_by_text(selenium, Y_AXIS_SELECT, 'PSA (PSA)')
    select_option_by_text(selenium, X_AXIS_SELECT, 'HBA (HBA)')

    # verify axis titles
    verify_is_visible(selenium, CHART_XAXIS_TITLE, 'HBA (HBA)')
    verify_is_visible(selenium, CHART_YAXIS_TITLE, 'PSA (PSA)')

    # verify plot axis labels
    xlabel = dom.get_element(selenium, CHART_XAXIS_LABEL).text.replace('\n', '')
    ylabel = dom.get_element(selenium, CHART_YAXIS_LABEL).text.replace('\n', '')

    assert xlabel == '012345', "X-axis labels do not match with expected. Expected : 012345, but got: {}".format(xlabel)
    assert ylabel == '020406080100120140', \
        "Y-axis labels do not match with expected. Expected : 020406080100120140, but got: {}".format(ylabel)

    # validating outliers
    outlier_ids = ['V035706', 'V035715', 'V035680', 'V035631', 'V035701']
    expected_outlier_tooltips = [
        'V035706\nLot Date Registered\n2015-05-08 14:59:16\nLot Scientist\ndemo\nHBA (HBA)\n0\nPSA (PSA)\n37.3',
        'V035715\nLot Date Registered\n2015-05-08 14:59:18\nLot Scientist\ndemo\nHBA (HBA)\n0\nPSA (PSA)\n26.07',
        'V035680\nLot Date Registered\n2015-05-08 14:59:11\nLot Scientist\ndemo\nHBA (HBA)\n0\nPSA (PSA)\n0',
        'V035631\nLot Date Registered\n2015-05-08 14:59:00\nLot Scientist\ndemo\nHBA (HBA)\n4\nPSA (PSA)\n111.9',
        'V035701\nLot Date Registered\n2015-05-08 14:59:15\nLot Scientist\ndemo\nHBA (HBA)\n1\nPSA (PSA)\n149.65'
    ]
    for index, outlier in enumerate(outlier_ids):
        verify_plot_tootip(selenium, BOX_PLOT_POINT.format(outlier), expected_outlier_tooltips[index])

    # Verify box plot boxes
    expected_box_tooltips = [
        'Maximum: 80.57\nUpper quartile: 80.57\nMedian: 80.57\nLower quartile: 46.33\nMinimum: 9.23',
        'Maximum: 104.36\nUpper quartile: 94.895\nMedian: 55.76\nLower quartile: 44.81\nMinimum: 34.15',
        'Maximum: 103.41\nUpper quartile: 81.59\nMedian: 68.6\nLower quartile: 54.04\nMinimum: 35.53',
        'Maximum: 82.72\nUpper quartile: 77.83\nMedian: 68.8\nLower quartile: 56.135\nMinimum: 48.67',
        'Maximum: 142.47\nUpper quartile: 134.96\nMedian: 81.7\nLower quartile: 71.25\nMinimum: 69.67'
    ]

    for index, box in enumerate(expected_box_tooltips):
        # using index for box id, box id starts from 1. hence used index+1
        verify_plot_tootip(selenium, BOX_PLOT_BOX_POINT.format(index + 1), expected_box_tooltips[index])
        plots.verify_plot_tooltip_removed(selenium)


def set_viewport_size(driver, width, height):
    """
    Setting browser viewport size.

    :param driver: Selenium webdriver
    :param width: int, Width of the browser window
    :param height: int, height of the browser window
    """
    # updating viewport sizes for browser. Here setting only user visible area as window size.
    window_size = driver.execute_script(
        """
        return [window.outerWidth - window.innerWidth + arguments[0],
          window.outerHeight - window.innerHeight + arguments[1]];
        """, width, height)
    driver.set_window_size(*window_size)
