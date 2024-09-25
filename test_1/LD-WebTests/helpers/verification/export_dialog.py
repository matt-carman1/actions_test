from library import dom
from library.wait import until_condition_met

from helpers.selection.modal import MODAL_DIALOG_HEADER, MODAL_TITLE_FIELD_LABEL, \
    MODAL_TITLE_FIELD_INPUT, MODAL_TITLE_FIELD_RESET, EXPORT_DIALOG_COMPOUNDS_LABEL, \
    EXPORT_DIALOG_COMPOUNDS_ALL, EXPORT_DIALOG_COLUMNS_ALL, EXPORT_DIALOG_COLUMNS_LABEL, \
    MODAL_OK_BUTTON, MODAL_CANCEL_BUTTON, EXPORT_DIALOG_COMPOUNDS_ALL_CHECKED, \
    EXPORT_DIALOG_COMPOUNDS_CURRENTLY_SELECTED_UNCHECKED, EXPORT_DIALOG_COMPOUNDS_ALL_UNCHECKED, \
    EXPORT_DIALOG_COMPOUNDS_CURRENTLY_SELECTED_CHECKED, EXPORT_DIALOG_COMPOUNDS_CURRENTLY_SELECTED, \
    EXPORT_DIALOG_COLUMNS_ALL_CHECKED, EXPORT_DIALOG_COLUMNS_CHOOSE_SUBSET_UNCHECKED, \
    EXPORT_DIALOG_COLUMNS_ALL_UNCHECKED, EXPORT_DIALOG_COLUMNS_CHOOSE_SUBSET, MODAL_LR_COLUMN_SEARCH_BOX, \
    MODAL_LR_COLUMN_SEARCH_BOX_INPUT, MODAL_LR_COLUMN_SEARCH_BOX_CLEAR_BUTTON, MODAL_LR_COLUMNS_LIST, \
    MODAL_LR_COLUMN_SELECTION_LINKS_WRAPPER, MODAL_LR_COLUMN_LABEL
from helpers.verification.element import verify_attribute_value, verify_is_visible, verify_is_not_visible


def verify_export_dialog_ui_constants(driver, lr_name):
    """
    Function to verify the following unchanging cases on the export dialog UI
    i) Check dialog is visible
    ii) Dialog header title
    iii) File Name row (label, LR name, clear icon)
    iv) Columns & Compounds label
    v) 'OK' and 'Cancel' button at the bottom

    :param driver: webdriver, Webdriver
    :param lr_name: str, LiveReport Name
    """
    verify_is_visible(driver, selector=MODAL_DIALOG_HEADER, selector_text='Export LiveReport')
    # File Name Row
    verify_is_visible(driver,
                      selector=MODAL_TITLE_FIELD_LABEL,
                      selector_text='File Name',
                      exact_selector_text_match=True)
    verify_attribute_value(driver,
                           selector=MODAL_TITLE_FIELD_INPUT,
                           attribute='value',
                           expected_attribute_value=lr_name)
    verify_is_visible(driver, selector=MODAL_TITLE_FIELD_RESET, selector_text='x')
    # Compounds Row
    verify_is_visible(driver,
                      selector=EXPORT_DIALOG_COMPOUNDS_LABEL,
                      selector_text='Compounds:',
                      exact_selector_text_match=True)
    verify_is_visible(driver, selector=EXPORT_DIALOG_COMPOUNDS_ALL, selector_text='All')
    # Columns Row
    verify_is_visible(driver,
                      selector=EXPORT_DIALOG_COLUMNS_LABEL,
                      selector_text='Columns:',
                      exact_selector_text_match=True)
    verify_is_visible(driver, selector=EXPORT_DIALOG_COLUMNS_ALL, selector_text='All')
    # Buttons
    verify_is_visible(driver, selector=MODAL_OK_BUTTON, selector_text='OK', exact_selector_text_match=True)
    verify_is_visible(driver, selector=MODAL_CANCEL_BUTTON, selector_text='Cancel', exact_selector_text_match=True)


def check_export_dialog_compounds_options(driver, all_option, selected_row_count=0):
    """
    Function to verify the compounds options selected on the export dialog.

    :param driver: webdriver, Webdriver
    :param all_option: bool, Set True to verify if 'All' option for the columns is checked
                             and 'Currently Selected()' option is unchecked; Set False to verify vice versa
    :param selected_row_count: int, Number of rows selected. By default value is 0
    """
    if all_option:
        verify_is_visible(driver, selector=EXPORT_DIALOG_COMPOUNDS_ALL_CHECKED)
        verify_is_visible(driver, selector=EXPORT_DIALOG_COMPOUNDS_CURRENTLY_SELECTED_UNCHECKED)
    else:
        verify_is_visible(driver, selector=EXPORT_DIALOG_COMPOUNDS_ALL_UNCHECKED)
        verify_is_visible(driver, selector=EXPORT_DIALOG_COMPOUNDS_CURRENTLY_SELECTED_CHECKED)

    verify_is_visible(driver,
                      selector=EXPORT_DIALOG_COMPOUNDS_CURRENTLY_SELECTED,
                      selector_text='Currently Selected ({})'.format(selected_row_count))


