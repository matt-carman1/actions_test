import pytest

from helpers.change import grid_column_menu
from helpers.change import filter_actions
from helpers.change.actions_pane import open_visualize_panel, close_filter_panel, open_filter_panel
from helpers.change.grid_column_menu import sort_grid_by
from helpers.change.grid_columns import click_compound_row
from helpers.change.plots import add_heatmap_column, set_tooltip_mode
from helpers.change.filter_actions import type_and_select_filter_item
from helpers.selection.coloring_rules import COLOR_WINDOW_OK_BUTTON
from helpers.selection.filter_actions import BOX_WIDGET_BODY_CATEGORY
from helpers.selection.grid import Footer
from helpers.selection.plots import VISUALIZATION_HEATMAP
from helpers.verification.grid import verify_footer_values
from helpers.verification.plots import verify_heatmap_cell_count, verify_selected_heatmap_cell_count, \
    verify_heatmap_column_headers, verify_heatmap_row_headers, verify_heatmap_cell_colors, \
    verify_heatmap_column_count, verify_heatmap_row_count, verify_first_chart_update_counts
from library import dom, wait

live_report_to_duplicate = {'livereport_name': '5 Compounds 4 Assays', 'livereport_id': '882'}


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_heatmap_plot(selenium):
    """
    Test heatmap plot:

    1. Open a new heatmap plot.
    2. Adding columns from the LR to the heatmap and confirm we have the right number of cells and columns
    3. Applying color schemes, confirming that the colors appear correctly in the heatmap.
    4. Sorting, confirming that the heatmap sorts in the same way as the LR table.
    5. Filtering, confirming that the heatmap is filtered accordingly.
    6. Selection, confirming that the heatmap cells are correctly highlighted for the selected LR rows.

    While this test is performed out we check for the expected number of updates to the chart after carrying out the
    various operations.

    :param selenium: selenium Webdriver
    """

    # Color a column.
    grid_column_menu.open_coloring_rules(selenium, 'Clearance (undefined)')
    dom.click_element(selenium, COLOR_WINDOW_OK_BUTTON)

    # Create a new heatmap.
    open_visualize_panel(selenium)
    dom.click_element(selenium, VISUALIZATION_HEATMAP)

    # Disable tooltips.
    set_tooltip_mode(selenium, 'none')

    # Add a couple of columns.
    add_heatmap_column(selenium, 'Clearance (undefined)')
    add_heatmap_column(selenium, 'CYP450 2C19-LCMS (%INH)')

    # Check we have the correct contents in heatmap.
    verify_heatmap_row_count(selenium, 5)
    verify_heatmap_column_count(selenium, 2)
    verify_heatmap_cell_count(selenium, 10)
    verify_heatmap_column_headers(selenium, ['Clearance (undefined)', 'CYP450 2C19-LCMS (%INH)'])
    verify_heatmap_row_headers(selenium, ['V055843', 'CRA-032913', 'CRA-032703', 'CRA-032664', 'CRA-032662'])
    verify_first_chart_update_counts(selenium, {
        'update': {
            'max': 3
        },
        'rebuild': {
            'max': 3
        },
        'resize': 0,
        'noop': 0,
        'updateSelection': 0
    })

    # Verify the colors in the cells are correct. The cells in the heatmap are ID'd by row ID and column ID.
    # We have cells are identified by a string including the compound ID and the column ID.
    # NOTE (ext_glysade_watson) The colors are different on > 8.7.x as the default min color was changed.
    # NOTE: SS-33107: After highcharts upgrade, highcharts is not setting id attribute to heatmap cell
    # verify_heatmap_cell_colors(selenium, [
    #     {'compound_id': 'V055843', 'column_id': '829', 'color': (255, 0, 0, 1)},
    #     {'compound_id': 'CRA-032913', 'column_id': '829', 'color': (244, 49, 49, 1)},
    #     {'compound_id': 'CRA-032703', 'column_id': '829', 'color': (215, 189, 189, 1)},
    #     {'compound_id': 'CRA-032664', 'column_id': '829', 'color': (213, 196, 196, 1)},
    #     {'compound_id': 'CRA-032662', 'column_id': '829', 'color': (211, 211, 211, 1)},
    # ])

    # Sort the table by the compound ID (descending) and check the y-axis headers are in the right order.
    sort_grid_by(selenium, 'ID', False)
    wait.until_live_report_loading_mask_not_visible(selenium)

    verify_heatmap_row_headers(selenium, ['CRA-032662', 'CRA-032664', 'CRA-032703', 'CRA-032913', 'V055843'])
    verify_first_chart_update_counts(selenium, {
        'update': {
            'max': 4
        },
        'rebuild': {
            'max': 4
        },
        'resize': 0,
        'noop': 0,
        'updateSelection': 0
    })

    # Filter the grid.
    open_filter_panel(selenium)
    filter_actions.add_filter(selenium, 'ID')
    ids_filter_element = filter_actions.get_filter(selenium, 'ID', filter_position=3)
    wait.until_visible(ids_filter_element, BOX_WIDGET_BODY_CATEGORY)
    type_and_select_filter_item(ids_filter_element, 'CRA-032662')
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(5),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(1)
        })

    verify_first_chart_update_counts(selenium, {
        'update': {
            'max': 6
        },
        'rebuild': {
            'max': 6
        },
        'resize': 0,
        'noop': 0,
        'updateSelection': 0
    })
    close_filter_panel(selenium)

    # Verify we have the right number of rows in the heatmap and they are in the right order.
    verify_heatmap_row_count(selenium, 1)
    verify_heatmap_row_headers(selenium, ['CRA-032662'])

    # Select something and check we have the corresponding cells selected in the heatmap.
    click_compound_row(selenium, 'CRA-032662')
    verify_first_chart_update_counts(selenium, {
        'update': {
            'max': 7
        },
        'rebuild': {
            'max': 6
        },
        'resize': 0,
        'noop': 0,
        'updateSelection': 1
    })
    verify_selected_heatmap_cell_count(selenium, 2)
