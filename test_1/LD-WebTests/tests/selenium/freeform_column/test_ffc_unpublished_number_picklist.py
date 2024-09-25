import pytest

from helpers.change.freeform_column_action import create_ffc, add_remove_picklist_ffc_item, set_picklist_ffc_values, \
    edit_picklist_ffc_cell
from helpers.change.grid_column_menu import click_column_menu_item
from helpers.selection.freeform_columns import FreeformColumnDialog, FreeformColumnCommonErrors
from helpers.selection.modal import MODAL_DIALOG_HEADER, MODAL_CANCEL_BUTTON
from helpers.verification.data_and_columns_tree import verify_no_column_exists_in_column_tree
from helpers.verification.element import verify_is_visible
from helpers.verification.grid import verify_column_contents
from library import dom

# Set LiveReport to duplicate
live_report_to_duplicate = {'livereport_name': 'Test Reactants - Nitriles', 'livereport_id': '2553'}


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_ffc_unpublished_number_picklist(selenium):
    """
    Test creation, cell selection, and editing of unpublished picklist text type freeform column.

    :param selenium: Webdriver
    :return:
    """
    description = 'This is a picklist number FFC'
    unpublished_picklist_number_ffc = 'FFC 1'
    values = ['5.2', '6.0', '12.3']
    incorrect_value = 'Text not supported'
    # Creating an FFC of picklist type
    create_ffc(selenium,
               unpublished_picklist_number_ffc,
               description,
               column_type='Number',
               allow_any_value=False,
               picklist_values=values,
               publish=False)

    # Selecting values from the picklist type FFC
    edit_picklist_ffc_cell(selenium, unpublished_picklist_number_ffc, 'V047518', values=values[0])
    edit_picklist_ffc_cell(selenium, unpublished_picklist_number_ffc, 'V055820', values=values[2])

    # Verifying contents of the column after editing the FFC
    verify_column_contents(selenium, unpublished_picklist_number_ffc, ['5.2', '', '12.3', '', '', ''])

    # Editing the existing picklist definition to remove one value and add another value
    add_remove_picklist_ffc_item(selenium, unpublished_picklist_number_ffc, value_to_remove='5.2', value_to_add='9.3')

    # Selecting new values from the edited picklist
    edit_picklist_ffc_cell(selenium, unpublished_picklist_number_ffc, 'V047755', values='9.3')
    verify_column_contents(selenium, unpublished_picklist_number_ffc, ['5.2', '9.3', '12.3', '', '', ''])

    # Search D&C tree for FFC column name (Since this is unpublished, it should only exist in the context of the LR
    verify_no_column_exists_in_column_tree(selenium, unpublished_picklist_number_ffc)

    # Checking that text values are disallowed
    click_column_menu_item(selenium, unpublished_picklist_number_ffc, 'Edit Freeform Column')
    ffc_edit_window = dom.get_element(selenium, FreeformColumnDialog.FFC_EDIT_WINDOW)

    verify_is_visible(ffc_edit_window, MODAL_DIALOG_HEADER, 'Edit Freeform Column')
    dom.click_element(ffc_edit_window, FreeformColumnDialog.FFC_PICKLIST_ACTION, text='Add Item')

    set_picklist_ffc_values(selenium, picklist_value=incorrect_value)
    verify_is_visible(selenium, FreeformColumnCommonErrors.FFC_VALUE_VALIDATION_ERROR_MESSAGE, 'Invalid number')
    edit_element = dom.get_element(selenium, FreeformColumnDialog.FFC_CELL_EDIT_WINDOW)
    dom.click_element(edit_element, MODAL_CANCEL_BUTTON)
    dom.click_element(ffc_edit_window, FreeformColumnDialog.FFC_DIALOG_CLOSE)
