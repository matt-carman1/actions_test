import time

from helpers.change.actions_pane import open_add_data_panel, close_add_data_panel
from helpers.change.grid_column_menu import click_column_menu_item
from helpers.change.grid_columns import get_cell
from helpers.selection.column_tree import COLUMN_TREE_PICKER_CREATE_NEW_FFC_BUTTON
from helpers.selection.freeform_columns import FreeformColumnDialog, FreeformColumnCellEdit, FreeformColumnBulkEdit
from helpers.selection.grid import GRID_HEADER_CELL
from helpers.selection.live_report_tab import TAB_ACTIVE
from helpers.selection.modal import MODAL_DIALOG_HEADER, MODAL_OK_BUTTON
from helpers.verification.element import verify_is_visible
from helpers.verification.grid import check_for_butterbar
from library import dom, simulate, wait, utils
from library.select import select_option_by_text
from library.simulate import hover
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select


def open_edit_ffc_panel(driver, column_name):
    """
    Opens Edit Freeform Column panel

    :param driver: webdriver
    :param column_name: name of the freeform column to edit
    :type column_name: <str>
    """
    click_column_menu_item(driver, column_name, "Edit Freeform Column")
    wait.until_visible(driver, FreeformColumnDialog.FFC_WINDOW)


def edit_ffc_cell(driver, column_name, structure_id, value, is_date=False, is_boolean=False):
    """
    Edit a FreeForm Column cell to have the given value.

    :param driver: webdriver
    :param column_name: name of the FFC
    :type column_name: <str>
    :param structure_id: the structure ID
    :type structure_id: <str>
    :param value: value for the FFC cell
    :type value: <str>
    :param is_date: flag for if the FFC is
    :type is_date: <boolean>
    :param is_boolean: Set it to true if FFC is of boolean type
    :type is_boolean: <boolean>
    """
    ffc_cell = get_cell(driver, structure_id, column_name)

    if is_boolean:
        hover(driver, ffc_cell)
        value = value.lower()
        if not value or value == 'clear':
            dom.click_element(ffc_cell, FreeformColumnCellEdit.FFC_BOOLEAN_OPTION.format(''))
        else:
            dom.click_element(ffc_cell, FreeformColumnCellEdit.FFC_BOOLEAN_OPTION.format(value))
        return

    simulate.click(driver, ffc_cell)
    dom.click_element(ffc_cell, FreeformColumnCellEdit.FFC_EDIT_ICON)
    # FFC date cells have an input rather than a textarea
    tag_name = 'input' if is_date else 'textarea'
    # you can't reliably click on the textarea, so we can't use
    # set_element_value(ffc_cell_1, 'textarea', value)

    element = dom.get_element(ffc_cell, tag_name)
    element.clear()
    simulate.typing(element, value)
    dom.click_element(ffc_cell, FreeformColumnCellEdit.FFC_CELL_EDIT_SAVE)


def open_create_ffc_dialog_from_column_tree(driver):
    """
    Open create FFC dialog by clicking New option on FFC Section on D&C Tree

    :param driver: Webdriver
    :return:
    """
    # open the "Add Data" action panel, if it is not already open
    open_add_data_panel(driver)

    # Click "New" button for Freeform Columns
    dom.click_element(driver, COLUMN_TREE_PICKER_CREATE_NEW_FFC_BUTTON, text="NEW")

    # Ensures that the FFC window is open before choosing settings (This is necessary because the opening of the
    # window is slow, and sometimes it is not ready when choose_ffc_settings() starts running)
    wait.until_visible(driver, FreeformColumnDialog.FFC_NAME)


def set_ffc_name(driver, ffc_name, is_unique_name_required=False):
    """
    Function to set name in the FFC dialog
    If is_unique_name is set to True, unique ffc_name will be generated
    :param driver: Webdriver
    :param ffc_name: str, name of the FFC
    :param is_unique_name_required: bool, Whether a unique FFC name is needed.
                                    False - User provided ffc name will be used (Default)
                                    True - Unique name will be generated using user provided ffc name
    :return:
    """
    ffc_name = utils.make_unique_name(ffc_name) if is_unique_name_required else ffc_name
    dom.set_element_value(driver, selector=FreeformColumnDialog.FFC_NAME, value=ffc_name)


def create_ffc(driver,
               column_name,
               description=None,
               column_type='Text',
               allow_any_value=True,
               picklist_values=[],
               multiselect_in_picklist=False,
               publish=False,
               read_only=False,
               access_users=[],
               is_unique_name_required=False):
    """
    Creates a FreeForm Column

    :param driver: webdriver
    :param column_name: name of the FFC
    :type column_name: <str>
    :param description: unique description of the FFC
    :type description: <str>
    :param column_type: type of FFC (default is 'Text')
    :type column_type: <str>
    :param allow_any_value: setting for whether to constrain values or not
    :type allow_any_value: <boolean>
    :param picklist_values: the list of values in the picklist to be selected
    :type picklist_values: <list>
    :param multiselect_in_picklist: True to enable multi-selecting in FFCs
    :type multiselect_in_picklist: <boolean>
    :param publish: setting for whether to publish the FFC or not
    :type publish: <boolean>
    :param read_only: True to make FFC read-only (default is False)
    :type read_only: <boolean>
    :param access_users: list of users to be checked in read-only allow-list
    :type read_only: <list>
    :param is_unique_name_required: whether a unique name is required for FFC
    :type is_unique_name_required: <boolean>
    """
    open_create_ffc_dialog_from_column_tree(driver)

    if column_type in ('File / Image', 'True/false'):
        allow_any_value = None

    # choose settings
    choose_ffc_settings(driver, column_name, description, column_type, allow_any_value, picklist_values,
                        multiselect_in_picklist, publish, read_only, access_users, is_unique_name_required)

    # close the "Add Data Action panel
    close_add_data_panel(driver)


