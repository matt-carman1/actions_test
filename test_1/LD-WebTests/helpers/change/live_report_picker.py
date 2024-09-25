"""
State changes made from the livereport picker.
"""
import time

from helpers.selection.general import MENU_ITEM
from helpers.selection.live_report_picker import REPORT_PICKER, METAPICKER_NEW_LIVE_REPORT_BUTTON, REPORT_LIST_ID, \
    REPORT_LIST_SELECTED_ITEM_ALIAS, REPORT_LIST_TITLE, REPORT_LIST_SELECTED_ITEM_TITLE, REPORT_LIST_ROW, SORT_DESC, \
    SORT_ASC, PROJECT_HOME_NEW_FOLDER_BUTTON, METAPICKER_FOLDER, METAPICKER_FOLDER_MENU, MOVE_DELETE_BUTTON, \
    MOVE_DELETE_BUTTON_MENU_ITEM, METAPICKER_FOLDER_DROP_TARGET, REPORT_LIST_SELECTED_FOLDER, REPORT_SEARCH_CROSS_MARK, \
    MERGE_LIVE_REPORTS_DIALOG, MERGE_LIVE_REPORTS_REFERENCE_RADIO_, MERGE_LIVE_REPORTS_MERGE_MODE_DROPDOWN, \
    MERGE_LIVE_REPORTS_CHECKBOX_CONTAINER_LABEL
from helpers.selection.live_report_tab import CREATE_LIVE_REPORT_TAB, LIVE_REPORT_TYPE_PICKER, TAB_ACTIVE, \
    LIVE_REPORT_PICKER_TAB, CREATE_LIVE_REPORT_WINDOW_FOLDER_DOWNARROW, CREATE_LIVE_REPORT_WINDOW_TEMPLATE_DROPDOWN, \
    CREATE_LIVE_REPORT_TEMPLATE_LIST, LABEL_LIVE_REPORT_NAME, CREATE_NEW_LIVE_REPORT
from helpers.selection.modal import MODAL_WINDOW, MODAL_DIALOG_BUTTON, MODAL_DIALOG, WINDOW_HEADER_TEXT, \
    BOUND_LIST_ITEM, OK_BUTTON
from helpers.change.live_report_menu import choose_folder_for_livereport_to_move
from helpers.verification.element import verify_is_not_visible, verify_is_visible
from library import dom, base, wait, simulate, ensure, actions, select, utils
from library.dom import LiveDesignWebException, get_parent_element
from library.utils import make_unique_name
from library.base import click_ok, set_input_text
from selenium.webdriver import ActionChains


def open_metapicker(driver):
    ensure.element_visible(driver, action_selector=LIVE_REPORT_PICKER_TAB, expected_visible_selector=REPORT_PICKER)


def close_metapicker(driver):
    ensure.element_not_visible(driver,
                               action_selector=MODAL_DIALOG_BUTTON,
                               expected_not_visible_selector=REPORT_PICKER,
                               action_selector_text='Cancel')


def open_new_live_report_dialog(driver, metapicker=False):
    """
    Opens the 'New LiveReport...' dialog

    :param driver: webdriver
    :param metapicker: bool, default False if metapicker is not open. True, if needs to "New LiveReport" button in
                       metapicker needs to be clicked.
    """
    if metapicker:
        open_metapicker(driver)
        dom.click_element(driver, METAPICKER_NEW_LIVE_REPORT_BUTTON, text='New LiveReport')
    else:
        dom.click_element(driver, CREATE_LIVE_REPORT_TAB)

    wait.until_visible(driver, WINDOW_HEADER_TEXT, text=CREATE_NEW_LIVE_REPORT)


def create_and_open_live_report(driver,
                                report_name='test',
                                template='Blank',
                                folder_name=None,
                                metapicker=False,
                                lr_type='Devices',
                                rationale=None,
                                confirm_open=True):
    """
    Create and open a LiveReport with a given name. Note that a random 8-digit
    number will be appended to the end of the supplied report_name

    :param driver: webdriver
    :param report_name: str, desired LiveReport name
    :param template: str, LiveReport Template name. Default is 'Blank',
    :param folder_name: str, desired Folder name
    :param metapicker: boolean, if set to True, create and open livereport via metapicker else
                       if set to False, create and open livereport by clicking on the '+' button.
    :param lr_type: str, type of LiveReport: Compounds or Devices in Materials Science mode. Default is Devices
    :param rationale: str, desired default rationale for an LR
    :param confirm_open: boolean, confirm LR tab of created LR is active. Useful as False where workflow doesn't end
                        with active LR tab visible, like a confirmation dialog after creating a LR to copy compounds to
    :return: str, the actual name of the created LiveReport, with appended random number.
    """

    open_new_live_report_dialog(driver, metapicker)

    new_livereport_name = fill_details_for_new_livereport(driver, report_name, template, folder_name, lr_type,
                                                          rationale)
    if confirm_open:
        wait.until_visible(driver, TAB_ACTIVE, new_livereport_name)

    return new_livereport_name


