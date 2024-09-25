import pytest
from selenium.webdriver.common.keys import Keys

from helpers.change.grid_columns import get_cell
from helpers.change.live_report_picker import open_live_report
from helpers.flows.grid import select_grid_cells_with_navigation_keys
from helpers.selection.grid import GRID_ROW_SELECTION_CELL, GRID_HEADER_SELECTOR_
from helpers.verification.element import verify_is_not_visible, verify_is_visible
from library import dom, simulate, wait
from helpers.change.scroll import scroll_to_right, scroll_to_left, scroll_to_down, scroll_to_up, scroll_to_rightmost
from library.utils import is_k8s


@pytest.mark.xfail(not is_k8s(), reason="QA-6106")
def test_keyboard_navigation(selenium, open_project):
    """
    Tests to check keyboard navigation
    This test checks if

    1. the correct cell is selected for the following key presses:
        - up & left
        - down & right
        - Ctrl/Command + down
        - Ctrl/Command + up
        - End
        - Home

    2. a LR can scroll using the keys:
        - Navigation keys while no cell is selected
        - Page Up
        - Page Down

    3. multiple cells are selected by holding down Shift and using navigation keys
    """
    # ----- Test setup ----- #
    # Open a LR that is sorted by ID
    open_live_report(selenium, name="50 Compounds 10 Assays")
    # Wait till the LR loads to prevent flakiness
    wait.until_loading_mask_not_visible(selenium)

    # ----- Verify grid scrolling by pressing navigation keys while no cell is selected ----- #
    # Need to select an element, otherwise press_keys() or send_keys() don't work on Livereport
    column_header = dom.get_element(selenium, GRID_HEADER_SELECTOR_.format("Lot Scientist"))
    simulate.click(selenium, column_header)

    # Horizontal scrolling
    scroll_to_right(selenium, 5)
    verify_is_visible(selenium, GRID_HEADER_SELECTOR_.format("r_epik_Ionization_Penalty (undefined)"))

    scroll_to_left(selenium, 5)
    verify_is_visible(selenium, GRID_HEADER_SELECTOR_.format("Rationale"))

    # Vertical scrolling
    scroll_to_down(selenium, 3)
    verify_is_not_visible(selenium, GRID_ROW_SELECTION_CELL, selector_text="1")

    scroll_to_up(selenium, 3)
    verify_is_visible(selenium, GRID_ROW_SELECTION_CELL, selector_text="1")

    # Selecting a cell
    starting_highlighted_cell = get_cell(selenium, "CRA-035509", "Rationale")
    simulate.click(selenium, starting_highlighted_cell)

    # ----- Verify cell selected after pressing keys to navigate up & left ---- #
    dom.press_keys(selenium, Keys.UP, Keys.LEFT)
    verify_cell_selected(selenium, "CRA-035508", "ID")

    # ----- Verify cell selected after pressing keys to navigate down & right ---- #
    dom.press_keys(selenium, Keys.DOWN, Keys.RIGHT)
    # original cell should be highlighted
    verify_cell_selected(selenium, "CRA-035509", "Rationale")

    # ----- Verify cell selected after pressing keys Ctrl/Cmd + down ---- #
    dom.press_ctrl_and_keys(selenium, Keys.DOWN)
    verify_cell_selected(selenium, "CRA-035563", "Rationale")

    # ----- Verify cell selected after pressing keys Ctrl/Cmd + up ---- #
    dom.press_ctrl_and_keys(selenium, Keys.UP)
    verify_cell_selected(selenium, "CRA-035507", "Rationale")

    # ----- Verify Page Down navigates the LR ----- #
    dom.press_keys(selenium, Keys.PAGE_DOWN)
    verify_is_not_visible(selenium, GRID_ROW_SELECTION_CELL, selector_text="1")

    # ----- Verify Page Up navigates the LR ----- #
    dom.press_keys(selenium, Keys.PAGE_UP)
    verify_is_visible(selenium, GRID_ROW_SELECTION_CELL, selector_text="1")

    # ----- Verify cell selected after pressing key End ----- #
    scroll_to_rightmost(selenium)
    verify_cell_selected(selenium, "CRA-035507", "s_seurat_Registration_Database (undefined)")

    # ----- Verify cell selected after pressing key Home ----- #
    dom.press_keys(selenium, Keys.HOME)
    verify_cell_selected(selenium, "CRA-035507", "Compound Structure")

    # ----- Select multiple cells by holding down Shift and using navigation keys ----- #
    select_grid_cells_with_navigation_keys(selenium, Keys.RIGHT * 3, Keys.DOWN * 3)

    # ----- Verify two selected cells after the operation ----- #
    verify_cell_selected(selenium, "CRA-035507", "Lot Scientist")
    verify_cell_selected(selenium, "CRA-035510", "Compound Structure")


def verify_cell_selected(driver, compound_id, column_title):
    """
    Verify the cell for provided compound_id and column is highlighted

    :param driver: Selenium driver
    :param compound_id: str, structure ID
    :param column_title: str, column name
    :return: None
    """
    cell = get_cell(driver, compound_id, column_title)
    assert dom.get_element(cell, '.selected-cell'), \
        "Cell for structure id `{}` and column `{}` is not selected".format(compound_id, column_title)
