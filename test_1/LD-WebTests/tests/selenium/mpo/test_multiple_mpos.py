"""

Testing multiple MPOs in a LR

"""
import pytest

from helpers.change.columns_action import add_column_by_name
from helpers.change.grid_column_menu import open_edit_mpo_window
from helpers.change.mpo_actions import open_mpo_create_window, add_in_live_report_constituent
from helpers.selection.grid import GRID_FDT_CELL_WRAPPER_1
from helpers.selection.mpo import MPO_OK_BUTTON
from helpers.verification.grid import verify_column_contents
from helpers.verification.color import verify_column_color
from helpers.selection.mpo import MPO_CONSTITUENT_BUTTON, MPO_DELETE_CONSTITUENT
from helpers.verification.mpo import verify_mpo_tooltip
from library import dom, simulate

from library.utils import make_unique_name

# Set LiveReport to duplicate
live_report_to_duplicate = {'livereport_name': '4 Compounds 3 Formulas', 'livereport_id': '890'}


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
@pytest.mark.flaky(reason="LDIDEAS-6690")
def test_multiple_mpos(selenium):
    """
    Test creation and addition of multiple MPOs in an LR

    :param selenium: Selenium Webdriver
    :return:
    """
    mpo_one = {
        "name": make_unique_name('MPO Name'),
        "expected_colors": [(177, 255, 0, 1), (255, 107, 0, 1), (255, 181, 0, 1), (255, 198, 0, 1)],
        "expected_column_contents": ['0.651', '0.211', '0.357', '0.389'],
        "constituent": "A1 (undefined)",
        "mpo_distribution": "Higher Better",
        "mpo_distribution_values": ['20', '100'],
        "expected_tooltip_values": {
            'A1 (undefined)': '78'
        },
        "expected_tooltip_colors": {
            'A1 (undefined)': (177, 255, 0, 1)
        }
    }
    mpo_two = {
        "name": make_unique_name('Second MPO'),
        "expected_colors": [(255, 206, 0, 1), (81, 255, 0, 1), (255, 219, 0, 1), (254, 113, 0, 1)],
        "expected_column_contents": ['0.406', '0.841', '0.431', '0.223'],
        "constituent": "A2 (undefined)",
        "mpo_distribution": "Lower Better",
        "mpo_distribution_values": ['20', '100']
    }

    # ----- Create a new MPO through button in D&C tree ----- #

    description = 'This is an MPO column.'
    open_mpo_create_window(selenium, mpo_one["name"], description)
    add_in_live_report_constituent(selenium, mpo_one["constituent"], mpo_one["mpo_distribution"],
                                   mpo_one["mpo_distribution_values"])
    dom.click_element(selenium, MPO_OK_BUTTON)

    # Add MPO to LiveReport
    add_column_by_name(selenium, '(JS Testing) ' + mpo_one["name"])

    # Verify MPO column contents, for all the 4 rows in the LR
    verify_column_contents(selenium,
                           mpo_one["name"],
                           mpo_one["expected_column_contents"],
                           match_length_to_expected=True)
    # Verify color of both the MPO column and the constituent column are as expected
    verify_column_color(selenium,
                        mpo_one["name"],
                        mpo_one["expected_colors"],
                        match_length_to_expected=True,
                        child_selector=GRID_FDT_CELL_WRAPPER_1)
    verify_column_color(selenium, mpo_one["constituent"], mpo_one["expected_colors"], match_length_to_expected=True)

    # ------- Create a second MPO depending on another column now -------- #
    description = 'This is a second MPO column.'
    open_mpo_create_window(selenium, mpo_two["name"], description)
    add_in_live_report_constituent(selenium, mpo_two["constituent"], mpo_two["mpo_distribution"],
                                   mpo_two["mpo_distribution_values"])
    dom.click_element(selenium, MPO_OK_BUTTON)

    # Add second MPO to LiveReport
    add_column_by_name(selenium, '(JS Testing) ' + mpo_two["name"])

    # Verify MPO column contents, for all the 4 rows in the LR
    verify_column_contents(selenium,
                           mpo_two["name"],
                           mpo_two["expected_column_contents"],
                           match_length_to_expected=True)

    # Verify color of both the MPO column and the constituent column are as expected
    verify_column_color(selenium,
                        mpo_two["name"],
                        mpo_two["expected_colors"],
                        match_length_to_expected=True,
                        child_selector=GRID_FDT_CELL_WRAPPER_1)
    verify_column_color(selenium, mpo_two["constituent"], mpo_two["expected_colors"], match_length_to_expected=True)

    # Edit MPO Constituent for the second MPO by removing the existing constituent and adding the same constituent
    # as the first MPO

    open_edit_mpo_window(selenium, mpo_two["name"])
    get_mpo_constituent_element = dom.get_element(selenium, MPO_CONSTITUENT_BUTTON, text='A2 (undefined)')
    simulate.hover(selenium, get_mpo_constituent_element)
    dom.click_element(selenium, MPO_DELETE_CONSTITUENT)
    add_in_live_report_constituent(selenium, mpo_one["constituent"], mpo_one["mpo_distribution"],
                                   mpo_one["mpo_distribution_values"])
    dom.click_element(selenium, MPO_OK_BUTTON)

    # Verify MPO contents and color after editing
    verify_column_contents(selenium,
                           mpo_two["name"],
                           mpo_one["expected_column_contents"],
                           match_length_to_expected=True)
    verify_column_color(selenium,
                        mpo_two["name"],
                        mpo_one["expected_colors"],
                        match_length_to_expected=True,
                        child_selector=GRID_FDT_CELL_WRAPPER_1)

    # --------- Verify tooltip for both the MPO and ensure the values and color are as expected -------- #
    verify_mpo_tooltip(selenium, 'V035624', mpo_one["name"], mpo_one["expected_tooltip_values"],
                       mpo_one["expected_tooltip_colors"])
    verify_mpo_tooltip(selenium, 'V035624', mpo_two["name"], mpo_one["expected_tooltip_values"],
                       mpo_one["expected_tooltip_colors"])