def open_live_report(driver, name=None, alias=None):
    """
    Open the livereport by name, or alias if specified

    :param driver: webdriver
    :param name: the name of the report to open
    :param alias: the id of the report to open
    """
    if not (alias or name):
        raise ValueError('One of `name` or `alias` must be supplied to this function')

    if alias:
        search_term = str(alias)
        column_selector_to_click = REPORT_LIST_ID
        selected_column_selector = REPORT_LIST_SELECTED_ITEM_ALIAS
    else:
        search_term = name
        column_selector_to_click = REPORT_LIST_TITLE
        selected_column_selector = REPORT_LIST_SELECTED_ITEM_TITLE

    live_report_element = search_for_live_report(driver, name=name, alias=alias)
    if not live_report_element:
        raise LiveDesignWebException("No LiveReport with {} {} found".format('alias' if alias else 'name', search_term))

    # click the cell with the correct text
    dom.click_element(live_report_element, column_selector_to_click, search_term)

    # wait until the column is selected
    wait.until_visible(live_report_element, selected_column_selector, search_term)
    base.click_ok(driver)


def search_for_live_report(driver, name=None, alias=None, directory="All LiveReports"):
    """
    Search in Metapicker for one livereport

    Note: one of alias and name must be specified as a named argument

    :param driver: Selenium WebDriver
    :param name: report name as string. This will be ignored if alias is specified
    :param alias: report alias as string or int
    :param directory: Metapicker directory
    :return: livereport metapicker web element
    """
    if alias:
        search_term = str(alias)
        column_selector_to_check = f"{REPORT_LIST_ROW} {REPORT_LIST_ID}"
    else:
        search_term = name
        column_selector_to_check = f"{REPORT_LIST_ROW} {REPORT_LIST_TITLE}"

    set_search_text_in_live_report_metapicker(driver, search_term, directory)
    picker = dom.get_element(driver, REPORT_PICKER)
    live_report_match = dom.get_element(picker,
                                        column_selector_to_check,
                                        text=search_term,
                                        exact_text_match=True,
                                        dont_raise=True)
    if live_report_match is None:
        return live_report_match
    return get_parent_element(get_parent_element(live_report_match))


def search_for_live_reports(driver, search_term, directory="All LiveReports"):
    """
    Search in Metapicker for livereports.

    :param driver: webdriver
    :param search_term: text for searchign
    :param directory: Metapicker directory
    :return: list of visible LR webelements in Metapicker
    """
    set_search_text_in_live_report_metapicker(driver, search_term, directory)
    # TODO find better way to wait for client side javascript work + DOM redraw
    time.sleep(1)
    picker = dom.get_element(driver, REPORT_PICKER)
    live_reports = dom.get_elements(picker, REPORT_LIST_ROW, dont_raise=True, timeout=2)

    return live_reports


def set_search_text_in_live_report_metapicker(driver, search_term, directory="All LiveReports"):
    """
    Fill the search input in the Metapicker for livereports.

    :param driver: webdriver
    :param search_term: text for searchign
    :param directory: Metapicker directory
    """
    open_metapicker(driver)
    picker = dom.get_element(driver, REPORT_PICKER)
    dom.click_element(picker, 'a', directory)
    dom.set_element_value(picker, 'input', search_term)


def sort_metapicker_column(driver, selector, header, desc=False):
    """
    Sort the specified metapicker column.

    :param driver: webdriver
    :param selector: column header selector
    :param header: column header name
    :param desc: sort order
    """
    order_selector = SORT_DESC if desc else SORT_ASC

    # Double click the column header
    element = dom.get_element(driver, selector, text=header)
    simulate.click(driver, element)

    # Ensure that the column header is in the right sort order
    while not dom.get_element(driver, order_selector, dont_raise=True, timeout=3):
        simulate.click(driver, element)


