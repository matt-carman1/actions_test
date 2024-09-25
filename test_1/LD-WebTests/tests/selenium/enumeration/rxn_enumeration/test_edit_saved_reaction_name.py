import pytest
from helpers.change.enumeration import open_enumeration_wizard, search_for_reaction, choose_a_rxn_source
from helpers.verification.element import verify_is_visible
from helpers.selection.enumeration import ENUMERATION_LINKS, SAVE_REACTION_NAME_INPUT, REACTION_EDIT_PICKER, \
    CREATE_NEW_OVERWRITE_OK, DELETE_REACTION
from helpers.selection.sketcher import RXN_ENUM_SKETCHER_IFRAME
from helpers.selection.modal import MODAL_DIALOG_HEADER
from library import dom, base, wait, iframe
from library.utils import make_unique_name

test_rxn_representation = "$RXN V3000\n\n      Mrv1908  030120221950\n\nM  V30 COUNTS 1 1\nM  V30 BEGIN REACTANT\nM  V30 BEGIN CTAB\nM  V30 COUNTS 6 6 0 0 0\nM  V30 BEGIN ATOM\nM  V30 1 C -4.4137 1.54 0 1\nM  V30 2 C -3.08 0.77 0 2\nM  V30 3 C -3.08 -0.77 0 3\nM  V30 4 C -4.4137 -1.54 0 4\nM  V30 5 C -5.7474 -0.77 0 5\nM  V30 6 C -5.7474 0.77 0 6\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 2 1 2\nM  V30 2 1 2 3\nM  V30 3 2 3 4\nM  V30 4 1 4 5\nM  V30 5 2 5 6\nM  V30 6 1 6 1\nM  V30 END BOND\nM  V30 END CTAB\nM  V30 END REACTANT\nM  V30 BEGIN PRODUCT\nM  V30 BEGIN CTAB\nM  V30 COUNTS 7 7 0 0 0\nM  V30 BEGIN ATOM\nM  V30 1 C 6.3937 0.77 0 1\nM  V30 2 C 7.7274 -0 0 2\nM  V30 3 C 7.7274 -1.54 0 3\nM  V30 4 C 6.3937 -2.31 0 4\nM  V30 5 C 5.06 -1.54 0 5\nM  V30 6 C 5.06 0 0 6\nM  V30 7 F 6.3937 2.31 0 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 2 1 2\nM  V30 2 1 2 3\nM  V30 3 2 3 4\nM  V30 4 1 4 5\nM  V30 5 2 5 6\nM  V30 6 1 6 1\nM  V30 7 1 1 7\nM  V30 END BOND\nM  V30 END CTAB\nM  V30 END PRODUCT\nM  END\n\n"
test_rxn_name = "Reactions of benzene"
test_reaction_desc = "Benzene reacted with ammonium fluorinated salts ex. Diphenyl sulphonyl fluoride"
test_reactant_classes = ["benzene"]
test_reactant_keywords = ["halogenation"]


# @pytest.mark.skip(reason="fix with SS-37616")
@pytest.mark.require_webgl
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_edit_saved_reaction(selenium, create_new_rxn):
    """
    Selenium test for Confirm Reaction update dialog box in Reaction Enumeration. The workflow followed is:
    1. Used a fixture to create a saved reaction.
    2. Creating a copy of the old reaction but with a different name (old reaction is unaffected)
        a. Edit the reaction and click on Save.
        b. Make changes to the reaction name and ensure the "Confirm Reaction Update" dialog box opens.
        c. Click on "Create New" which should create a new reaction.
    3. Navigate to the new copy of the reaction and update it. (overwriting the reaction)
        a. Follow steps 2a, 2b, 2c and then click on "Update" instead of "Create New".
    4. Ensure that the reaction is Updated.
    5. Subsequently delete the updated reaction.

    :param selenium: Selenium Webdriver
    :param create_new_rxn: Fixture to create a new reaction.
    """

    # Opening the reaction enumeration wizard
    open_enumeration_wizard(selenium)

    # Choose a reaction source (Schrodinger collection, saved or New)
    choose_a_rxn_source(selenium, get_reaction_from="Saved reactions")

    # Search and select the reaction
    search_for_reaction(selenium, reaction_name=create_new_rxn.name)
    dom.click_element(selenium, REACTION_EDIT_PICKER)

    # The Maestro sketcher sometime takes time to load, so adding a wait for it to load.
    @iframe.within_iframe(RXN_ENUM_SKETCHER_IFRAME)
    def wait_for_maestro_sketcher_to_load(_driver):
        wait.until_visible(_driver, '#qtcanvas')

    wait_for_maestro_sketcher_to_load(selenium)

    # -------- Creating a copy of the old reaction but with a different name (old reaction is unaffected) -------- #
    dom.click_element(selenium, ENUMERATION_LINKS, text='Save')
    verify_is_visible(selenium, MODAL_DIALOG_HEADER, selector_text='Save Reaction')
    new_reaction_name = make_unique_name("Fluorination of benzene")
    dom.set_element_value(selenium, SAVE_REACTION_NAME_INPUT, new_reaction_name)
    base.click_ok(selenium)

    # Verification of dialog box and clicking Create New
    verify_is_visible(selenium, MODAL_DIALOG_HEADER, selector_text='Confirm Reaction Update')
    dom.click_element(selenium, CREATE_NEW_OVERWRITE_OK, text="Create New")

    # Choose a reaction source (Schrodinger collection, saved or New).
    choose_a_rxn_source(selenium, get_reaction_from="Saved reactions")

    # Search and select the reaction
    search_for_reaction(selenium, reaction_name=new_reaction_name)
    dom.click_element(selenium, REACTION_EDIT_PICKER)

    # -------- Navigate to the new copy of the reaction and update it. (overwriting the reaction) -------- #
    dom.click_element(selenium, ENUMERATION_LINKS, text='Save')
    verify_is_visible(selenium, MODAL_DIALOG_HEADER, selector_text='Save Reaction')
    updated_reaction_name = make_unique_name("Fluorination of benzene updated")
    dom.set_element_value(selenium, SAVE_REACTION_NAME_INPUT, updated_reaction_name)
    base.click_ok(selenium)
    verify_is_visible(selenium, MODAL_DIALOG_HEADER, selector_text='Confirm Reaction Update')
    dom.click_element(selenium, CREATE_NEW_OVERWRITE_OK, text="Update")

    # -------- Searching for the reaction and deleting the updated reaction. -------- #
    choose_a_rxn_source(selenium, get_reaction_from="Saved reactions")
    search_for_reaction(selenium, reaction_name=updated_reaction_name)
    dom.click_element(selenium, DELETE_REACTION)
    base.click_ok(selenium)
