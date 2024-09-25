import time
from library import dom, wait
from library.simulate import hover
from library.eventually import eventually_equal

from selenium.webdriver.common.by import By

from helpers.extraction.plots import get_first_chart_update_count_map
from helpers.selection.plots import CUSTOM_BINNING_ACTIVE_RULE_TYPE_LABEL, HEATMAP_CELL, HEATMAP_SELECTED_CELL, \
    CHART_XAXIS_LABEL, CHART_YAXIS_LABEL, SCATTER_POINTS, SCATTER_SELECTED_POINTS, HEATMAP_POINT, HISTOGRAM_BAR, \
    PIE_SLICE, RADAR_AXIS, \
    RADAR_AXIS_LABEL, RADAR_LEGEND_ITEM, RADAR_LINE, RADAR_LINE_TRACKER, PIE_DISPLAY_RANGES, PLOT_TOOLTIP, \
    PIE_SLICE_BY_ID, X_AXIS_SELECT, Y_AXIS_SELECT, SCATTER_PATHS
from helpers.selection.plots import TOOLTIP_COMPOUND_ID, TOOLTIP_BIN_COUNT
from helpers.selection.visualize import VISUALIZE_TITLE_BAR
from helpers.verification.element import verify_is_visible
from helpers.verification.color import color_string_to_tuple
from helpers.selection import plots, visualize

DEFAULT_HEATMAP_CELL_COLOR = (238, 238, 238, 1)


def verify_histogram_bar_count(selenium, expected_bar_count, simplified_bin_labels=False):
    """
    Verify that the histogram has the expected number of bars

    :param selenium: Webdriver
    :param expected_bar_count: The number of histogram bars that should exist
    :type expected_bar_count: int
    :param simplified_bin_labels: Whether the histogram is attempting to simplify the display of the labels in which
                                  case a dummy bin is created and needs to be accounted for
    :type simplified_bin_labels: bool

    :return:
    """

    def _get_histogram_bar_count(driver):
        return len(dom.get_elements(driver, HISTOGRAM_BAR))

    count = (expected_bar_count + 1) if simplified_bin_labels else expected_bar_count
    assert eventually_equal(selenium, _get_histogram_bar_count, count), \
        'Number of histogram bars does not equal %r' % expected_bar_count


def verify_pie_slice_count(selenium, expected_slice_count):
    """
    Verify that the pie chart has the expected number of slices

    :param selenium: Webdriver
    :param expected_slice_count: The number of pie slices that should exist
    :type expected_slice_count: int
    :return:
    """

    def _get_pie_slice_count(driver):
        return len(dom.get_elements(driver, PIE_SLICE))

    assert eventually_equal(selenium, _get_pie_slice_count, expected_slice_count), \
        'Number of pie slices does not match %r' % expected_slice_count


def verify_radar_axis_count(selenium, expected_axis_count):
    """
    Verify that the radar plot has the expected number of axes

    :param selenium: Webdriver
    :param expected_axis_count: The number of axes that should exist
    :type expected_axis_count: int
    :return:
    """

    def _get_radar_axis_count(driver):
        return len(dom.get_elements(driver, RADAR_AXIS))

    # NOTE (ext_glysade_watson) that the number of elements from the RADAR_AXIS selector is always axis_count + 1.
    assert eventually_equal(selenium, _get_radar_axis_count, expected_axis_count + 1), \
        'Number of radar axes does not match %r' % expected_axis_count


def verify_radar_line_count(selenium, expected_line_count):
    """
    Verify that the radar plot has the expected number of lines

    :param selenium: Webdriver
    :param expected_line_count: The number of lines that should exist
    :type expected_line_count: int
    :return:
    """

    def _get_radar_line_count(driver):
        return len(dom.get_elements(driver, RADAR_LINE))

    assert eventually_equal(selenium, _get_radar_line_count, expected_line_count)

    def _get_radar_line_tracker_count(driver):
        return len(dom.get_elements(driver, RADAR_LINE_TRACKER))

    assert eventually_equal(selenium, _get_radar_line_tracker_count, expected_line_count), \
        'Number of radar lines does not match %r' % expected_line_count