def check_export_dialog_columns_options(driver, all_option):
    """
    Function to verify the columns options selected on the export dialog.

    :param driver: webdriver, Webdriver
    :param all_option: bool, Set True to verify if 'All' option for the columns is checked
                             and 'Choose Subset' option is unchecked; Set False to verify vice versa
    """
    if all_option:
        verify_is_visible(driver, selector=EXPORT_DIALOG_COLUMNS_ALL_CHECKED)
        verify_is_visible(driver, selector=EXPORT_DIALOG_COLUMNS_CHOOSE_SUBSET_UNCHECKED)
    else:
        verify_is_visible(driver, selector=EXPORT_DIALOG_COLUMNS_ALL_UNCHECKED)
        verify_is_not_visible(driver, selector=EXPORT_DIALOG_COLUMNS_CHOOSE_SUBSET_UNCHECKED)


def verify_export_dialog_choose_subset_part(driver, expected_columns_list):
    """
    Function to click on Choose Subset option for columns and verify the related parts of the dialog

    :param driver: Selenium Webdriver
    :param expected_columns_list: list of str, Expected columns name that should be present on export dialog
    """
    dom.click_element(driver, selector=EXPORT_DIALOG_COLUMNS_CHOOSE_SUBSET, text='Choose Subset')
    # Search Field
    verify_is_visible(driver, selector=MODAL_LR_COLUMN_SEARCH_BOX)
    verify_is_visible(driver, selector=MODAL_LR_COLUMN_SEARCH_BOX_INPUT)
    verify_is_visible(driver, selector=MODAL_LR_COLUMN_SEARCH_BOX_CLEAR_BUTTON)
    # Columns List
    verify_is_visible(driver, selector=MODAL_LR_COLUMNS_LIST)
    fetch_and_compare_export_columns_list(driver,
                                          selector=MODAL_LR_COLUMN_LABEL,
                                          expected_columns_list=expected_columns_list)
    # Select Columns
    verify_is_visible(driver,
                      selector=MODAL_LR_COLUMN_SELECTION_LINKS_WRAPPER,
                      selector_text='Select Columns:\nAll\nVisible\nNone')


def fetch_and_compare_export_columns_list(driver, selector, expected_columns_list):
    """
    Function to fetch list of selector based columns on the export dialog and compare with expected columns list.

    :param driver: Selenium webdriver
    :param selector: str, Column label selector for example, hidden/checked/unchecked column
    :param expected_columns_list: list of str, Expected list of columns to compare
    """

    def fetch_and_compare():
        col_elements = dom.get_elements(driver, selector)
        actual_columns_list = [element.text for element in col_elements]
        assert expected_columns_list == actual_columns_list, \
            'Expected columns list is {}, but got {}'.format(expected_columns_list, actual_columns_list)

    until_condition_met(fetch_and_compare, retries=3, interval=1)


def search_and_verify_filtered_columns_on_export_dialog(driver, search_item, expected_filtered_columns):
    """
    Function to set search item, fetch and verify filtered columns on the export dialog

    :param driver: Selenium webdriver
    :param search_item: str, Item to be searched
    :param expected_filtered_columns: list of str, Expected list of filtered columns to compare
    """
    # Set search item
    dom.set_element_value(driver, selector=MODAL_LR_COLUMN_SEARCH_BOX_INPUT, value=search_item)
    verify_attribute_value(driver,
                           selector=MODAL_LR_COLUMN_SEARCH_BOX_INPUT,
                           attribute='value',
                           expected_attribute_value=search_item)
    if expected_filtered_columns:
        fetch_and_compare_export_columns_list(driver,
                                              selector=MODAL_LR_COLUMN_LABEL,
                                              expected_columns_list=expected_filtered_columns)
    else:
        """
        NOTE: If no matching columns are found, then the message 'No columns match the search filter.' is displayed
              using the pseudocode element(::after), so using dom.get_pseudo_element_property_value method and using
              the output for verification
        """
        expected_content = '"No columns match the search filter."'
        actual_content = dom.get_pseudo_element_property_value(driver,
                                                               selector=MODAL_LR_COLUMNS_LIST,
                                                               pseudo_elem=':after',
                                                               property_='content')
        assert actual_content == expected_content, 'Expected {} but got {}'.format(expected_content, actual_content)

    # Clear the search input field by clicking 'X' button
    dom.click_element(driver, selector=MODAL_LR_COLUMN_SEARCH_BOX_CLEAR_BUTTON)
    verify_attribute_value(driver,
                           selector=MODAL_LR_COLUMN_SEARCH_BOX_INPUT,
                           attribute='value',
                           expected_attribute_value='')
