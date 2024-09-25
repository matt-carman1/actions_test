import pytest

from helpers.change.grid_row_actions import select_multiple_rows, select_all_rows
from helpers.flows.grid import choose_row_selection_type_and_verify_footer
from helpers.selection.grid import GRID_ALL_ROWS_CHECKBOX_INPUT, Footer
from helpers.verification.grid import verify_footer_values, verify_selected_row_ids
from library import dom

live_report_to_duplicate = {'livereport_name': 'Test Reactants - Halides', 'livereport_id': '2554'}


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_row_selection_and_inversion(selenium):
    """
    Test row selection and inversion using checkbox.

    1. Invert the selection and verification.
    2. Select All and verification.
    3. Select None and verification.
    4. check the row selection type checkbox functionality.
    :param selenium: Selenium WebDriver
    """
    # Test Data
    all_compound_count = 7
    selected_compounds_first = 3

    # selecting multiple rows and verification
    select_multiple_rows(selenium, 'V055824', 'V055826', 'V055828')
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(all_compound_count),
            Footer.ROW_SELECTED_COUNT_KEY: Footer.ROW_SELECTED_COUNT_VALUE.format(selected_compounds_first)
        })

    # ----- Invert the selection and verification ----- #
    choose_row_selection_type_and_verify_footer(selenium,
                                                'Invert',
                                                all_rows_count=all_compound_count,
                                                selected_count=all_compound_count - selected_compounds_first)
    verify_selected_row_ids(selenium, 'V055825', 'V055827', 'V055829', 'V055830')

    # checking deselect all rows by clicking selection checkbox on partial selection
    select_all_rows(selenium)
    verify_selected_row_ids(selenium)

    # ----- Select All and verification ----- #
    choose_row_selection_type_and_verify_footer(selenium,
                                                'All',
                                                all_rows_count=all_compound_count,
                                                selected_count=all_compound_count)
    verify_selected_row_ids(selenium, 'V055824', 'V055825', 'V055826', 'V055827', 'V055828', 'V055829', 'V055830')

    # ----- Select None and verification ----- #
    choose_row_selection_type_and_verify_footer(selenium, 'None', all_rows_count=all_compound_count, selected_count=0)
    verify_selected_row_ids(selenium)

    # ----- check row selection type checkbox functionality ----- #
    # selecting all rows by clicking checkbox
    select_all_rows(selenium)

    # verification selected row ids
    verify_selected_row_ids(selenium, 'V055824', 'V055825', 'V055826', 'V055827', 'V055828', 'V055829', 'V055830')
    # Verify that the select All checkbox is selected
    select_all_checkbox = dom.get_element(selenium, GRID_ALL_ROWS_CHECKBOX_INPUT, must_be_visible=False)
    assert select_all_checkbox.is_selected(), "The Select All checkbox with selector {} is not selected".format(
        GRID_ALL_ROWS_CHECKBOX_INPUT)

    # deselecting all rows by clicking checkbox
    select_all_rows(selenium)

    # verify selected row ids
    verify_selected_row_ids(selenium)
    # Verify that the select All checkbox is not selected
    assert not select_all_checkbox.is_selected(), "The Select All checkbox with selector {} is selected".format(
        GRID_ALL_ROWS_CHECKBOX_INPUT)
