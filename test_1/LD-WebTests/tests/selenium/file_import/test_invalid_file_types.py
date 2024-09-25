import pytest

from helpers.change import actions_pane, compound_actions
from helpers.extraction import paths
from helpers.selection.add_compound_panel import IMPORT_FILE_BUTTON_DISABLED_STATE, ERROR_DIALOG_TEXT, \
    ERROR_DIALOG_OK_BUTTON
from library import dom, wait


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_pdf_jpeg_import(selenium):
    """
    Testing importing of invalid file types. Checks if:
    1. files can be selected and added from the local machine
    2. PDF & JPEG are invalid file types for importing and import button is disabled

    :param selenium: Webdriver
    :return:
    """

    # Opening the Compounds Menu
    actions_pane.open_add_compounds_panel(selenium)

    # Navigating to the "IMPORT FROM FILE" accordion
    actions_pane.open_file_import_panel(selenium)

    # ----- TESTING PDF FILE IMPORT ----- #

    # Selecting a PDF file to upload
    file_path = paths.get_resource_path("livereport_export_importtestPDF.pdf")
    compound_actions.set_upload_file_path(selenium, file_path)

    # Verifying that the correct invalid file type message appears and that the import button is disabled
    wait.until_visible(selenium,
                       ERROR_DIALOG_TEXT,
                       text="Invalid file type. Must be sdf, csv (.csv or .txt), Excel (.xls or .xlsx) or Maestro "
                       "(.mae, .mae.gz or .maegz).")
    dom.click_element(selenium, ERROR_DIALOG_OK_BUTTON)
    dom.get_element(selenium, IMPORT_FILE_BUTTON_DISABLED_STATE, text="Import File")

    # ----- TESTING JPEG FILE (IMAGE) IMPORT ----- #

    # Repeating file upload and verification steps for a JPEG file below
    file_path = paths.get_resource_path("CHEMBL103.jpeg")
    compound_actions.set_upload_file_path(selenium, file_path)
    wait.until_visible(selenium,
                       ERROR_DIALOG_TEXT,
                       text="Invalid file type. Must be sdf, csv (.csv or .txt), Excel (.xls or .xlsx) or Maestro "
                       "(.mae, .mae.gz or .maegz).")
    dom.click_element(selenium, ERROR_DIALOG_OK_BUTTON)
    dom.get_element(selenium, IMPORT_FILE_BUTTON_DISABLED_STATE, text="Import File")