def verify_radar_axis_labels(selenium, expected_axis_names):
    """
    Verify that axis labels are as we expect in the radar plot.

    :param selenium: Webdriver
    :param expected_axis_names: The set of names of the axes that should appear as labels in the radar plot
    :type expected_axis_names: set e.g. {'Axis 1', 'Axis 2'}
    :return:
    """

    # Since removing the HTML style axis labels this has become slightly more complicated.
    # The axis labels are made up of the column name + the axis range e.g. AlogP (AlogP) [1.4 to 5.6].
    # Highcharts displays the axis labels in one or more tspan elements. Highcharts does some work to figure out how to
    # wrap the axis label to give the 'best' layout. So very often they split the string and display the resulting
    # each substring in a tspan e.g.
    #
    # </tspan><tspan>AlogP (AlogP) [1.4 to</tspan>
    # <tspan dy="15" x="511.35386112375727">5.6]</tspan>
    #
    # Given that we don't really know the method they use to split the strings would be difficult to reconstitute the
    # string from the tspans. Instead we get the first tspan for each axis, obtain the text and test to see if it
    # starts with one of the expected axis names or one of the expected axis names stars with the tspan text.
    #
    elements = dom.get_elements(selenium, RADAR_AXIS_LABEL)
    assert len(elements) == len(expected_axis_names)
    for element in elements:
        text = element.text
        matches = bool([s for s in expected_axis_names if (s.startswith(text) or text.startswith(s))])
        assert matches, '%r not not found in set of expected axis names' % text


def verify_radar_legend(selenium, expected_names):
    """
    Verify that legend items appear for the selected rows in the radar plot.

    :param selenium: Webdriver
    :param expected_names: The expected names for the legend items
    :type expected_names: set
    :return:
    """

    elements = dom.get_elements(selenium, RADAR_LEGEND_ITEM)
    assert len(elements) == len(expected_names)
    for element in elements:
        assert element.text in expected_names, '%r not not found in set of expected legends' % element.text


def verify_selected_scatter_point_count(selenium, expected_selected_point_count):
    """
    Verify that the scatter plot has the expected number of selected points

    :param selenium: Webdriver
    :param expected_selected_point_count: The number of scatter points that should be selected
    :return:
    """

    def _get_selected_scatter_point_count(driver):
        return len(dom.get_elements(driver, SCATTER_SELECTED_POINTS))

    assert eventually_equal(selenium, _get_selected_scatter_point_count, expected_selected_point_count)


def verify_scatter_point_count(selenium, expected_point_count):
    """
    Verify that the scatter plot has the expected number of points

    :param selenium: Webdriver
    :param expected_point_count: The number of scatter points that should exist
    :type expected_point_count: int
    :return:
    """

    def _get_scatter_point_count(driver):
        return len(dom.get_elements(driver, SCATTER_POINTS))

    assert eventually_equal(selenium, _get_scatter_point_count, expected_point_count), \
        'Number of scatter plot points does not match %r' % expected_point_count


def verify_scatter_plot_params(driver, plot_title, x_axis_col, y_axis_col, point_count):
    """
    Function specific to verify the scatter plot and its parameters
    Note: Currently it just checks plot title, X and Y axis name & point count

    :param driver: Webdriver
    :param plot_title: str, Title of the plot
    :param x_axis_col: str, Column name selected for x-axis
    :param y_axis_col: str, Column name selected for y-axis
    :param point_count: int, Number of scatter plot points
    """
    verify_is_visible(driver, VISUALIZE_TITLE_BAR, selector_text=plot_title)
    verify_is_visible(driver, Y_AXIS_SELECT, selector_text=y_axis_col)
    verify_is_visible(driver, X_AXIS_SELECT, selector_text=x_axis_col)
    verify_scatter_point_count(driver, expected_point_count=point_count)


def verify_heatmap_cell_count(selenium, expected):
    """
    Verify the number of cells equals the provided expected count.

    :param selenium: Webdriver
    :param expected: Expected number of cells.
    :type expected: int
    """

    def _get_heatmap_cell_count(driver):
        return len(dom.get_elements(driver, HEATMAP_CELL))

    assert eventually_equal(selenium, _get_heatmap_cell_count, expected)


def verify_heatmap_point_count(selenium, expected_point_count):
    """
    Verify that the heatmap plot has the expected number of points

    :param selenium: Webdriver
    :param expected_point_count: The number of heatmap points that should exist
    :type expected_point_count: int
    :return:
    """

    def _get_heatmap_point_count(driver):
        return len(dom.get_elements(driver, HEATMAP_POINT))

    assert eventually_equal(selenium, _get_heatmap_point_count, expected_point_count), \
        'Number of heatmap points does not equal %r' % expected_point_count


