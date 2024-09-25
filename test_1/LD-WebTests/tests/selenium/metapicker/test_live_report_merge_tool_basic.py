import pytest

from helpers.change.grid_column_menu import sort_grid_by
from helpers.change.live_report_picker import merge_live_reports
from helpers.selection.grid import Footer
from helpers.selection.live_report_tab import TAB_ACTIVE
from helpers.verification.grid import verify_column_contents, verify_footer_values
from library import wait

first_lreport = "4 Compounds 3 Formulas"
second_lreport = "2 Compounds 2 Freeform Column"


@pytest.mark.smoke
@pytest.mark.parametrize("first_lreport, second_lreport, lr_merge_type, col_name, expected_footer_content, "
                         "expected_id_col_content",
                         ((first_lreport, second_lreport, "Union", 'ID', {
                             Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(4),
                             Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(13),
                             Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(2)
                         }, ['V035624', 'V035625', 'V035626', 'V035627']),
                          (first_lreport, second_lreport, "Intersection", 'ID', {
                              Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(2),
                              Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(13),
                              Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(2)
                          }, ['V035624', 'V035625']), (first_lreport, second_lreport, "Difference", 'ID', {
                              Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(2),
                              Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(13),
                              Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(2)
                          }, ['V035626', 'V035627'])))
@pytest.mark.usefixtures("open_project")
def test_live_report_merge_tool_basic(selenium, first_lreport, second_lreport, lr_merge_type, col_name,
                                      expected_footer_content, expected_id_col_content):
    """
    Merge Two LiveReports keeping the reference LiveReport constant by:
    1. Union - Brings all compounds in from both the LR
    2. Intersection - Only compounds that are common to both LRs
    3. Difference - Compounds in reference LR but not in other LR.

    :param: Selenium Webdriver
    :param first_lreport: first_live_report_name from parametrize data
    :type first_lreport: str
    :param second_lreport: second_live_report_name from parametrize data
    :type second_lreport: str
    :param lr_merge_type: merge types(Union, Intersection & Difference)
    :type lr_merge_type: str
    :param col_name: column name
    :type col_name: str
    :param expected_footer_content: expected footer values
    :type expected_footer_content: dict
    :param expected_id_col_content: expected compounds
    :type expected_id_col_content: list
    """
    # ----- MERGE LIVEREPORTS BY UNION, INTERSECTION & DIFFERENCE ----- #
    merge_type_name = merge_live_reports(selenium,
                                         first_lreport,
                                         second_lreport,
                                         reference_live_report=1,
                                         merge_type=lr_merge_type)
    wait.until_visible(selenium, TAB_ACTIVE, merge_type_name)

    # sort the merged LR by ID to maintain order for verify_column_content
    sort_grid_by(selenium, column_name=col_name)

    # Check the number of compounds and columns
    verify_footer_values(selenium, expected_footer_content)
    verify_column_contents(selenium, column_name=col_name, expected_content=expected_id_col_content)