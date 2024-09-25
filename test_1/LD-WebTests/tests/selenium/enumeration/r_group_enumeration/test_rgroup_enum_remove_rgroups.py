import pytest
from library import wait

from resources.structures.structures_test_rgroup_enum_edit_and_remove_rgroups import \
    ONE_THREE_SUSTITUTED_CYCLOHEXANE_SCAFFOLD, RGROUP_A_FOR_ONE_THREE_SUBSTITUTED_CYCLOHEXANE_SCAFFOLD,\
    RGROUP_B_FOR_ONE_THREE_SUBSTITUTED_CYCLOHEXANE_SCAFFOLD, ONE_THREE_SUBSTITUTED_CYCLOHEXANE_SMILES_LIST_REMOVE_RGROUP,\
    EDITED_RGROUP_A_FOR_ONE_THREE_SUBSTITUTED_CYCLOHEXANE_SCAFFOLD,\
    EDITED_RGROUP_B_FOR_ONE_THREE_SUBSTITUTED_CYCLOHEXANE_SCAFFOLD
from helpers.change.enumeration import open_enumeration_wizard, click_enumeration_proceed_button,\
    add_structures_via_sketcher, edit_or_remove_r_group_from_enum_panel, close_enumeration_wizard,\
    select_and_remove_multiple_r_groups
from helpers.change.sketcher import import_structure_into_sketcher
from helpers.selection.enumeration import ENUMERATION_SCAFFOLD_SKETCHER, ENUMERATION_STRUCTURE_COUNT, ENUMERATION_STATUS
from helpers.verification.element import verify_is_visible
from helpers.verification.grid import verify_footer_values, verify_visible_columns_in_live_report, verify_column_contents
from helpers.change.grid_column_menu import sort_grid_by


@pytest.mark.require_webgl
@pytest.mark.usefixtures('open_livereport')
@pytest.mark.usefixtures('new_live_report')
def test_rgroup_enum_remove_rgroups(selenium):
    """
    Removes R-group in R-Group Enumeration wizard by right-clicking the R-group & selecting 'Remove Selected' option

    1. Provide Scaffold & R-groups (2 R-group structures for both R1 & R2) in the R-group Enumeration Wizard
    2. Verify the number of structures in R1, R2 & Product Preview containers
    3. Right click R-group in container 'R1' & choose "Remove Selected"
    4. Bulk select & remove 2 R-groups from 'R1' container using shift-click action
    5. Verify the number of structures in R1 & Product Preview containers
    6. Click on 'Enumerate' button and wait till Enumeration is completed
    7. Close R-group Enumeration Wizard
    8. Verify LR's footer values, expected column's list & Compound SMILES to confirm expected products & columns are present

    :param selenium: Webdriver
    """

    scaffold = ONE_THREE_SUSTITUTED_CYCLOHEXANE_SCAFFOLD
    list_of_R1_rgroups = [
        RGROUP_A_FOR_ONE_THREE_SUBSTITUTED_CYCLOHEXANE_SCAFFOLD,
        RGROUP_B_FOR_ONE_THREE_SUBSTITUTED_CYCLOHEXANE_SCAFFOLD,
        EDITED_RGROUP_A_FOR_ONE_THREE_SUBSTITUTED_CYCLOHEXANE_SCAFFOLD,
        EDITED_RGROUP_B_FOR_ONE_THREE_SUBSTITUTED_CYCLOHEXANE_SCAFFOLD
    ]
    list_of_R2_rgroups = [
        RGROUP_A_FOR_ONE_THREE_SUBSTITUTED_CYCLOHEXANE_SCAFFOLD, RGROUP_B_FOR_ONE_THREE_SUBSTITUTED_CYCLOHEXANE_SCAFFOLD
    ]

    # Open R-group Enumeration wizard
    open_enumeration_wizard(selenium, enumeration_type='R-Group')

    # Select New Sketch option & add/ import the scaffold to the sketcher
    import_structure_into_sketcher(selenium,
                                   molv3_or_smiles=scaffold,
                                   sketcher_iframe_selector=ENUMERATION_SCAFFOLD_SKETCHER)

    # Click on "Next" button to take you to R-group tab
    click_enumeration_proceed_button(selenium)

    # Add R-group/s via New sketches option
    add_structures_via_sketcher(selenium, structures=list_of_R1_rgroups, structure_tag="R1", reaction_enum=False)
    add_structures_via_sketcher(selenium,
                                structures=list_of_R2_rgroups,
                                structure_tag="R2",
                                explicitly_open_sketcher=True,
                                reaction_enum=False)

    # Verify the number of R-group/s in each R-group container/s
    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('first-child'),
                      selector_text="(4 structures",
                      exact_selector_text_match=True,
                      custom_timeout=10)

    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('nth-child(2)'),
                      selector_text="(2 structures",
                      exact_selector_text_match=True,
                      custom_timeout=10)

    # Verify the number of products in Product Preview structure container
    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format("last-child"),
                      selector_text="(7 structures",
                      exact_selector_text_match=True,
                      custom_timeout=20)

    # Stay in R-group Enumeration wizard, right click & select 2nd R-group from 'R1' container & select "Remove Selected"
    edit_or_remove_r_group_from_enum_panel(selenium,
                                           rgroup_container_index=0,
                                           rgroup_to_right_click_index=1,
                                           action_item="Remove Selected")

    # Perform Shift-click to select last 2 R-groups from 'R1' container & click "Remove Selected"
    select_and_remove_multiple_r_groups(selenium, parent_index=0, start_rgroup_index=1, end_rgroup_index=2)

    # Verify the number of structures in R1 & Product Preview structure container
    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('first-child'),
                      selector_text="(1 structures",
                      exact_selector_text_match=True,
                      custom_timeout=10)

    verify_is_visible(selenium,
                      selector=ENUMERATION_STRUCTURE_COUNT.format("last-child"),
                      selector_text="(2 structures",
                      exact_selector_text_match=True,
                      custom_timeout=15)

    # Click on "Enumerate" button to proceed & wait till enumeration is completed
    click_enumeration_proceed_button(selenium)
    wait.until_visible(selenium, ENUMERATION_STATUS, text="Enumeration completed")

    # Close R-group Enum wizard
    close_enumeration_wizard(selenium)

    # Verify number of rows & columns in the LR
    verify_footer_values(selenium,
                         expected_grid_metadata={
                             'row_all_count': '2 Total Compounds',
                             'row_displayed_count': '2 Displayed Compounds',
                             'row_selected_count': '0 Selected',
                             'column_all_count': '6 Columns',
                             'column_hidden_count': '1 Hidden'
                         })

    # Verify expected visible columns in the LR
    expected_column_list = [
        'Compound Structure', 'ID', 'All IDs', 'Rationale', 'Lot Scientist', 'Highlighted Substructure'
    ]

    verify_visible_columns_in_live_report(selenium, expected_column_list=expected_column_list)

    # Verify enumerated compound's SMILES
    compounds_smiles_list = ONE_THREE_SUBSTITUTED_CYCLOHEXANE_SMILES_LIST_REMOVE_RGROUP
    sort_grid_by(selenium, column_name='Compound Structure', sort_ascending=True)
    verify_column_contents(selenium, column_name='Compound Structure', expected_content=compounds_smiles_list)
