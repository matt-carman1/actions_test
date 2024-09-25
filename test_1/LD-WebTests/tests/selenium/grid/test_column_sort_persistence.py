import pytest

from helpers.change.grid_column_menu import sort_grid_by
from helpers.change.live_report_picker import open_live_report
from helpers.change.project import open_project
from helpers.selection.grid import GRID_COLUMN_HEADER_SORT_ICON_
from helpers.verification.element import verify_is_visible
from helpers.verification.grid import verify_column_contents

from library.authentication import logout, login

live_report_to_duplicate = {'livereport_name': 'Scatterplot Data', 'livereport_id': '877'}
# {'Lot Date Registered': '29', 'Compound Structure': '1228', 'ID': '1226', 'Rationale': '1229', 'Lot Scientist': '28',
# 'All IDs': '1227', 'Entity ID': '1225', 'Clearance (undefined)': '829', 'My Score (undefined)': '830',
# 'Solubility (undefined)': '831', 'Lot Amount Prepared': '1283', 'Entity Type': '83150'}
# Note: Compound Structure, Rationale, ID, Lot Scientist etc. are some columns that are copied by default.
column_ids_subset = ['829']


@pytest.mark.app_defect(reason="SS-34468")
def test_column_sort_persistence(selenium, duplicate_live_report, open_livereport):
    """
    Test to check persistence of sort order.
        1. Sort a column and verify that the values are sorted
        2. Logout and Login with a different user. 'userC' in this case.
        3. Check the sort order of the LR is same.
        4. Reverse the sort order.
        5. Logout and login with the 'demo' user again.
        6. Verify that the sort order persists.

    :param selenium: Selenium Webdriver
    :param duplicate_live_report: fixture to duplicate LiveReport and returns the LR name.

    """
    livereport_name = duplicate_live_report
    clearance_column = 'Clearance (undefined)'

    # ----- SORT COLUMN BY ASCENDING ORDER AND VALIDATE VALUES ----- #
    sort_grid_by(selenium, clearance_column)
    # verify column values as per sort order
    verify_column_contents(selenium, clearance_column, ['40', '50', '60'])
    # verify column header has the sort icon as per sort order
    verify_is_visible(selenium, GRID_COLUMN_HEADER_SORT_ICON_.format('ASC'))

    logout_relogin_open_livereport(selenium, livereport_name, username='userC', password='userC')

    # ----- VALIDATE SORT ORDER PERSISTENCE AND UPDATE SORT ORDER by DIFFERENT USER ----- #
    verify_is_visible(selenium, GRID_COLUMN_HEADER_SORT_ICON_.format('ASC'))

    # Reversing the sort order
    sort_grid_by(selenium, clearance_column, sort_ascending=False)
    verify_column_contents(selenium, clearance_column, ['60', '50', '40'])

    # verify column header has the sort icon as per sort order
    verify_is_visible(selenium, GRID_COLUMN_HEADER_SORT_ICON_.format('DESC'))

    # ----- VALIDATE SORT ORDER IS UPDATED AND PERSISTS ----- #
    # logging in back with 'demo' user.
    logout_relogin_open_livereport(selenium, livereport_name)
    verify_is_visible(selenium, GRID_COLUMN_HEADER_SORT_ICON_.format('DESC'))


def logout_relogin_open_livereport(selenium, livereport_name, username='demo', password='demo'):
    """
    Logout of LiveDesign and then re-login with the given username and open the mentioned LR.
    :param selenium: Selenium Webdriver
    :param livereport_name: str, name of the LiveReport to open.
    :param username: str, Username to be used for logging into LD.
    :param password: str, password for the username to login.
    """

    logout(selenium)
    login(selenium, uname=username, pword=password)

    # Opens JS testing by default.
    open_project(selenium)

    open_live_report(selenium, name=livereport_name)
