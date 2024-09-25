import pytest

from helpers.change.columns_action import add_column_by_name
from helpers.change.mpo_actions import remove_constituent, clone_mpo
from helpers.selection.mpo import MPO_NAME_FIELD, MPO_GENERAL_SETTINGS_FORM, MPO_OK_BUTTON
from helpers.verification.data_and_columns_tree import verify_visible_columns_from_column_mgmt_ui, \
    verify_column_visible_in_column_tree_by_searching
from library import dom, wait
from library.utils import make_unique_name

live_report_to_duplicate = {'livereport_name': '4 Compounds 3 Formulas', 'livereport_id': '890'}

# Columns being copied: ID, "A1 (undefined)", "A3 (undefined)"
column_ids_subset = ['1226', '36', '813']


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_mpo_cloning(selenium):
    """
    Test to clone an existing MPO
    1. Clone a n existing MPO.
    2. Add it to the LR.
    3. Check it is added to the LR along with Desirability score without issues.

    :param selenium: Selenium Webdriver
    """

    # MPO to be cloned
    parent_mpo = "(JS Testing) (Global) Mixed A1 - A5"

    # ----- CLONING THE MPO ----- #
    clone_mpo(selenium, mpo_to_clone=parent_mpo)

    mpo_name = make_unique_name('MPO_Name')
    # Ensure that the Clone MPO window is open before choosing settings (This is necessary because the opening of the
    # window is slow and sometimes it is not ready when choose_ffc_settings() starts running.)
    wait.until_visible(selenium, MPO_GENERAL_SETTINGS_FORM)

    # Set MPO name
    dom.set_element_value(selenium, MPO_NAME_FIELD, mpo_name)

    # Remove some of the MPO Constituents
    remove_constituent(selenium, 'A2 (undefined)')
    remove_constituent(selenium, 'A4 (undefined)')
    remove_constituent(selenium, 'A5 (undefined)')

    # Finally save the MPO
    dom.click_element(selenium, MPO_OK_BUTTON)

    # Indirectly waits for column to start appearing in column-tree
    verify_column_visible_in_column_tree_by_searching(selenium, "(JS Testing) {}".format(mpo_name), retries=3)

    # Adding MPO to the LR.
    add_column_by_name(selenium, "(JS Testing) {}".format(mpo_name))

    # Verify that the MPO and Desirability Score group is added to the LR.
    verify_visible_columns_from_column_mgmt_ui(selenium, [
        'ID', 'Rationale', 'Lot Scientist', 'A1 (undefined)', 'A3 (undefined)', mpo_name,
        '{} Desirability Scores and Number of Missing Inputs'.format(mpo_name), 'A1 (undefined) Desirability',
        'A3 (undefined) Desirability', 'Number of missing inputs'
    ])
