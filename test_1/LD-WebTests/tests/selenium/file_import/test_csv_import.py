import pytest

from helpers.change import actions_pane, compound_actions, grid_column_menu, grid_columns
from helpers.extraction import paths
from helpers.selection.grid import Footer
from helpers.verification import grid
from library import dom, select
from library.utils import is_k8s
from helpers.selection.add_compound_panel import IMPORT_FROM_FILE_CHECKBOX, \
    IMPORT_FILE_BUTTON_ENABLED_STATE, IMPORT_FROM_FILE_COLUMN_SELECTION_LIST_DROPDOWN


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
@pytest.mark.usefixtures("use_module_isolated_project")
@pytest.mark.xfail(not is_k8s(), reason="SS-43040: Old data dump in old jenkins causes test to fail")
def test_csv_import(selenium):
    """
    Test importing CSV files containing structures that exist in the DB.

    First CSV import will import only compounds using the "Compound Structure" column.
    Second CSV import will import compounds and columns using the "ID" column.

    There may be app flakiness where the 'PSA (PSA)' column fails to import its data. This is tracked in
    SS-25411. A flaky or xfail mark should be added to the test if this becomes problematic.

    Verify the correct data is imported into the LR in each case
    :param selenium: Webdriver
    :return:
    """

    # Opening the Compounds Menu
    actions_pane.open_add_compounds_panel(selenium)

    # Navigating to "IMPORT" tab
    actions_pane.open_file_import_panel(selenium)

    # ----- TESTING CSV FILE IMPORT (COMPOUNDS ONLY) ----- #

    # Selecting a CSV file to import compounds only
    file_path = paths.get_resource_path("livereport_export_CSV.csv")
    compound_actions.set_upload_file_path(selenium, file_path)

    # Selecting the column, "Compound Structure", to use for CSV import
    select.select_option_by_text(selenium, IMPORT_FROM_FILE_COLUMN_SELECTION_LIST_DROPDOWN, 'Compound Structure')

    # clicking here deselects the checkbox, so we only import Compounds
    dom.click_element(selenium, IMPORT_FROM_FILE_CHECKBOX, text="SMILES")
    dom.click_element(selenium, IMPORT_FROM_FILE_CHECKBOX, text="Columns")
    dom.click_element(selenium, IMPORT_FILE_BUTTON_ENABLED_STATE, 'Import File')
    grid.check_for_butterbar(selenium, "Uploading structures from livereport_export_CSV.csv ...")

    # Check for the butter bar and wait for it to disappear, sort by ID, and then verify grid contents
    grid.check_for_butterbar(selenium, "Uploading structures from livereport_export_CSV.csv ...", visible=False)
    grid_column_menu.sort_grid_by(selenium, 'ID')
    grid.verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(2),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(5),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(1)
        })
    grid.verify_column_contents(selenium, 'ID', ['CRA-032718', 'CRA-032845'])

    # ----- TESTING CSV FILE IMPORT (COMPOUNDS AND COLUMNS) ----- #

    # Selecting another CSV file to import both "Compounds & columns"
    file_path = paths.get_resource_path("livereport_export_csv_columns.csv")
    compound_actions.set_upload_file_path(selenium, file_path)

    # Selecting the column to import from, which is "ID" in this case.
    select.select_option_by_text(selenium, IMPORT_FROM_FILE_COLUMN_SELECTION_LIST_DROPDOWN, 'ID')
    dom.click_element(selenium, IMPORT_FILE_BUTTON_ENABLED_STATE, 'Import File')
    grid.check_for_butterbar(selenium, "Uploading structures from livereport_export_csv_columns.csv ...")

    # Wait for the butter bar to disappear
    grid.check_for_butterbar(selenium, "Uploading structures from livereport_export_csv_columns.csv ...", visible=False)

    # Minimize add compounds panel for window sizing
    actions_pane.close_add_compounds_panel(selenium)

    # Checking that columns are added by scrolling to one of the column
    grid_columns.scroll_to_column_header(selenium, 'PSA (PSA)')

    # Final verification of grid contents
    grid.verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(3),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(11),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(1)
        })
    grid.verify_grid_contents(
        selenium, {
            'ID': ['CRA-031437', 'CRA-032718', 'CRA-032845'],
            'Text  - published (undefined)': ['Tom', '', ''],
            'Date String (Date String)': ['4/23/2018 20:46', '', ''],
            'PSA (PSA)': ['111', '', '']
        })
