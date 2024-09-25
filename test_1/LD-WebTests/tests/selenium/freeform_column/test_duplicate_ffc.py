import pytest

from helpers.change.actions_pane import close_add_data_panel
from helpers.change.freeform_column_action import create_ffc, edit_ffc_cell
from helpers.change.grid_column_menu import hide_column
from helpers.change.live_report_menu import delete_open_live_report
from helpers.flows.live_report_management import copy_active_live_report
from helpers.verification.grid import verify_column_contents
from library import wait

# Set LiveReport to duplicate
live_report_to_duplicate = {'livereport_name': 'FFC', 'livereport_id': '1250'}


# NOTE (tchoi) V035624 is used in other tests and we think this test overwrites their expected values
def test_duplicate_ffc(selenium, duplicate_live_report, open_livereport):
    """
    Tests duplication of published and unpublished text FFCs.

    Verifies both published and unpublished text FFCs:
        1. can be edited and
        2. appears and retains edited values in a duplicated LR

    Uniquely verify an unpublished text FFC:
        1. can have different values on different LRs for the same structure

    Uniquely verify a published text FFC:
        1. shows the same text for a structure on every LR, regardless of which LR is used to edit

    :param selenium: Selenium Webdriver
    :param duplicate_live_report: passing the fixture 'duplicate_live_report' as the argument to duplicate a custom LR
    :return:
    """
    create_ffc(selenium, 'Unpublished FFC', 'unpublished freeform column')
    close_add_data_panel(selenium)

    # open up space to avoid horizontal scrolling
    hide_column(selenium, 'Lot Scientist')
    hide_column(selenium, 'Rationale')

    # set FFC values
    edit_ffc_cell(selenium, 'Published Freeform Text Column', 'V035624', 'original public')
    edit_ffc_cell(selenium, 'Unpublished FFC', 'V035624', 'original secret')

    # duplicate the LR (without closing it)
    duplicate_live_report_2 = copy_active_live_report(selenium, duplicate_live_report, 'Freeform Test Copy')

    # values for both FFC columns copy over to new LR
    verify_column_contents(selenium, 'Published Freeform Text Column', ['original public', 'Sample Data 2'])
    verify_column_contents(selenium, 'Unpublished FFC', ['original secret', ''])

    # alter values in Freeform Test Copy
    edit_ffc_cell(selenium, 'Published Freeform Text Column', 'V035624', 'revised public')
    edit_ffc_cell(selenium, 'Unpublished FFC', 'V035624', 'revised secret')

    # delete the duplicate LR to return to original LR
    delete_open_live_report(selenium, duplicate_live_report_2)
    wait.until_live_report_loading_mask_not_visible(selenium)

    # verify only the published FFC value has changed in the original LR
    verify_column_contents(selenium, 'Published Freeform Text Column', ['revised public', 'Sample Data 2'])
    verify_column_contents(selenium, 'Unpublished FFC', ['original secret', ''])

    # return published FFC to initial value (out of courtesy)
    edit_ffc_cell(selenium, 'Published Freeform Text Column', 'V035624', 'Sample Published Text')
