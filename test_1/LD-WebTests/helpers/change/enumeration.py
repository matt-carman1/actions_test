from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from helpers.change.actions_pane import open_tools_pane, TOOLS_PANE_TOOL
from helpers.change.live_report_picker import open_live_report
from helpers.selection.live_report_picker import REPORT_PICKER
from helpers.selection.live_report_tab import CREATE_NEW_LIVE_REPORT
from helpers.selection.modal import WINDOW_HEADER_TEXT
from helpers.change.sketcher import import_structure_into_sketcher
from helpers.verification.element import verify_is_visible
from helpers.selection.enumeration import NEW_ENUMERATION_WIZARD_WINDOW, \
    EXIT_ENUMERATION_BUTTON, ENUMERATION_TAB, ENUMERATION_SOURCE_PICKER_LIST_LABEL, REACTION_FILTER_INPUT, \
    REACTION_PICKER_LIST, ENUMERATION_SIDEBAR_TAB, REACTION_ENUM_IMPORT_FROM_FILE, ENUMERATION_NEW_SKETCH_BUTTON, \
    ENUMERATION_SOURCE_PICKER, CLOSE_SKETCHER_DIALOG, ENUMERATION_RGROUP_SKETCHER, \
    ENUMERATION_CHOOSE_LIVE_REPORT_LINK, ENUMERATION_REACTANT_SKETCHER, SAVE_REACTANT_A_NAME_INPUT, \
    SAVE_REACTANT_B_NAME_INPUT, SAVE_REACTION_DESCRIPTION_INPUT, SAVE_REACTION_NAME_INPUT, ENUMERATION_LINKS, \
    ENUMERATION_CSV_DIALOG_ID_DROPDOWN, ENUMERATION_PROCEED_BUTTON, RGROUP_ENUM_TARGET_LR_DROPDOWN, \
    RGROUP_ENUM_SELECT_TARGET_LR, RGROUP_ENUM_ADD_BUTTON, RGROUP_ENUM_CANCEL_BUTTON, RGROUP_CONTAINERS, R_GROUPS
from helpers.selection.modal import MODAL_DIALOG_HEADER
from helpers.extraction import paths
from library.dom import LiveDesignWebException
from library import dom, base, ensure, wait, select, simulate


def open_enumeration_wizard(driver, enumeration_type='Reaction'):
    """
    Opens Enumeration Panel based on the enumeration type
    :param driver: Selenium Webdriver
    enumeration_type: str, "Reaction" or "R-Group"
                    Default is "Reaction"
    :return:
    """

    if enumeration_type not in ("Reaction", "R-Group"):
        raise LiveDesignWebException('enumeration_type must be either "Reaction" or "R-Group"')

    open_tools_pane(driver)
    dom.click_element(driver, TOOLS_PANE_TOOL, enumeration_type, True)
    # Verify reaction enumeration wizard is open
    verify_is_visible(driver, NEW_ENUMERATION_WIZARD_WINDOW, message='Could not locate Enumeration Wizard window')


def close_enumeration_wizard(driver):
    """
    Closes the Enumeration Wizard panel on the right side

    :param driver: Selenium Webdriver
    """
    ensure.element_not_visible(driver,
                               action_selector=EXIT_ENUMERATION_BUTTON,
                               expected_not_visible_selector=NEW_ENUMERATION_WIZARD_WINDOW)


def choose_a_rxn_source(driver, get_reaction_from="Schrödinger collection"):
    """
    Choose a source for the reaction.

    :param driver: Selenium Webdriver
    :param get_reaction_from: str, reaction collections whether Schrödinger collection or Saved reactions or New Sketch.
                              Default is Schrödinger collection.
    """
    dom.click_element(driver, ENUMERATION_TAB, text="CHOOSE REACTION")
    dom.click_element(driver, ENUMERATION_SOURCE_PICKER_LIST_LABEL, text=get_reaction_from, exact_text_match=True)


def search_for_reaction(driver, reaction_name):
    """
    Search for reaction from the Schrödinger collection or Saved reactions.

    :param driver: Selenium Webdriver
    :param reaction_name: str, reaction name to be searched.
    """
    dom.set_element_value(driver, REACTION_FILTER_INPUT, value=reaction_name)
    dom.click_element(driver, REACTION_PICKER_LIST, text=reaction_name, exact_text_match=True)


