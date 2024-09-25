import pytest

from helpers.change.enumeration import open_enumeration_wizard, search_for_reaction, choose_a_rxn_source, \
    add_structures_from_live_report, close_enumeration_wizard
from helpers.change.actions_pane import close_add_data_panel
from helpers.change.columns_management_ui import open_column_mgmt_panel
from helpers.selection.grid import Footer
from helpers.verification.grid import verify_footer_values
from helpers.verification.element import verify_is_visible
from helpers.verification.data_and_columns_tree import verify_visible_columns_from_column_mgmt_ui

from helpers.selection.enumeration import ENUMERATION_PROCEED_BUTTON, ENUMERATION_ACTIVE_TAB, ENUMERATION_STATUS, \
    ENUMERATION_STRUCTURE_COUNT, ENUMERATION_LINKS, ENUMERATION_REACTANT_COLUMNS_DIALOG, \
    ENUMERATION_EXTRA_COLUMN_APPLY_ALL, ENUMERATION_EXTRA_COLUMN_CHECKED, \
    EXTRA_COLUMNS_CHECKBOXES, ENUM_EXTRA_COLUMN_APPLY_ALL_CHECKED
from helpers.selection.modal import MODAL_DIALOG_BUTTON
from library import dom, wait, base
from library.utils import is_k8s


@pytest.mark.app_defect(reason="SS-43919: Dialog reloads while selecting extra columns")
@pytest.mark.require_webgl
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_rxn_enum_extra_columns_apply_all_functionality(selenium):
    """
    Basic Reaction enumeration test via LiveReports with emphasis on Extra Columns dialog- part II:
    1. Choose a reaction from the Schrodinger collection.
    2. Import Reactant A via LiveReports. (Apply all checkbox selection does not persist, filed SS-34763)
    3. Import Reactant B via LiveReports.
    4. Click on the "Extra Columns: (choose)" link now and click on Apply to All checkbox.
    5. Select two reactant columns - which equates to four columns
    6. Click on Enumerate.
    7. Verify that all the four columns appear in the LR from the Column Management UI


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

    # This will pop open the extra column dialog, close before proceeding
    wait.until_visible(selenium, ENUMERATION_REACTANT_COLUMNS_DIALOG)
    dom.click_element(selenium, MODAL_DIALOG_BUTTON, text="Cancel")

    # Verification that all reactants are imported
    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('first-child'),
                      selector_text="(6 structures",
                      exact_selector_text_match=True,
                      custom_timeout=10)

    # Add reactants from LiveReports and verify the number of reactants - Reactant B
    add_structures_from_live_report(selenium, live_report_name='Test Reactants - Halides', structure_name='B')

    # This will pop open the select column dialog, close before proceeding
    wait.until_visible(selenium, ENUMERATION_REACTANT_COLUMNS_DIALOG)
    dom.click_element(selenium, MODAL_DIALOG_BUTTON, text="Cancel")

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

    # Clicking on the Apply to All checkbox
    dom.click_element(selenium, ENUMERATION_EXTRA_COLUMN_APPLY_ALL)
    verify_is_visible(selenium, ENUM_EXTRA_COLUMN_APPLY_ALL_CHECKED)

    # Selecting a column - should be selected for both Reactant A and B
    dom.click_element(selenium, EXTRA_COLUMNS_CHECKBOXES, text="Lot Scientist (Test " "Reactants - Nitriles)")

    # Selecting another column - should be selected for both Reactant A and B
    dom.click_element(selenium, EXTRA_COLUMNS_CHECKBOXES, text="Lot Date Registered (Test " "Reactants - Nitriles)")

    # verification that the column is checked
    # Running it in serial helped us reduce the flakiness around this. However, we could not figure out why this does
    # not work in parallel after multiple trials. henceforth, this test is only run serially.
    verify_is_visible(selenium,
                      ENUMERATION_EXTRA_COLUMN_CHECKED,
                      selector_text="Lot Scientist (Test "
                      "Reactants - Nitriles)")

    # Verification that the column is checked
    verify_is_visible(selenium,
                      ENUMERATION_EXTRA_COLUMN_CHECKED,
                      selector_text="Lot Date Registered (Test "
                      "Reactants - Nitriles)")

    base.click_ok(selenium)

    # Enumerating after the product preview is populated
    dom.click_element(selenium, ENUMERATION_PROCEED_BUTTON, text="Enumerate")
    wait.until_visible(selenium, ENUMERATION_STATUS, text='Enumeration completed')

    close_enumeration_wizard(selenium)

    # Validate the number of products and columns for both reactants are populated in the LiveReport
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(30),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(13),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(1)
        })

    expected_column_list = [
        'ID', 'All IDs', 'Rationale', 'Lot Scientist', 'R1: Structure (Schrodinger)', 'R1: All IDs (Schrodinger)',
        'R1: Lot Scientist (Schrodinger)', 'R1: Lot Date Registered (Schrodinger)', 'R2: Structure (Schrodinger)',
        'R2: All IDs (Schrodinger)', 'R2: Lot Scientist (Schrodinger)', 'R2: Lot Date Registered (Schrodinger)'
    ]

    # Verifies that all the expected columns are visible from the Column management UI
    open_column_mgmt_panel(selenium)

    verify_visible_columns_from_column_mgmt_ui(selenium, expected_column_list)
    close_add_data_panel(selenium)
