import pytest
from library import dom, ensure
from selenium.webdriver.support.ui import Select

# Column Tree & FFC related imports
from helpers.change.actions_pane import open_add_data_panel
from helpers.change.columns_action import search_and_selecting_column_in_columns_tree
from helpers.change.freeform_column_action import set_picklist_ffc_values, open_create_ffc_dialog_from_column_tree
from helpers.selection.column_tree import COLUMN_TREE_PICKER_SEARCH
from helpers.selection.freeform_columns import FreeformColumnDialog, FreeformColumnCommonErrors
from helpers.verification.element import verify_is_visible, verify_attribute_value

# MPO-related Imports
from helpers.selection.mpo import MPO_OK_BUTTON_DISABLED_STATE, MPO_CANCEL_BUTTON, \
    MPO_VALIDATION_ERROR
from helpers.change.mpo_actions import add_in_live_report_constituent, remove_constituent, clone_mpo

# Formula-related Imports
from helpers.change.formula_actions import open_create_formula_window, add_name_to_formula, add_expression_to_formula
from helpers.selection.formula import FORMULA_SAVE_BUTTON, FORMULA_COMMA_DECIMAL_WARNING, FORMULA_CANCEL_BUTTON,\
    FORMULA_VALIDATION_ERROR

# Coloring Rules related Imports
from helpers.change.grid_column_menu import open_coloring_rules
from helpers.selection.coloring_rules import SLIDER_MIN, SLIDER_MAX, COLOR_WINDOW_CANCEL_BUTTON

# Parameterized Model Modal related Imports
from helpers.selection.modal import MODAL_DIALOG_LABEL_INPUT, PARAM_MODEL_DIALOG_OK_BUTTON_DISABLED, \
    PARAM_MODEL_DIALOG_OK_BUTTON, PARAM_MODEL_VALIDATION_ERROR, PARAM_MODEL_DIALOG_CANCEL_BUTTON, MODAL_CANCEL_BUTTON

test_username = 'commaDecimalUser'
test_password = 'commaDecimalUser'
live_report_to_duplicate = {'livereport_name': 'FFC - All types, published and unpublished', 'livereport_id': '1299'}


@pytest.mark.usefixtures('open_livereport')
@pytest.mark.usefixtures('duplicate_live_report')
def test_comma_separator_in_modal_dialogs(selenium):
    """
    Checks the comma separator and associated error messages in modal dialogs
    i) FFC Modal
    ii) Coloring Rules Dialog (Slider values - automatic changes from (dot) input to (comma))
    iii) Formula Modal (Dot only allowed as decimal separator in formula expression)
    iv) MPO Modal
    v) Parameterize Model Modal

    :param selenium: Webdriver
    """
    # FFC Modal
    open_create_ffc_dialog_from_column_tree(selenium)
    select = Select(dom.get_element(selenium, FreeformColumnDialog.FFC_TYPE))
    select.select_by_visible_text('Number')
    dom.click_element(selenium, FreeformColumnDialog.FFC_PICKLIST_FIELD)
    dom.click_element(selenium, FreeformColumnDialog.FFC_PICKLIST_ACTION, text='Add Item')
    set_picklist_ffc_values(selenium, '2.0')
    verify_is_visible(selenium,
                      selector=FreeformColumnCommonErrors.FFC_VALUE_VALIDATION_ERROR_MESSAGE,
                      selector_text='Invalid number')
    edit_element = dom.get_element(selenium, FreeformColumnDialog.FFC_CELL_EDIT_WINDOW)
    dom.click_element(edit_element, MODAL_CANCEL_BUTTON)
    dom.click_element(selenium, FreeformColumnDialog.FFC_DIALOG_CLOSE)

    # Coloring Rules Dialog
    ffc_name = 'Number - published'
    open_coloring_rules(selenium, column_name=ffc_name)
    dom.set_element_value(selenium, SLIDER_MIN, "4.5")
    dom.set_element_value(selenium, SLIDER_MAX, "41.8")
    dom.press_enter_key(selenium)
    verify_attribute_value(selenium, selector=SLIDER_MIN, attribute='value', expected_attribute_value='4,5')
    verify_attribute_value(selenium, selector=SLIDER_MAX, attribute='value', expected_attribute_value='41,8')
    dom.click_element(selenium, COLOR_WINDOW_CANCEL_BUTTON, text='Cancel')

    # Formula Modal
    expression = '2,2 + 3,2'
    open_create_formula_window(selenium)
    add_name_to_formula(selenium, formula_column_name='TestFormula')
    verify_is_visible(selenium,
                      selector=FORMULA_COMMA_DECIMAL_WARNING,
                      selector_text='Decimal commas are not supported in formulas. Please use decimal points.')
    add_expression_to_formula(selenium, expression_to_add=expression)
    expected_formula_error_message = 'Failed to parse formula {}'.format(expression)
    ensure.element_visible(selenium,
                           expected_visible_selector=FORMULA_VALIDATION_ERROR,
                           expected_visible_selector_text=expected_formula_error_message,
                           action_selector=FORMULA_SAVE_BUTTON)
    dom.click_element(selenium, FORMULA_CANCEL_BUTTON)

    # MPO Modal
    mpo_to_clone = '(JS Testing) Test RPE MPO'
    clone_mpo(selenium, mpo_to_clone)
    # TODO: Remove the below line after SS-34287 is fixed.
    remove_constituent(selenium, column_name='PK_PO_RAT (AUC)')
    add_in_live_report_constituent(selenium, ffc_name, 'Higher Better', ['-2.2', '3.2'])
    verify_is_visible(selenium, selector=MPO_OK_BUTTON_DISABLED_STATE)
    expected_mpo_error_message = 'Make sure to enter proper numerical ranges for {}.'.format(ffc_name)
    ensure.element_visible(selenium,
                           expected_visible_selector=MPO_VALIDATION_ERROR,
                           expected_visible_selector_text=expected_mpo_error_message,
                           action_selector=MPO_OK_BUTTON_DISABLED_STATE)
    dom.click_element(selenium, MPO_CANCEL_BUTTON)

    # Parameterized Model Modal
    model_name = 'Parameterizable Example'
    open_add_data_panel(selenium)
    search_and_selecting_column_in_columns_tree(selenium,
                                                column_name=model_name,
                                                picker_search_selector=COLUMN_TREE_PICKER_SEARCH)
    dom.set_element_value(selenium, selector=MODAL_DIALOG_LABEL_INPUT.format('Password Length'), value='10.9')
    verify_is_visible(selenium, selector=PARAM_MODEL_DIALOG_OK_BUTTON_DISABLED)
    ensure.element_visible(selenium,
                           expected_visible_selector=PARAM_MODEL_VALIDATION_ERROR,
                           action_selector=PARAM_MODEL_DIALOG_OK_BUTTON)
    expected_error_message = 'The Password Length field must be a proper numerical value'
    verify_is_visible(selenium, selector=PARAM_MODEL_VALIDATION_ERROR, selector_text=expected_error_message)
    dom.click_element(selenium, PARAM_MODEL_DIALOG_CANCEL_BUTTON)
