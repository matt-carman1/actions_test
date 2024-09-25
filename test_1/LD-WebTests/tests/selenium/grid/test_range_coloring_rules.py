import pytest

from helpers.change.grid_column_menu import hide_column, open_coloring_rules
from helpers.selection.coloring_rules import SLIDER_MAX, SLIDER_MIN, COLOR_WINDOW_OK_BUTTON
from helpers.verification.color import verify_column_color
from helpers.verification.grid import check_for_butterbar
from library import dom, base

# Set name of LiveReport that will be duplicated
live_report_to_duplicate = {'livereport_name': 'Coloring Rules', 'livereport_id': '879'}


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_range_coloring_rules(selenium):
    """
    Test range coloring rules, specifically on "CR Solubility (pH 7.4)" column

    :param selenium: Selenium WebDriver
    """
    # There is a bug when browsers run headless, in which horizontal grid scrolling breaks in this test. To work
    # around, hide some unused columns.
    hide_column(selenium, "Lot Scientist")
    hide_column(selenium, "Author (undefined)")
    hide_column(selenium, "CR GScore (undefined)")

    # ----- Test coloring rules for CR Solubility (pH 7.4) ----- #
    solubility_column_name = "CR Solubility (pH 7.4)"

    # Open coloring rules
    open_coloring_rules(selenium, solubility_column_name)

    # Enter 12 as a minimum and 50 as a maximum
    dom.set_element_value(selenium, SLIDER_MIN, "12")
    dom.set_element_value(selenium, SLIDER_MAX, "50")

    # Save
    dom.click_element(selenium, COLOR_WINDOW_OK_BUTTON)

    # There should be a butterbar
    check_for_butterbar(selenium, 'Applying coloring rules', visible=True)

    # The butterbar should go away before we test colors
    check_for_butterbar(selenium, 'Applying coloring rules', visible=False)

    # Verifying column color pattern #
    verify_column_color(selenium,
                        solubility_column_name,
                        expected_colors=[(0, 0, 0, 0), (0, 0, 0, 0), (231, 111, 111, 1), (255, 0, 0, 1),
                                         (211, 211, 211, 1)])
