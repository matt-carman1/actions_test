import pytest

from helpers.change import advanced_search_actions
from helpers.change.actions_pane import open_add_compounds_panel, open_advanced_search, close_add_compounds_panel
from helpers.change.grid_column_menu import sort_grid_by
from helpers.change.strict_match_actions import open_create_limited_assay_column_dialog, set_limited_column_title, set_limiting_condition_range, \
    add_remove_limiting_conditions
from helpers.selection.advanced_search import SEARCH_AND_ADD_COMPOUNDS_BUTTON
from helpers.selection.grid import Footer
from helpers.verification.assay import verify_limited_assay_column_tooltip
from helpers.verification.grid import check_for_butterbar, verify_footer_values, verify_column_subcell_contents
from library import dom, base


@pytest.mark.smoke
@pytest.mark.app_defect(reason="SS-43520: Flakiness Finding column PK_PO_RAT")
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_create_limited_assay_column_via_grid(selenium):
    """
    Smoke test for Strict Match. Create Limited Assay Column using the Assay column in the grid:
    1. From Advanced Search add compounds for the assay column
    2. From Assay Column Context Menu Define Limited Assay Column
    3. Verify the the tooltip content for the limited assay column
    4. Verify the Column contents for the limited assay column

    :param selenium: Selenium Webdriver
    """

    # Test Data
    assay_column_name = 'PK_PO_RAT (AUC)'
    assay_column_name_with_units = "{} [uM.min]".format(assay_column_name)
    limiting_condition = 'Absorption'

    # Add the assay column and compounds via Advanced Search.
    open_add_compounds_panel(selenium)
    open_advanced_search(selenium)
    advanced_search_actions.add_query(selenium, assay_column_name)
    condition_box = advanced_search_actions.get_query(selenium, assay_column_name)
    advanced_search_actions.set_query_range(condition_box, lower_limit=21, upper_limit=50)

    # Perform Advanced search to get compounds in the LR and create a Limited Assay Column
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)

    # Verify Compounds and close the Compounds Panel
    check_for_butterbar(selenium, 'Searching for compounds...')
    check_for_butterbar(selenium, 'Searching for compounds...', visible=False)
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(4),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(6)
        })
    close_add_compounds_panel(selenium)

    # Create a Limited assay column with a limiting condition
    create_limiting_assay_dialog = open_create_limited_assay_column_dialog(selenium, assay_column_name_with_units)
    set_limited_column_title(selenium, assay_column_name)
    limiting_condition_element = add_remove_limiting_conditions(create_limiting_assay_dialog,
                                                                condition=limiting_condition)
    set_limiting_condition_range(limiting_condition_element, lower_limit=20, upper_limit=50)
    base.click_ok(selenium)

    sort_grid_by(selenium, 'ID')

    limited_assay_column_name = '[LIM] PK_PO_RAT (AUC) [uM.min]'
    limited_assay_tooltip_title = '[LIM]\nPK_PO_RAT (AUC)'
    limited_assay_tooltip = ['Absorption:\n20 to 50']

    # Check the tooltip for limited assay column
    verify_limited_assay_column_tooltip(selenium, limited_assay_column_name, limited_assay_tooltip_title,
                                        limited_assay_tooltip)

    # Verify Limited Assay Column Content
    verify_column_subcell_contents(selenium, limited_assay_column_name, [['', ''], ['', '34.4'], ['', '24'], ['21.5']])