def verify_selected_heatmap_cell_count(selenium, expected):
    """
    Verify the number of selected cells equals the provided expected count.

    :param selenium: Webdriver
    :param expected: Expected number of selected cells.
    :type expected: int
    """

    def _get_selected_heatmap_cell_count(driver):
        return len(dom.get_elements(driver, HEATMAP_SELECTED_CELL))

    assert eventually_equal(selenium, _get_selected_heatmap_cell_count, expected)


def verify_heatmap_column_count(selenium, expected):
    """
    Verify the number of heatmap columns equals the provided expected count.

    :param selenium: Webdriver
    :param expected: Expected number of columns.
    :type expected: int
    """
    elements = dom.get_elements(selenium, CHART_XAXIS_LABEL + ' text')
    assert len(elements) == expected, 'Heatmap column count, %r, should match expected, %r' \
                                      % (len(elements), expected)


def verify_heatmap_column_headers(selenium, expected):
    """
    Verify the column headers match those provided in the expected array and that they are in the same order.

    :param selenium: Webdriver
    :param expected: Expected array of column names.
    :type expected: list
    """
    elements = dom.get_elements(selenium, CHART_XAXIS_LABEL + ' text')
    assert len(elements) == len(expected), 'Heatmap columns length, %r, should match expected, %r' \
                                           % (len(elements), len(expected))
    for i in range(len(elements)):
        expected_title = expected[i]
        actual_title = elements[i].text
        assert actual_title == expected_title, 'Heatmap column header, %r, should match expected, %r' \
                                               % (actual_title, expected_title)


def verify_heatmap_row_count(selenium, expected):
    """
    Verify the number of heatmap rows equals the provided expected count.

    :param selenium: Webdriver
    :param expected: Expected number of rows.
    :type expected: int
    """
    elements = dom.get_elements(selenium, CHART_YAXIS_LABEL + ' text')
    assert len(elements) == expected, 'Heatmap row count, %r, should match expected, %r' \
                                      % (len(elements), expected)


def verify_heatmap_row_headers(selenium, expected):
    """
    Verify the row headers match those provided in the expected array and that they are in the same order.

    :param selenium: Webdriver
    :param expected: Expected array of row header names.
    :type expected: list
    """
    elements = dom.get_elements(selenium, CHART_YAXIS_LABEL + ' text')
    assert len(elements) == len(expected), 'Heatmap row count, %r, should match expected, %r' \
                                           % (len(elements), len(expected))
    for i in range(len(elements)):
        expected_title = expected[i]
        actual_title = elements[i].text
        assert actual_title == expected_title, 'Heatmap row header, %r, should match expected, %r' \
                                               % (actual_title, expected_title)


def verify_heatmap_cell_color(selenium, compound_id, column_id, expected):
    """
    Verify the heatmap cell (selected using the compound ID and column ID) is the expected color.

    :param selenium: Webdriver
    :param compound_id: The compound identifier.
    :type compound_id: str
    :param column_id: The column ID (not the column name).
    :type column_id: str
    :param expected: The expected color.
    :type expected: tuple
    """

    def _color_matches(element):
        color_string = element.get_attribute('fill')
        color = color_string_to_tuple(color_string)
        return color == expected

    element_color_condition = dom.ElementCriteriaCondition(
        (By.CSS_SELECTOR, "path[id*='%s-%s']" % (compound_id, column_id)), filter_function=_color_matches)
    message = 'Expected element color to be `{}` for `{}` `{}`'.format(expected, compound_id, column_id)
    dom.wait_until(selenium, element_color_condition, message)


def verify_heatmap_cell_colors(selenium, selector_and_color_list):
    """
    Verify the heatmap cells (selected using the compound ID and column ID) are the expected colors.

    :param selenium: Webdriver
    :param selector_and_color_list: List of dictionary objects defining the selector for the cells and the expected
                                    colors e.g. {"compound_id": "CRA-035608", "column_id": "829",
                                    color: (255, 0, 0, 1) }. The compound_id and column_id are strings, the color is a
                                    tuple.
    :type selector_and_color_list: list
    """
    for selector_and_color in selector_and_color_list:
        verify_heatmap_cell_color(selenium, selector_and_color["compound_id"], selector_and_color["column_id"],
                                  selector_and_color["color"])


