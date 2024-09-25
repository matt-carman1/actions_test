import time

import pytest

from helpers.selection.grid import GRID_FIND_INPUT, GRID_FIND_MATCH_COUNT, GRID_FIND_PREV_BUTTON, \
    GRID_FIND_NEXT_BUTTON, GRID_FIND_CLOSE_BUTTON, GRID_FIND_PANEL, GRID_FIND_BUTTON
from helpers.verification.element import verify_is_visible, verify_is_not_visible
from helpers.verification.grid import verify_grid_matching_elements, verify_grid_find_panel
from library.dom import press_enter_key, press_ctrl_and_keys, set_element_value, click_element

live_report_to_duplicate = {'livereport_name': '3 Compounds 2 Poses', 'livereport_id': '883'}


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_grid_find(selenium):
    """
    Test Grid Find using:

    1. Set Grid Find text which has 1 match and verification
    2. Set Grid Find text which has more matches and Verification
    3. Remove Grid Find using X mark and Verification
    4. Open grid find panel by clicking Grid Find button and check Default grid panel
    """
    # Ctrl+F to open grid find panel
    press_ctrl_and_keys(selenium, 'f')

    # ----- Set Grid Find text which has 1 match and Verify ----- #
    text_with_one_match_in_grid = 'CRA-035000'
    set_element_value(selenium, GRID_FIND_INPUT, value=text_with_one_match_in_grid)
    # verify grid panel which includes verifying grid find input and navigation buttons are visible
    verify_grid_find_panel(selenium, match_count='1 of 1')
    # verifying current matching element and all matches count
    verify_grid_matching_elements(selenium, 1, expected_matching_text=text_with_one_match_in_grid)

    # ----- Set Grid Find text which has more matches and Verify ----- #
    text_with_three_matches_in_grid = 'small'
    set_element_value(selenium, GRID_FIND_INPUT, value=text_with_three_matches_in_grid)
    # verify grid panel which includes verifying grid find input and navigation are buttons visible
    verify_grid_find_panel(selenium, match_count='1 of 3')
    # verifying current matching element and all matches count
    verify_grid_matching_elements(selenium, 3, expected_matching_text=text_with_three_matches_in_grid)

    # ----- Verify Navigation of matched elements ----- #
    # navigating to next selected element by Enter key and verification
    press_enter_key(selenium)
    verify_is_visible(selenium, GRID_FIND_MATCH_COUNT, selector_text='2 of 3')
    # navigating to next selected element by '>' button and verification
    click_element(selenium, GRID_FIND_NEXT_BUTTON)
    verify_is_visible(selenium, GRID_FIND_MATCH_COUNT, selector_text='3 of 3')
    # navigating to previous selected element by '<' button and verification
    click_element(selenium, GRID_FIND_PREV_BUTTON)
    verify_is_visible(selenium, GRID_FIND_MATCH_COUNT, selector_text='2 of 3')

    # ----- Remove Grid Find using X button and Verify ----- #
    click_element(selenium, GRID_FIND_CLOSE_BUTTON)
    # Verify grid find panel not visible and grid find button is visible
    verify_is_not_visible(selenium, GRID_FIND_PANEL)
    verify_is_visible(selenium, GRID_FIND_BUTTON)
    time.sleep(0.5)
    # Verify there are no orange and yellow matches in Grid
    verify_grid_matching_elements(selenium, 0)

    # ----- Open grid find panel by clicking Grid Find button and check Default grid panel ----- #
    click_element(selenium, GRID_FIND_BUTTON)
    # Verify grid find panel visible and grid find button not visible
    verify_is_visible(selenium, GRID_FIND_PANEL)
    verify_is_not_visible(selenium, GRID_FIND_BUTTON)
    # verify grid panel which includes verifying grid find input and navigation are buttons visible
    verify_grid_find_panel(selenium, match_count='Not Found')
