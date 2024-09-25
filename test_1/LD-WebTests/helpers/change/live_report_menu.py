from helpers.change.menus import click_submenu_option
from helpers.extraction.live_report import get_active_live_report_name
from helpers.selection.grid import GRID_PROGRESS_NOTIFICATION
from helpers.selection.live_report_menu import LIVEREPORT_DROPDOWN_MENU
from helpers.selection.general import MENU_ITEM
from helpers.selection.live_report_tab import PRIVATE_ICON, SHORTCUT_PENDING, TAB, TAB_ACTIVE, TAB_DOWNARROW, TAB_NAMED_
from helpers.selection.modal import MODAL_DIALOG_HEADER, LR_RENAME_DIALOG_INPUT, WINDOW_HEADER_TEXT_DEFAULT, \
    WINDOW_HEADER_TEXT, MODAL_WINDOW, MODAL_DIALOG_HEADER_LABEL, COPY_LR_TO_PROJECT_LIST
from helpers.selection.template import NEW_TEMPLATE_NAME, LIVE_REPORT_TEMPLATE_LIST
from helpers.verification.grid import check_for_butterbar
from library import base, dom, simulate, utils, wait
from library.select import select_option_by_text


def close_live_report(driver, live_report_name):
    """
    Closes an open LiveReport
    :param driver: Webdriver
    :param live_report_name: LiveReport name, to be closed
    :return:
    """
    switch_to_live_report(driver, live_report_name)
    # Wait for the grid to switch to the new LR (not just the tab)
    # TODO (jordan) come up with a better way to wait on the grid to switch
    wait.sleep_if_k8s(1)
    click_live_report_menu_item(driver, live_report_name, 'Close', exact_text_match=True)
    wait.until_not_visible(driver, TAB, live_report_name)


def delete_open_live_report(driver, live_report_name):
    """
    Delete a open LiveReport
    :param driver: Webdriver
    :param live_report_name: LiveReport name, to be deleted
    :return:
    """
    switch_to_live_report(driver, live_report_name)
    click_live_report_menu_item(driver, live_report_name, 'Delete')
    base.click_ok(driver)


def make_live_report_read_only(driver, live_report_name):
    """
    Make a LiveReport Read-only
    :param driver: Webdriver
    :param live_report_name: LiveRport name, to be made read-only
    :return:
    """
    dom.click_element(driver, TAB, live_report_name)
    wait.until_visible(driver, TAB_ACTIVE, live_report_name)
    click_live_report_menu_item(driver, live_report_name, 'Make Read-Only')
    base.click_ok(driver)


def open_live_report_menu(driver, live_report_name):
    """
    Opens LiveReport menu only. Make sure to switch to the correct LR before calling this.
    :param driver: Webdriver
    :param live_report_name: str, LiveReport name
     """
    tab = get_live_report_tab(driver, live_report_name)
    dom.click_element(tab, TAB_DOWNARROW)
    simulate.hover(driver, tab)
    wait.until_visible(driver, LIVEREPORT_DROPDOWN_MENU)


def click_live_report_menu_item(driver, live_report_name, item_name, sub_menu=None, exact_text_match=False):
    """
    Opens LiveReport menu and selects the desired item. Make sure to switch to the correct LR before calling this.
    :param driver: Webdriver
    :param live_report_name: str, LiveReport name
    :param item_name: str, menu item name to be selected
    :param sub_menu: str, sub-menu item to be selected
    :param exact_text_match: bool, whether to match the menu item exactly
    """
    open_live_report_menu(driver, live_report_name)
    if sub_menu:
        click_submenu_option(driver, item_name, sub_menu)
    else:
        dom.click_element(driver, MENU_ITEM, item_name, exact_text_match=exact_text_match)


def make_live_report_hidden(driver, live_report_name):
    """
    Makes a LiveReport hidden
    :param driver: Webdriver
    :param live_report_name: LiveReport, to be made hidden
    :return:
    """
    switch_to_live_report(driver, live_report_name)
    click_live_report_menu_item(driver, live_report_name, 'Make Hidden')
    base.click_ok(driver)

    tab = get_live_report_tab(driver, live_report_name)
    wait.until_visible(tab, PRIVATE_ICON)


def make_live_report_visible(driver, live_report_name):
    """
    Converts a hidden LiveReport to a visible LiveReport
    :param driver: Webdriver
    :param live_report_name: LiveReport, to be made visible
    :return:
    """
    switch_to_live_report(driver, live_report_name)
    click_live_report_menu_item(driver, live_report_name, 'Make Visible')
    base.click_ok(driver)

    tab = get_live_report_tab(driver, live_report_name)
    wait.until_not_visible(tab, PRIVATE_ICON)


