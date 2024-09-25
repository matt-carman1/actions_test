from helpers.change.grid_row_actions import select_rows
from helpers.flows.live_report_management import duplicate_livereport
from helpers.selection.grid import Footer
from helpers.verification.grid import verify_footer_values, verify_column_contents

live_report_to_duplicate = {'livereport_name': "5 Fragments 4 Assays", 'livereport_id': '2248'}


def test_duplicate_livereport_with_selected_compounds(selenium, duplicate_live_report, open_livereport):
    """
    Test duplicate live report with selected compounds
    1. Select compounds
    2. Duplicate Livereport with selected compounds
    3. Verify footer values and column contents in duplicated livereport

    :param selenium: Selenium webdriver
    :param duplicate_live_report: a fixture which duplicates live report
    :param open_livereport: a fixture which opens live report
    """
    compound_ids_to_duplicate = ['R055831', 'R055833']
    # select compounds
    select_rows(selenium, compound_ids_to_duplicate)

    # Duplicating livereport with selected compounds
    duplicate_livereport(selenium, livereport_name=duplicate_live_report, selected_compounds=compound_ids_to_duplicate)

    # verify footer values and column contents in duplicated livereport
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(len(compound_ids_to_duplicate)),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(8),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(len(compound_ids_to_duplicate)),
            Footer.ROW_SELECTED_COUNT_KEY: Footer.ROW_SELECTED_COUNT_VALUE.format(0)
        })
    verify_column_contents(selenium, 'ID', compound_ids_to_duplicate)
