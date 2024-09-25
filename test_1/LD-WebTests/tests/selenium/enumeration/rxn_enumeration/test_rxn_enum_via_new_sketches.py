import pytest

from helpers.change.enumeration import open_enumeration_wizard, search_for_reaction, choose_a_rxn_source, \
    add_structures_via_sketcher
from helpers.selection.grid import Footer
from helpers.verification.grid import verify_footer_values, verify_visible_columns_in_live_report, verify_column_contents
from helpers.verification.element import verify_is_visible
from helpers.selection.enumeration import ENUMERATION_PROCEED_BUTTON, ENUMERATION_ACTIVE_TAB, ENUMERATION_STATUS, \
    ENUMERATION_STRUCTURE_COUNT, ENUMERATION_CLOSE_BUTTON
from library import dom, wait


@pytest.mark.xfail(reason="SS-36770")
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_rxn_enum_via_new_sketches(selenium):
    """
    Basic Reaction enumeration test via new sketch:
    1. Enumerate for a reaction with reactants via New Sketch.
    2. Validated the number of products and columns in the LiveReport.

    :param selenium: Selenium Webdriver
    """
    # Reactant A is an aromatic sulphonyl chloride
    list_of_reactant_a = ['ClS(=O)(=O)C1=CC=CC=C1 |c:6,8,t:4,lp:0:3,2:2,3:2|']
    # Reactant B are primary nitriles
    list_of_reactant_b = ['CN |lp:1:1|', 'CCN |lp:2:1|']
    enumerated_smiles_list = ['CNS(=O)(=O)C1=CC=CC=C1', 'CCNS(=O)(=O)C1=CC=CC=C1']

    open_enumeration_wizard(selenium)

    # Choose a reaction source (Schrodinger collection, saved or New). Default is Schrodinger collection
    choose_a_rxn_source(selenium)

    # Search and select the reaction
    search_for_reaction(selenium, reaction_name="Sulfonamide coupling")

    # Navigate to the ADD REACTANTS tab
    dom.click_element(selenium, ENUMERATION_PROCEED_BUTTON, text="Next >")
    wait.until_visible(selenium, ENUMERATION_ACTIVE_TAB, text="ADD REACTANTS")

    # Adding structures via New Sketch for both reactant
    add_structures_via_sketcher(selenium, list_of_reactant_a, structure_tag='REACTANT A', reaction_enum='True')
    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('first-child'),
                      selector_text="(1 structures",
                      exact_selector_text_match=True,
                      custom_timeout=10)

    add_structures_via_sketcher(selenium,
                                list_of_reactant_b,
                                structure_tag='B',
                                explicitly_open_sketcher=True,
                                reaction_enum='True')
    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('nth-child(2)'),
                      selector_text="(2 structures",
                      exact_selector_text_match=True,
                      custom_timeout=10)

    # Verify the number of expected products
    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('last-child'),
                      selector_text="(2 structures",
                      exact_selector_text_match=True,
                      custom_timeout=10)

    # Enumerating after the product preview is populated
    dom.click_element(selenium, ENUMERATION_PROCEED_BUTTON, text="Enumerate")
    wait.until_visible(selenium, ENUMERATION_STATUS, text='Enumeration completed')

    # close_enumeration_wizard by clicking on CLOSE button link
    dom.click_element(selenium, ENUMERATION_CLOSE_BUTTON)

    # Validate the number of products and columns in the LiveReport
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(2),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(9),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(1)
        })

    expected_column_list = [
        'Compound Structure', 'ID', 'All IDs', 'Rationale', 'Lot Scientist', 'R1: Structure (Schrodinger)',
        'R1: All IDs (Schrodinger)', 'R2: Structure (Schrodinger)', 'R2: All IDs (Schrodinger)'
    ]

    verify_visible_columns_in_live_report(selenium, expected_column_list)

    # Verifying that Compound SMILES are as expected
    verify_column_contents(selenium, 'Compound Structure', enumerated_smiles_list)
