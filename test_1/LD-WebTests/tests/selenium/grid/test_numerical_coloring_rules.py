import pytest

from helpers.change import grid_column_menu
from helpers.change.range_actions import set_range_color_in_coloring_rule_dialog
from helpers.selection.coloring_rules import COLOR_WINDOW_OK_BUTTON
from helpers.verification.color import verify_column_color
from helpers.verification.grid import check_for_butterbar
from library import dom, wait

# Name of LiveReport that will be duplicated
live_report_to_duplicate = {'livereport_name': 'Coloring Rules', 'livereport_id': '879'}


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
@pytest.mark.parametrize("color_left, color_right, verify_colors", [('#3333FF', '#FFFFFF', [(0, 0, 0, 0),
                                                                                            (255, 255, 255, 1),
                                                                                            (156, 156, 255, 1),
                                                                                            (100, 100, 255, 1),
                                                                                            (51, 51, 255, 1)]),
                                                                    ('#FFCC66', '#33FF33', [(0, 0, 0, 0),
                                                                                            (51, 255, 51, 1),
                                                                                            (149, 230, 75, 1),
                                                                                            (205, 216, 89, 1),
                                                                                            (255, 204, 102, 1)]),
                                                                    ('#FFFFFF', '#FFFFFF', [(0, 0, 0, 0),
                                                                                            (255, 255, 255, 1),
                                                                                            (255, 255, 255, 1),
                                                                                            (255, 255, 255, 1),
                                                                                            (255, 255, 255, 1)])])
def test_numerical_coloring_rules(selenium, color_left, color_right, verify_colors):
    """
    Test numerical coloring rules, for "CR GScore (undefined)" column. The test sets the following colors in the
    left and right range of the coloring rule and verifies the same -
    1. left = blue, right = white
    2. left = yellow, right = green
    3. left = white, right = white
    :param selenium: Selenium WebDriver
    :param color_left: str, color selector for the left range
    :param color_right: str, color selector for the right range
    :param verify_colors: list of tuples, expected background color
    """
    # Test "CR GScore (undefined)' column coloring rule
    numeric_column_name = "CR GScore (undefined)"
    # To reduce flakiness of selecting wrong column
    wait.until_loading_mask_not_visible(selenium)

    # Open coloring rules dialog
    grid_column_menu.open_coloring_rules(selenium, numeric_column_name)

    # Select color for left and right range
    set_range_color_in_coloring_rule_dialog(selenium, color_left, color_right)

    # Saving coloring rule
    dom.click_element(selenium, COLOR_WINDOW_OK_BUTTON)

    # There should be a butterbar
    check_for_butterbar(selenium, 'Applying coloring rules', visible=True)
    # The butterbar should go away before we test colors
    check_for_butterbar(selenium, 'Applying coloring rules', visible=False)

    # Verification of the column color pattern
    verify_column_color(selenium, numeric_column_name, expected_colors=verify_colors)
