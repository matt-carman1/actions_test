"""
Selenium test for Reaction Enumeration via file upload
"""

import pytest

from helpers.change.enumeration import open_enumeration_wizard, search_for_reaction, choose_a_rxn_source, \
    close_enumeration_wizard, add_structures_via_file_upload
from helpers.selection.grid import Footer
from helpers.verification.grid import verify_footer_values, verify_grid_contents
from helpers.verification.data_and_columns_tree import verify_visible_columns_from_column_mgmt_ui
from helpers.verification.element import verify_is_visible
from helpers.change.actions_pane import open_add_data_panel, close_add_data_panel
from helpers.change.grid_column_menu import sort_grid_by
from helpers.selection.enumeration import ENUMERATION_PROCEED_BUTTON, ENUMERATION_STRUCTURE_COUNT, \
    ENUMERATION_ACTIVE_TAB, ENUMERATION_STATUS
from helpers.selection.column_tree import COLUMNS_TREE_LIVEREPORT_TAB
from library import dom, wait
from library.utils import is_k8s


@pytest.mark.xfail(not is_k8s(), reason="SS-40265: RMQ issues in Old Jenkins")
@pytest.mark.require_webgl
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_rxn_enum_via_file_upload(selenium):
    """
    Reaction enumeration test via file upload:
    1. Enumerate for a reaction with reactants via File upload
    2. Validated the number of products and columns in the LiveReport.
    3. Validated the contents of these columns in the LiveReport.

    :param selenium: Selenium Webdriver
    """
    sdf_metadata_reactant_a = {
        "reagant_id": ['CHEMBL1275940', 'CHEMBL1275940', 'CHEMBL1275971', 'CHEMBL1275971'],
        "vendor_list": ['Jannsen', 'Jannsen', 'BMS', 'BMS'],
        "price_list": ['7000', '7000', '800', '800']
    }
    sdf_metadata_reactant_b = {
        "reagant_id": ['CMPD-32796', 'V35003', 'CMPD-32796', 'V35003'],
        "vendor_list": ['Sanofi', 'Celgene', 'Sanofi', 'Celgene'],
        "price_list": ['230', '510', '230', '510']
    }

    open_enumeration_wizard(selenium)

    # Choose a reaction source (Schrodinger collection, saved or New). Default is Schrodinger collection
    choose_a_rxn_source(selenium)

    # Search and select the reaction
    search_for_reaction(selenium, reaction_name="Suzuki coupling of aryl/vinyl boronates with aryl/vinyl halides")

    # Navigate to the ADD REACTANTS tab
    dom.click_element(selenium, ENUMERATION_PROCEED_BUTTON, text="Next >")
    wait.until_visible(selenium, ENUMERATION_ACTIVE_TAB, text="ADD REACTANTS")

    # Adding reactants via file upload
    add_structures_via_file_upload(selenium, "test_aryl_bromides.sdf")
    add_structures_via_file_upload(selenium, "test_aryl_boronates.sdf", structure='B')

    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('first-child'),
                      selector_text="(2 structures",
                      exact_selector_text_match=True,
                      custom_timeout=2)
    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('nth-child(2)'),
                      selector_text="(2 structures",
                      exact_selector_text_match=True,
                      custom_timeout=2)

    # Verify the number of expected products
    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('last-child'),
                      selector_text="(4 structures",
                      exact_selector_text_match=True,
                      custom_timeout=15)

    # Enumerating after the product preview is populated
    dom.click_element(selenium, ENUMERATION_PROCEED_BUTTON, text="Enumerate")
    wait.until_visible(selenium, ENUMERATION_STATUS, text='Enumeration completed')

    close_enumeration_wizard(selenium)

    # Validate the number of products and columns in the LiveReport
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(4),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(17),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(1)
        })

    expected_column_list = [
        'ID', 'All IDs', 'Rationale', 'Lot Scientist', 'R1: Structure (Schrodinger)', 'R1: All IDs (Schrodinger)',
        'R1: File upload (file name)', 'R1: File upload (reagent ID)', 'R1: File upload (price)',
        'R1: File upload (Vendor name)', 'R2: Structure (Schrodinger)', 'R2: All IDs (Schrodinger)',
        'R2: File upload (file name)', 'R2: File upload (reagent ID)', 'R2: File upload (Vendor)',
        'R2: File upload (price)'
    ]

    # Verifies that all the expected columns are visible from the Column management UI
    open_add_data_panel(selenium)
    dom.click_element(selenium, COLUMNS_TREE_LIVEREPORT_TAB)

    verify_visible_columns_from_column_mgmt_ui(selenium, expected_column_list)
    close_add_data_panel(selenium)

    sort_grid_by(selenium, column_name='All IDs')

    # Verifying that the contents of the reactant metadata columns from reactant A and B are as expected
    verify_grid_contents(
        selenium, {
            expected_column_list[7]: sdf_metadata_reactant_a["reagant_id"],
            expected_column_list[8]: sdf_metadata_reactant_a["price_list"],
            expected_column_list[9]: sdf_metadata_reactant_a["vendor_list"],
            expected_column_list[13]: sdf_metadata_reactant_b["reagant_id"],
            expected_column_list[14]: sdf_metadata_reactant_b["vendor_list"],
            expected_column_list[15]: sdf_metadata_reactant_b["price_list"]
        })
