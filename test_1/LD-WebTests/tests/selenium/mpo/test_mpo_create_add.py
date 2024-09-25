"""
Test MPO columns
"""
import pytest

from helpers.change.columns_action import add_column_by_name
from helpers.change.grid_column_menu import open_edit_mpo_window
from helpers.change.grid_columns import get_cell
from helpers.change.mpo_actions import open_mpo_create_window, add_in_live_report_constituent, edit_constituent
from helpers.selection.grid import GRID_FDT_CELL_WRAPPER_1
from helpers.selection.mpo import MPO_OK_BUTTON
from helpers.verification.color import verify_column_color
from helpers.verification.data_and_columns_tree import verify_column_visible_in_column_tree_by_searching
from helpers.verification.grid import verify_column_contents
from helpers.verification.mpo import verify_mpo_tooltip
from library import dom, wait
from library.utils import make_unique_name

# Set LiveReport to duplicate
live_report_to_duplicate = {'livereport_name': '50 Compounds 10 Assays', 'livereport_id': '881'}


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_mpo_create_add(selenium):
    """
    Test creation of MPO column

    :param selenium: Webdriver
    :return:
    """
    # ----- Create a new MPO through button in D&C tree ----- #
    mpo_name = make_unique_name('MPO Name')
    description = 'This is an MPO column.'
    open_mpo_create_window(selenium, mpo_name, description)
    add_in_live_report_constituent(selenium, 'r_glide_XP_GScore (undefined)', 'Higher Better', ['-10', '-9'])
    add_in_live_report_constituent(selenium, 'r_glide_XP_Sitemap (undefined)', 'Lower Better', ['0.1', '0.2'])
    add_in_live_report_constituent(selenium, 'i_i_glide_lignum (undefined)', 'Middle Good',
                                   ['1', '300', '3000', '5000'])
    add_in_live_report_constituent(selenium, 'i_i_glide_XP_nbrot (undefined)', 'Middle Bad', ['1', '3', '7', '9'])
    add_in_live_report_constituent(selenium, 's_glide_best_ensemble (undefined)', 'Categorical (Text)',
                                   [['1uu8'], ['3qd4'], ['3qd3']])
    dom.click_element(selenium, MPO_OK_BUTTON)

    # Indirectly waits for column to start appearing in column-tree
    verify_column_visible_in_column_tree_by_searching(selenium, '(JS Testing) ' + mpo_name, retries=3)

    # Add to LiveReport
    wait.sleep_if_k8s(1)  # Wait so the column appears in the column tree before we search for it
    add_column_by_name(selenium, '(JS Testing) ' + mpo_name)

    # Verify MPO column contents, just the first 5 rows since this LR has 50
    verify_column_contents(selenium,
                           mpo_name, ['0.136', '0.418', '0.106', '0.247', '0.4'],
                           match_length_to_expected=True)
    verify_column_color(selenium,
                        mpo_name,
                        expected_colors=[(255, 69, 0, 1), (255, 213, 0, 1), (254, 53, 0, 1), (255, 125, 0, 1),
                                         (255, 203, 0, 1)],
                        match_length_to_expected=True,
                        child_selector=GRID_FDT_CELL_WRAPPER_1)

    # Verification of the column color pattern for first 5 rows of the constituents
    verify_column_color(selenium,
                        'r_glide_XP_GScore (undefined)',
                        expected_colors=[(255, 3, 0, 1), (255, 9, 0, 1), (255, 11, 0, 1), (255, 15, 0, 1),
                                         (255, 17, 0, 1)],
                        match_length_to_expected=True)
    verify_column_color(selenium,
                        'r_glide_XP_Sitemap (undefined)',
                        expected_colors=[(7, 255, 0, 1), (0, 255, 0, 1), (255, 0, 0, 1), (0, 255, 0, 1),
                                         (2, 255, 0, 1)],
                        match_length_to_expected=True)
    verify_column_color(selenium,
                        'i_i_glide_lignum (undefined)',
                        expected_colors=[(5, 255, 0, 1), (9, 255, 0, 1), (49, 255, 0, 1), (198, 255, 0, 1),
                                         (164, 255, 0, 1)],
                        match_length_to_expected=True)
    verify_column_color(selenium,
                        'i_i_glide_XP_nbrot (undefined)',
                        expected_colors=[(255, 7, 0, 1), (101, 255, 0, 1), (255, 255, 0, 1), (255, 255, 0, 1),
                                         (255, 255, 0, 1)],
                        match_length_to_expected=True)
    verify_column_color(selenium,
                        's_glide_best_ensemble (undefined)',
                        expected_colors=[(255, 255, 0, 1), (50, 255, 0, 1), (50, 255, 0, 1), (255, 51, 0, 1),
                                         (50, 255, 0, 1)],
                        match_length_to_expected=True)

    # Verify MPO tooltip
    expected_tooltip_values = {
        'r_glide_XP_GScore (undefined)': '-11.33',
        'r_glide_XP_Sitemap (undefined)': '-0.00246',
        'i_i_glide_lignum (undefined)': '787',
        'i_i_glide_XP_nbrot (undefined)': '5',
        's_glide_best_ensemble (undefined)': '3qd4',
    }
    expected_tooltip_colors = {
        'r_glide_XP_GScore (undefined)': (255, 3, 0, 1),
        'r_glide_XP_Sitemap (undefined)': (7, 255, 0, 1),
        'i_i_glide_lignum (undefined)': (5, 255, 0, 1),
        'i_i_glide_XP_nbrot (undefined)': (255, 7, 0, 1),
        's_glide_best_ensemble (undefined)': (255, 255, 0, 1),
    }
    verify_mpo_tooltip(selenium, 'CRA-035507', mpo_name, expected_tooltip_values, expected_tooltip_colors)

    # Edit MPO settings and re-verify
    open_edit_mpo_window(selenium, mpo_name)
    edit_constituent(selenium, 'i_i_glide_lignum (undefined)', 'Middle Bad', ['1', '300', '3000', '5000'])
    dom.click_element(selenium, MPO_OK_BUTTON)

    # Wait until MPO changes have flowed through
    def is_value_changed(selenium):
        cell = get_cell(selenium, 'CRA-035507', mpo_name)
        return cell.text != '0.136'

    dom.wait_until(selenium, is_value_changed)

    verify_column_color(selenium,
                        'i_i_glide_lignum (undefined)',
                        expected_colors=[(255, 5, 0, 1), (255, 9, 0, 1), (255, 49, 0, 1), (255, 198, 0, 1),
                                         (255, 164, 0, 1)],
                        match_length_to_expected=True)

    # Verify MPO column contents
    verify_column_contents(selenium,
                           mpo_name, ['0.056', '0.189', '0.068', '0.225', '0.344'],
                           match_length_to_expected=True)
    verify_column_color(selenium,
                        mpo_name,
                        expected_colors=[(255, 28, 0, 1), (255, 96, 0, 1), (255, 34, 0, 1), (255, 114, 0, 1),
                                         (255, 175, 0, 1)],
                        match_length_to_expected=True,
                        child_selector=GRID_FDT_CELL_WRAPPER_1)
