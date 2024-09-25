import pytest

from helpers.change import actions_pane, compound_actions, grid_column_menu
from helpers.extraction import paths
from helpers.selection.grid import Footer
from helpers.verification import grid
from library import dom, wait
from library.utils import is_k8s
from helpers.selection.add_compound_panel import IMPORT_FROM_FILE_CHECKBOX, IMPORT_FILE_BUTTON_ENABLED_STATE


@pytest.mark.smoke
@pytest.mark.usefixtures("use_module_isolated_project")
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
@pytest.mark.xfail(not is_k8s(), reason="SS-43040: Old data dump in old jenkins causes test to fail")
def test_sdf_mae_import(selenium):
    """
    Test file importing of structures that already exist in the DB. Checks if:
    1. files can be selected and added from the local machine
    2. SDF & MAE are valid file types for importing and compounds are imported to LD

    :param selenium: Webdriver
    :return:
    """

    # Opening the Compounds Menu
    actions_pane.open_add_compounds_panel(selenium)

    # Navigating to the "IMPORT FROM FILE" accordion
    actions_pane.open_file_import_panel(selenium)

    # ----- TESTING SDF FILE IMPORT ----- #

    # This (os.path.join) will pick the correct path to upload local files across OS in all browsers
    # Behavior of tbe browser or OS may vary depending on whether forward or backslash is used
    file_path = paths.get_resource_path("livereport_export_SDF.sdf")

    # Calling the helper to set the upload file path
    compound_actions.set_upload_file_path(selenium, file_path)

    # Deselect "Columns" checkbox so that we import only Compounds
    dom.click_element(selenium, IMPORT_FROM_FILE_CHECKBOX, text="Columns")

    # Importing the file by clicking the "Import file" button
    dom.click_element(selenium, IMPORT_FILE_BUTTON_ENABLED_STATE, text='Import File')

    # Checking for the butter bar and wait for it to disappear, sort the grid by ID, and then verifying grid contents
    grid.check_for_butterbar(selenium, "Uploading structures from livereport_export_SDF.sdf ...")
    grid.check_for_butterbar(selenium, "Uploading structures from livereport_export_SDF.sdf ...", visible=False)
    grid_column_menu.sort_grid_by(selenium, 'ID')
    wait.until_loading_mask_not_visible(selenium)
    grid.verify_column_contents(selenium, 'ID', ['CHEMBL1031', 'CRA-031925'])

    # Verify footer values
    grid.verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(2),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(5),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(1)
        })

    # ----- TESTING MAE FILE IMPORT ----- #

    # repeating SDF importing steps above for a MAE file
    file_path = paths.get_resource_path("import_test_mae.mae")
    compound_actions.set_upload_file_path(selenium, file_path)
    dom.click_element(selenium, IMPORT_FROM_FILE_CHECKBOX, text="Columns")
    dom.click_element(selenium, IMPORT_FILE_BUTTON_ENABLED_STATE, 'Import File')

    # Checking for the butter bar and wait for it to disappear, sort the grid by ID, and then verifying grid contents
    grid.check_for_butterbar(selenium, "Uploading structures from import_test_mae.mae ...")
    grid.check_for_butterbar(selenium, "Uploading structures from import_test_mae.mae ...", visible=False)
    grid.verify_column_contents(selenium, 'ID', ['CHEMBL1031', 'CRA-031925', 'V047002'])
    grid.verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(3),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(5),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(1)
        })
