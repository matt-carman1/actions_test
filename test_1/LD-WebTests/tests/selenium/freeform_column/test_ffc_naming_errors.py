from helpers.change.freeform_column_action import open_create_ffc_dialog_from_column_tree, set_ffc_name
from helpers.change.grid_column_menu import click_column_menu_item
from helpers.selection.freeform_columns import FreeformColumnDialog
from helpers.selection.modal import MODAL_OK_BUTTON_DISABLED, MODAL_CANCEL_BUTTON
from helpers.verification.element import verify_is_visible
from library import dom

live_report_to_duplicate = {'livereport_name': 'FFC - All types, published and unpublished', 'livereport_id': '1299'}


def test_ffc_naming_errors(selenium, duplicate_live_report, open_livereport):
    """
    Test to verify the different FFC naming errors displayed on the FFC dialog

    :param selenium: Selenium Webdriver
    :param duplicate_live_report: a fixture which duplicates the LiveReport
    :param open_livereport: a fixture which opens the LiveReport
    :return:
    """
    # Access Create Freeform Column Dialog from D&C Tree
    open_create_ffc_dialog_from_column_tree(selenium)

    # FFC name same as unpublished FFC already existing in the current LR
    set_ffc_name(selenium, ffc_name='Number  - unpublished')
    verify_ffc_dialog_error_message(
        selenium,
        expected_error_message='A column with the same name already exists in this LiveReport. Please use another name.'
    )

    # Empty FFC name field
    set_ffc_name(selenium, ffc_name='')
    verify_ffc_dialog_error_message(selenium, expected_error_message='Please enter a name for this freeform column.')

    dom.click_element(selenium, MODAL_CANCEL_BUTTON)

    # Access Edit Freeform Column Dialog through one of the unpublished FFCs column context menu
    click_column_menu_item(selenium, column_name='Text - unpublished', column_option_name='Edit Freeform Column')

    # FFC name same as published FFC already existing in 'JS Testing' project
    set_ffc_name(selenium, ffc_name='Published Freeform Text Column')
    verify_ffc_dialog_error_message(
        selenium,
        expected_error_message=
        'A published Freeform column with the same name exists in project "JS Testing". Please use another name, or rename that column first'
    )

    # FFC name > 40 chars
    set_ffc_name(selenium, ffc_name='Name for testing FFC name field > 40 char')
    verify_ffc_dialog_error_message(
        selenium,
        expected_error_message=
        'A column name must be less than 40 characters to add it to the LiveReport. Please use another name.')

    # TODO: FFC name same as published FFC already existing in 'Global' project blocked by QA-5972

    dom.click_element(selenium, MODAL_CANCEL_BUTTON)


def verify_ffc_dialog_error_message(driver, expected_error_message):
    """
    Function to verify if the FFC error message is displayed in the dialog and Add to LiveReport/Save button is disabled
    :param driver: Webdriver
    :param expected_error_message: str, Expected FFC dialog error message
    :return:
    """
    verify_is_visible(driver,
                      selector=FreeformColumnDialog.FFC_ERROR_CONTAINER,
                      selector_text=expected_error_message,
                      exact_selector_text_match=True)
    verify_is_visible(driver, selector=MODAL_OK_BUTTON_DISABLED)
