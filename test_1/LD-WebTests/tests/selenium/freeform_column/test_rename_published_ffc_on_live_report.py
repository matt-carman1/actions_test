import pytest

from helpers.change.data_and_columns_tree import clear_column_tree_search, search_column_tree
from helpers.change.freeform_column_action import create_ffc, open_edit_ffc_panel, open_add_data_panel
from helpers.selection.column_tree import COLUMN_TREE_PICKER_NODE_TEXT_AREA, COLUMN_TREE_SECTION_NODE, \
    EDIT_TOOLTIP_BUTTON
from helpers.selection.freeform_columns import FreeformColumnDialog
from helpers.selection.modal import MODAL_OK_BUTTON
from helpers.verification.data_and_columns_tree import verify_column_exists_in_column_tree
from library import dom, simulate, wait
from library.utils import make_unique_name

live_report_to_duplicate = {'livereport_name': '3D Pose Data', 'livereport_id': '2799'}
test_report_name = '3D Pose Data'
test_type = 'selenium'


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_rename_published_ffc_on_live_report(driver):
    """
    Test rename and edit FFC on live_report
    :param driver: webdriver
    """
    ffc_name = make_unique_name("ffc")
    # creating new ffc
    create_ffc(driver, ffc_name, publish=True)
    verify_column_exists_in_column_tree(driver, ffc_name, search_retries=3)
    # Rename the FFC
    open_edit_ffc_panel(driver, ffc_name)
    new_ffc_name = make_unique_name(ffc_name)
    dom.set_element_value(driver, FreeformColumnDialog.FFC_NAME, new_ffc_name)
    dom.click_element(driver, MODAL_OK_BUTTON)
    verify_column_exists_in_column_tree(driver, new_ffc_name, search_retries=3)
    # Rename the FFC from the D&C tree "edit" button
    open_add_data_panel(driver)
    dom.click_element(driver, COLUMN_TREE_SECTION_NODE, 'Freeform Columns')

    # Search column tree and hover over new ffc
    # Note we wait for to update to the search by checking that Other Columns is not visible
    # This is necessary to avoid attempting to hover over the ffc while it's offscreen
    search_column_tree(driver, ffc_name)
    wait.until_not_visible(driver, COLUMN_TREE_PICKER_NODE_TEXT_AREA, text="Other Columns")
    simulate.hover(driver,
                   dom.get_element(driver, COLUMN_TREE_PICKER_NODE_TEXT_AREA, text=new_ffc_name, exact_text_match=True))

    dom.click_element(driver, EDIT_TOOLTIP_BUTTON)
    wait.until_visible(driver, FreeformColumnDialog.FFC_WINDOW)
    second_new_ffc_name = new_ffc_name
    dom.set_element_value(driver, FreeformColumnDialog.FFC_NAME, second_new_ffc_name)
    dom.click_element(driver, MODAL_OK_BUTTON)

    clear_column_tree_search(driver)
    verify_column_exists_in_column_tree(driver, second_new_ffc_name, search_retries=3)
