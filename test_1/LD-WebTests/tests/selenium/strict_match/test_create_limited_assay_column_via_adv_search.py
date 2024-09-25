import time

import pytest

from helpers.change import advanced_search_actions
from helpers.change.actions_pane import open_advanced_search, close_add_compounds_panel, open_add_compounds_panel
from helpers.change.grid_column_menu import sort_grid_by, ungroup_columns
from helpers.change.strict_match_actions import open_edit_limited_assay_column_dialog_from_adv_search, \
    add_remove_limiting_conditions, set_limiting_condition_range, select_limit_multiple_endpoints_checkbox
from helpers.selection.advanced_search import SEARCH_AND_ADD_COMPOUNDS_BUTTON
from helpers.selection.grid import GRID_GROUP_HEADER_CELL, Footer
from helpers.selection.modal import MODAL_DIALOG_HEADER, OK_BUTTON
from helpers.verification.assay import verify_limited_assay_column_tooltip
from helpers.verification.element import verify_is_visible
from helpers.verification.grid import verify_footer_values, check_for_butterbar, verify_column_subcell_contents
from library import dom, base, wait


@pytest.mark.smoke
# @pytest.mark.app_defect(reason="SS-43520: Flakiness Finding column PK_PO_RAT")
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_create_limited_assay_column_via_adv_search(selenium):
    """
    Smoke test for Strict Match. Create Limited Assay Column via Advanced Search:
    1. From Advanced Search
    2. Set the limiting conditions
    3. Verify that the limited assay group is present
    4. Verify the the tooltip content for the limited assay column
    5. Verify the column contents for the limited columns.

    :param selenium: Selenium Webdriver
    """
    # Test Data
    assay_name = 'PK_PO_RAT'
    assay_column_name = 'PK_PO_RAT (AUC)'
    limit_column = 'Dose'

    # ----- CREATE LIMITING ASSAY COLUMN FROM ADVANCED SEARCH PANEL ----- #

    # Add assay query condition in Advanced Search and set upper_limit to 5 to minimize the compounds returned by search
    open_add_compounds_panel(selenium)
    open_advanced_search(selenium)
    advanced_search_actions.add_query(selenium, assay_column_name)
    condition_box = advanced_search_actions.get_query(selenium, assay_column_name)
    advanced_search_actions.set_query_range(condition_box, upper_limit=5)

    select_limit_multiple_endpoints_checkbox(selenium, assay_column_name, assay_name)

    # Create Limiting Assay Column by selecting the checkbox and setting conditions by opening the Limiting Assay dialog
    # On selecting the checkbox 'Limiting Multiple Endpoints' the endpoint name gets removed from the Adv Query.
    create_limiting_assay_dialog = open_edit_limited_assay_column_dialog_from_adv_search(selenium, assay_name)
    limiting_condition_element = add_remove_limiting_conditions(create_limiting_assay_dialog, condition=limit_column)
    set_limiting_condition_range(limiting_condition_element, limit_column, upper_limit=20)
    base.click_ok(selenium)

    # Perform Advanced search to get compounds in the LR and generate a Limited Assay Column
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)

    # Verify Compounds and close the Compounds Panel
    check_for_butterbar(selenium, 'Searching for compounds...', visible=False)

    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(5),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(8)
        })
    close_add_compounds_panel(selenium)

    sort_grid_by(selenium, 'ID')

    # Verify the Limited Assay group
    # group name in the DOM does not show the space between [LIM] and assay name
    limited_assay_group_name = '[LIM] PK_PO_RAT'
    verify_is_visible(selenium,
                      GRID_GROUP_HEADER_CELL,
                      selector_text=limited_assay_group_name.replace(' ', ''),
                      exact_selector_text_match=True)

    # Ungrouping the columns such that [LIM] keyword would show up for individual limited columns to distinguish it
    # from the parent assay column name
    ungroup_columns(selenium, limited_assay_group_name)
    wait.until_visible(selenium,
                       MODAL_DIALOG_HEADER,
                       text='Ungroup Limited Assay Columns in Limited Assay Column '
                       'Group',
                       timeout=3)
    dom.click_element(selenium, OK_BUTTON, text='Keep')

    # Limited Assay Column Names after ungrouping
    auc_limited_assay_column = '[LIM] PK_PO_RAT (AUC) [uM.min]'
    dose_limited_assay_column = '[LIM] PK_PO_RAT (Dose) [mg/kg]'
    """
    The test fails SOMETIMES when verifying the tooltip text as filed in SS-30148. Please refer to the snapshots in the
    ticket. Briefly, the limited assay column tooltip does not have a consistent way of showing the limited conditions.
    So we are relying on the strategy followed in verify_limited_assay_column_tooltip
    """
    # Hover over limiting column and check the tooltip
    # NOTE (tchoi) Leaving out suffix for tooltip_title and doing a substring search.  See note for SS-30148 above.
    auc_limited_assay_column_tooltip_title = '[LIM]\nPK_PO_RAT'
    auc_limited_assay_column_tooltip = ['AUC:\n-∞ to 5', 'Dose:\n-∞ to 20']
    verify_limited_assay_column_tooltip(selenium,
                                        auc_limited_assay_column,
                                        auc_limited_assay_column_tooltip_title,
                                        auc_limited_assay_column_tooltip,
                                        exact_text_match=False)

    # NOTE (tchoi) Leaving out suffix for tooltip_title and doing a substring search.  See note for SS-30148 above.
    dose_limited_assay_column_tooltip_title = '[LIM]\nPK_PO_RAT'
    dose_limited_assay_column_tooltip = ['AUC:\n-∞ to 5', 'Dose:\n-∞ to 20']
    verify_limited_assay_column_tooltip(selenium,
                                        dose_limited_assay_column,
                                        dose_limited_assay_column_tooltip_title,
                                        dose_limited_assay_column_tooltip,
                                        exact_text_match=False)

    # Verify Column contents
    verify_column_subcell_contents(selenium, auc_limited_assay_column,
                                   [['1.98', ''], ['4.03', ''], ['0.382', ''], ['1.15', ''], ['1.22', '']])
    verify_column_subcell_contents(selenium, dose_limited_assay_column,
                                   [['5', ''], ['5', ''], ['2', ''], ['2', ''], ['2', '']])
