import time
import pytest

from helpers.change.grid_row_actions import select_rows
from helpers.selection.live_report_tab import TAB_ACTIVE
from helpers.flows.live_report_management import duplicate_livereport
from helpers.verification.element import verify_is_visible
from helpers.verification.grid import verify_column_contents, verify_visible_columns_in_live_report

test_livereport = '4 Compounds 3 Formulas'


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("open_project")
def test_duplicate_livereport_subset(selenium):
    """
    Test to check the working of duplicate livereport helper that has option to duplicate the subset of an LR.
    """
    # Selecting compounds in the LR
    select_rows(selenium, list_of_entity_ids=['V035624'])

    copied_lr = duplicate_livereport(selenium,
                                     livereport_name='4 Compounds 3 Formulas',
                                     selected_compounds='1',
                                     selected_columns=['substructureSearch'])
    time.sleep(2)
    verify_is_visible(selenium, selector=TAB_ACTIVE, selector_text=copied_lr)
    verify_visible_columns_in_live_report(
        selenium, ['Compound Structure', 'ID', 'Rationale', 'Lot Scientist', 'substructureSearch'])
    verify_column_contents(selenium, column_name='ID', expected_content=['V035624'])
