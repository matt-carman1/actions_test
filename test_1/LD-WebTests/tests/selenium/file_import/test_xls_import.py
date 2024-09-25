import time

import pytest

from helpers.change.actions_pane import open_add_compounds_panel, close_add_compounds_panel, open_file_import_panel
from helpers.change.compound_actions import set_upload_file_path
from helpers.change.grid_column_menu import sort_grid_by
from helpers.extraction.paths import get_resource_path
from helpers.selection.add_compound_panel import IMPORT_FROM_FILE_CHECKBOX, IMPORT_FILE_BUTTON_ENABLED_STATE, \
    IMPORT_FROM_FILE_COLUMN_SELECTION_LIST_DROPDOWN
from helpers.selection.grid import Footer
from helpers.verification.grid import verify_footer_values, verify_grid_contents, check_for_notification_tip
from library import dom, select

SORT_BAR_TEXT = 'Sorting. TIP: Hold Shift while double clicking columns to add secondary sort(s).'


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
@pytest.mark.usefixtures("use_module_isolated_project")
def test_xls_import_by_id(selenium):
    """
    1. Upload the xls file using "ID" as column identifier
    2. Check for the valid file type message.
    3. Include only "Compounds"
    4. Verify footer values
    5. Verify the grid contents.

    :param selenium: Selenium Webdriver
    """

    # Opening the Compounds Menu
    open_add_compounds_panel(selenium)

    # Navigating to "IMPORT FROM FILE" accordion
    open_file_import_panel(selenium)

    # ----- TESTING XLS FILE IMPORT (COMPOUNDS ONLY BY ID) ----- #

    # Selecting a XLS file to import compounds only by ID
    file_path = get_resource_path("import_from_xls_by_id.xls")
    set_upload_file_path(selenium, file_path)

    # Added wait because xls file loading take slightly more time than other file formats.
    time.sleep(2)
    # Selecting the column, "ID", to use for XLS import
    select.select_option_by_text(selenium, IMPORT_FROM_FILE_COLUMN_SELECTION_LIST_DROPDOWN, 'ID')

    dom.click_element(selenium, IMPORT_FILE_BUTTON_ENABLED_STATE, 'Import File')

    # Sort and close compounds panel
    sort_grid_by(selenium, column_name="ID")
    close_add_compounds_panel(selenium)
    check_for_notification_tip(selenium, tip_text=SORT_BAR_TEXT, visible=False)

    # Verify footer values
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(2),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(10),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(1)
        })

    verify_grid_contents(
        selenium, {
            'Compound Structure': [
                'COC1=CC2=NC=CC(OC3=CC=C(NC4=C(NC5=CC=C(F)C=C5)C(=O)C4=O)C=C3F)=C2C=C1OC',
                'COC1=CC2=C(OC3=CC=C(NC(=O)C4(CC4)C(=O)NC4=CC=C(F)C=C4)C=C3F)C=CN=C2C=C1O'
            ],
            'ID': ['CRA-032662', 'CRA-032703'],
            'SMILES (undefined)': ['c1ccccc1(Cl)', ''],
            'STABILITY-PB-PH 7.4 (%Rem) [%]': ['77', '88'],
            'Clearance (undefined)': ['4', '7'],
            'CYP450 2C19-LCMS (%INH) [%]) [%]': ['10', '10'],
            'Solubility (undefined)': ['1', '203']
        })


@pytest.mark.app_defect(reason="SS-33646")
@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
@pytest.mark.usefixtures("use_module_isolated_project")
def test_xls_import_by_smiles(selenium):
    """
    1. Upload the xls file using "SMILES" as column identifier
    2. Check for the valid file type message.
    3. Include only "Compounds & Columns"
    4. Verify footer values
    5. Verify the grid contents.

    :param selenium: Selenium Webdriver
    """

    # Opening the Compounds Menu
    open_add_compounds_panel(selenium)

    # Navigating to "IMPORT FROM FILE" accordion
    open_file_import_panel(selenium)

    # ----- TESTING XLS FILE IMPORT (COMPOUNDS ONLY BY SMILES) ----- #

    # Selecting a XLS file to import compounds only by SMILES
    file_path = get_resource_path("import_from_xls_by_smiles.xls")
    set_upload_file_path(selenium, file_path)

    time.sleep(2)
    # Selecting the column, "SMILES", to use for XLS import
    select.select_option_by_text(selenium, IMPORT_FROM_FILE_COLUMN_SELECTION_LIST_DROPDOWN, 'SMILES')
    dom.click_element(selenium, IMPORT_FROM_FILE_CHECKBOX, text="SMILES")

    dom.click_element(selenium, IMPORT_FILE_BUTTON_ENABLED_STATE, 'Import File')

    # Sort and close compounds panel
    sort_grid_by(selenium, column_name="ID")
    close_add_compounds_panel(selenium)
    check_for_notification_tip(selenium, tip_text=SORT_BAR_TEXT, visible=False)

    # Sort and verify grid content
    sort_grid_by(selenium, column_name="ID")

    verify_grid_contents(
        selenium, {
            'Compound Structure': [
                'ClC1=CC=CC=C1', 'FC(F)(F)C1=CC(NC2=CC(NC3=CC(NC(=O)C4CC4)=CC=C3)=NC=N2)=CC=C1',
                'CCOC(=O)C1=C(C)NC(C=C2C(=O)NC3=CC=CC=C23)=C1C'
            ],
            'STABILITY-PB-PH 7.4 (%Rem) [%]': ['77', '50', '20'],
            'Clearance (undefined)': ['4', '1', '2'],
            'CYP450 2C19-LCMS (%INH) [%]) [%]': ['10', '12', '10'],
            'Solubility (undefined)': ['1', '2.5', '3']
        })
