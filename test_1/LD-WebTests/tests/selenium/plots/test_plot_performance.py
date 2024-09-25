import pytest

from helpers.change.actions_pane import open_visualize_panel
from helpers.change.grid_columns import click_compound_row
from helpers.change.plots import open_advanced_options_panel, close_advanced_options_panel
from helpers.selection.plots import VISUALIZATION_SCATTER, X_AXIS_SELECT, Y_AXIS_SELECT
from helpers.verification.plots import verify_first_chart_update_counts, verify_selected_scatter_point_count
from library.select import select_option_by_text
from library import dom

live_report_to_duplicate = {'livereport_name': '5 Compounds 4 Assays', 'livereport_id': '882'}


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_plot_performance(selenium):
    """
    Demonstrate usage of the chart update counts allowing us to track number of updates to a plot based on various
    events.

    :param selenium: selenium Webdriver
    """

    # Create a new scatter plot.
    open_visualize_panel(selenium)
    dom.click_element(selenium, VISUALIZATION_SCATTER)

    # Select the axes
    select_option_by_text(selenium, Y_AXIS_SELECT, 'Clearance (undefined)')
    select_option_by_text(selenium, X_AXIS_SELECT, 'CYP450 2C19-LCMS (%INH)')
    verify_first_chart_update_counts(selenium, {'update': 2, 'rebuild': 2, 'noop': 0})

    # Select a point.
    _select_row_and_verify(selenium)
    verify_first_chart_update_counts(selenium, {'update': 3, 'rebuild': 2, 'updateSelection': 1, 'noop': 0})
    # Just opening advanced options panel shouldn't update anything,
    open_advanced_options_panel(selenium)
    verify_first_chart_update_counts(selenium, {
        'update': 3,
        'rebuild': 2,
        'updateSelection': 1,
        'resize': 0,
        'noop': 0
    })

    # Just closing advanced options panel shouldn't update anything.
    close_advanced_options_panel(selenium)
    verify_first_chart_update_counts(selenium, {
        'update': 3,
        'rebuild': 2,
        'updateSelection': 1,
        'resize': 0,
        'noop': 0
    })


def _select_row_and_verify(selenium):
    """
    Selects a single row and verifies it was selected.

    :param selenium: Webdriver
    """
    click_compound_row(selenium, 'CRA-032662')
    verify_selected_scatter_point_count(selenium, 1)
