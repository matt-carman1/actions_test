import pytest

from helpers.change.actions_pane import open_visualize_panel
from helpers.change.grid_columns import click_compound_row
from helpers.change.plots import open_advanced_options_panel, change_advanced_options_panel_tab, \
    close_advanced_options_panel
from helpers.selection.coloring_rules import COLOR_WINDOW_OK_BUTTON
from helpers.selection.plots import LEGEND, LEGEND_SELECT, PLOT_OPTIONS_PANEL, PLOT_OPTIONS_TAB_NAME_STYLE, \
    COLOR_BY_AXIS_SELECT, SCATTER_POINTS, TOOLTIP_FIELD_LIST, TOOLTIP_COMPOUND_ID, VISUALIZATION_SCATTER, \
    X_AXIS_SELECT, Y_AXIS_SELECT
from helpers.verification.plots import verify_first_chart_update_counts, verify_scatter_point_count, \
    verify_selected_scatter_point_count
from library import dom, wait, style
from library.eventually import eventually_equal
from library.select import select_option_by_text
from library.simulate import hover

live_report_to_duplicate = {'livereport_name': 'Plots test LR', 'livereport_id': '2598'}


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_scatter_plot(selenium):
    """
    Test basic scatter plot with two numeric axes.

    :param selenium: selenium Webdriver
    """

    # Create a new scatter plot.
    open_visualize_panel(selenium)
    dom.click_element(selenium, VISUALIZATION_SCATTER)

    # Select the axes
    select_option_by_text(selenium, Y_AXIS_SELECT, 'HBA (HBA)')
    select_option_by_text(selenium, X_AXIS_SELECT, 'AlogP (AlogP)')
    verify_scatter_point_count(selenium, 5)
    verify_first_chart_update_counts(selenium, {'update': {'max': 3}, 'rebuild': {'max': 3}, 'noop': 0})

    # Select one row in LR and verify it is selected in scatter plot.
    click_compound_row(selenium, 'V035752')
    verify_selected_scatter_point_count(selenium, 1)
    verify_first_chart_update_counts(selenium, {
        'update': {
            'max': 4
        },
        'rebuild': {
            'max': 3
        },
        'updateSelection': 1,
        'noop': 0
    })
    click_compound_row(selenium, 'V035752')

    # Trigger tooltip
    point_selector = '{}[id*="{}"]'.format(SCATTER_POINTS, 'V035752')
    hover(selenium, dom.get_element(selenium, point_selector))

    # Verify tooltip's compound ID matches
    wait.until_visible(selenium, TOOLTIP_COMPOUND_ID, text='V035752')

    # Select color by axis
    open_advanced_options_panel(selenium)
    change_advanced_options_panel_tab(selenium, PLOT_OPTIONS_TAB_NAME_STYLE)
    select_option_by_text(selenium, '{} {}'.format(PLOT_OPTIONS_PANEL, COLOR_BY_AXIS_SELECT), 'HBA (HBA)')
    dom.click_element(selenium, COLOR_WINDOW_OK_BUTTON)
    close_advanced_options_panel(selenium)
    #
    # SS-28011 Sometimes get multiple updates to the plot models on changing the coloring (as the updated information
    # sometimes seems to appear in fragments), resulting in extra plot updates/rebuilds. We allow for that here by
    # setting the max allowable update and rebuild in verify_first_chart_update_counts.
    #
    verify_first_chart_update_counts(selenium, {
        'update': {
            'max': 7
        },
        'rebuild': {
            'max': 6
        },
        'updateSelection': 2,
        'noop': 0
    })

    # Hide the legend as it gets in the way of the points for the hover.
    open_advanced_options_panel(selenium)
    change_advanced_options_panel_tab(selenium, PLOT_OPTIONS_TAB_NAME_STYLE)
    select_option_by_text(selenium, LEGEND_SELECT, 'None')
    close_advanced_options_panel(selenium)
    wait.until_not_visible(selenium, LEGEND)

    # Verify points' colors and that colors match in tooltips
    expected_point_colors = {
        'V035752': '#E96969',
        'V038399': '#FF0000',
        'V041170': '#D3D3D3',
        'V041471': '#D3D3D3',
        'V044401': '#FF0000'
    }

    _verify_scatter_point_colors(selenium, expected_point_colors)

    cyp_position = 5
    _verify_tooltip_colors(selenium, expected_point_colors, cyp_position)


def _verify_scatter_point_colors(selenium, expected_point_colors):
    """
    Verify that the points have the colors we're expecting

    :param selenium: Webdriver
    :param expected_point_colors: Dictionary of compound ID -> expected hex colors
    :return:
    """
    for compound_id in expected_point_colors.keys():
        point_selector = '{}[id*="{}"]'.format(SCATTER_POINTS, compound_id)
        point_element = dom.get_element(selenium, point_selector)
        point_color_actual = point_element.get_attribute('fill').upper()
        point_color_expected = expected_point_colors[compound_id]
        assert point_color_actual == point_color_expected


def _verify_tooltip_colors(selenium, expected_tooltip_colors, property_position):
    """
    Verify that the background color in the tooltip's field list are as expected

    :param selenium: Webdriver
    :param expected_tooltip_colors: Dictionary of compound ID -> expected hex colors
    :param property_position: The ordinal position of the property in the field list that we're checking
    :return:
    """
    for compound_id in expected_tooltip_colors.keys():
        point_selector = '{}[id*="{}"]'.format(SCATTER_POINTS, compound_id)
        point_element = dom.get_element(selenium, point_selector)
        point_color_expected = expected_tooltip_colors[compound_id]

        hover(selenium, point_element)
        wait.until_visible(selenium, '.plot-tooltip')

        def get_background_color_from_tooltip(driver):
            """
            Gets the background color from the field list in the tooltip, which should match the coloring rules
            of the LiveReport

            :param driver: Webdriver
            :return: Hex color of the background
            """
            field_value_selector = '{} li:nth-child({}) .field-value'.format(TOOLTIP_FIELD_LIST, property_position)
            field_value_element = dom.get_element(driver, field_value_selector)
            field_value_inline_styles = style.get_inline_style_as_dict(field_value_element)

            background_color = field_value_inline_styles.get('background-color', '')
            return _convert_rgb_to_hex(background_color) if background_color else ''

        assert eventually_equal(selenium, get_background_color_from_tooltip, point_color_expected)


def _convert_rgb_to_hex(rgb):
    """
    Convert an rgb string to a hex string

    :param rgb: the rgb string itself
    :return:
    """
    rgb_string = rgb[rgb.find('(') + 1:rgb.find(')')]
    rgb_values = [int(value) for value in rgb_string.split(', ')]
    return ('#%02x%02x%02x' % tuple(rgb_values)).upper()