def verify_first_chart_update_counts(selenium, expected):
    """
    Checks that the chart update counts for the first chart contains the expected values.

    :param selenium: Webdriver
    :param expected: Dictionary where the keys are the types of updates that have happened to a chart and
                     their values are an expected count or a dict defining and acceptable min and/or max e.g.
                     expected = {'update': 3, 'rebuild': {'max': 2}, updateSelection: {'min': 0, 'max': 1}}
                     The possible count types are:
                     'update', the number of times the update method on the ChartUpdater is called. This is
                     called every time the plot configuration is updated on the Chart.jsx react component.
                     'rebuild', the number of times the change in the plot configuration requires disposing
                     the chart and rebuilding from scratch. This happens on things like changing the axes,
                     or changing the color by column.
                     'updateSelection', the number of times we were able to update the chart without a
                     rebuild on a selection change. Should only be triggered by selecting things in a chart
                     or by selecting rows.
                     'resize', the number of times we were able to update the chart without requiring
                     rebuild on a resize. Should only happen when the plot is resized.
                     'noop', the number of times the update method was called, but the supplied configuration
                     for the chart was exactly the same as the existing configuration. We want to avoid this
                     happening as much as possible as this indicates we are recalculating the plot model
                     objects unnecessarily.
    :type expected: dict
    """

    def _check_first_chart_update_counts(driver):
        chart_update_counts = get_first_chart_update_count_map(driver)
        for expected_event, expected_count_or_range in expected.items():
            actual_count = chart_update_counts[expected_event]
            if isinstance(expected_count_or_range, int):
                expected_count = expected_count_or_range
                if actual_count != expected_count:
                    return False
            elif isinstance(expected_count_or_range, dict):
                expected_count_dict = expected_count_or_range
                if 'min' not in expected_count_dict and 'max' not in expected_count_dict:
                    raise ValueError('expected value is dictionary, but should contain min and/or max int entries ')
                if 'min' in expected_count_dict:
                    expected_min = expected_count_dict['min']
                    if actual_count < expected_min:
                        return False
                if 'max' in expected_count_dict:
                    expected_max = expected_count_dict['max']
                    if actual_count > expected_max:
                        return False
            else:
                raise ValueError('expected value should be int or dict containing min and/or max int entries')
        return True

    assert eventually_equal(selenium, _check_first_chart_update_counts, True), \
        'Chart update counts did not match expected %r %r' % (get_first_chart_update_count_map(selenium), expected)


def verify_plot_tooltip_compound_id(selenium, point_selector, compound_id):
    """
    Hovers over a point/line/cell on a chart and verifies that the tooltip appears and that it has the expected`
    compound ID.

    :param selenium: Webdriver
    :param point_selector: The selector for the point/cell/line on a chart that would produce a tooltip if hovered.
    :type point_selector: str
    :param compound_id: The ID for the compound that should appear in the tooltip.
    :type compound_id: str
    """

    # NOTE (ext_watson_glysade) The reason for this function is that we have had issues with hovering over chart objects
    # waiting for tooltips to appear during a debounced chart resize. This method is an effort to mitigate the tooltip
    # not appearing because the point moves due to the debounced chart resize.
    def _hover_and_check_tooltip(point):
        hover(selenium, point)
        wait.until_visible(selenium, TOOLTIP_COMPOUND_ID, timeout=2, text=compound_id)

    # Add a sleep here to (potentially) make the test run faster i.e. allow the _hover_and_check_tooltip function to
    # succeed first time.
    time.sleep(1)
    assert dom.get_element(selenium, point_selector, action_callback=_hover_and_check_tooltip), \
        'Could not find tooltip with compound ID {}'.format(compound_id)


def verify_custom_binning_active_rule_type(selenium, expected):
    """
    Verifies the active rule type is as expected. Allowable expected values are 'numeric_range', 'value'.

    :param selenium: Webdriver
    :param expected: The expected active rule type, allowable expected values are 'numeric_range', 'value'
    :type expected: str
    """

    def _get_active_rule_type(driver):
        element = dom.get_element(driver, CUSTOM_BINNING_ACTIVE_RULE_TYPE_LABEL)
        return element.get_attribute('data-rule-type')

    assert eventually_equal(selenium, _get_active_rule_type, expected), \
        'Active rule type (%r) does not match expected (%r)' % (_get_active_rule_type(selenium), expected)