def add_structures_from_live_report(driver, live_report_name, structure_name='REACTANT A'):
    """
    Add structures from the given LiveReport for the requested reactant/r-group name.
    :param driver: Selenium Webdriver
    :param live_report_name: str, LiveReport name containing reactants/r-group
    :param structure_name: str, Reactant/R-group name for which structures are to be added from the LiveReport.
    :return:
    """
    # Click on the reactant
    dom.click_element(driver, ENUMERATION_SIDEBAR_TAB, text=structure_name)

    dom.click_element(driver, ENUMERATION_SOURCE_PICKER_LIST_LABEL, text='LiveReports')
    dom.click_element(driver, ENUMERATION_CHOOSE_LIVE_REPORT_LINK, text='Choose LiveReport...')
    open_live_report(driver, name=live_report_name)


def add_structures_via_file_upload(driver, structure_file, structure='REACTANT A', is_csv_file=False):
    """
    Helper for file upload of reactants with/without metadata.

    :param driver: Selenium Webdriver
    :param structure_file: str, the name of the  file to be uploaded for reactants or r-groups.
    :param structure: str, The reactant or r-group to be selected, defaults to 'REACTANT A'.
    :param is_csv_file: boolean, Set to True if the imported file type is of csv format
    """
    # Setting path for the reactant files to be uploaded
    file_path = paths.get_resource_path(structure_file)

    dom.click_element(driver, ENUMERATION_SIDEBAR_TAB, structure)
    file_input = dom.get_element(driver, REACTION_ENUM_IMPORT_FROM_FILE, must_be_visible=False)
    file_input.send_keys(file_path)

    if is_csv_file:
        verify_is_visible(driver, MODAL_DIALOG_HEADER, selector_text="Confirm CSV File Contents")

        select.select_option_by_text(driver, ENUMERATION_CSV_DIALOG_ID_DROPDOWN, "ID")
        base.click_ok(driver)


def add_structures_via_sketcher(driver,
                                structures=[],
                                structure_tag="R1",
                                explicitly_open_sketcher=False,
                                reaction_enum=False):
    """
    Selects the Reactant/R-group tab and sketches a reactant/R-group for it.
    :param driver: Selenium Webdriver
    :param structures: list, List of reactants/R-groups structures.
    :param structure_tag: str, The structure_tag to be used, Ex: R1, REACTANT A etc.
    :param explicitly_open_sketcher: Boolean, true if the sketcher needs to be opened explicitly.
    :param reaction_enum: Boolean, true if using the Reaction Enumeration
    """

    dom.click_element(driver, ENUMERATION_SIDEBAR_TAB, text=structure_tag)

    if reaction_enum:
        sketcher_iframe = ENUMERATION_REACTANT_SKETCHER
    else:
        sketcher_iframe = ENUMERATION_RGROUP_SKETCHER

    # Ensure that the radio button for "New sketches..." is selected
    ensure.element_visible(driver,
                           action_selector=ENUMERATION_SOURCE_PICKER_LIST_LABEL,
                           action_selector_text='New sketches...',
                           expected_visible_selector=ENUMERATION_NEW_SKETCH_BUTTON)
    # Ensure that the sketcher is open else click on "Add Sketch..." to open it. This is because we might need to
    # close the sketcher once and then open again. That would require clicking on "Add Sketch..."
    if explicitly_open_sketcher:
        dom.click_element(driver, ENUMERATION_SOURCE_PICKER, text='Add Sketch...')
    wait.until_visible(driver, sketcher_iframe)

    for structure in structures:
        import_structure_into_sketcher(driver, structure, sketcher_iframe_selector=sketcher_iframe)
        base.click_ok(driver)

    dom.click_element(driver, CLOSE_SKETCHER_DIALOG, text='Close')


