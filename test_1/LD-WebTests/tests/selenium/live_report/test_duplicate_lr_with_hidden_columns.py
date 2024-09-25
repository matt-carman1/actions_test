import pytest

from helpers.change.grid_column_menu import hide_column
from helpers.flows.live_report_management import duplicate_livereport
from helpers.selection.grid import GRID_HEADER_CELL, Footer
from helpers.verification.element import verify_is_visible
from helpers.verification.grid import verify_footer_values, verify_columns_not_visible

# Live report with 5 compounds, 4 Columns and 4 Hidden columns
live_report_to_duplicate = {'livereport_name': 'Test Date Assay Column', 'livereport_id': '2699'}


@pytest.mark.smoke
def test_duplicate_lr_with_hidden_columns(selenium, duplicate_live_report, open_livereport):
    """
    Test to duplicate live report with Hidden columns selected

    1. Duplicate livereport selecting 1 hidden column and 1 visible column
    2. Verify one column is in hidden state and verify footer values in duplicated livereport

    :param selenium: Selenium webdriver
    :param duplicate_live_report: fixture that duplicates live report
    :param open_livereport: a fixture which opens livereport
    """
    hide_column(selenium, 'Test Dates Assay (value)')
    # ----- Duplicate livereport selecting 1 hidden column and 1 visible column ----- #
    # duplicate live report with 1 hidden column and 1 normal column (Test Dates Assay (value) is hidden column here)
    duplicate_livereport(selenium,
                         livereport_name=duplicate_live_report,
                         selected_columns=['Test Dates Assay (value)', 'Test Dates Assay (date)'])

    # ----- Verify one column is in hidden state and verify footer values in duplicated livereport ----- #
    # verify footer values
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(4),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(3),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(5),
            Footer.ROW_SELECTED_COUNT_KEY: Footer.ROW_SELECTED_COUNT_VALUE.format(0)
        })
    # verify Test Dates Assay (value) column is in hidden state
    verify_columns_not_visible(selenium, ['Test Dates Assay (value)'])
    # verify 'Test Dates Assay (date)' is in non hidden mode
    verify_is_visible(selenium, GRID_HEADER_CELL, 'Test Dates Assay (date)')