def choose_ffc_settings(driver,
                        column_name,
                        description=None,
                        column_type='Text',
                        allow_any_value=True,
                        picklist_values=[],
                        multiselect_in_picklist=False,
                        publish=False,
                        read_only=False,
                        access_users=[],
                        is_unique_name_required=False):
    """
    Chooses FreeFrom Column settings

    :param driver: webdriver
    :param column_name: name of the FFC
    :type column_name: <str>
    :param description: unique description of the FFC
    :type description: <str>
    :param column_type: type of FFC (default is 'Text')
    :type column_type: <str>
    :param allow_any_value: setting for whether to constrain values or not
    :type allow_any_value: <boolean>
    :param picklist_values: the list of values in the picklist to be selected
    :type picklist_values: <list>
    :param multiselect_in_picklist: True to enable multi-selecting in FFCs
    :type multiselect_in_picklist: <boolean>
    :param publish: setting for whether to publish the FFC or not
    :type publish: <boolean>
    :param read_only: True to make FFC read-only (default is False)
    :type read_only: <boolean>
    :param access_users: list of users to be checked in read-only allow-list
    :type access_users: <list>
    :param is_unique_name_required: whether a unique name is required for FFC
    :type is_unique_name_required: <boolean>
    """

    # Add unique name
    set_ffc_name(driver, ffc_name=column_name, is_unique_name_required=is_unique_name_required)

    time.sleep(1)

    # Select type
    select = Select(dom.get_element(driver, FreeformColumnDialog.FFC_TYPE))
    select.select_by_visible_text(column_type)

    # Select values to allow
    if allow_any_value is None:
        pass
    elif allow_any_value:
        dom.click_element(driver, FreeformColumnDialog.FFC_CONSTRAINT_ANY)
    else:
        dom.click_element(driver, FreeformColumnDialog.FFC_PICKLIST_FIELD)
        for picklist_value in picklist_values:
            dom.click_element(driver, FreeformColumnDialog.FFC_PICKLIST_ACTION, text='Add Item')
            set_picklist_ffc_values(driver, picklist_value)

    # Add unique description
    if description:
        dom.set_element_value(driver, FreeformColumnDialog.FFC_DESCRIPTION, description)

    # Determine setting for "Publish" checkbox
    if publish:
        publish_checkbox = dom.get_element(driver, FreeformColumnDialog.FFC_PUBLISHED_CHECKBOX)
        if not publish_checkbox.is_selected():
            simulate.click(driver, publish_checkbox)
    if multiselect_in_picklist:
        dom.click_element(driver, FreeformColumnDialog.FFC_MULTISELECT_IN_PICKLIST)

    # Make FFC Read-Only and checking users on allow-list
    if read_only:
        read_only_checkbox = dom.get_element(driver, FreeformColumnDialog.FFC_READ_ONLY_CHECKBOX)
        if not read_only_checkbox.is_selected():
            simulate.click(driver, read_only_checkbox)
        # Select users in access_users list on the read-only allow-list
        if access_users:
            for username in access_users:
                allowlist_search = dom.get_element(driver, FreeformColumnDialog.FFC_READ_ONLY_ALLOWLIST_SEARCH)
                simulate.typing(allowlist_search, value=username)
                # After searching a username, checking the first username on the list
                dom.click_element(driver,
                                  selector=FreeformColumnDialog.FFC_READ_ONLY_ALLOWLIST_FIRST_VALUE,
                                  text=username)
                dom.set_element_value(driver, selector=FreeformColumnDialog.FFC_READ_ONLY_ALLOWLIST_SEARCH, value="")

    # Add to LiveReport
    dom.click_element(driver, MODAL_OK_BUTTON)


def add_remove_picklist_ffc_item(driver, column_name, value_to_remove=None, value_to_add=None, use_calendar=False):
    """
    Edit a freeform column from the column dropdown and make changes to the existing FFC definition.

    :param driver: webdriver
    :param column_name: name of the FFC
    :type column_name: <str>
    :param value_to_remove: The value to be removed from the constrained list
    :type value_to_remove: <str>
    :param value_to_add: The value to be added in the constrained list
    :type value_to_add: <str>
    :param use_calendar: True if the picklist is of date type, defaults to False
    :type  use_calendar: Boolean
    """

    click_column_menu_item(driver, column_name, 'Edit Freeform Column')
    verify_is_visible(driver, MODAL_DIALOG_HEADER, 'Edit Freeform Column')

    if value_to_remove:
        dom.click_element(driver, FreeformColumnDialog.FFC_PICKLIST_VALUE_SELECT, text=value_to_remove)
        dom.click_element(driver, FreeformColumnDialog.FFC_PICKLIST_ACTION, text='Remove Item')
    if value_to_add:
        dom.click_element(driver, FreeformColumnDialog.FFC_PICKLIST_ACTION, text='Add Item')
        if use_calendar:
            set_picklist_ffc_values(driver, picklist_value=value_to_add, calendar_pick=True)
        else:
            set_picklist_ffc_values(driver, picklist_value=value_to_add)

    dom.click_element(driver, MODAL_OK_BUTTON)


