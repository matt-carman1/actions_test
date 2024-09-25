from helpers.change.actions_pane import open_sar_panel, close_sar_panel
from helpers.change.grid_row_actions import select_rows
from helpers.change.live_report_picker import open_live_report, fill_details_for_new_livereport, create_new_lr_folder
from helpers.selection.live_report_picker import METAPICKER_NEW_LIVE_REPORT_BUTTON
from helpers.change.grid_column_menu import click_column_menu_item
from helpers.verification.grid import check_for_butterbar
from library import base, dom, ensure, wait
from helpers.flows.add_compound import import_structure_into_sketcher
from helpers.selection.sar_analysis import ADD_SAR_SCAFFOLD_BUTTON, SAR_HEADER, SAR_HEADER_GEAR_BTN, \
    SAR_OPTION_DELETE
from helpers.selection.modal import MODAL_DIALOG
from helpers.selection.sketcher import SAR_SKETCHER_IFRAME


def create_sar_scaffold(driver, molv3):
    """
    Create an SAR and add it to the LR.

    :param driver: Webdriver
    :param molv3: str, molv3 string to be added to the sketcher and imported
    """

    # If the SAR sketcher is not open, open it from the SAR panel
    if not dom.get_element(driver, SAR_SKETCHER_IFRAME, timeout=2, dont_raise=True):
        open_sar_panel(driver)
        dom.click_element(driver, ADD_SAR_SCAFFOLD_BUTTON)
    import_structure_into_sketcher(driver, molv3, sketcher_iframe_selector=SAR_SKETCHER_IFRAME)
    base.click_ok(driver)
    check_for_butterbar(driver, notification_text='Scaffold addition in progress...', visible=True)
    check_for_butterbar(driver, notification_text='Scaffold addition in progress...', visible=False)

    # Close SAR Analysis Tool
    close_sar_panel(driver)


def remove_sar_scaffold(driver, name):
    """
    Remove an SAR scaffold from LR.

    :param driver: webdriver
    :param name: str, name of sar to remove
    """
    open_sar_panel(driver)
    sar_header = dom.get_element(driver, SAR_HEADER, text=name)
    ensure.element_visible(sar_header, SAR_HEADER_GEAR_BTN, SAR_OPTION_DELETE)
    dom.click_element(sar_header, SAR_OPTION_DELETE)
    base.click_ok(driver)


def save_all_r_groups(driver, r_group_column, lr_name, new_lr=False, list_of_entity_ids=[]):
    """
    This function saves R-groups from a SAR scaffold.

    :param driver: Selenium Webdriver.
    :param r_group_column: str, the name of the R-group to be saved, Ex: R1 (SAR).
    :param lr_name: str, the destination livereport where these R-groups will be saved.
    :param new_lr: boolean, True if the R-groups are going to be saved on a new LR, False for an existing LR
    :param list_of_entity_ids: list, the list of entity Ids to be selected.
    return: str, name of LiveReport R-Groups saved to
    """

    select_rows(driver, list_of_entity_ids)
    click_column_menu_item(driver, r_group_column, "Save all R-Groups")
    wait.until_visible(driver, MODAL_DIALOG)

    if new_lr:
        new_folder = create_new_lr_folder(driver, 'new_sar_folder')
        dom.click_element(driver, METAPICKER_NEW_LIVE_REPORT_BUTTON, text='New LiveReport')
        lr_name = fill_details_for_new_livereport(driver, report_name=lr_name, folder_name=new_folder)
    else:
        # This method is used to choose the LiveReport for saving the R-group. Make sure to edit this method name
        # after QA-4105 is completed.
        open_live_report(driver, lr_name)

    return lr_name