def switch_to_live_report(driver, live_report_name, exact_text_match=True):
    """
    Switches to a given open LiveReport tab
    :param exact_text_match: (Optional) If True, the function will perform an exact text match when identifying the
        LiveReport tab. If False, it will use a partial text match.
    :type exact_text_match: bool, optional
    :param driver: Webdriver
    :param live_report_name: LiveReport Name, to switch to.
    :return:
    """
    wait.until_visible(driver, TAB_ACTIVE)
    current_live_report = dom.get_element(driver, TAB_ACTIVE).text
    if current_live_report != live_report_name:
        dom.click_element(driver, TAB, live_report_name, exact_text_match=exact_text_match)
        wait.until_visible(driver, f"{TAB_ACTIVE}{TAB_NAMED_.format(live_report_name)} {TAB_DOWNARROW}")
        wait.until_not_visible(driver, SHORTCUT_PENDING)


def rename_a_live_report(driver, live_report_name, new_name_for_live_report):
    """
    Rename a LiveReport to a new Desired name
    :param driver: Selenium Webdriver
    :param live_report_name: str, LiveReport name to be renamed
    :param new_name_for_live_report: str, LiveReport will be renamed to this string value.
    :return:
    """

    switch_to_live_report(driver, live_report_name)
    click_live_report_menu_item(driver, live_report_name, 'Rename…')
    wait.until_visible(driver, MODAL_DIALOG_HEADER, text='Rename LiveReport')

    dom.set_element_value(driver, LR_RENAME_DIALOG_INPUT, value=new_name_for_live_report)
    base.click_ok(driver)


def save_as_new_template(driver, template_name='', live_report_name='', exact_text_match=True):
    """
    Save a template for a given LiveReport with a random name.

    :param exact_text_match: (Optional) If True, the function will perform an exact text match when identifying the
                             LiveReport tab. If False, it will use a partial text match.
    :type exact_text_match: bool, optional
    :param driver: Selenium Webdriver
    :param template_name: str, name for new template being created.
                            If not provided, will be set to the active LiveReport's name.
                            Will append a random number to the name.
    :param live_report_name: str, LiveReport tab to switch to.
    :return: str, name of the template created
    """
    if not live_report_name:
        live_report_name = get_active_live_report_name(driver)
    if not template_name:
        template_name = live_report_name
    template_name = utils.make_unique_name(template_name)
    # Creating a random template name from the LiveReport name

    switch_to_live_report(driver, live_report_name, exact_text_match)
    click_live_report_menu_item(driver, live_report_name, item_name='Manage Templates', sub_menu='Save as New...')
    wait.until_visible(driver, WINDOW_HEADER_TEXT, text='Create New Template')
    dom.set_element_value(driver, NEW_TEMPLATE_NAME, value=template_name)
    base.click_ok(driver)
    check_for_butterbar(driver, notification_text="Creating New Template {}".format(template_name))
    check_for_butterbar(driver, notification_text="Creating New Template {}".format(template_name), visible=False)
    return template_name


def open_delete_template_dialog(driver, live_report_name=''):
    """
    Opens the "Delete Existing Template" dialog for the current active (or named) LiveReport.

    :param driver: Selenium Webdriver
    :param live_report_name: str, LiveReport name. Default value is the current active LiveReport
    """
    if not live_report_name:
        live_report_name = get_active_live_report_name(driver)
    click_live_report_menu_item(driver, live_report_name, item_name='Manage Templates', sub_menu='Delete...')
    wait.until_visible(driver, MODAL_DIALOG_HEADER, text='Delete Existing Template')


def delete_template(driver, template_name, live_report_name=''):
    """
    Delete a LiveReport template.

    :param driver: Selenium Webdriver
    :param template_name: str, template name
    :param live_report_name: str, LiveReport name. Default value is the current active LiveReport
    """
    delete_dialog_header_text = 'Confirm Delete Existing Template'

    open_delete_template_dialog(driver, live_report_name)
    # Open dropdown and select 1st item in list that matches template name provided
    # todo: investigate flakiness with opening dropdown. No selector for down arrow.
    element = dom.get_elements(driver, LIVE_REPORT_TEMPLATE_LIST, text=template_name)[0]
    # simulate.click(driver, element) fails with `javascript error: Cannot read property 'left' of undefined`
    element.click()

    # Click OK buttons to delete template
    # note: first OK click fails if dropdown covers OK button.
    base.click_ok(driver)
    wait.until_visible(driver, MODAL_DIALOG_HEADER, text=delete_dialog_header_text)
    base.click_ok(driver)
    wait.until_not_visible(driver, MODAL_DIALOG_HEADER, text=delete_dialog_header_text)