def open_lr_by_double_click(driver, live_report_name, exact_text_match=False):
    """
    This opens a livereport in the Metapicker by double clicking.

    :param driver: webdriver
    :param live_report_name: str, name of livereport on which to double click
    :param exact_text_match: bool, Text match to be exact ot not. Default is False
    """
    dom.click_element(driver, LIVE_REPORT_PICKER_TAB)
    dom.click_element(driver, 'a', 'All LiveReports')

    live_report_element = dom.get_element(driver,
                                          REPORT_LIST_TITLE,
                                          text=live_report_name,
                                          exact_text_match=exact_text_match)

    # This cannot be replaced with double_click as it internally also calls simulate.hover() which uses ActionChains
    # and causes issue with Firefox. In Firefox, using simulate.double_click() would throw "move target out of
    # bounds" error.
    driver.execute_script(
        """
        return (function(target) {
            if (target.fireEvent) {
                target.fireEvent('ondblclick');
            } else {
                var evObj = new MouseEvent('dblclick', {
                    bubbles: true,
                    cancelable: true,
                    view: window
                });
                target.dispatchEvent(evObj);
            }
            return true;
        })(arguments[0]);""", live_report_element)


def create_new_lr_folder(driver, folder_name):
    """
    Create a new LiveReport folder in the Metapicker with a given name. Note that a random 8-digit
    number will be appended to the end of the supplied folder_name.

    :param driver: Webdriver
    :param folder_name: str, name of the folder to be created
    :return:
    """

    sanitized_folder_name = make_unique_name(folder_name)

    dom.click_element(driver, PROJECT_HOME_NEW_FOLDER_BUTTON)
    wait.until_visible(driver, WINDOW_HEADER_TEXT, text='Create a new folder for LiveReports')

    window = dom.get_element(driver, MODAL_WINDOW)

    base.set_input_text(window, sanitized_folder_name, input_label='Folder name:')

    base.click_ok(window)

    wait.until_visible(driver, METAPICKER_FOLDER, text=sanitized_folder_name)

    return sanitized_folder_name


def create_subfolder(driver, folder_name, subfolder_name):
    """
    Creates a new LiveReport subfolder in the Metapicker. It will also create a new folder if it doesn't exist.
    Note that a random 8-digit number will be appended to the end of the provided subfolder_name.

    :param driver: Webdriver
    :param folder_name: str, name of the folder. If it doesn't exist, it will be created
    :param subfolder_name: str, name of the subfolder to be created
    :return: str, name of the subfolder created
    """
    if not dom.get_element(driver, METAPICKER_FOLDER, text=folder_name, timeout=1, dont_raise=True):
        folder_name = create_new_lr_folder(driver, folder_name)
    dom.click_element(driver, METAPICKER_FOLDER, folder_name)
    dom.click_element(driver, METAPICKER_FOLDER_MENU)
    dom.click_element(driver, MENU_ITEM, 'Create Nested Folder')

    subfolder_name = make_unique_name(subfolder_name)
    set_input_text(driver, subfolder_name, input_label='Folder name:')
    new_folder_dialog = dom.get_element(driver, MODAL_WINDOW, 'Create a new folder for LiveReports')
    dom.click_element(new_folder_dialog, OK_BUTTON)
    return subfolder_name


def delete_folder(driver, folder_name):
    """
    Deletes a folder or subfolder. Assumes the Metapicker is already open and folder/subfolder is in view.

    Note:
    - folder/subfolder can only be deleted if it is empty

    :param driver: webdriver
    :param folder_name: str, name of the folder that will be deleted
    """
    dom.click_element(driver, METAPICKER_FOLDER, folder_name)
    dom.click_element(driver, METAPICKER_FOLDER_MENU)
    dom.click_element(driver, MENU_ITEM, 'Delete Folder')
    delete_folder_dialog = dom.get_element(driver, MODAL_DIALOG, 'Confirm Delete')
    dom.click_element(delete_folder_dialog, OK_BUTTON)
    verify_is_not_visible(driver, METAPICKER_FOLDER, folder_name)


def delete_selected_live_report_via_metapicker(driver):
    """
    Deletes selected LiveReports(s) via delete option in the Metapicker.

    :param driver: Webdriver
    :return:
    """

    # Deleting the LiveReport
    dom.click_element(driver, MOVE_DELETE_BUTTON)
    dom.click_element(driver, MOVE_DELETE_BUTTON_MENU_ITEM, text='Delete')
    dialog = dom.get_element(driver, MODAL_DIALOG, text='Confirm Delete')
    click_ok(dialog)


