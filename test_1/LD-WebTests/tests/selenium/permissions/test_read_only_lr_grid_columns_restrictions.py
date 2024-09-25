import pytest

from helpers.change.live_report_menu import make_live_report_read_only
from helpers.change.grid_columns import get_cell
from helpers.change.grid_column_menu import freeze_a_column_via_menu_option, open_column_menu
from helpers.change.live_report_picker import open_live_report
from helpers.change.project import open_project
from helpers.selection.grid import GRID_HEADER_CELL, GRID_COLUMN_HEADER_SORT_ICON_, GRID_FOOTER_COLUMN_HIDDEN_LINK
from helpers.selection.freeform_columns import FreeformColumnCellEdit
from helpers.selection.sar_analysis import SAR_MATCH_SCAFFOLD_LINK
from helpers.selection.data_and_columns import RATIONALE_EDIT_ICON
from helpers.verification.features_enabled_disabled import verify_menu_items_are_disabled
from helpers.verification.element import verify_is_not_visible, verify_is_visible
from library.authentication import logout, login
from library import simulate, dom, wait

live_report_to_duplicate = {'livereport_name': 'Read Only Selenium Test LR', 'livereport_id': '2303'}
test_report_name = 'test_read_only_LR_grid_column'


def test_read_only_lr_grid_columns_restrictions(selenium, duplicate_live_report, open_livereport):
    """
    Tests permissions and features in the columns of a Read-only LiveReport.
    1. Create a Read only LR.
    2. Freeze a column.
    3. Validate that a non-admin non-owner cannot:
        a) Sort a column.
        c) Edit all types FFCs
        b) Edit rationale
        d) Edit SAR column.
        e) Unfreeze a column
        e) See links for hidden Columns in footer.

    :param selenium: Webdriver
    :return:
    """

    # Getting Duplicate LR name
    read_only_lr = duplicate_live_report

    # Make the Live report as read only
    make_live_report_read_only(selenium, read_only_lr)

    # Freezing a column
    freeze_a_column_via_menu_option(selenium, 'PK_PO_RAT (AUC) [uM]')
    wait.until_extjs_loading_mask_not_visible(selenium)

    logout(selenium)

    # Login with a non-admin non-owner user and open read only LR
    login(selenium, uname='userB', pword='userB')
    open_project(selenium)
    open_live_report(selenium, name=read_only_lr)

    # ----- Validate that Sorting is not possible by a non-admin non-owner ----- #
    get_assay_element = dom.get_element(selenium, GRID_HEADER_CELL, text='PK_PO_RAT (AUC) [uM]')
    simulate.double_click(get_assay_element)
    verify_is_not_visible(selenium, GRID_COLUMN_HEADER_SORT_ICON_.format('ASC'))

    # ----- Validate that editing all types of FFC is not permitted by a non-admin non-owner ----- #
    # Check Unpublished FFC edit icon is disabled
    ffc_cell_unpublished = get_cell(selenium, 'V035625', 'Unpublished Freeform Text Column')
    simulate.hover(selenium, ffc_cell_unpublished)
    verify_is_not_visible(ffc_cell_unpublished,
                          FreeformColumnCellEdit.FFC_EDIT_ICON,
                          message='FFC EDIT ICON for Unpublished FFC should not be visible.')

    # Check Published FFC edit icon is disabled
    ffc_cell = get_cell(selenium, 'V035625', 'Published Freeform Text Column')
    simulate.hover(selenium, ffc_cell)
    verify_is_not_visible(ffc_cell,
                          FreeformColumnCellEdit.FFC_EDIT_ICON,
                          message='FFC EDIT ICON for Published FFC should not be visible.')

    # Check File FFC Upload Link is not visible
    file_ffc_cell = get_cell(selenium, 'V055682', 'File FFC')
    simulate.hover(selenium, file_ffc_cell)
    verify_is_not_visible(file_ffc_cell,
                          FreeformColumnCellEdit.FILE_FFC_ATTACHMENT_ICON,
                          selector_text='Upload File',
                          message='UPLOAD FILE LINK for File type FFC should not be visible')

    # Check File FFC edit and delete tray icon is not visible but popout icon is visible
    ffc_cell_with_uploaded_file = get_cell(selenium, 'V035625', 'File FFC')
    ffc_button_tray = dom.get_element(ffc_cell_with_uploaded_file, FreeformColumnCellEdit.FILE_FFC_BUTTON_TRAY)
    simulate.hover(selenium, ffc_button_tray)
    verify_is_not_visible(ffc_cell_with_uploaded_file,
                          FreeformColumnCellEdit.FILE_FFC_PENCIL_ICON,
                          message='Uploaded file in FFC cannot be edited')
    verify_is_not_visible(ffc_cell_with_uploaded_file,
                          FreeformColumnCellEdit.FILE_FFC_DELETE_ICON,
                          message='Deleting an existing file in FFC is not allowed')
    verify_is_visible(ffc_cell_with_uploaded_file,
                      FreeformColumnCellEdit.FILE_FFC_POP_OUT_ICON,
                      message='Pop out icon for the File in FFC should be visible')

    # ----- Validate that Editing a Rationale is not permitted by a non-admin non-owner ----- #
    rationale_cell = get_cell(selenium, 'V035625', 'Rationale')
    simulate.hover(selenium, rationale_cell)
    verify_is_not_visible(rationale_cell, RATIONALE_EDIT_ICON, message='RATIONALE EDIT ICON should not be visible.')

    # ----- Validate that editing SAR columns is not allowed for a non-admin non-user ----- #
    r1_sar_cell = get_cell(selenium, 'V055682', 'R1 (SAR)')
    simulate.hover(selenium, r1_sar_cell)
    verify_is_not_visible(r1_sar_cell,
                          SAR_MATCH_SCAFFOLD_LINK,
                          selector_text='Match another scaffold',
                          message='MATCH ANOTHER SCAFFOLD link should not be visible and click-able.')

    # ----- Validate columns can't be unfrozen ----- #
    # Check that the Unfreeze Column option is disabled
    open_column_menu(selenium, column_name='PK_PO_RAT (AUC) [uM]')
    verify_menu_items_are_disabled(selenium, 'Unfreeze')

    # Cannot see links for hidden Columns in footer
    verify_is_not_visible(selenium, GRID_FOOTER_COLUMN_HIDDEN_LINK, selector_text='7 Hidden')
