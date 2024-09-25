from helpers.selection.plots import CHART
from library import dom


def get_plot_ids_for_visible_charts(selenium):
    """
    Returns a list of the plot IDs that are set on chart divs using the data-plot-id attribute.

    :param selenium: Webdriver
    :return: A list of the plot IDs that are set on chart divs
    :rtype: list
    """
    return [element.get_attribute('data-plot-id') for element in dom.get_elements(selenium, CHART)]


def get_chart_update_count_maps(selenium, plot_ids=[]):
    """
    Returns a dict of the chart update count maps for charts with the provided plot_ids. If the plot_ids are not
    provided this returns the chart update count maps for all the visible charts.

    :param selenium: Webdriver
    :param plot_ids: Optional list of plot IDs.
    :type plot_ids: list
    :return: A dictionary of the chart count maps keyed by the plot ID.
    :rtype: dict
    """
    if not plot_ids:
        plot_ids = get_plot_ids_for_visible_charts(selenium)
    chart_update_count_map = selenium.execute_script('return bb.perfMetrics.ChartUpdaterCountsMap;')
    return dict((plot_id, chart_update_count_map[plot_id]) for plot_id in plot_ids if plot_id in chart_update_count_map)


def get_first_chart_update_count_map(selenium):
    """
    Returns the chart update count map for the first visible chart. Useful in cases where there is only one chart
    currently displayed.

    :param selenium: Webdriver
    :return: The chart count map for the first visible chart.
    :rtype: dict
    """
    chart_update_count_map = get_chart_update_count_maps(selenium)
    return next(iter(chart_update_count_map.values()))
