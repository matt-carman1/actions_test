"""
Test Weighted MPOs
"""
import pytest

from helpers.change.columns_action import add_column_by_name
from helpers.change.grid_column_menu import open_edit_mpo_window
from helpers.change.mpo_actions import open_mpo_create_window, add_in_live_report_constituent, add_constituent_weight
from helpers.flows.grid import hide_columns_contiguously
from helpers.selection.grid import GRID_FDT_CELL_WRAPPER_1
from helpers.selection.mpo import MPO_OK_BUTTON
from helpers.verification.color import verify_column_color
from helpers.verification.data_and_columns_tree import verify_column_visible_in_column_tree_by_searching
from helpers.verification.grid import verify_column_contents
from library import dom
from library.utils import make_unique_name, is_k8s

# Set LiveReport to duplicate
live_report_to_duplicate = {'livereport_name': '5 Compounds 4 Assays', 'livereport_id': '882'}


@pytest.mark.xfail(not is_k8s(), reason="SS-40265: RMQ issues in Old Jenkins")
@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_weighted_mpo(selenium):
    """
    Test Weighted MPOs
    This test simulates creating, adding, and updating a weighted MPO.
    This covers interacting with the MPO dialog, and verifying column colors and column contents.

    :param selenium: Webdriver
    :return:
    """
    # ----- Hide columns not used ----- #
    hide_columns_contiguously(selenium, 'ID', 'Lot Scientist')

    # ----- Create and add new MPO through button in D&C tree ----- #
    mpo_name = make_unique_name('MPO Name')
    first_column_name = 'CYP450 2C19-LCMS (%INH)'
    second_column_name = 'STABILITY-PB-PH 7.4 (%Rem@2hr)'
    open_mpo_create_window(selenium, mpo_name)
    add_in_live_report_constituent(selenium, first_column_name, 'Middle Good', ['5', '15', '50', '100'])
    add_in_live_report_constituent(selenium, second_column_name, 'Higher Better', ['60', '100'])
    add_constituent_weight(selenium, first_column_name, 5)
    dom.click_element(selenium, MPO_OK_BUTTON)

    # Indirectly waits for column to start appearing in column-tree
    verify_column_visible_in_column_tree_by_searching(selenium, '(JS Testing) ' + mpo_name, retries=3)

    add_column_by_name(selenium, '(JS Testing) ' + mpo_name)

    # ----- MPO Verification ----- #
    # Verify addition of weights is reflected in value of each cell in the MPO column
    verify_column_contents(selenium, mpo_name, expected_content=['0.491', '0.66', '0.52', '0.669', '0.648'])
    # Verify addition of weights to 1st constituent column is reflected in color of MPO column's first cell
    verify_column_color(selenium,
                        mpo_name,
                        expected_colors=[(255, 250, 0, 1)],
                        match_length_to_expected=True,
                        child_selector=GRID_FDT_CELL_WRAPPER_1)
    # Add weight to second constituent column and re-verify MPO
    open_edit_mpo_window(selenium, mpo_name)
    add_constituent_weight(selenium, second_column_name, 5)
    dom.click_element(selenium, MPO_OK_BUTTON)
    # Verify addition of weights is reflected in value of each cell in the MPO column
    verify_column_contents(selenium, mpo_name, expected_content=['0.473', '0.713', '0.564', '0.404', '0.648'])
    # Verify addition of weights to 2nd constituent column is reflected in color of MPO column's first cell
    verify_column_color(selenium,
                        mpo_name,
                        expected_colors=[(255, 241, 0, 1)],
                        match_length_to_expected=True,
                        child_selector=GRID_FDT_CELL_WRAPPER_1)
