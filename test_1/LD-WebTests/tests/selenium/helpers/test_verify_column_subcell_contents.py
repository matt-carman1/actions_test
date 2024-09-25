# Set LiveReport to duplicate
import pytest

from helpers.change import actions_pane
from helpers.verification.grid import verify_column_subcell_contents

live_report_to_duplicate = {'livereport_name': 'Compound Lot Salt', 'livereport_id': '1701'}


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_verify_column_subcell_contents(selenium):
    """
    Test creation, cell selection, and editing of unpublished picklist text type freeform column.

    :param selenium: Webdriver
    :return:
    """
    actions_pane.toggle_lr_mode(selenium, row_per_mode='Compound')

    verify_column_subcell_contents(selenium, 'Lot Number', [['V2', 'V1', 'C2'], ['V1', 'C2']])
