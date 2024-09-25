import pytest

from helpers.change import advanced_search_actions
from helpers.change.actions_pane import open_add_compounds_panel, open_advanced_search, open_add_data_panel
from helpers.change.advanced_search_actions import get_query
from helpers.change.autosuggest_actions import set_autosuggest_items
from helpers.change.columns_action import add_column_by_name
from helpers.change.freeform_column_action import create_ffc
from helpers.change.live_report_menu import click_live_report_menu_item
from helpers.change.live_report_picker import create_and_open_live_report
from helpers.change.project import open_project
from helpers.flows.add_compound import search_by_id
from helpers.selection.advanced_search import SEARCH_AND_ADD_COMPOUNDS_BUTTON
from helpers.selection.grid import GRID_PROGRESS_NOTIFICATION, Footer
from helpers.selection.live_report_tab import TAB_ACTIVE
from helpers.selection.modal import MODAL_DIALOG_HEADER, OK_BUTTON, COPY_LR_TO_PROJECT_PREVIEW_TEXT, \
    COPY_LR_TO_PROJECT_LIST
from helpers.selection.project import PROJECT_TITLE
from helpers.verification.data_and_columns_tree import verify_column_exists_in_column_tree, \
    verify_no_column_exists_in_column_tree
from helpers.verification.element import verify_is_visible
from helpers.verification.grid import verify_footer_values, check_for_butterbar
from library import dom, wait, utils
from library.authentication import login
from library.select import select_option_by_text


@pytest.mark.app_defect(reason="SS-29582")
@pytest.mark.smoke
def test_copy_lr_with_ffc_mpo_to_new_project(selenium, use_module_isolated_project):
    """
    Test for copy Livereport with FFC and MPO to new Project.

    1. Adding columns to the New Livereport
    2. Copy the Livereport to New Project
    3. Verification of copied Livereport in new Project.

    :param selenium: Selenium Webdriver
    :param use_module_isolated_project: it is fixture used to create new project.
    :return:
    """
    ffc_column_name = 'Published Freeform Text Column'
    mpo_column_name = '(JS Testing) Test RPE MPO'
    unpublished_ffc_column = utils.make_unique_name('UnpublishedFFC')

    project_name = use_module_isolated_project
    login(selenium)
    open_project(selenium)

    lr_name = create_and_open_live_report(selenium, utils.make_unique_name('test_copy_lr_with_ffc_mpo_to_new_project'))

    # ----- Adding Columns to Livereport -----  #
    create_ffc(selenium, column_name=unpublished_ffc_column)
    open_add_data_panel(selenium)
    add_column_by_name(selenium, mpo_column_name)

    # Add Compounds through compound ID
    open_add_compounds_panel(selenium)
    search_by_id(selenium, 'CRA-033619')

    # Add compounds through advance search on ffc column name
    open_advanced_search(selenium)
    # Add range query and search
    advanced_search_actions.add_query(selenium, ffc_column_name)
    # Set value "(defined)" in text query
    query = get_query(selenium, ffc_column_name)
    set_autosuggest_items(query, ["(defined)"])
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)

    # verify footer values
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(3),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(8)
        })

    # ----- Copy the Livereport to New Project ----- #
    click_live_report_menu_item(selenium, lr_name, item_name='Copy to Project...')
    wait.until_visible(selenium, MODAL_DIALOG_HEADER, text="Copy Live Report to Another Project")
    # Choose the project from the dialog to copy the LR to.
    select_option_by_text(selenium, COPY_LR_TO_PROJECT_LIST, project_name)

    # verifying preview text in Copy Livereport to Another Project window
    columns_and_compound_ids_preview_txt_expected = [
        'If you proceed with this Copy action the following columns and their data will now be accessible to all '
        'members of the selected project:\n{}\n{}\n{}'.format(unpublished_ffc_column,
                                                              mpo_column_name.split(') ')[1], ffc_column_name),
        'If you proceed with this Copy action the following compounds will now be accessible to all members of the '
        'selected project:\nV035624\nV035625'
    ]

    columns_and_compound_ids_preview_txt_elems = dom.get_elements(selenium, COPY_LR_TO_PROJECT_PREVIEW_TEXT)
    columns_and_compound_ids_preview_txt_actual = [
        preview.text for preview in columns_and_compound_ids_preview_txt_elems
    ]
    assert columns_and_compound_ids_preview_txt_actual == columns_and_compound_ids_preview_txt_expected

    dom.click_element(selenium, OK_BUTTON)

    # Checking for relevant butterbars
    check_for_butterbar(selenium, "Copying Live Report...")
    check_for_butterbar(selenium, "Copying Live Report...", visible=False)
    check_for_butterbar(selenium, "Live Report has been copied.\nGo to copied live report")
    # Navigate to the copied LR in another project
    dom.click_element(selenium, GRID_PROGRESS_NOTIFICATION + ' a', text="Go to copied live report")
    check_for_butterbar(selenium, "Live Report has been copied.", visible=False)

    # ----- Verification of copied Livereport in new Project ----- #
    # verifying project title
    verify_is_visible(selenium, PROJECT_TITLE, selector_text=project_name)
    # verifying livereport title
    verify_is_visible(selenium, TAB_ACTIVE, selector_text=lr_name)

    # verify footer values
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(3),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(8)
        })

    # verify columns published FFC and MPO columns present in new project
    verify_column_exists_in_column_tree(selenium,
                                        '{} (Copied from Project JS Testing)'.format(ffc_column_name),
                                        search_retries=3)
    verify_column_exists_in_column_tree(selenium,
                                        '({}) {} (Copied from Project JS Testing)'.format(
                                            project_name,
                                            mpo_column_name.split(') ')[1]),
                                        search_retries=3)
    # verify unpublished ffc not present in new project
    verify_no_column_exists_in_column_tree(selenium,
                                           '{} (Copied from Project JS Testing)'.format(unpublished_ffc_column))
