import pytest
from library import wait
from library.utils import is_k8s

from resources.structures.structures_test_export_rgroup_enum_results_to_new_lr import \
    ONE_THREE_SUBSTITUTED_CYCLOPENTANE_SCAFFOLD, RGROUP_A_FOR_ONE_THREE_SUBSTITUTED_CYCLOPENTANE_SCAFFOLD, \
    RGROUP_B_FOR_ONE_THREE_SUBSTITUTED_CYCLOPENTANE_SCAFFOLD, ONE_THREE_SUBSTITUTED_CYCLOPENTANE_SMILES_LIST
from helpers.change.enumeration import open_enumeration_wizard, close_enumeration_wizard,\
    add_structures_via_sketcher, click_enumeration_proceed_button, open_create_live_report_dialog_from_enum_panel
from helpers.selection.enumeration import ENUMERATION_SCAFFOLD_SKETCHER, ENUMERATION_STRUCTURE_COUNT, ENUMERATION_STATUS
from helpers.verification.element import verify_is_visible
from helpers.change.live_report_picker import fill_details_for_new_livereport
from helpers.verification.live_report import verify_live_report_open
from helpers.verification.grid import verify_footer_values, verify_visible_columns_in_live_report,\
    verify_column_contents
from helpers.change.grid_column_menu import sort_grid_by
from helpers.change.sketcher import import_structure_into_sketcher

test_livereport = "Enumeration"


@pytest.mark.xfail(not is_k8s(), reason="SS-40265: RMQ issues in Old Jenkins")
@pytest.mark.xfail(is_k8s(), reason="SS-42730: Unknown failure reason on New Jenkins")
@pytest.mark.require_webgl
@pytest.mark.usefixtures("open_livereport")
def test_export_rgroup_enum_results_to_new_lr(selenium):
    """
    Exports R-group Enumeration products into a new LR

    1. Provide Scaffold & R-groups (2 R-group structures for both R1 & R2) in the R-group Enumeration Wizard
    2. Verify the number of structures in R1, R2 & Product Preview containers
    3. Select 'New LiveReport' option as the target LR and fill in the details for the same
    4. Verify if the newly created LR is open
    5. Click on 'Enumerate' button and wait till Enumeration is completed
    6. Close R-group Enumeration Wizard
    7. Verify new LR's footer values & expected column's list to confirm number of products & columns added
    8. Verify the Compound SMILES to confirm that expected products are enumerated

    :param selenium: Webdriver
    """

    # Add & pull all Structures to & from resources >> structures >> test_file_name.py file respectively
    scaffold = ONE_THREE_SUBSTITUTED_CYCLOPENTANE_SCAFFOLD
    list_of_r_groups = [
        RGROUP_A_FOR_ONE_THREE_SUBSTITUTED_CYCLOPENTANE_SCAFFOLD,
        RGROUP_B_FOR_ONE_THREE_SUBSTITUTED_CYCLOPENTANE_SCAFFOLD
    ]
    compound_smiles_list = ONE_THREE_SUBSTITUTED_CYCLOPENTANE_SMILES_LIST

    # Open the R-group Enumeration wizard
    open_enumeration_wizard(selenium, enumeration_type='R-Group')

    # Select New Sketch option and add the scaffold to the Sketcher
    import_structure_into_sketcher(selenium,
                                   molv3_or_smiles=scaffold,
                                   sketcher_iframe_selector=ENUMERATION_SCAFFOLD_SKETCHER)

    # Click on 'Next' button (takes the user to R-group tab)
    click_enumeration_proceed_button(selenium)

    # Add R-groups via New Sketches option
    add_structures_via_sketcher(selenium, structures=list_of_r_groups, structure_tag="R1", reaction_enum=False)
    add_structures_via_sketcher(selenium,
                                structures=list_of_r_groups,
                                structure_tag="R2",
                                explicitly_open_sketcher=True,
                                reaction_enum=False)

    # Verify the number of R-groups in each R-group structure container, should be 3
    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('first-child'),
                      selector_text="(2 structures",
                      exact_selector_text_match=True,
                      custom_timeout=10)

    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('nth-child(2)'),
                      selector_text="(2 structures",
                      exact_selector_text_match=True,
                      custom_timeout=10)

    # Verify the number of products in Product Preview structure container
    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('last-child'),
                      selector_text="(3 structures",
                      exact_selector_text_match=True,
                      custom_timeout=10)

    # Choose 'New LiveReport' option from 'target-lr-dropdown' to save enumeration results
    open_create_live_report_dialog_from_enum_panel(selenium)

    # Add New LR details & open new LR
    new_lr_for_enumeration = fill_details_for_new_livereport(selenium,
                                                             report_name="R-group Enum to New LR",
                                                             template="Blank",
                                                             folder_name="JS Testing Home",
                                                             rationale=None)

    # Verify that the new LR is indeed open
    verify_live_report_open(selenium, live_report_name=new_lr_for_enumeration, pending_timeout=10)

    # Click on 'Enumerate' button to proceed & wait till enumeration is completed
    click_enumeration_proceed_button(selenium)
    wait.until_visible(selenium, ENUMERATION_STATUS, text="Enumeration completed")

    close_enumeration_wizard(selenium)

    # Verify number of rows & columns in the new LR's footer
    verify_footer_values(selenium, {
        'row_all_count': '3 Compounds',
        'column_all_count': '6 Columns',
        'column_hidden_count': '1 Hidden'
    })

    # Verify expected visible columns in new LR
    expected_column_list = [
        'Compound Structure', 'ID', 'All IDs', 'Rationale', 'Lot Scientist', 'Highlighted Substructure'
    ]
    verify_visible_columns_in_live_report(selenium, expected_column_list)

    # Verify enumerated compound's SMILES
    sort_grid_by(selenium, column_name='Compound Structure', sort_ascending=True)
    verify_column_contents(selenium, column_name='Compound Structure', expected_content=compound_smiles_list)
