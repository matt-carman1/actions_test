import pytest

from helpers.selection.grid import Footer
from library import dom, base

from helpers.change.actions_pane import open_add_data_panel
from helpers.change.columns_action import add_column_by_name
from helpers.change.live_report_menu import click_live_report_menu_item
from helpers.selection.modal import DUPLICATE_LR_RADIO_BUTTON_LABEL, MODAL_LR_COLUMN_LABEL, \
    MODAL_LR_NOT_SELECTED_COLUMN_LABEL, DUPLICATE_LR_COLUMN_SELECTION_WARNING_MSG, \
    DUPLICATE_LR_COLUMN_SELECTION_WARNING_MSG_UNDO_LINK
from helpers.selection.modal import MODAL_DIALOG_HEADER
from helpers.verification.data_and_columns_tree import verify_visible_columns_from_column_mgmt_ui
from helpers.verification.element import verify_is_visible, verify_is_not_visible
from helpers.verification.grid import verify_footer_values
from helpers.verification.live_report import verify_columns_not_visible_in_duplicate_lr_dialog

live_report_to_duplicate = {'livereport_name': 'Test Reactants - Nitriles', 'livereport_id': '2553'}


@pytest.mark.app_defect(reason="SS-34757: Flaky test")
def test_duplicate_livereport_with_mpo_column(selenium, duplicate_live_report, open_livereport):
    """
    Duplicate live report with MPO column

    1. Add MPO column to the LR
    2. Open Duplicate LR dialog and Choose column subset option.
    3. Verify default columns like Lot Scientist columns and MPO Constituent columns not showing in Column subset
    4. Verify warning message Before and after selecting MPO column
    5. Check whether Undo operation works properly in the warning
    6. Duplicate Livereport with MPO column
    7. Verify MPO column and Constituent columns duplicated

    :param selenium: Selenium webdriver
    :param duplicate_live_report: a fixture which duplicates live report
    :param open_livereport: a fixture which opens live report
    """
    # MPO column
    mpo_column = 'Test RPE MPO'

    # ----- Add MPO column to the LR ----- #
    open_add_data_panel(selenium)
    add_column_by_name(selenium, "(JS Testing) {}".format(mpo_column))

    # ----- Opening the duplicate LR dialog ----- #
    click_live_report_menu_item(selenium, duplicate_live_report, 'Duplicate...')
    # verify Duplicate Live Report dialog opened
    verify_is_visible(selenium, MODAL_DIALOG_HEADER, 'Duplicate LiveReport')

    dom.click_element(selenium, DUPLICATE_LR_RADIO_BUTTON_LABEL, text='Choose Subset')

    # ----- verify default columns and MPO Constituent columns are not visible in Duplicate Livereport dialog ----- #
    verify_columns_not_visible_in_duplicate_lr_dialog(selenium, [
        'ID', 'Compound Structure', 'All IDs', 'Test RPE MPO Desirability Scores and Number of '
        'Missing Inputs', 'PK_PO_RAT (AUC) Desirability', 'Number of missing inputs'
    ])

    # ----- Verify warning message Before and after selecting MPO column ----- #
    # verify there is no warning message when not selected MPO column
    verify_is_not_visible(selenium, DUPLICATE_LR_COLUMN_SELECTION_WARNING_MSG, custom_timeout=5)

    # Select MPO column
    dom.click_element(selenium, MODAL_LR_COLUMN_LABEL, text=mpo_column)

    # verify the warning message after selecting MPO column
    verify_is_visible(
        selenium, DUPLICATE_LR_COLUMN_SELECTION_WARNING_MSG,
        'One or more of the selected columns is a formula, MPO, or column-as-param model, and each '
        'input to each of those columns was selected.')

    # ----- check whether Undo operation works properly in the warning ----- #
    # Click Undo link to deselect the MPO column
    dom.click_element(selenium, DUPLICATE_LR_COLUMN_SELECTION_WARNING_MSG_UNDO_LINK)
    # verify MPO column deselected
    verify_is_visible(selenium, MODAL_LR_NOT_SELECTED_COLUMN_LABEL, mpo_column)

    # ----- Duplicate Livereport with MPO column ----- #
    # select MPO column again and duplicate the lr
    dom.click_element(selenium, MODAL_LR_COLUMN_LABEL, text=mpo_column)
    base.click_ok(selenium)

    # ----- Verify MPO column and Constituent columns duplicated ----- #
    # verify only selected columns duplicated
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(6),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(8),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(1),
            Footer.ROW_SELECTED_COUNT_KEY: Footer.ROW_SELECTED_COUNT_VALUE.format(0)
        })
    # verify MPO desirability columns visible
    verify_visible_columns_from_column_mgmt_ui(selenium, [
        'ID', 'All IDs', 'Rationale', 'Lot Scientist', 'Test RPE MPO',
        'Test RPE MPO Desirability Scores and Number of Missing '
        'Inputs', 'PK_PO_RAT (AUC) Desirability', 'Number of missing inputs'
    ])
