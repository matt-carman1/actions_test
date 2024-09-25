import pytest

from helpers.change.freeform_column_action import create_ffc
from helpers.change.grid_columns import get_cell
from helpers.selection.actions_pane import REFRESH_BUTTON
from helpers.selection.freeform_columns import FreeformColumnCellEdit
from helpers.selection.modal import MODAL_WINDOW
from helpers.verification.data_and_columns_tree import verify_no_column_exists_in_column_tree
from helpers.verification.element import verify_is_visible
from library import dom, simulate, base, wait

# LiveReport to be duplicated for the test
live_report_to_duplicate = {'livereport_name': 'File FFC Selenium Test LR', 'livereport_id': '2300'}


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_ffc_unpublished_file(selenium):
    """
    Test File type Unpublished FFC.
    1. Create a File type Unpublished FFC
    2. Check for existing File FFC w.r.t to buttons available on hover over. The uploads should
    show up.
    Note: Since it is difficult to simulate uploading a file for FFC using existing Selenium
    Architecture, we would be testing on an already existing File type Unpublished FFC.

    :param selenium: Webdriver
    :return:
    """

    # ----- Test with an existing File Type FFC Columns 'Test File' ----- #

    # Check for 'Upload File' link for V041170
    ffc_cell_no_file = get_cell(selenium, 'V041170', 'Test File')
    simulate.hover(selenium, ffc_cell_no_file)
    verify_is_visible(ffc_cell_no_file,
                      FreeformColumnCellEdit.FILE_FFC_ATTACHMENT_ICON,
                      selector_text='Upload File',
                      message='FFC with no attachment should have a link to Upload File. ')

    # .svg upload should show attachment icon and not the image without hovering over.
    ffc_cell_svg_file = get_cell(selenium, 'V052298', 'Test File')
    verify_is_visible(ffc_cell_svg_file,
                      FreeformColumnCellEdit.FILE_FFC_ATTACHMENT_ICON_HAS_ATTACHMENT.format('410.svg'))

    # All files apart from .png or .jpeg files should show attachment icon without hovering over.
    ffc_cell_pdf_file = get_cell(selenium, 'V047121', 'Test File')
    verify_is_visible(ffc_cell_pdf_file,
                      FreeformColumnCellEdit.FILE_FFC_ATTACHMENT_ICON_HAS_ATTACHMENT.format('genscan_ciona.pdf'))

    # Check for image attachment in FFC.
    ffc_cell_image_file = get_cell(selenium, 'V053230', 'Test File')
    verify_is_visible(ffc_cell_image_file, FreeformColumnCellEdit.FILE_FFC_ATTACHMENT_ICON_HAS_ATTACHMENT_IMAGE)

    # Check File FFC edit, delete and popout icon visible
    ffc_cell_button_tray = dom.get_element(ffc_cell_image_file, FreeformColumnCellEdit.FILE_FFC_BUTTON_TRAY)
    simulate.hover(selenium, ffc_cell_button_tray)
    verify_is_visible(ffc_cell_image_file,
                      FreeformColumnCellEdit.FILE_FFC_PENCIL_ICON,
                      message='FFC cell with uploaded file should have an edit pencil icon. ')
    verify_is_visible(ffc_cell_image_file,
                      FreeformColumnCellEdit.FILE_FFC_DELETE_ICON,
                      message='FFC cell with uploaded file should have a delete icon to delete the uploaded file. ')
    verify_is_visible(ffc_cell_image_file,
                      FreeformColumnCellEdit.FILE_FFC_POP_OUT_ICON,
                      message='FFC cell with uploaded file should have a popout option. ')

    # Delete the .png file for V053230
    dom.click_element(ffc_cell_image_file, FreeformColumnCellEdit.FILE_FFC_DELETE_ICON)
    wait.until_visible(selenium, MODAL_WINDOW)
    base.click_ok(selenium)

    # Verify that the image is deleted
    simulate.hover(selenium, ffc_cell_image_file)
    verify_is_visible(ffc_cell_image_file,
                      FreeformColumnCellEdit.FILE_FFC_ATTACHMENT_ICON,
                      selector_text='Upload File',
                      message='FFC with no attachment should have a link to Upload File. ')

    # ----- Create a new Unpublished File type FFC and test ----- #
    create_ffc(selenium,
               column_name='Unpublished File FFC',
               description='File Type Unpublished FFC',
               column_type='File / Image')

    # verify column contents for 'Unpublished File FFC column for one of the compound
    ffc_cell_no_file = get_cell(selenium, 'V041170', 'Unpublished File FFC')
    simulate.hover(selenium, ffc_cell_no_file)
    verify_is_visible(ffc_cell_no_file,
                      FreeformColumnCellEdit.FILE_FFC_ATTACHMENT_ICON,
                      selector_text='Upload File',
                      message='FFC with no attachment should have a link to Upload File. ')

    # Search D&C tree for FFC column name (Since this is unpublished, it should only exist in the context of the LR
    # and never show up in the Data and Columns Tree.)
    verify_no_column_exists_in_column_tree(selenium, 'Unpublished File FFC')

    # Refresh the LR and verify 'Test File' FFC content for one of the row/compound.
    dom.click_element(selenium, REFRESH_BUTTON)
    ffc_cell_pdf_file = get_cell(selenium, 'V047121', 'Test File')
    verify_is_visible(ffc_cell_pdf_file,
                      FreeformColumnCellEdit.FILE_FFC_ATTACHMENT_ICON_HAS_ATTACHMENT.format('genscan_ciona.pdf'))