def move_selected_live_report_to_folder(driver, destination_folder):
    """
    Move selected LiveReport(s) to a different folder using the menu item option in the Metapicker.

    :param driver: Webdriver
    :param destination_folder: str, folder to which the given LiveReport needs to be moved
    :return:
    """

    dom.click_element(driver, MOVE_DELETE_BUTTON)
    dom.click_element(driver, MOVE_DELETE_BUTTON_MENU_ITEM, text='Move to folder')
    choose_folder_for_livereport_to_move(driver, destination_folder)


def drag_drop_live_report(driver, live_report_name, destination_folder):
    """
    Simulate Drag drop action to move livereports between folders.

    :param driver: Webdriver
    :param live_report_name: str, LiveReport name
    :param destination_folder: str, folder to which the given LiveReport needs to be dragged
    :return:
    """

    # Search and click the report and then wait until it's selected before dragging and dropping
    search_for_live_report(driver, name=live_report_name)
    dom.click_element(driver, REPORT_LIST_TITLE, live_report_name)
    wait.until_visible(driver, REPORT_LIST_SELECTED_ITEM_TITLE, live_report_name)

    # TODO: Investigate why LR is not selected at 2nd instance using the live_report_element
    # live_report_element = search_for_live_report(driver, name=live_report_name)
    # dom.click_element(live_report_element, REPORT_LIST_TITLE, live_report_name)

    # Define element corresponding to LR in metapicker (this element will be dragged)
    source_element = dom.get_element(driver, REPORT_LIST_SELECTED_ITEM_TITLE, text=live_report_name)

    # Define new folder element (element where the LR will be dragged into)
    dest_element = dom.get_element(driver, METAPICKER_FOLDER_DROP_TARGET, text=destination_folder)

    # Perform drag and drop LR into MPO folder
    actions.drag_and_drop(driver, source_element, dest_element)

    # Select the source element, then make sure the selected report is in destination_folder
    simulate.click(driver, source_element)
    wait.until_visible(driver, REPORT_LIST_SELECTED_FOLDER, text=destination_folder)


def select_multiple_live_reports(driver, list_of_live_report):
    """
    Simulates selecting multiple LiveReports using combination of Control key and Click.

    :param driver: Webdriver
    :param list_of_live_report: list, List of LiveReport names to be selected
    :return:
    """

    control_key = dom.get_ctrl_key()

    for name in list_of_live_report:
        # Note we could not just use dom.get_element() here because in Firefox we get the error
        # out of bound viewport width and height. Seems like the element in not in viewable
        # range. Also tried by setting must_be_visible=False
        live_report_element = search_for_live_report(driver, name=name)
        ActionChains(driver).key_down(control_key).click(live_report_element). \
            key_up(control_key).perform()
        wait.until_visible(driver, REPORT_LIST_SELECTED_ITEM_TITLE, name)
        # Clearing the LiveReport search input
        dom.click_element(driver, REPORT_SEARCH_CROSS_MARK)


def open_merge_tool(driver):
    """
    Opens New LR Merge Tool from the metapicker. This only works if and only if two LRs are selected.

    :param driver: Selenium webdriver
    :return merge_tool_dialog_element: web element
    """

    dom.click_element(driver, MOVE_DELETE_BUTTON)
    dom.click_element(driver, MOVE_DELETE_BUTTON_MENU_ITEM, text='Merge Reports...')
    merge_tool_dialog_element = dom.get_element(driver, MERGE_LIVE_REPORTS_DIALOG)
    return merge_tool_dialog_element


def fill_details_for_new_livereport(driver,
                                    report_name='test',
                                    template='Blank',
                                    folder_name=None,
                                    lr_type='Devices',
                                    rationale=None):
    """
    Fill the details for the new LiveReport in the Create New LiveReport Dialog. The Create New LiveReport dialog
    must be open before calling this.

    :param driver: webdriver
    :param report_name: str, desired LiveReport name
    :param template: str, LiveReport Template name. Default is 'Blank',
    :param folder_name: str, desired Folder name
    :param lr_type: str, type of LiveReport: Compounds or Devices in Materials Science mode. Default is Devices
    :param rationale: str, desired default rationale for an LR
    :return: str, the actual name of the created LiveReport, with appended random number.
    """

    sanitized_name = make_unique_name(report_name)
    window = dom.get_element(driver, MODAL_WINDOW)

    base.set_input_text(window, sanitized_name, input_label=LABEL_LIVE_REPORT_NAME)

    # Selecting LiveReport Template if different from Default(Blank)
    if template != 'Blank':
        dom.click_element(window, CREATE_LIVE_REPORT_WINDOW_TEMPLATE_DROPDOWN)
        dom.click_element(driver,
                          CREATE_LIVE_REPORT_TEMPLATE_LIST,
                          text=template,
                          exact_text_match=True,
                          must_be_visible=False)

    if not folder_name:
        folder_name = 'JS Testing Home'
    # Selecting the LiveReport folder
    dom.click_element(window, CREATE_LIVE_REPORT_WINDOW_FOLDER_DOWNARROW)
    dom.click_element(driver, BOUND_LIST_ITEM, folder_name, must_be_visible=False)

    # Selecting the LiveReport Type: Compounds or Devices when in Materials Science mode
    lr_type_picker = dom.get_element(driver, LIVE_REPORT_TYPE_PICKER, timeout=0.5, dont_raise=True)
    if lr_type_picker:
        dom.click_element(driver, LIVE_REPORT_TYPE_PICKER)
        dom.click_element(driver, BOUND_LIST_ITEM, text=lr_type)

    if rationale:
        base.set_input_text(window, rationale, input_label='Default rationale (optional):')

    base.click_ok(window)

    return sanitized_name