def open_change_project_default_template_dialog(driver, live_report_name=''):
    """
    Opens the "Change Project Default" dialog for the current active (or named) LiveReport.

    :param driver: Selenium Webdriver
    :param live_report_name: str, LiveReport name. Default value is the current active LiveReport
    """
    if not live_report_name:
        live_report_name = get_active_live_report_name(driver)
    click_live_report_menu_item(driver,
                                live_report_name,
                                item_name='Manage Templates',
                                sub_menu='Change Project '
                                'Default...')
    wait.until_visible(driver, WINDOW_HEADER_TEXT_DEFAULT, text='Change Project Default...')


def change_project_default_template(driver, template_name, live_report_name=''):
    """
    Change the project default template.

    :param driver: Selenium Webdriver
    :param template_name: str, template name
    :param live_report_name: str, LiveReport name. Default value is the current active LiveReport
    """
    open_change_project_default_template_dialog(driver, live_report_name)

    # Open dropdown and select 1st item in list that matches template name provided
    dom.click_element(driver, '.x-trigger-index-0')
    dom.click_element(driver, '.x-boundlist-item', text=template_name)
    base.click_ok(driver)


def open_overwrite_existing_template_dialog(driver, live_report_name=''):
    """
    Opens the "Overwrite Existing Template" dialog for the current active (or named) LiveReport.

    :param driver: Selenium Webdriver
    :param live_report_name: str, LiveReport name. Default value is the current active LiveReport
    """
    if not live_report_name:
        live_report_name = get_active_live_report_name(driver)
    click_live_report_menu_item(driver,
                                live_report_name,
                                item_name='Manage Templates',
                                sub_menu='Overwrite '
                                'Existing...')
    wait.until_visible(driver, MODAL_DIALOG_HEADER, text='Overwrite Existing Template')


def overwrite_existing_template(driver, template_name, live_report_name=''):
    """
    Overwrite an existing template.

    :param driver: Selenium Webdriver
    :param template_name: str, template name
    :param live_report_name: str, LiveReport name. Default value is the current active LiveReport
    """
    open_overwrite_existing_template_dialog(driver, live_report_name)

    # Open dropdown and select 1st item in list that matches template name provided
    element = dom.get_elements(driver, LIVE_REPORT_TEMPLATE_LIST, text=template_name)[0]
    # element = dom.get_elements(driver, '.live-report-menu select option', text=template_name)[0]
    element.click()
    base.click_ok(driver)
    # confirm overwrite
    base.click_ok(driver)


def choose_folder_for_livereport_to_move(driver, folder_name):
    window = dom.get_element(driver, MODAL_WINDOW, text='Move LiveReport to Folder')
    dom.click_element(window, '[id="tags-for-move-live-report-folder-triggerWrap"] ' '.x-trigger-index-0')
    dom.click_element(driver, '.x-list-plain li.x-boundlist-item', text=folder_name)
    base.click_ok(window)


def open_export_dialog_from_lr_dropdown(driver, livereport, file_format):
    """
    Function to open export dialog from LR dropdown

    :param driver: Selenium webdriver
    :param livereport: LiveReport Name
    :param file_format: str, Format of the output file
    """
    open_live_report_menu(driver, livereport)
    click_submenu_option(driver, item_name='Export Report', submenu_item=file_format, exact_text_match=True)


def get_live_report_tab(driver, live_report_name):
    """
    Gets the tab element for a LiveReport
    :param driver: Webdriver
    :param live_report_name: str, LiveReport name
    """
    tab_selector = TAB_NAMED_.format(live_report_name)
    return dom.get_element(driver, tab_selector)


def copy_live_report_to_project(driver, project_name, live_report_name, open_lr=False):
    """
    Copy a LiveReport to another project
    :param driver: Webdriver
    :param project_name: str, project name to be copied to
    :param live_report_name: str, LiveReport name
    :param open_lr: boolean,True if open copied LiveReport; Default value is False
    :return:
    """
    click_live_report_menu_item(driver, live_report_name, item_name='Copy to Project...')
    wait.until_visible(driver, MODAL_DIALOG_HEADER_LABEL, text="Copy LiveReport to Another Project")
    dom.click_element(driver, COPY_LR_TO_PROJECT_LIST)
    select_option_by_text(driver, COPY_LR_TO_PROJECT_LIST, project_name)
    base.click_ok(driver)

    if open_lr:
        wait.until_visible(driver, GRID_PROGRESS_NOTIFICATION + ' a', text="Go to copied LiveReport")
        dom.click_element(driver, GRID_PROGRESS_NOTIFICATION + ' a', text="Go to copied LiveReport")