def save_reaction_form(driver, reaction_name, reaction_description, reactant_a, reactant_b):
    """
    Helper for filling the form for newly sketched reactions- for two component reaction.

    :param driver: Selenium Webdriver
    :param reaction_name: str, the name of the reaction.
    :param reaction_description: str, the reaction description.
    :param reactant_a: str, the name of reactant A
    :param reactant_b: str, the name of reactant B
    """
    dom.click_element(driver, ENUMERATION_LINKS, text='Save')
    verify_is_visible(driver, MODAL_DIALOG_HEADER, selector_text='Save Reaction')
    dom.set_element_value(driver, SAVE_REACTION_NAME_INPUT, reaction_name)
    dom.set_element_value(driver, SAVE_REACTION_DESCRIPTION_INPUT, reaction_description)
    dom.set_element_value(driver, SAVE_REACTANT_A_NAME_INPUT, reactant_a)
    dom.set_element_value(driver, SAVE_REACTANT_B_NAME_INPUT, reactant_b)
    base.click_ok(driver)


def click_enumeration_proceed_button(driver):
    """
    Helper serves two alternative purposes in Enumeration wizard:

    A. It can be used to click "Next" button on Scaffold tab & Choose Reaction tab under Enumeration wizard
    B. OR it can be used to click "Enumerate" button on R-Groups tab & Add Reactants tab under Enumeration wizard

    :param driver: Selenium Webdriver
    """
    dom.click_element(driver, ENUMERATION_PROCEED_BUTTON)


def open_create_live_report_dialog_from_enum_panel(driver):
    """
    1. Opens "Create New LiveReport" dialog from Enumeration Wizard
    2. User can create a new LR & save Enumeration Results to it

    :param driver: Selenium Webdriver
    """
    dom.click_element(driver, RGROUP_ENUM_TARGET_LR_DROPDOWN)
    ensure.element_visible(driver,
                           action_selector=RGROUP_ENUM_SELECT_TARGET_LR.format('first-child'),
                           action_selector_text="New LiveReport...",
                           action_selector_exact_text_match=True,
                           expected_visible_selector=WINDOW_HEADER_TEXT,
                           expected_visible_selector_text=CREATE_NEW_LIVE_REPORT)


def open_live_report_meta_picker_from_enum_panel(driver):
    """
    1. Opens "LiveReport Meta Picker" from Enumeration Wizard
    2. User can choose an LR to save Enumeration Results

    :param driver: Selenium Webdriver
    """
    dom.click_element(driver, RGROUP_ENUM_TARGET_LR_DROPDOWN)
    ensure.element_visible(driver,
                           action_selector=RGROUP_ENUM_SELECT_TARGET_LR.format('last-child'),
                           action_selector_text="Choose LiveReport...",
                           action_selector_exact_text_match=True,
                           expected_visible_selector=REPORT_PICKER)


def select_to_edit_or_remove_r_group(driver, action_item_name):
    """
    User can either choose "Remove Selected" to delete selected r-group Or "Edit Structure" to edit selected R-group

    :param driver: Selenium Webdriver
    :param action_item_name: str, name of the action item to be applied on selected R-group/s
    """
    RGROUP_ENUM_RGROUP_ACTIONS = RGROUP_ENUM_SELECT_TARGET_LR
    dom.click_element(driver,
                      text=action_item_name,
                      exact_text_match=True,
                      selector=RGROUP_ENUM_RGROUP_ACTIONS,
                      timeout=10,
                      must_be_visible=True)


def click_rgroup_enum_sketcher_add_button_and_close_sketcher(driver):
    """
    Helper is used to add structure to open r-group enumeration sketcher & close the sketcher:

    A. Clicks "Add" button on R-group Enumeration Sketcher when it is opened from "Edit Structure" option & new structure is added
    B. Then closes the Sketcher by clicking "Cancel" button to take user back to R-Groups tab

    :param driver: Selenium Webdriver
    """
    dom.click_element(driver, RGROUP_ENUM_ADD_BUTTON)
    dom.click_element(driver, RGROUP_ENUM_CANCEL_BUTTON, text="Cancel")