def merge_live_reports(driver,
                       live_report_one,
                       live_report_two,
                       reference_live_report,
                       merge_type,
                       open_merged_live_report=True,
                       merged_live_report_folder=None,
                       rationale=None):
    """
    :param driver: Selenium Webdriver
    :param live_report_one: str, one of the LR to be included in the merge
    :param live_report_two: str, other LR to be included in the merge
    :param reference_live_report: int, which livereport should be reference. Eg. Reference LR is 1 if the name
                                  appears first in the merge LiveReport dialog.
    :param merge_type: str, type of merging viz. Union, Intersection, Difference
    :param open_merged_live_report: boolean, Choose True if merged LR is to be opened following the merge.
    :param merged_live_report_folder: str, folder to place the merged LiveReport.
    :param rationale: str, Rationale for the merged LR.
    :return merged_live_report_name: str, merged livereport name.
    """

    open_metapicker(driver)
    select_multiple_live_reports(driver, [live_report_one, live_report_two])
    merge_tool_dialog_element = open_merge_tool(driver)
    merged_live_report_name = set_param_for_merge_live_reports(merge_tool_dialog_element,
                                                               reference_live_report,
                                                               merge_type,
                                                               open_merged_live_report,
                                                               merged_live_report_folder,
                                                               rationale=rationale)

    return merged_live_report_name


def set_param_for_merge_live_reports(parent_element,
                                     reference_live_report,
                                     merge_type,
                                     open_merged_live_report=True,
                                     merged_live_report_folder=None,
                                     rationale=None):
    """
    :param parent_element: Selenium Webdriver
    :param reference_live_report: int, which livereport should be reference. Eg. Reference LR is 1 if the name
                                  appears first in the merge LiveReport dialog.
    :param merge_type: str, type of merging viz. Union, Intersection, Difference
    :param open_merged_live_report: boolean, Choose True if merged LR is to be opened following the merge.
    :param merged_live_report_folder: str, folder to place the merged LiveReport.
    :param rationale: str, Rationale for the merged LR.
    :return merged_live_report_name: str, merged livereport name.
    """

    # ----- CHOOSE OPTIONS FOR MERGING LIVEREPORTS ----- #
    # Choose reference LR
    dom.click_element(parent_element, MERGE_LIVE_REPORTS_REFERENCE_RADIO_.format(str(reference_live_report)))

    # Select merge type
    select.select_option_by_text(parent_element, MERGE_LIVE_REPORTS_MERGE_MODE_DROPDOWN, option_text=merge_type)

    if not open_merged_live_report:
        checkbox_label = dom.get_element(parent_element, MERGE_LIVE_REPORTS_CHECKBOX_CONTAINER_LABEL, timeout=3)
        if checkbox_label.get_attribute('checked'):
            dom.click_element(parent_element, MERGE_LIVE_REPORTS_CHECKBOX_CONTAINER_LABEL, timeout=3)
    base.click_ok(parent_element)

    driver = utils.get_driver_from_element(parent_element)
    verify_is_visible(driver, selector=WINDOW_HEADER_TEXT, selector_text=CREATE_NEW_LIVE_REPORT)

    # ----- NAMING LR AND SELECTING FOLDER FOR THE MERGE LIVEREPORT ----- #
    merged_live_report_name = fill_details_for_new_livereport(driver,
                                                              report_name="Merge-{}".format(merge_type),
                                                              folder_name=merged_live_report_folder,
                                                              rationale=rationale)

    return merged_live_report_name
