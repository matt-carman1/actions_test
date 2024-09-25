import pytest

from helpers.change.enumeration import open_enumeration_wizard, search_for_reaction, choose_a_rxn_source, \
    add_structures_from_live_report, close_enumeration_wizard
from helpers.selection.grid import Footer
from helpers.verification.grid import verify_footer_values, verify_visible_columns_in_live_report
from helpers.verification.element import verify_is_visible
from helpers.selection.enumeration import ENUMERATION_PROCEED_BUTTON, ENUMERATION_ACTIVE_TAB, ENUMERATION_STATUS, \
    ENUMERATION_STRUCTURE_COUNT, ENUMERATION_REACTANT_COLUMNS_DIALOG
from helpers.selection.modal import MODAL_DIALOG_BUTTON
from library import dom, wait


# TODO: Investigate using api fixture to create LRs in a new project.
@pytest.mark.xfail(reason="SS-36770")
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_rxn_enum_via_livereports(selenium):
    """
    Basic Reaction enumeration test:
    1. Enumerate for a reaction with reactants from the LiveReports.
    2. Validated the number of products and columns in the LiveReport.

    :param selenium: Selenium Webdriver
    """
    open_enumeration_wizard(selenium)

    # Choose a reaction source (Schrodinger collection, saved or New). Default is Schrodinger collection
    choose_a_rxn_source(selenium)

    # Search and select the reaction
    search_for_reaction(selenium, reaction_name="1,5-disubstituted tetrazole synthesis")

    # Navigate to the ADD REACTANTS tab
    dom.click_element(selenium, ENUMERATION_PROCEED_BUTTON, text="Next >")
    wait.until_visible(selenium, ENUMERATION_ACTIVE_TAB, text="ADD REACTANTS")

    # Add reactants from LiveReports and verify that number of reactants
    add_structures_from_live_report(selenium, live_report_name='Test Reactants - Nitriles')

    #This will pop open the select column dialog, close before proceeding
    wait.until_visible(selenium, ENUMERATION_REACTANT_COLUMNS_DIALOG)
    dom.click_element(selenium, MODAL_DIALOG_BUTTON, text="Cancel")

    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('first-child'),
                      selector_text="(6 structures",
                      exact_selector_text_match=True,
                      custom_timeout=10)

    add_structures_from_live_report(selenium, live_report_name='Test Reactants - Halides', structure_name='B')

    #This will pop open the select column dialog, close before proceeding
    wait.until_visible(selenium, ENUMERATION_REACTANT_COLUMNS_DIALOG)
    dom.click_element(selenium, MODAL_DIALOG_BUTTON, text="Cancel")

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

    # Enumerating after the product preview is populated
    dom.click_element(selenium, ENUMERATION_PROCEED_BUTTON, text="Enumerate")
    wait.until_visible(selenium, ENUMERATION_STATUS, text='Enumeration completed')

    close_enumeration_wizard(selenium)

    # Validate the number of products and columns in the LiveReport
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(30),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(9),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(1)
        })

    expected_column_list = [
        'Compound Structure', 'ID', 'All IDs', 'Rationale', 'Lot Scientist', 'R1: Structure (Schrodinger)',
        'R1: All IDs (Schrodinger)', 'R2: Structure (Schrodinger)', 'R2: All IDs (Schrodinger)'
    ]

    verify_visible_columns_in_live_report(selenium, expected_column_list)
