import pytest

from helpers.change.enumeration import open_enumeration_wizard, search_for_reaction, choose_a_rxn_source, \
    close_enumeration_wizard
from helpers.change.sketcher import import_structure_into_sketcher
from helpers.selection.enumeration import ENUMERATION_REACTION_SKETCHER, REACTION_EDIT_PICKER, \
    ENUMERATION_PROCEED_BUTTON, ENUMERATION_LINKS, ENUMERATION_BACK_BUTTON, SAVE_REACTION_CANCEL_LINK
from helpers.selection.modal import MODAL_DIALOG_HEADER, MODAL_DIALOG_BODY
from helpers.verification.element import verify_is_visible

from library import dom, wait, base


@pytest.mark.xfail(reason="SS-36770")
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_rxn_enum_rxn_validation(selenium):
    """
    Reaction enumeration test to validate a reaction
    1. Open the reaction enumeration panel
    2. Edit a reaction from the Schrodinger Collection
    3. Replace the reaction with an invalid reaction - no products
    4. Verify that clicking on Save throws a error dialog and the disabled Enumerate button shows.
    5. Replace the reaction with a valid reaction - two products
    6. Verify that clicking on Save throws a error dialog and the disabled Enumerate button shows.
    7. Now, replace with a valid reaction.
    8. Ensure that Save is clickable and Enumerate button changes to Next.

    :param selenium: Selenium Webdriver
    """
    # Reaction smiles to be tested
    no_product_reaction = ['C1=CC=CC=C1>> |c:0,2,4|']
    two_product_reaction = ['C1=CC=CC=C1>>CC1=CC=CC=C1.Cl |c:0,2,4,9,11,t:7,lp:13:3|']
    correct_reaction = ['C1=CC=CC=C1>>CC1=CC=CC=C1 |c:0,2,4,9,11,t:7|']

    open_enumeration_wizard(selenium)

    # Choose a reaction source (Schrodinger collection, saved or New). Default is Schrodinger collection
    choose_a_rxn_source(selenium)

    # Search and select the reaction
    search_for_reaction(selenium, reaction_name="Benzimidazole formation")

    # Edit the reaction by clicking on the pencil icon
    dom.click_element(selenium, REACTION_EDIT_PICKER)
    wait.until_visible(selenium, ENUMERATION_REACTION_SKETCHER)

    # Replace with invalid reaction - no product and verification
    rxn_validation(selenium, no_product_reaction)

    # Replace with invalid reaction - two product and verification
    rxn_validation(selenium, two_product_reaction)

    # Replace with valid reaction - and subsequent verification
    rxn_validation(selenium, correct_reaction, is_invalid_reaction=False)

    # Closing the Enumeration wizard
    close_enumeration_wizard(selenium)


def rxn_validation(driver, rxn_smiles, is_invalid_reaction=True):
    """
    Positive and negative Validation of a reaction

    :param driver: webdriver
    :param rxn_smiles: list, list of rxn smiles
    :param is_invalid_reaction: boolean, default to True, if the reaction is invalid, False if the reaction is valid
    :return:
    """

    # importing structure into the sketcher
    import_structure_into_sketcher(driver, rxn_smiles, sketcher_iframe_selector=ENUMERATION_REACTION_SKETCHER)

    if is_invalid_reaction:
        verify_is_visible(driver, ENUMERATION_PROCEED_BUTTON, selector_text="Enumerate")
        dom.click_element(driver, ENUMERATION_LINKS, text="Save")

        verify_is_visible(driver, MODAL_DIALOG_HEADER, selector_text="Invalid Reaction")
        verify_is_visible(driver,
                          MODAL_DIALOG_BODY,
                          selector_text="Reactions must have at least one reactant and "
                          "exactly one product.")
        base.click_ok(driver)

    else:
        verify_is_visible(driver, ENUMERATION_PROCEED_BUTTON, selector_text="Next >")
        dom.click_element(driver, ENUMERATION_PROCEED_BUTTON, text="Next >")

        dom.click_element(driver, ENUMERATION_BACK_BUTTON, text='Back')

        dom.click_element(driver, ENUMERATION_LINKS, text="Save")
        verify_is_visible(driver, MODAL_DIALOG_HEADER, selector_text='Save Reaction')

        # Closing the Save reaction dialog
        dom.click_element(driver, SAVE_REACTION_CANCEL_LINK, text="Cancel")
