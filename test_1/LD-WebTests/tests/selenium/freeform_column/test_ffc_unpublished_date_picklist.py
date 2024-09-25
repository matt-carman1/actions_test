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
live_report_to_duplicate = {'livereport_name': 'Test Reactants - Halides', 'livereport_id': '2554'}


@pytest.mark.smoke
@pytest.mark.usefixtures('open_livereport')
@pytest.mark.usefixtures("duplicate_live_report")
def test_ffc_unpublished_date_picklist(selenium):
    """
    Test creation, cell selection, and editing of unpublished picklist date type freeform column.

    :param selenium: Webdriver
    :return:
    """
    description = 'This is a picklist date type FFC'
    unpublished_picklist_date_ffc = 'FFC Date'
    values = ['2020-01-15', '2019-01-19', '2017-05-30']
    error_message = 'Invalid format, use YYYY-MM-DD'
    # Creating an FFC of picklist type
    create_ffc(selenium,
               unpublished_picklist_date_ffc,
               description,
               column_type='Date',
               allow_any_value=False,
               picklist_values=values,
               publish=False)

    # Selecting values from the picklist type FFC
    edit_picklist_ffc_cell(selenium, unpublished_picklist_date_ffc, 'V055824', values=values[0])
    edit_picklist_ffc_cell(selenium, unpublished_picklist_date_ffc, 'V055826', values=values[2])

    # Verifying contents of the column after editing the FFC
    verify_column_contents(selenium, unpublished_picklist_date_ffc, ['2020-01-15', '', '2017-05-30', '', '', '', ''])

    date_to_add = '2021-10-29'
    # Editing the existing picklist definition to remove one value and add another value
    add_remove_picklist_ffc_item(selenium,
                                 unpublished_picklist_date_ffc,
                                 value_to_remove='2020-01-15',
                                 value_to_add=date_to_add,
                                 use_calendar=False)

    # Selecting new dates from the edited picklist
    edit_picklist_ffc_cell(selenium, unpublished_picklist_date_ffc, 'V055825', values=date_to_add)
    verify_column_contents(selenium, unpublished_picklist_date_ffc,
                           ['2020-01-15', date_to_add, '2017-05-30', '', '', '', ''])

    # Checking that incorrect dates are disallowed
    click_column_menu_item(selenium, unpublished_picklist_date_ffc, 'Edit Freeform Column')
    ffc_edit_window = dom.get_element(selenium, FreeformColumnDialog.FFC_EDIT_WINDOW)

    verify_is_visible(ffc_edit_window, MODAL_DIALOG_HEADER, 'Edit Freeform Column')
    dom.click_element(ffc_edit_window, FreeformColumnDialog.FFC_PICKLIST_ACTION, text='Add Item')
    values = ['2020-13-01', '13-01-2020', '19-12-21']

    # Checking for incorrect date
    set_picklist_ffc_values(selenium, picklist_value=values[0])
    verify_is_visible(selenium, FreeformColumnCommonErrors.FFC_VALUE_VALIDATION_ERROR_MESSAGE, error_message)

    # Checking for incorrect date format
    set_picklist_ffc_values(selenium, picklist_value=values[1])
    verify_is_visible(selenium, FreeformColumnCommonErrors.FFC_VALUE_VALIDATION_ERROR_MESSAGE, error_message)

    # Checking for incorrect date format
    set_picklist_ffc_values(selenium, picklist_value=values[2])
    verify_is_visible(selenium, FreeformColumnCommonErrors.FFC_VALUE_VALIDATION_ERROR_MESSAGE, error_message)
    edit_element = dom.get_element(selenium, FreeformColumnDialog.FFC_CELL_EDIT_WINDOW)
    dom.click_element(edit_element, MODAL_CANCEL_BUTTON)
    dom.click_element(ffc_edit_window, FreeformColumnDialog.FFC_DIALOG_CLOSE)

    # Search D&C tree for FFC column name (Since this is unpublished, it should only exist in the context of the LR
    verify_no_column_exists_in_column_tree(selenium, unpublished_picklist_date_ffc)
