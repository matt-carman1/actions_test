from helpers.flows.live_report_management import duplicate_livereport
from helpers.verification.grid import verify_footer_values

live_report_to_duplicate = {'livereport_name': "5 Fragments 4 Assays", 'livereport_id': '2248'}


def test_duplicate_livereport_without_select_compounds(selenium, duplicate_live_report, open_livereport):
    """
    Test duplicate live report without select compounds
    1. Open duplicate LR dialog and click 'Currently Selected (0)'
    2. Duplicate Livereport with no compounds selected
    3. Verify footer values and column contents in duplicated livereport

    :param selenium: Selenium webdriver
    :param duplicate_live_report: a fixture which duplicates live report
    :param open_livereport: a fixture which opens live report
    """

    # Open duplicate LR dialog and click 'Currently Selected (0)'
    duplicate_livereport(selenium,
                         livereport_name=duplicate_live_report,
                         selected_compounds='',
                         selected_columns=['All'])

    # verify footer values and column contents in duplicated livereport
    verify_footer_values(
        selenium, {
            'row_all_count': '0 Total Compounds',
            'row_selected_count': '0 Selected',
            'column_all_count': '8 Columns',
            'column_hidden_count': '2 Hidden'
        })
