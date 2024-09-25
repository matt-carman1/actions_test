import pytest
from helpers.change.grid_column_menu import click_column_menu_item, open_column_menu
from helpers.change.live_report_menu import switch_to_live_report
from helpers.change.live_report_picker import open_live_report
from helpers.flows.live_report_management import copy_active_live_report
from helpers.selection.assay import ASSAY_PROJECT_LEVEL_NAME_TEXT_BOX, ASSAY_PROJECT_LEVEL_NAME_RESET_BUTTON, \
    ASSAY_LR_LEVEL_NAME_CHECKBOX, ASSAY_LR_LEVEL_NAME_TEXT_BOX
from helpers.verification.data_and_columns_tree import verify_no_column_exists_in_column_tree
from library import base, dom

# Enable the LR column alias so that the "Use LiveReport alias" checkbox appears
# in the Column Details window. (This also should put the test into serial mode
# b/c it has a custom server configuration, which is good since a change in
# assay name across the project could interfere with other tests.)
LD_PROPERTIES = {'ENABLE_LIVE_REPORT_COLUMN_ALIAS': 'true'}


@pytest.mark.app_defect(reason="SS-32648: Flaky Test on master")
@pytest.mark.usefixtures("open_project")
@pytest.mark.usefixtures("customized_server_config")
def test_rename_assay_column(selenium):
    """
    Test renaming an assay column
    1. Open a LR with compounds and an assay column
    2. Change the name of an assay across the entire project
    3. Verify the name of the column has changed in a different LR
    4. Change the name within a single LR
    5. Verify that the name is changed in the LR
    6. Verify that the name has not changed in a different LR

    :param selenium: Selenium Webdriver
    """

    # Set name of LiveReport that will be duplicated
    live_report_to_duplicate = "5 Compounds 4 Assays"
    open_live_report(selenium, name=live_report_to_duplicate)

    # Duplicate Live Report
    duplicate_live_report = copy_active_live_report(selenium, live_report_name=live_report_to_duplicate)

    # -- Rename an assay column for the entire project -- #
    original_assay_name_for_project = "STABILITY-PB-PH 7.4 (%Rem@2hr) [%]"
    updated_assay_name_for_project = "STABILITY ASSAY PROJECT"

    # Open up the column details window
    click_column_menu_item(selenium, original_assay_name_for_project, 'Column Details...')
    # Set the name
    dom.set_element_value(selenium, ASSAY_PROJECT_LEVEL_NAME_TEXT_BOX, updated_assay_name_for_project)
    # Close the column details window
    base.click_ok(selenium)

    # ----- Check that the assay column was renamed across project, and reset it ----- #

    # Search for the assay with old name in Columns Tree and verify there isn't any.
    verify_no_column_exists_in_column_tree(selenium, original_assay_name_for_project)

    # TODO: IS IT POSSIBLE TO TEST SS-25664 BY REFRESHING THE COLUMN FOLDER TREE?

    # Switch to another live report with that assay
    switch_to_live_report(selenium, live_report_to_duplicate)

    # Open the column details window using the updated name
    click_column_menu_item(selenium, '{} [%]'.format(updated_assay_name_for_project), 'Column Details...')
    # Reset the name
    dom.click_element(selenium, ASSAY_PROJECT_LEVEL_NAME_RESET_BUTTON)
    # Close the column details window
    base.click_ok(selenium)

    # ----- Rename an assay column for the one LR project using alias ----- #

    lr_assay_name_alias = "Assay Name Alias"

    # Switch back to first LR
    switch_to_live_report(selenium, duplicate_live_report)
    # Open up the column details window
    click_column_menu_item(selenium, original_assay_name_for_project, 'Column Details...')
    # click the Use LiveReport alias checkbox
    dom.click_element(selenium, ASSAY_LR_LEVEL_NAME_CHECKBOX)
    # Change the name
    dom.set_element_value(selenium, ASSAY_LR_LEVEL_NAME_TEXT_BOX, lr_assay_name_alias)
    # Close the column details window
    base.click_ok(selenium)

    # ----- Check that the assay column was renamed in the LR ----- #

    # Scroll to the column using its new name
    open_column_menu(selenium, '{} [%]'.format(lr_assay_name_alias))

    # ----- Check that the assay column was NOT renamed across Project ----- #
    # Search in the columns tree with Alias
    verify_no_column_exists_in_column_tree(selenium, lr_assay_name_alias)

    # Switch to second LR
    switch_to_live_report(selenium, live_report_to_duplicate)
    # Verify that the column with the original name is found in other LR as Alias are per LR.
    open_column_menu(selenium, original_assay_name_for_project)
