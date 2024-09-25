"""
Validates a "Compound Detail" forms layout can be created, saved, and contains the correct data.
"""
import pytest

from helpers.change.forms import create_new_layout, open_saved_layout, save_forms_layout
from helpers.change.grid_row_actions import select_row
from helpers.selection.forms import FORM_STACK, ID_INFO, FORMS_ICON, FORMS_CONTAINER
from helpers.selection.general import MENU_ITEM
from helpers.selection.grid import GRID_ROW_ID_, GRID_ICON, GRID_FOOTER_ROW_ALL_COUNT
from helpers.verification.element import verify_is_visible
from helpers.verification.forms import verify_list_widget_contents, verify_forms_tabs_exist
from library import wait, dom

live_report_to_duplicate = {'livereport_name': "5 Compounds 4 Assays", 'livereport_id': '882'}


@pytest.mark.smoke
def test_new_assay_viewer(selenium, duplicate_live_report, open_livereport):
    """
    This test:
    1. Creates and saves a new "Compound Detail" layout
    2. Verifies the saved "Compound Detail" layout is listed while in grid view
    3. Verifies the saved "Compound Detail" layout loads
    4. Verify widgets below contains expected content for a selected structure:
        a. ID Widget - selected structure row is highlighted
        b. Compound Image Widget - shows am image and the correct structure ID is correct
        c. List Widget - contains the expected detail

    :param selenium: Webdriver
    :param duplicate_live_report: Fixture to duplicate an LR using ldclient and returns the LR name
    :param open_livereport: fixture that opens the LR
    """
    # ----- TEST SETUP ----- #
    create_new_layout(selenium, title=duplicate_live_report, layout="Compound Detail")
    save_forms_layout(selenium)

    # ----- Verify saved "Compound Detail" layout is listed while in grid view ----- #
    dom.click_element(selenium, GRID_ICON)
    wait.until_visible(selenium, GRID_FOOTER_ROW_ALL_COUNT)
    dom.click_element(selenium, FORMS_ICON)
    verify_is_visible(selenium, MENU_ITEM, duplicate_live_report)

    # ----- Verify saved "Compound Detail" layout loads ----- #
    open_saved_layout(selenium, title=duplicate_live_report)
    wait.until_not_visible(selenium, GRID_FOOTER_ROW_ALL_COUNT)
    dom.click_element(selenium, FORMS_ICON)
    verify_is_visible(selenium, FORMS_CONTAINER)

    # verify that ID, Compound Image, and List Widgets are present
    verify_forms_tabs_exist(selenium, "IDs 1", "Compound Image 1", "List 1")

    # ----- Verify widgets contains expected content -----#
    entity_id = "CRA-032703"
    widgets_all = dom.get_elements(selenium, FORM_STACK)

    # verify row with the structure in ID widget is selected
    widget_id = widgets_all[0]
    select_row(widget_id, entity_id)
    verify_is_visible(widget_id, GRID_ROW_ID_.format(entity_id) + " .selected-cell .checkbox-container")

    # verify Compound image widget contains an image and is showing the correct structure ID
    widget_compound_image = widgets_all[1]
    verify_is_visible(widget_compound_image, "img")
    id_input = dom.get_element(selenium, ID_INFO)
    assert id_input.get_attribute('value') == entity_id

    # verify List widget contains the correct information for the selected structure
    widget_list = widgets_all[2]
    verify_list_widget_contents(
        widget_list, {
            "Clearance (undefined)": "7",
            "Solubility (undefined)": "203",
            "STABILITY-PB-PH 7.4 (%Rem@2hr) [%]": "88",
            "CYP450 2C19-LCMS (%INH) [%]": "10"
        })
