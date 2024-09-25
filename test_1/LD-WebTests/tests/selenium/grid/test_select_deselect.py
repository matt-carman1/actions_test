"""
Selenium test for selecting and deselecting all rows in an LR
"""

import pytest

from library import dom
from helpers.change.grid_row_actions import select_all_rows
from helpers.verification.grid import verify_footer_values
from helpers.selection.grid import GRID_ALL_ROWS_CHECKBOX_INPUT, GRID_ROW_CHECKBOX_INPUT, Footer

live_report_to_duplicate = {'livereport_name': '2 Compounds 2 Freeform Column', 'livereport_id': '891'}


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_select_deselect_rows(selenium):
    """
     Test for selecting and deselecting all rows in an LR
     :param selenium: Selenium WebDriver
     """
    # ------- Selecting all rows of the LR and verify it ------- #
    select_all_rows(selenium)

    # Performing three-fold verification
    # Verify the footer value
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(2),
            Footer.ROW_SELECTED_COUNT_KEY: Footer.ROW_SELECTED_COUNT_VALUE.format(2)
        })

    # Verify that the checkbox for all compounds are selected
    select_all_checkbox = dom.get_element(selenium, GRID_ALL_ROWS_CHECKBOX_INPUT, must_be_visible=False)
    assert select_all_checkbox.is_selected(), "The checkbox with selector {} for both compounds are not " \
                                              "selected".format(GRID_ALL_ROWS_CHECKBOX_INPUT)

    # Verify that each of the rows are selected
    select_row_one = dom.get_element(selenium, GRID_ROW_CHECKBOX_INPUT.format('V035624'), must_be_visible=False)
    select_row_two = dom.get_element(selenium, GRID_ROW_CHECKBOX_INPUT.format('V035625'), must_be_visible=False)

    assert select_row_one.is_selected(), "The checkbox with selector {} for compound {} is not selected"\
                                            .format(GRID_ROW_CHECKBOX_INPUT.format('V035624'), "V035624")
    assert select_row_two.is_selected(), "The checkbox with selector {} for compound {} is not selected"\
                                            .format(GRID_ROW_CHECKBOX_INPUT.format('V035625'), "V035625")

    # ------- Deselecting all rows of the LR and verify it ------- #
    select_all_rows(selenium)

    # Three fold verification
    # Verify the footer value
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(2),
            Footer.ROW_SELECTED_COUNT_KEY: Footer.ROW_SELECTED_COUNT_VALUE.format(0)
        })

    # Verify that the checkbox for all compounds are selected
    assert not select_all_checkbox.is_selected(), "The checkbox selector {} for both compounds is selected"\
                                                    .format(GRID_ALL_ROWS_CHECKBOX_INPUT)

    # Verify that each of the rows are not selected
    assert not select_row_one.is_selected(), "The checkbox selector {} for compound {} is selected " \
                                                .format(GRID_ROW_CHECKBOX_INPUT.format('V035624'), "V035624")
    assert not select_row_two.is_selected(), "The checkbox selector {} for compound {} is selected"\
                                                .format(GRID_ROW_CHECKBOX_INPUT.format('V035625'), 'V035625')
