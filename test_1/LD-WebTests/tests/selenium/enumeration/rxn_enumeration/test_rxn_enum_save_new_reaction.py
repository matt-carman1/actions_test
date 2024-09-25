import pytest

from helpers.change.enumeration import open_enumeration_wizard, search_for_reaction, choose_a_rxn_source, \
    add_structures_via_sketcher, save_reaction_form
from helpers.change.sketcher import import_structure_into_sketcher
from helpers.selection.grid import Footer
from helpers.verification.grid import verify_footer_values, verify_visible_columns_in_live_report, \
    verify_column_contents
from helpers.verification.element import verify_is_visible
from helpers.selection.enumeration import ENUMERATION_PROCEED_BUTTON, ENUMERATION_ACTIVE_TAB, ENUMERATION_STATUS, \
    ENUMERATION_STRUCTURE_COUNT, ENUMERATION_CLOSE_BUTTON, REACTANT_NAME_INFO, \
    ENUMERATION_REACTION_SKETCHER, REACTION_PREVIEW
from library import dom, wait

# Input data required throughout the reaction A
# Input data required throughout the test
rxn_one_smiles = "NC1=CC=CC=C1O.O=CC1=CC=CC=C1>>C1C(OC2=CC=CC=C12)C1=CC=CC=C1 |c:3,5,12,14,21,29,31,t:1,10,19,23,27," \
              "lp:0:1,7:2,8:2,18:2|"
rxn_one_reactant_a_smiles = ["CCCNC1=CC(=CC(=C1O)S(N)(=O)=O)C(O)=O"]
rxn_one_reactant_b_smiles = ["CN1C(=CC=C1C(=O)C1=CC=C(C)C=C1)C(C)=O"]
rxn_one_product_smiles = ["CN1C(=CC=C1C1(CC2=CC(=CC(=C2O1)S(N)(=O)=O)C(O)=O)C1=CC=C(C)C=C1)C(C)=O"]
rxn_one_saved_reaction_name = "Loose Pattern matching"
rxn_one_saved_reaction_description = "To test loose pattern matching"
rxn_one_reactant_a_name = "Hydroxy aniline derivative"
rxn_one_reactant_b_name = "Benzaldehyde derivative"

rxn_one_data = (rxn_one_smiles, rxn_one_reactant_a_smiles, rxn_one_reactant_b_smiles, rxn_one_product_smiles,
                rxn_one_saved_reaction_name, rxn_one_saved_reaction_description, rxn_one_reactant_a_name,
                rxn_one_reactant_b_name)

# Input data required throughout the reaction B
rxn_two_smiles = "NC(=O)C1=CC(Br)=CC=C1.OB(O)[*]>>NC(=O)C1=CC=CC([*])=C1 " \
                "|$;;;;;;;;;;;;;_R1;;;;;;;;;_R1;$,c:6,8,18,21,t:3,16,lp:0:1,2:2,6:3,10:2,12:2,14:1,16:2|"
rxn_two_reactant_a_smiles = ["NC(=O)C1=CC(Br)=CC=C1"]
rxn_two_reactant_b_smiles = ["CB(O)O"]
rxn_two_product_smiles = ["CC1=CC=CC(=C1)C(N)=O"]
rxn_two_saved_reaction_name = "Partial R-group with Nitrogen"
rxn_two_saved_reaction_description = "To test out use case in SS-30409"
rxn_two_reactant_a_name = "3-Bromo-benzamide"
rxn_two_reactant_b_name = "Boron hydroxide derivative"

rxn_two_data = (rxn_two_smiles, rxn_two_reactant_a_smiles, rxn_two_reactant_b_smiles, rxn_two_product_smiles,
                rxn_two_saved_reaction_name, rxn_two_saved_reaction_description, rxn_two_reactant_a_name,
                rxn_two_reactant_b_name)