def make_ffc_published(driver, column_name):
    """
    Making FFC published if it is unpublished.
    :param driver: selenium webdriver
    :param column_name: name of the column
    :type column_name: <str>
    :return:
    """
    open_edit_ffc_panel(driver, column_name)
    dom.click_element(driver, FreeformColumnDialog.FFC_PUBLISHED_CHECKBOX)
    dom.click_element(driver, MODAL_OK_BUTTON)
    check_for_butterbar(driver, 'Editing Freeform Column...', visible=False)


def set_picklist_ffc_values(driver, picklist_value, calendar_pick=False):
    """
    This function adds constraint values to picklist type ffc

    :param driver: webdriver
    :param picklist_value: the values to be added in the picklist FFC
    :type picklist_value: <str>
    :param calendar_pick: True if the picklist is of date type, defaults to False
    :type calendar_pick: Boolean
    """

    if calendar_pick:
        dom.click_element(driver, FreeformColumnDialog.FFC_CALENDAR_ELEMENT)
        dom.click_element(driver, FreeformColumnDialog.FFC_CALENDAR_PICK, picklist_value, exact_text_match=True)
    else:
        dom.set_element_value(driver, FreeformColumnDialog.FFC_PICKLIST_VALUE_PLACEHOLDER, picklist_value)
    edit_element = dom.get_element(driver, FreeformColumnDialog.FFC_CELL_EDIT_WINDOW)
    dom.click_element(edit_element, MODAL_OK_BUTTON)


def edit_picklist_ffc_cell(driver, column_name, structure_id, values=[], multiselect=False):
    """
    Edit a FreeForm Column cell to have the given value.
    :param driver: webdriver
    :param column_name: name of the FFC
    :type column_name: <str>
    :param structure_id: the structure ID
    :type structure_id: <str>
    :param values: list of values for a picklist FFC cell
    :type values: list
    :param multiselect: True, to allow multi-selecting from picklist FFCs
    :type multiselect: <boolean>
    """
    ffc_cell = get_cell(driver, structure_id, column_name)
    simulate.click(driver, ffc_cell)
    dom.click_element(ffc_cell, FreeformColumnCellEdit.FFC_EDIT_ICON)
    if multiselect:
        control_key = dom.get_ctrl_key()
        for value in values:
            get_picklist_value = dom.get_element(driver, FreeformColumnCellEdit.FFC_PICKLIST_VALUES, text=value)
            ActionChains(driver).key_down(control_key).click(get_picklist_value).key_up(control_key).perform()
    else:
        dom.click_element(driver, FreeformColumnCellEdit.FFC_PICKLIST_VALUES, text=values)

    dom.click_element(ffc_cell, FreeformColumnCellEdit.FFC_CELL_EDIT_SAVE)


def bulk_edit_ffc(driver, ffc_column_name, structure_id, value=None, copy_from_column=False):
    """
    Bulk edit a Freeform Column.
    :param driver: webdriver
    :param ffc_column_name: name of the published FFC
    :type ffc_column_name: <str>
    :param structure_id: the structure ID
    :type structure_id: <str>
    :param value: value to be added in the FFC cells
    :type value: <str>
    :param copy_from_column: True, to allow selection of column from dropdown menu
    :type copy_from_column: <boolean>
    """
    dom.click_element(driver, GRID_HEADER_CELL, text=ffc_column_name, exact_text_match=True)
    dom.click_element(driver, TAB_ACTIVE)
    simulate.hover(driver, get_cell(driver, structure_id, ffc_column_name))
    wait.until_visible(driver, FreeformColumnCellEdit.FFC_EDIT_ICON)
    dom.click_element(driver, FreeformColumnCellEdit.FFC_EDIT_ICON)

    # Selecting a column from dropdown menu
    if copy_from_column:
        dom.click_element(driver, FreeformColumnBulkEdit.COLUMN_DROPDOWN)
        select_option_by_text(driver, FreeformColumnBulkEdit.COLUMN_DROPDOWN, value)

    else:
        # Adding a value in the textbox
        dom.set_element_value(driver, FreeformColumnBulkEdit.FFC_CELL_EDIT_VALUE_FIELD, value)

    # selecting apply to all compounds option
    dom.click_element(driver, FreeformColumnBulkEdit.FFC_CELL_EDIT_BULK_CHECKBOX)
    dom.click_element(driver, FreeformColumnBulkEdit.FFC_CELL_EDIT_BULK_SAVE)
