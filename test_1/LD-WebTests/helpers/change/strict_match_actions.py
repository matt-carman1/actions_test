from helpers.change import advanced_search_actions
from helpers.change.grid_column_menu import click_column_menu_item
from helpers.change.range_actions import set_range_limit_value
from helpers.selection.advanced_search import ADV_QUERY_COG_ICON, ADV_QUERY_PANEL_GEAR_BUTTON_MENU_OPEN, \
    QUERY_RANGE_LOWER_BOX
from helpers.selection.general import MENU_ITEM
from helpers.selection.strict_match import ASSAY_LIMITED_DIALOG, EDIT_LIMITING_CONDITION_BUTTON, \
    LIMITED_COLUMN_TITLE_INPUT, LIMITING_CONDITION_PICKLIST, LIMITING_CONDITION_TITLE_IN_DIALOG, LIMITING_CONDITION_QUERY_BOX_, \
    LIMITING_CONDITION_LOWER_RANGE_INPUT, LIMITING_CONDITION_UPPER_RANGE_INPUT
from helpers.verification.element import verify_is_visible, verify_is_not_visible
from helpers.selection.modal import MODAL_DIALOG_HEADER
from library import dom, wait


def open_create_limited_assay_column_dialog(driver, assay_name):
    """
    Opens the Create Limited Assay Column Dialog from the given Assay column context menu.
    :param driver: Selenium Webdriver
    :param assay_name: str, name of the name for which limited assay column has to be created.
    :return: element, create limited asssay column dialog web element
    """

    click_column_menu_item(driver, assay_name, 'Define Limiting Conditions…', exact_text_match=True)

    return dom.get_element(driver, ASSAY_LIMITED_DIALOG)


def open_edit_limited_assay_column_dialog_from_livereport(driver, limited_assay_column_name):
    """
    Opens the Edit Limited Assay Column Dialog from the given Limited Assay column context menu.
    :param driver: Selenium Webdriver
    :param limited_assay_column_name: str, limited assay column for which the limiting conditions are to be edited.
    :return: element, create limited asssay column dialog web element
    """

    click_column_menu_item(driver, limited_assay_column_name, 'Edit Limiting Conditions...', exact_text_match=True)

    return dom.get_element(driver, MODAL_DIALOG_HEADER, text='Edit Limited Assay Column')


def open_edit_limited_assay_column_dialog_from_adv_search(driver, assay_name):
    """
    Open Edit Limited Assay Column Dialog from Advanced Search. Make sure advanced search panel is open and the assay
    query is added. This would check for "Add Limiting Condition" button, if the button is not there it would open
    the dialog by selecting "Edit Limiting Conditions..." option from the assay query gear menu.

    :param driver: Selenium Webdriver
    :param assay_name: str, assay name fow which edit limited assay column dialog needs to be opened.
    :return: element, create limited assay column dialog web element
    """

    adv_query_condition_box = advanced_search_actions.get_query(driver, assay_name)
    dom.click_element(adv_query_condition_box, EDIT_LIMITING_CONDITION_BUTTON, text='Edit Assay Conditions…')

    return dom.get_element(driver, ASSAY_LIMITED_DIALOG)


def set_limited_column_title(driver, column_title):
    """
    Set the value for the Column Title input in the Define/Edit Limiting Conditions dialog

    :param driver: Selenium Webdriver
    :param column_title: str, limited assay column title
    """

    dom.set_element_value(driver, LIMITED_COLUMN_TITLE_INPUT, column_title)


def add_remove_limiting_conditions(driver, condition, add=True, exact_text_match=False):
    """
    Add/Remove Limiting conditions for the Limited Assay given Edit/Create Limited Assay Column dialog is open.

    :param driver: Selenium Webdriver
    :param condition: str, the condition name to limit the assay upon
    :param add: boolean, Defaults to True which means the condition needs to be added. To remove, set it to False.
    :param exact_text_match: boolean, Whether text match should be exact or not. Disabled by default.
    :return boolean, condition element if the limiting condition is added else return nothing.
    """

    # TODO: Scroll to options click_element might fail in Firefox if the option is not in the visible area.
    dom.click_element(driver, LIMITING_CONDITION_PICKLIST, text=condition, exact_text_match=exact_text_match)

    if add:
        verify_is_visible(driver, LIMITING_CONDITION_TITLE_IN_DIALOG, selector_text=condition)
        return dom.get_element(driver, LIMITING_CONDITION_QUERY_BOX_.format(condition))
    else:
        verify_is_not_visible(driver, LIMITING_CONDITION_TITLE_IN_DIALOG, selector_text=condition)


def set_limiting_condition_range(limiting_condition_element, lower_limit=None, upper_limit=None):
    """
    Sets the range values for limiting conditions in the Create/Edit Limited Assay column dialog. Please ensure that the
    Limited Assay dialog is open before calling this helper.
    This is exactly similar to advanced_search_actions/set_query_range() helper but the selector for input boxes are
    different so we have to write this for limited assay range limit input.
    :param limiting_condition_element: web element for the limiting condition panel
    :param lower_limit: int, lower bound value to be set for the limiting condition
    :param upper_limit: int, upper bound value to be set for the limiting condition
    :return:
    """

    if lower_limit:
        set_range_limit_value(limiting_condition_element, LIMITING_CONDITION_LOWER_RANGE_INPUT, lower_limit)
    if upper_limit:
        set_range_limit_value(limiting_condition_element, LIMITING_CONDITION_UPPER_RANGE_INPUT, upper_limit)


def select_limit_multiple_endpoints_checkbox(driver, assay_column_name, assay_name):
    """
    Opens the gear menu for the given assay column name and selects the "Limit Multiple Endpoints" checkbox and finally
    closes the gear menu.
    :param driver: Selenium Webdriver
    :param assay_column_name: str, Full name of the assay with endpoint
    :param assay_name: str, name of the assay without the endpoint. We need this because once we select the checkbox
                       for limiting conditions the query condition only shows the assay name like "PK_PO_RAT" rather
                       than "PK_PO_RAT (AUC)".
    """
    condition_box = advanced_search_actions.get_query(driver, assay_column_name)

    # Tick the checkbox for Limit Multiple Endpoints
    dom.click_element(condition_box, ADV_QUERY_COG_ICON)
    wait.until_visible(condition_box, ADV_QUERY_PANEL_GEAR_BUTTON_MENU_OPEN)
    dom.click_element(condition_box, MENU_ITEM, text='Limit Multiple Endpoints')

    # Closing the gear menu
    # Using 'assay_name' here because choosing to limit the column removes the endpoint information from query condition
    condition_box = advanced_search_actions.get_query(driver, assay_name)
    dom.click_element(condition_box, QUERY_RANGE_LOWER_BOX)
