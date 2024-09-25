"""
Selenium test for testing the persistence of hidden columns(QA-3491)
"""
import pytest

from helpers.change.live_report_picker import open_live_report
from helpers.flows.grid import hide_columns_selectively
from helpers.change.footer_actions import show_hidden_columns
from helpers.change.project import open_project
from helpers.verification.grid import verify_footer_values, verify_columns_not_visible
from library.authentication import login, logout

live_report_to_duplicate = {'livereport_name': '5 Compounds 4 Assays', 'livereport_id': '882'}


@pytest.mark.smoke
def test_hide_columns_persistence(selenium, duplicate_live_report, open_livereport):
    """
    Test hiding columns and testing its persistence.

    :param selenium: Selenium WebDriver
    """
    # Select two columns using ctrl key and hide them
    hide_columns_selectively(selenium, 'Lot Scientist', 'Clearance (undefined)')
    verify_footer_values(selenium, {'column_all_count': '6 Columns', 'column_hidden_count': '4 Hidden'})
    verify_columns_not_visible(selenium, ['Lot Scientist', 'Clearance (undefined)'])

    # Refreshes the browser and verify that the hidden columns are still hidden
    selenium.refresh()
    verify_footer_values(selenium, {'column_all_count': '6 Columns', 'column_hidden_count': '4 Hidden'})
    verify_columns_not_visible(selenium, ['Lot Scientist', 'Clearance (undefined)'])

    # Logs out, logs back in and then reopens the LiveReports and verifies that the columns remain hidden.
    logout(selenium)
    login(selenium, uname='demo', pword='demo')
    open_project(selenium, project_name='JS Testing')
    open_live_report(selenium, duplicate_live_report)
    verify_footer_values(selenium, {'column_all_count': '6 Columns', 'column_hidden_count': '4 Hidden'})
    verify_columns_not_visible(selenium, ['Lot Scientist', 'Clearance (undefined)'])

    # Shows all 4 hidden columns and verifies them in the LR
    show_hidden_columns(selenium, 4)
    verify_footer_values(selenium, {'column_all_count': '10 Columns'})