def verify_bin_tooltip_bin_count(selenium, bar_selector, expected_count):
    """
    Verifies the tooltip for a binned plot object (e.g. bar on a histogram or a pie slice) contains the correct
    count value.

    :param selenium: Webdriver
    :param bar_selector: CSS selector for the histogram bar
    :type bar_selector: str
    :param expected_count: Expected number of items in bar
    :type expected_count: int
    """

    def _hover_and_check_tooltip(bar):
        hover(selenium, bar)
        wait.until_visible(selenium, TOOLTIP_BIN_COUNT, timeout=2, text=str(expected_count))

    # Add a sleep here to (potentially) make the test run faster i.e. allow the _hover_and_check_tooltip function to
    # succeed first time.
    # time.sleep(1)
    assert dom.get_element(selenium, bar_selector, action_callback=_hover_and_check_tooltip), \
        'Could not find tooltip with count {}'.format(expected_count)


def verify_plot_tooltip_removed(selenium):
    """
    Verify the bin tooltip is removed by hovering outside of the bin ( To do this, we are clicking on current Active Tab of Visulizer)
    """

    dom.click_element(selenium, visualize.VISUALIZER_ACTIVE_TAB_TITLE_BAR)
    wait.until_not_visible(selenium, plots.PLOT_TOOLTIP, timeout=4)


def verify_display_ranges_in_pie_chart(driver, expected_display_ranges):
    """
    Verify display ranges for all pies in pie chart.

    :param driver: selenium webdriver
    :param expected_display_ranges: list, expected display ranges
    """
    display_range_elems = dom.get_elements(driver, PIE_DISPLAY_RANGES)
    display_ranges = [display_range_elem.text for display_range_elem in display_range_elems]
    assert display_ranges == expected_display_ranges


def verify_plot_tootip(driver, slice_selector, tooltip_text):
    """
    Hovers over a point/line/slice on a chart and verifies that the tooltip appears and that it has the expected text.

    :param driver: Selenium Webdriver
    :param slice_selector: str, selector for the point/line/slice on a chart
    :param tooltip_text: str, expected tooltip text
    """

    def _hover_and_check_tooltip(point):
        hover(driver, point)
        wait.until_visible(driver, PLOT_TOOLTIP, timeout=2, text=tooltip_text)

    assert dom.get_element(driver, slice_selector, action_callback=_hover_and_check_tooltip), \
        'Could not find tooltip with text {}'.format(tooltip_text)


def verify_display_ranges_and_tooltips_for_pie_chart(selenium, bin_count, display_ranges,
                                                     display_range_for_tooltip_check, tooltip_text):
    """
    Verify Equal Bin Input in chart which includes verify pie slice count, verify display ranges, verify pie tooltip
    which contains data range and count.

    :param selenium: selenium webdriver
    :param bin_count: int, number of equal bins(i,e equal bin input text box number)
    :param display_ranges: list, list of display ranges which are appearing in pie chart
    :param display_range_for_tooltip_check: str, display range for any pie slice to check tooltip text.
    Usage: decimal points needs to be replaced with -, ex: 162-32.3 should be passed as 162-32-2
    :param tooltip_text: str, tooltip text which needs to be verified
    """
    # verify pie slice count
    verify_pie_slice_count(selenium, bin_count)
    # verify display ranges
    verify_display_ranges_in_pie_chart(selenium, display_ranges)
    # hovering on pie slice and verify pie tooltip which includes Data Range and Count verification
    verify_plot_tootip(selenium, PIE_SLICE_BY_ID.format(display_range_for_tooltip_check), tooltip_text)


def verify_scatter_shape_point_count(selenium, expected_shape_point_count):
    """
    Verify that the scatter plot has the expected number of shapes

    :param selenium: Webdriver
    :param expected_shape_point_count: The number of scatter shape points that should exist
    :type expected_shape_point_count: int
    """

    def _get_scatter_shape_point_count(driver):
        shapes = dict()
        els = dom.get_elements(driver, SCATTER_PATHS)
        # number of paths
        for el in els:
            # each path contains shape value
            shape = el.get_attribute('shape')
            # if shape value present
            if shape:
                # add count to the shapes dictionary
                shapes[shape] = shapes.get(shape, 0) + 1
        return sum(shapes.values())
    assert eventually_equal(selenium, _get_scatter_shape_point_count, expected_shape_point_count), \
        'Number of scatter plot shape points does not match %r' % expected_shape_point_count