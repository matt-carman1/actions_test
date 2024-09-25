from helpers.selection.grid import GRID_FOOTER_ROW_HIDDEN_COUNT, GRID_FOOTER_COLUMN_HIDDEN_COUNT
from helpers.selection.modal import MODAL_DIALOG, MODAL_DIALOG_BODY, MODAL_DIALOG_HEADER
from helpers.verification.element import verify_is_visible
from library import dom, wait, base


def show_hidden_compounds(driver, hidden_compounds_count):
    """
    This method performs these 2 actions:
    1. Left click on the footer cell which shows hidden compounds count
    2. Click on OK for the OKCancel Dialog that comes after this, which will show all compounds
    It will also verify that the number of hidden_compounds is matched in the dialog.

    :param driver: Selenium WebDriver
    :param hidden_compounds_count: Number of hidden compounds
    """
    dialog_body_text = 'Show {} Hidden Compound{}?'.format(hidden_compounds_count,
                                                           's' if hidden_compounds_count != 1 else '')

    dom.click_element(driver, GRID_FOOTER_ROW_HIDDEN_COUNT)
    wait.until_visible(driver, MODAL_DIALOG_HEADER, text='Show Compounds')
    verify_is_visible(driver, MODAL_DIALOG_BODY, selector_text=dialog_body_text)
    base.click_ok(driver)
    wait.until_not_visible(driver, MODAL_DIALOG)
    wait.until_loading_mask_not_visible(driver)


def show_hidden_columns(driver, hidden_columns_count):
    """
    This method performs these 2 actions:
    1. Left click on the footer cell which shows hidden columns count
    2. Click on OK for the OKCancel Dialog that comes after this, which will show all columns
    It will also verify that the number of hidden columns is matched in the dialog.

    :param driver: Selenium WebDriver
    :param hidden_columns_count: Number of hidden columns
    """
    dialog_body_text = 'Show {} Hidden Column{}?'.format(hidden_columns_count, 's' if hidden_columns_count != 1 else '')

    dom.click_element(driver, GRID_FOOTER_COLUMN_HIDDEN_COUNT)
    wait.until_visible(driver, MODAL_DIALOG_HEADER, text='Show Columns')
    verify_is_visible(driver, MODAL_DIALOG_BODY, selector_text=dialog_body_text)
    base.click_ok(driver)
    wait.until_not_visible(driver, MODAL_DIALOG)