@pytest.mark.xfail(reason="SS-36770")
@pytest.mark.parametrize("rxn_smiles, reactant_a_smiles, reactant_b_smiles, product_smiles, saved_reaction_name,"
                         "saved_reaction_description, reactant_a_name, reactant_b_name", [rxn_one_data, rxn_two_data])
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_rxn_enum_save_reaction(selenium, rxn_smiles, reactant_a_smiles, reactant_b_smiles, product_smiles,
                                saved_reaction_name, saved_reaction_description, reactant_a_name, reactant_b_name):
    """
       Reaction enumeration test which: (Handles two reactions)
       1. Saves a new reaction from New Sketch.
       2. Uses this newly sketched reaction to perform an enumeration.
       3. Reactants are brought via hand sketch.
       4. Verified that all results are as expected.

       :param selenium: Selenium Webdriver
       :param rxn_smiles: str, the reaction smiles to be used
       :param reactant_a_smiles: list, the list of smiles for reactant A
       :param reactant_b_smiles: list, the list of smiles for reactant B
       :param product_smiles: list, the list of smiles for the enumerated product
       :param saved_reaction_name: str, the name of the saved reaction
       :param saved_reaction_description: str, the description of the saved reaction
       :param reactant_a_name: str, the name of the reactant A
       :param reactant_b_name: str, the name of reactant B
       """

    # ---------- Saves a new reaction from New Sketch ---------- #
    open_enumeration_wizard(selenium)

    # Choose source as New Sketch and import a reaction to the sketcher
    choose_a_rxn_source(selenium, get_reaction_from="New sketch")
    import_structure_into_sketcher(selenium, rxn_smiles, sketcher_iframe_selector=ENUMERATION_REACTION_SKETCHER)

    # Saving a reaction and filling in the Save Reaction form
    save_reaction_form(selenium, saved_reaction_name, saved_reaction_description, reactant_a_name, reactant_b_name)

    # --------- Uses this newly sketched reaction to perform an enumeration ------- #
    choose_a_rxn_source(selenium, get_reaction_from="Saved reactions")
    # Search and select the reaction
    search_for_reaction(selenium, reaction_name=saved_reaction_name)
    verify_is_visible(selenium, REACTION_PREVIEW, selector_text=saved_reaction_description)

    # Navigate to the ADD REACTANTS tab
    dom.click_element(selenium, ENUMERATION_PROCEED_BUTTON, text="Next >")
    wait.until_visible(selenium, ENUMERATION_ACTIVE_TAB, text="ADD REACTANTS")

    verify_is_visible(selenium, REACTANT_NAME_INFO, selector_text="Reactant A - {}".format(reactant_a_name))
    verify_is_visible(selenium, REACTANT_NAME_INFO, selector_text="Reactant B - {}".format(reactant_b_name))

    # ----------- Reactants are brought via hand sketch ---------- #
    add_structures_via_sketcher(selenium, reactant_a_smiles, structure_tag='REACTANT A', reaction_enum='True')
    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('first-child'),
                      selector_text="(1 structures",
                      exact_selector_text_match=True,
                      custom_timeout=10)

    add_structures_via_sketcher(selenium,
                                reactant_b_smiles,
                                structure_tag='B',
                                explicitly_open_sketcher=True,
                                reaction_enum='True')
    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('nth-child(2)'),
                      selector_text="(1 structures",
                      exact_selector_text_match=True,
                      custom_timeout=10)

    # Verify the number of expected products
    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('last-child'),
                      selector_text="(1 structures",
                      exact_selector_text_match=True,
                      custom_timeout=15)

    # Enumerating after the product preview is populated
    dom.click_element(selenium, ENUMERATION_PROCEED_BUTTON, text="Enumerate")
    wait.until_visible(selenium, ENUMERATION_STATUS, text='Enumeration completed')

    # close_enumeration_wizard by clicking on CLOSE button link
    dom.click_element(selenium, ENUMERATION_CLOSE_BUTTON)

    # ---------- Validate the results in a LiveReport -------- #
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(1),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(9),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(1)
        })

    expected_column_list = [
        'Compound Structure', 'ID', 'All IDs', 'Rationale', 'Lot Scientist', 'R1: Structure (Schrodinger)',
        'R1: All IDs (Schrodinger)', 'R2: Structure (Schrodinger)', 'R2: All IDs (Schrodinger)'
    ]

    verify_visible_columns_in_live_report(selenium, expected_column_list)

    # Verifying that Compound SMILES are as expected
    verify_column_contents(selenium, 'Compound Structure', product_smiles, exact_match=False)
