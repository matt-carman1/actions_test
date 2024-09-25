import pytest

from helpers.change.enumeration import open_enumeration_wizard, search_for_reaction, choose_a_rxn_source, \
    add_structures_from_live_report, close_enumeration_wizard
from helpers.change.actions_pane import open_add_data_panel, close_add_data_panel
from helpers.selection.grid import Footer
from helpers.verification.grid import verify_footer_values
from helpers.verification.element import verify_is_visible
from helpers.verification.data_and_columns_tree import verify_visible_columns_from_column_mgmt_ui

from helpers.selection.enumeration import ENUMERATION_PROCEED_BUTTON, ENUMERATION_ACTIVE_TAB, ENUMERATION_STATUS, \
    ENUMERATION_STRUCTURE_COUNT, ENUMERATION_REACTANT_COLUMNS_DIALOG, ENUMERATION_LINKS, EXTRA_COLUMNS_LINKS, \
    EXTRA_COLUMNS_CHECKBOX_CHECKED, EXTRA_COLUMNS_CHECKBOXES, EXTRA_COLUMNS_REACTANT_SELECTION
from helpers.selection.column_tree import COLUMNS_TREE_LIVEREPORT_TAB
from library import dom, wait, base
from library.utils import is_k8s


@pytest.mark.xfail(not is_k8s(), reason="SS-40265: RMQ issues in Old Jenkins")
@pytest.mark.require_webgl
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_rxn_enum_extra_columns(selenium):
    """
    Basic Reaction enumeration test via LiveReports with emphasis on Extra Columns dialog:
    1. Choose a reaction from the Schrodinger collection.
    2. Import Reactant A via LiveReports and select all reactant columns.
    3. Import Reactant B via LiveReports and select all reactant columns.
    4. Click on the "Extra Columns: (choose)" link now and unselect all reactant columns.
    5. Select one reactant column each for Reactant A and Reactant B.
    6. Click on Enumerate.
    7. Verify that all the selected columns appear in the LR from the Column Management UI


    :param selenium: Selenium Webdriver
    """
    open_enumeration_wizard(selenium)

    # Choose a reaction source from the Schrodinger collection
    choose_a_rxn_source(selenium)

    # Search and select the reaction
    search_for_reaction(selenium, reaction_name="2,5-disubstituted tetrazole synthesis")

    # Navigate to the ADD REACTANTS tab
    dom.click_element(selenium, ENUMERATION_PROCEED_BUTTON, text="Next >")
    wait.until_visible(selenium, ENUMERATION_ACTIVE_TAB, text="ADD REACTANTS")

    # Add reactants from LiveReports and verify that number of reactants
    add_structures_from_live_report(selenium, live_report_name='Test Reactants - Nitriles')

    # Select all reactants from the Extra columns dialog - Reactant A
    wait.until_visible(selenium, ENUMERATION_REACTANT_COLUMNS_DIALOG)
    dom.click_element(selenium, EXTRA_COLUMNS_LINKS, text="Check All")
    base.click_ok(selenium)

    # Verification that all reactants are imported
    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('first-child'),
                      selector_text="(6 structures",
                      exact_selector_text_match=True,
                      custom_timeout=10)

    # Add reactants from LiveReports and verify the number of reactants - Reactant B
    add_structures_from_live_report(selenium, live_report_name='Test Reactants - Halides', structure_name='B')

    # Select all reactant columns from the extra columns dialog - reactant B
    wait.until_visible(selenium, ENUMERATION_REACTANT_COLUMNS_DIALOG)
    dom.click_element(selenium, EXTRA_COLUMNS_LINKS, text="Check All")
    base.click_ok(selenium)

    # Verification that all reactants are imported
    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('nth-child(2)'),
                      selector_text="(7 structures",
                      exact_selector_text_match=True,
                      custom_timeout=10)

    # Verify the number of expected products
    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('last-child'),
                      selector_text="(35 structures",
                      exact_selector_text_match=True,
                      custom_timeout=10)

    # ---- Interaction with the Extra Columns dialog ---- #
    dom.click_element(selenium, ENUMERATION_LINKS, text="(choose)")

    # Un-selecting all columns.
    dom.click_element(selenium, EXTRA_COLUMNS_LINKS, text="Clear All")

    # Switching to Reactant A and selecting a column
    dom.click_element(selenium, EXTRA_COLUMNS_REACTANT_SELECTION, text="Reactant A")
    dom.click_element(selenium, EXTRA_COLUMNS_CHECKBOXES, text="Lot Date Registered (Test " "Reactants - Nitriles)")
    # Verification that the column is checked
    verify_is_visible(selenium, EXTRA_COLUMNS_CHECKBOX_CHECKED)

    # Switching to reactant B and selecting a column
    dom.click_element(selenium, EXTRA_COLUMNS_REACTANT_SELECTION, text="B")
    dom.click_element(selenium, EXTRA_COLUMNS_CHECKBOXES, text="ID (Test Reactants - Halides)")
    # Verification that the column is checked
    verify_is_visible(selenium, EXTRA_COLUMNS_CHECKBOX_CHECKED)

    base.click_ok(selenium)

    # Enumerating after the product preview is populated
    dom.click_element(selenium, ENUMERATION_PROCEED_BUTTON, text="Enumerate")
    wait.until_visible(selenium, ENUMERATION_STATUS, text='Enumeration completed')

    close_enumeration_wizard(selenium)

    # Validate the number of products and columns in the LiveReport
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(30),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(11),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(1)
        })

    expected_column_list = [
        'ID', 'All IDs', 'Rationale', 'Lot Scientist', 'R1: Structure (Schrodinger)', 'R1: All IDs (Schrodinger)',
        'R1: Lot Date Registered (Schrodinger)', 'R2: Structure (Schrodinger)', 'R2: All IDs (Schrodinger)',
        'R2: ID (Schrodinger)'
    ]

    # Verifies that all the expected columns are visible from the Column management UI
    open_add_data_panel(selenium)
    dom.click_element(selenium, COLUMNS_TREE_LIVEREPORT_TAB)

    verify_visible_columns_from_column_mgmt_ui(selenium, expected_column_list)
    close_add_data_panel(selenium)
