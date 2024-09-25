import pytest

from helpers.change.forms import add_spreadsheet_widget, create_new_layout, save_forms_layout
from helpers.change.grid_row_actions import select_row
from helpers.selection.forms import (FORMS_ICON, FORMS_CONTAINER, ID_INFO, LIST_GADGET, DECREASE_ROW_SELECTION,
                                     FORMS_STRUCTURE_GADGET, SPREADSHEET_WIDGET)
from helpers.selection.general import MENU_ITEM
from helpers.selection.grid import GRID_ICON, GRID_FOOTER_ROW_ALL_COUNT, GRID_ROW_ID_
from helpers.verification.element import verify_is_visible
from library import dom, wait

live_report_to_duplicate = {'livereport_name': "5 Compounds 4 Assays", 'livereport_id': '882'}


@pytest.mark.smoke
def test_new_assay_viewer(selenium, duplicate_live_report, open_livereport):
    """
    This test ensures the "Assay Viewer" forms view:
        1. can be saved and reloaded
        2. a compound image widget is present with correct data
        3. shows a spreadsheet widget with row pre-selected in grid view selected
        4. assay data for structures are correctly shown
    """
    # ----- Test setup ----- #
    # pre-select row to later validate structure data shown when a new "Assay Viewer" loads
    compound_id = 'CRA-032664'
    select_row(selenium, entity_id=compound_id)
    # create a new "Assay Viewer" layout
    create_new_layout(selenium, title=duplicate_live_report, layout="Assay Viewer")
    # add spreadsheet widget to later verify correct row is added
    add_spreadsheet_widget(selenium, -1)
    save_forms_layout(selenium)

    # ----- "Assay Viewer" layout can be saved and reloaded ----- #
    # verify saved layout listed in forms dropdown
    dom.click_element(selenium, GRID_ICON)
    wait.until_visible(selenium, GRID_FOOTER_ROW_ALL_COUNT)
    dom.click_element(selenium, FORMS_ICON)
    verify_is_visible(selenium, MENU_ITEM, duplicate_live_report)

    # verify layout loads
    dom.click_element(selenium, MENU_ITEM, duplicate_live_report)
    wait.until_not_visible(selenium, GRID_FOOTER_ROW_ALL_COUNT)
    verify_is_visible(selenium, FORMS_CONTAINER)

    # ----- Compound image widget is present ----- #
    verify_is_visible(selenium, FORMS_STRUCTURE_GADGET)
    # verify correct structure shown (pre-selected in grid view)
    id_input = dom.get_element(selenium, ID_INFO)
    assert id_input.get_attribute('value') == compound_id

    # ----- Spreadsheet widget verification ----- #
    # verify Spreadsheet widget is visible
    verify_is_visible(selenium, SPREADSHEET_WIDGET)
    # verify structure selected in grid view is also selected
    verify_is_visible(selenium,
                      GRID_ROW_ID_.format(compound_id) + " .selected-cell",
                      error_if_selector_matches_many_elements=False)

    # ----- Assay value verification ----- #
    # verify assay data
    verify_is_visible(selenium, LIST_GADGET, 'STABILITY-PB-PH 7.4 (%Rem@2hr) [%]\n100')
    verify_is_visible(selenium, LIST_GADGET, 'Clearance (undefined)\n6')
    verify_is_visible(selenium, LIST_GADGET, 'Solubility (undefined)\n500')
    verify_is_visible(selenium, LIST_GADGET, 'CYP450 2C19-LCMS (%INH) [%]\n12')

    # change structure shown via the compound image widget
    dom.click_element(selenium, DECREASE_ROW_SELECTION)

    # verify correct structure shown
    id_input = dom.get_element(selenium, ID_INFO)
    assert id_input.get_attribute('value') == 'CRA-032662'

    # assay data correct
    verify_is_visible(selenium, LIST_GADGET, 'STABILITY-PB-PH 7.4 (%Rem@2hr) [%]\n77')
    verify_is_visible(selenium, LIST_GADGET, 'Clearance (undefined)\n4')
    verify_is_visible(selenium, LIST_GADGET, 'Solubility (undefined)\n1')
    verify_is_visible(selenium, LIST_GADGET, 'CYP450 2C19-LCMS (%INH) [%]\n10')
