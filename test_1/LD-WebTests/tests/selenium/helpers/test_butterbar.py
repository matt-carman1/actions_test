import pytest

from helpers.change import actions_pane, live_report_picker, live_report_menu, compound_actions
from helpers.extraction import paths
from helpers.selection.add_compound_panel import IMPORT_FROM_FILE_CHECKBOX, IMPORT_FILE_BUTTON_ENABLED_STATE
from helpers.selection.grid import GRID_PROGRESS_NOTIFICATION, Footer
from helpers.selection.modal import MODAL_DIALOG_HEADER, OK_BUTTON, COPY_LR_TO_PROJECT_LIST
from helpers.selection.project import PROJECT_TITLE
from library import dom, wait
from helpers.verification import grid
from helpers.flows import add_compound
from library.select import select_option_by_text


@pytest.mark.usefixtures("open_project")
def test_butterbar(selenium):
    """
    Test the appearance and disappearance of butter while performing the
    following:
    1. Importing a file into LD.
    2. Adding compound through search by ID.
    3. Copying the LR to a different project.
    Success of each of these tasks are verified based on some parameters
    only when the butterbar disappears.
    All this is based on manual observation as well.

    :param selenium: Selenium Webdriver
    :return:
    """

    # this is used instead of the fixture as we require the LR name. Since
    # fixtures doesn't return the LR name(AFAIK) this function was called
    # explicitly.
    lr_name = live_report_picker.create_and_open_live_report(selenium, "test_butterbar")

    # TESTING BUTTER WHEN IMPORTING A FILE INTO LD
    # Opening the Compounds Menu and switching to Import from File accordion
    actions_pane.open_add_compounds_panel(selenium)
    actions_pane.open_file_import_panel(selenium)
    # Importing .sdf file
    # This(os.path.join) would make the code pick the correct path in all
    # browsers and OSes as behavior of browser or OS may vary when using forward
    # or back slash
    file_path = paths.get_resource_path("livereport_import_SDF.sdf")
    compound_actions.set_upload_file_path(selenium, file_path)

    # Deselect "Columns" checkbox so that we import only Compounds
    dom.click_element(selenium, IMPORT_FROM_FILE_CHECKBOX, text='Columns')
    dom.click_element(selenium, IMPORT_FILE_BUTTON_ENABLED_STATE, 'Import File')
    grid.check_for_butterbar(selenium, "Uploading structures from " "livereport_import_SDF.sdf ...")
    grid.check_for_butterbar(selenium, "Uploading structures from livereport_import_SDF.sdf ...", visible=False)
    grid.verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(7)})

    # TESTING BUTTERBAR FOR SEARCH BY COMPOUND ID
    search_keyword = "CHEMBL105*,CHEMBL103*"
    # Search Compounds by ID
    add_compound.search_by_id(selenium, search_keyword)
    grid.check_for_butterbar(selenium, "Compound search in progress...")
    grid.check_for_butterbar(selenium, "Updating LiveReport...")
    grid.check_for_butterbar(selenium, "Updating LiveReport...", visible=False)
    grid.verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(29)})

    # TESTING BUTTERBAR FOR COPY TO PROJECT
    live_report_menu.click_live_report_menu_item(selenium, lr_name, "Copy to Project")
    wait.until_visible(selenium, MODAL_DIALOG_HEADER, text="Copy LiveReport to Another Project")
    # Choose the project from the dialog to copy the LR to.
    select_option_by_text(selenium, COPY_LR_TO_PROJECT_LIST, 'CMET')
    dom.click_element(selenium, OK_BUTTON)
    # Checking for relevant butterbars
    grid.check_for_butterbar(selenium, "Copying LiveReport...")
    grid.check_for_butterbar(selenium, "LiveReport has been copied.\nGo to copied LiveReport")
    # Navigate to the copied LR in another project
    dom.click_element(selenium, GRID_PROGRESS_NOTIFICATION + ' a', text="Go to copied LiveReport")
    grid.check_for_butterbar(selenium, "LiveReport has been copied.", visible=False)
    # Asserting that the project has been switched
    assert dom.get_element(selenium, PROJECT_TITLE, text="CMET")
