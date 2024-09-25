import time

import pytest

from helpers.change.tile_view import select_multiple_tiles, switch_to_tile_view, check_select_all_tiles_checkbox
from helpers.flows.grid import choose_row_selection_type_and_verify_footer
from helpers.selection.grid import Footer
from helpers.selection.tile_view import TILE_VIEW_SELECTION_CHECKBOX_INPUT
from helpers.verification.grid import verify_footer_values
from helpers.verification.tile_view import verify_selected_tile_ids
from library import dom

live_report_to_duplicate = {'livereport_name': 'Test Reactants - Halides', 'livereport_id': '2554'}


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_tile_selection_and_inversion(selenium):
    """
    Test row selection and inversion using checkbox.

    1. Invert the Selection and Verification.
    2. Select All and Verification.
    3. Select None and Verification.
    4. check row selection type checkbox functionality.
    :param selenium: Selenium WebDriver
    """
    # Test Data
    all_compound_count = 7
    selected_compounds_first = 3
    # Open tile view
    switch_to_tile_view(selenium)

    # Select tiles in tile view and verification
    select_multiple_tiles(selenium, ['V055824', 'V055826', 'V055828'])
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(all_compound_count),
            Footer.ROW_SELECTED_COUNT_KEY: Footer.ROW_SELECTED_COUNT_VALUE.format(selected_compounds_first)
        })

    # ----- Invert the selection and verification ----- #
    choose_row_selection_type_and_verify_footer(selenium, 'Invert', all_compound_count,
                                                all_compound_count - selected_compounds_first)
    verify_selected_tile_ids(selenium, 'V055825', 'V055827', 'V055829', 'V055830')

    # checking deselect all rows by clicking selection checkbox on partial selection
    check_select_all_tiles_checkbox(selenium)
    time.sleep(1)
    verify_selected_tile_ids(selenium)

    # ----- Select All and Verification ----- #
    choose_row_selection_type_and_verify_footer(selenium, 'All', all_compound_count, all_compound_count)
    verify_selected_tile_ids(selenium, 'V055824', 'V055825', 'V055826', 'V055827', 'V055828', 'V055829', 'V055830')

    # ----- Select None and Verification ----- #
    choose_row_selection_type_and_verify_footer(selenium, 'None', all_compound_count, 0)
    verify_selected_tile_ids(selenium)

    # ----- check row selection type checkbox functionality ----- #
    # select all tiles by clicking checkbox
    check_select_all_tiles_checkbox(selenium)
    time.sleep(1)
    verify_selected_tile_ids(selenium, 'V055824', 'V055825', 'V055826', 'V055827', 'V055828', 'V055829', 'V055830')
    # Verify that the select All checkbox is selected
    select_all_checkbox = dom.get_element(selenium, TILE_VIEW_SELECTION_CHECKBOX_INPUT, must_be_visible=False)
    assert select_all_checkbox.is_selected(), "The Select All checkbox with selector {} is not selected".format(
        TILE_VIEW_SELECTION_CHECKBOX_INPUT)

    # deselecting all tiles by clicking checkbox
    check_select_all_tiles_checkbox(selenium)
    time.sleep(1)
    verify_selected_tile_ids(selenium)
    # Verify that the select All checkbox is not selected
    assert not select_all_checkbox.is_selected(), "The Select All checkbox with selector {} is selected".format(
        TILE_VIEW_SELECTION_CHECKBOX_INPUT)
