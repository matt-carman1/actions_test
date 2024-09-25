"""
Selenium test for Reaction Enumeration via file upload
"""

import pytest

from helpers.change.enumeration import open_enumeration_wizard, search_for_reaction, choose_a_rxn_source, \
    close_enumeration_wizard, add_structures_via_file_upload
from helpers.change.actions_pane import close_add_data_panel
from helpers.change.columns_management_ui import open_column_mgmt_panel
from helpers.selection.grid import Footer
from helpers.verification.grid import verify_footer_values
from helpers.verification.data_and_columns_tree import verify_visible_columns_from_column_mgmt_ui
from helpers.verification.element import verify_is_visible
from helpers.selection.enumeration import ENUMERATION_PROCEED_BUTTON, ENUMERATION_STRUCTURE_COUNT, \
    ENUMERATION_ACTIVE_TAB, ENUMERATION_STATUS
from library import dom, wait
from library.utils import is_k8s


@pytest.mark.xfail(not is_k8s(), reason="SS-40265: RMQ issues in Old Jenkins")
@pytest.mark.require_webgl
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_rxn_enum_via_csv_file_upload(selenium):
    """
    Reaction enumeration test via file upload by csv:
    1. Enumerate for a reaction with reactants via File upload by csv.
    2. Interact with the csv dialog box.
    3. Validated the number of products and columns in the LiveReport.

    :param selenium: Selenium Webdriver
    """

    open_enumeration_wizard(selenium)

    # Choose a reaction source from the Schrodinger collection
    choose_a_rxn_source(selenium)

    # Search and select the reaction
    search_for_reaction(selenium, reaction_name="1,5-disubstituted tetrazole synthesis")

    # Navigate to the ADD REACTANTS tab
    dom.click_element(selenium, ENUMERATION_PROCEED_BUTTON, text="Next >")
    wait.until_visible(selenium, ENUMERATION_ACTIVE_TAB, text="ADD REACTANTS")

    # Adding reactants via file upload- csv type
    add_structures_via_file_upload(selenium, "nitriles.csv", is_csv_file=True)

    add_structures_via_file_upload(selenium, "halides.csv", structure='B', is_csv_file=True)

    # Verification that the desired number of reactants are populated
    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('first-child'),
                      selector_text="(7 structures",
                      exact_selector_text_match=True,
                      custom_timeout=10)
    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('nth-child(2)'),
                      selector_text="(5 structures",
                      exact_selector_text_match=True,
                      custom_timeout=10)

    # Verify the number of expected products
    verify_is_visible(selenium,
                      ENUMERATION_STRUCTURE_COUNT.format('last-child'),
                      selector_text="(15 structures",
                      exact_selector_text_match=True,
                      custom_timeout=10)

    # Enumerating after the product preview is populated
    dom.click_element(selenium, ENUMERATION_PROCEED_BUTTON, text="Enumerate")
    wait.until_visible(selenium, ENUMERATION_STATUS, text='Enumeration completed')

    close_enumeration_wizard(selenium)

    # Validate the number of products and columns in the LiveReport
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(15),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(16),
            Footer.COLUMN_HIDDEN_COUNT_KEY: Footer.COLUMN_HIDDEN_COUNT_VALUE.format(1)
        })

    expected_column_list = [
        'ID', 'All IDs', 'Rationale', 'Lot Scientist', 'R1: Structure (Schrodinger)', 'R1: All IDs (Schrodinger)',
        'R1: File upload (file name)', 'R1: File upload (test formula)', 'R1: File upload (Quick Properties (AlogP))',
        'R1: File upload (ID)', 'R2: Structure (Schrodinger)', 'R2: All IDs (Schrodinger)',
        'R2: File upload (file name)', 'R2: File upload (Mw plus 201 formula)', 'R2: File upload (ID)'
    ]

    # Verifies that all the expected columns are visible from the Column management UI
    open_column_mgmt_panel(selenium)

    verify_visible_columns_from_column_mgmt_ui(selenium, expected_column_list)
    close_add_data_panel(selenium)