def select_and_remove_multiple_r_groups(driver, parent_index, start_rgroup_index, end_rgroup_index):
    """
    Helper to select & delete multiple R-groups of an R-group container with Shift click action:

    A. Gets list of all R-group containers, based on number of R-groups added to the Scaffold
    B. Gets required R-group container by using its corresponding index in the list
    C. Gets list of all R-groups from selected R-group container
    D. Identifies start & end R-groups for bulk selection using their corresponding indices
    E. Performs Shift click action to select all R-groups from start_rgroup to end_rgroup
    F. Performs right click action on end_rgroup
    G. Deletes all selected R-groups in one go

    For Example, for a Scaffold with 2 R-groups, 'R1' & 'R2', 'R1' container will have index of '0' & 'R2' container
    will have index of '1'. And first R-group in 'R1' container will have index of '0'.

    :param driver: Selenium Webdriver
    :param parent_index: Index of required R-group container from the R-group containers list
    :param start_rgroup_index: Index of first R-group needs to be deleted, from the R-group list
    :param end_rgroup_index: Index of last R-group needs to be deleted, from the R-group list
    """
    rgroup_containers_list = dom.get_elements(driver, selector=RGROUP_CONTAINERS, timeout=15)
    rgroup_container_element = rgroup_containers_list[parent_index]
    rgroups_list = dom.get_elements(rgroup_container_element, selector=R_GROUPS, timeout=10)
    start_rgroup = rgroups_list[start_rgroup_index]
    end_rgroup = rgroups_list[end_rgroup_index]
    ActionChains(driver).click(start_rgroup).key_down(Keys.SHIFT).click(end_rgroup).key_up(Keys.SHIFT).perform()
    simulate.right_click(end_rgroup)
    select_to_edit_or_remove_r_group(driver, action_item_name="Remove Selected")


def edit_rgroup_by_double_click(driver, rgroup_container_index, rgroup_to_double_click_index):
    """
    Helper to get & select R-group with double click action and ensure that Sketcher opens to add new R-group

    A. Gets list of all R-group containers, based on number of R-groups added to the Scaffold
    B. Gets required R-group container by using its corresponding index in the list
    C. Gets list of all R-groups from selected R-group container
    D. Performs double click action on R-group to be edited
    E. Ensures that the R-group Enumeration Sketcher is indeed open

    For Example, for a Scaffold with 2 R-groups, 'R1' & 'R2', 'R1' container will have index of '0' & 'R2' container
    will have index of '1'. And first R-group in 'R1' container will have index of '0'.

    :param driver: Selenium Webdriver
    :param rgroup_container_index: Index of required R-group container from the R-group containers list
    :param rgroup_to_double_click_index: Index of the R-group needs to be double-clicked & edited
    """
    rgroup_container_list = dom.get_elements(driver, selector=RGROUP_CONTAINERS, timeout=10)
    rgroup_container_element = rgroup_container_list[rgroup_container_index]
    rgroup_list = dom.get_elements(rgroup_container_element, selector=R_GROUPS, timeout=10)
    simulate.double_click(rgroup_list[rgroup_to_double_click_index])
    verify_is_visible(driver, selector=ENUMERATION_RGROUP_SKETCHER, custom_timeout=3)


def edit_or_remove_r_group_from_enum_panel(driver, rgroup_container_index, rgroup_to_right_click_index, action_item):
    """
    Helper to get, select & edit/ remove R-group with right click action:

    A. Gets list of all R-group containers, based on number of R-groups added to the Scaffold
    B. Gets required R-group container by using its corresponding index in the list
    C. Gets list of all R-groups from selected R-group container
    D. Performs right click action on R-group to be edited/ deleted
    E. Selects the action to be performed on selected R-group

    For Example, for a Scaffold with 2 R-groups, 'R1' & 'R2', 'R1' container will have index of '0' & 'R2' container
    will have index of '1'. And second R-group in 'R1' container will have index of '1'.

    :param driver: Selenium Webdriver
    :param rgroup_container_index: Index of required R-group container from the R-group containers list
    :param rgroup_to_right_click_index: Index of the R-group needs to be right-clicked
    :param action_item: str, name of the action item to be applied on selected R-group/s
    """
    rgroup_container_list = dom.get_elements(driver, selector=RGROUP_CONTAINERS, timeout=10)
    rgroup_container_element = rgroup_container_list[rgroup_container_index]
    rgroup_list = dom.get_elements(rgroup_container_element, selector=R_GROUPS, timeout=10)
    simulate.right_click(rgroup_list[rgroup_to_right_click_index])
    select_to_edit_or_remove_r_group(driver, action_item_name=action_item)
