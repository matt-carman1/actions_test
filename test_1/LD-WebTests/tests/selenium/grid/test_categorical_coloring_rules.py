import pytest
import time

from helpers.change import grid_column_menu
from helpers.selection.coloring_rules import ADD_COLORING_RULE, CELL_SELECTOR_LABEL, COLOR_SELECTOR, COLOR_WINDOW_OK_BUTTON, COLOR_RULE, BLUE
from helpers.selection.grid import GRID_CELL_ASSAY_SUBCELL, GRID_ROWS_CONTAINER
from helpers.verification.color import verify_element_color, verify_column_color
from helpers.verification.grid import check_for_butterbar
from library import dom, base, scroll

# Set name of LiveReport that will be duplicated
live_report_to_duplicate = {'livereport_name': 'Coloring Rules', 'livereport_id': '879'}


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_categorical_coloring_rules(selenium):
    """
    Test categorical coloring rules, specifically "Author (undefined)" column

    :param selenium: Selenium WebDriver
    """
    # Test "Author (undefined)' column coloring rule #
    author_column_name = "Author (undefined)"

    # Open coloring rules
    grid_column_menu.open_coloring_rules(selenium, author_column_name)

    # This sleep is necessary to avoid race condition between selenium and javascript that occasionally causes test
    # to not be able to find element.
    time.sleep(.5)

    # click 2nd coloring rule and select blue
    dom.click_element(selenium, COLOR_SELECTOR.format(2))
    dom.click_element(selenium, BLUE)

    # select bob
    dom.click_element(selenium, COLOR_RULE.format(2))
    dom.click_element(selenium, CELL_SELECTOR_LABEL, text="bob")

    # click outside to close the dropdown
    # NOTE (agupta): Tried using `dom.click_element` on body, but for some reason selenium does an actual click on
    # some random element on the screen. Instead, by using a dispatchEvent, we make sure that the click is still
    # processed without affecting any other elements.
    selenium.execute_script('document.body.dispatchEvent(new Event("click", { bubbles: true }));')

    # Save
    dom.click_element(selenium, COLOR_WINDOW_OK_BUTTON)

    # There should be a butterbar
    check_for_butterbar(selenium, 'Applying coloring rules', visible=True)

    # The butterbar should go away before we test colors
    check_for_butterbar(selenium, 'Applying coloring rules', visible=False)

    # Verification of the column color pattern
    verify_column_color(selenium,
                        author_column_name,
                        expected_colors=[(0, 0, 0, 0), (51, 51, 255, 1), (51, 51, 255, 1), (255, 204, 102, 1),
                                         (255, 255, 0, 1)])


# TODO: check with @Arjuna if we would want to keep it with new helper in place.
def _check_cell_color(driver, cell_text, color):
    """
    Test that the cell color matches the expected color.

    :param driver: webdriver
    :param cell_text: text in the cell
    :param color: color of the cell background
    """

    grid_row_container = dom.get_element(driver, GRID_ROWS_CONTAINER)

    cell = scroll.scroll_until_visible(driver,
                                       grid_row_container,
                                       GRID_CELL_ASSAY_SUBCELL,
                                       text=cell_text,
                                       delta_px=200)
    verify_element_color(cell, color)
