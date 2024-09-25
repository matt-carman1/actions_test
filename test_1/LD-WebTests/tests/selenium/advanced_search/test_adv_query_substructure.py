"""
Selenium test for Substructure advanced search for Compounds and R-groups
"""

import pytest
from helpers.change.advanced_search_actions import add_query_compound_structure
from helpers.change.grid_column_menu import sort_grid_by
from helpers.change.sketcher import import_structure_into_sketcher
from helpers.selection.advanced_search import SEARCH_AND_ADD_COMPOUNDS_BUTTON, CLEAR_REPORT_CHECKED, \
    CLEAR_REPORT_CHECKBOX, ADV_SEARCH_SKETCHER
from helpers.selection.filter_actions import COMPOUND_TYPE_CHECKBOX
from helpers.selection.grid import Footer
from helpers.selection.sketcher import ADVANCED_SEARCH_SKETCHER_IFRAME
from helpers.change.actions_pane import open_add_compounds_panel, open_advanced_search
from helpers.verification.grid import check_for_butterbar
from helpers.verification.grid import verify_footer_values, verify_column_contents, verify_is_visible
from library import dom, base


@pytest.mark.app_defect(reason="SS-33756")
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_adv_query_substructure(selenium):
    """
    Add compounds(both real and virtual) and R-groups using Advanced Substructure Compound Search and verifies the
    correct count and ID of compounds returned in LR

    Note: This Selenium test replicates Javascript system test feature.AdvQuerySubstructure
    :param selenium: Selenium Webdriver
    """
    smiles = 'NC1=CC=CC(O)=C1Cl'
    r_group_smiles = 'C* |$;_AP1$|'

    # ----- Substructure advanced Search for REAL only ----- #
    # Open the Compounds Panel & then the advanced search panel
    open_add_compounds_panel(selenium)
    open_advanced_search(selenium)
    # Need to disable VIRTUAL for a Real only search
    dom.click_element(selenium, COMPOUND_TYPE_CHECKBOX, text="VIRTUAL")
    # Adding a compound query
    add_query_compound_structure(selenium, smiles_str=smiles)

    # Validate all real compounds added to the LR #
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)
    check_for_butterbar(selenium, notification_text='Searching for compounds...', visible=True)
    check_for_butterbar(selenium, notification_text='Searching for compounds...', visible=False)

    sort_grid_by(selenium, column_name='ID')
    # Verify compounds are added to the LR
    verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(2)})
    verify_column_contents(selenium, 'ID', ['CHEMBL1033', 'CHEMBL1035'])

    # ----- Substructure advanced Search for VIRTUAL only ----- #
    # Need to disable REAL for a VIRTUAL only search
    dom.click_element(selenium, COMPOUND_TYPE_CHECKBOX, text="REAL")
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)
    check_for_butterbar(selenium, notification_text='Searching for compounds...', visible=True)
    check_for_butterbar(selenium, notification_text='Searching for compounds...', visible=False)

    # Verify compounds are added to the LR
    verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(3)})
    verify_column_contents(selenium, 'ID', ['CHEMBL1033', 'CHEMBL1035', 'V036109'])

    # ----- Substructure advanced Search for R-groups ----- #
    # need to disable COMPOUND for an R-group only search
    dom.click_element(selenium, COMPOUND_TYPE_CHECKBOX, text="COMPOUND")
    dom.click_element(selenium, ADV_SEARCH_SKETCHER)
    # Clearing the old compound and adding an R-group
    import_structure_into_sketcher(selenium, r_group_smiles, sketcher_iframe_selector=ADVANCED_SEARCH_SKETCHER_IFRAME)
    base.click_ok(selenium)

    # Clearing all old results so that only the R-groups persist in the LR
    dom.click_element(selenium, CLEAR_REPORT_CHECKBOX)
    verify_is_visible(selenium, CLEAR_REPORT_CHECKED)

    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)
    base.click_ok(selenium)
    check_for_butterbar(selenium, notification_text='Removing all and Searching for compounds...', visible=True)
    check_for_butterbar(selenium, notification_text='Removing all and Searching for compounds...', visible=False)

    # Verify R-groups are added to the LR
    verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(5)})
    verify_column_contents(selenium, 'ID', ['R055831', 'R055832', 'R055833', 'R055834', 'R055835'])
