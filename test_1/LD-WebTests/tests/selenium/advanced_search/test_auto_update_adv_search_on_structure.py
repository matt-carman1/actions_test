import pytest
from helpers.change.advanced_search_actions import add_query_compound_structure, \
    set_similarity_percent_for_structure_search
from helpers.change.actions_pane import open_add_compounds_panel, open_advanced_search
from helpers.selection.advanced_search import SEARCH_AND_ADD_COMPOUNDS_BUTTON, AUTO_UPDATE_CHECKBOX, \
    ADV_QUERY_STOP_SEARCH, AUTO_UPDATE_CHECKED, AUTO_UPDATE_NOT_CHECKED
from helpers.selection.grid import Footer
from helpers.verification.grid import verify_footer_values, verify_is_visible, verify_column_contents
from library import dom


@pytest.mark.app_defect(reason='SS-37305: flaky test')
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
@pytest.mark.require_webgl
def test_auto_update_adv_search_on_structure(selenium):
    """
    Selenium test to test the Auto update Advanced search. Three objectives of the test are:
    Objective #1:
        1. Added a Compound Structure query, enabled Auto-update and ran an advanced search on substructure.
        2. Verified the Compounds returned.
        3. Halted the Auto update search and verified that the Compound count changes to zero.
    Objective #2:
        4. With auto update enabled ran an advanced search on similarity. (using the same smiles)
        5. Verified the compounds and columns returned and stopped the search.
    Objective #3:
        6. Disabled the Auto update checkbox.
        7. Ran a normal search with similarity and verified the compounds returned.

    :param selenium: Selenium Webdriver
    """
    # Data required throughout the test
    molv3_input = "\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 33 36 0 0 1\nM  V30 BEGIN ATOM\nM  V30 1 C 6.206541 -0.987380 0.000000 0\nM  V30 2 C 5.293370 -1.397044 0.000000 0\nM  V30 3 C 5.087239 -2.374659 0.000000 0\nM  V30 4 C 5.757092 -3.118011 0.000000 0\nM  V30 5 N 6.734877 -2.909143 0.000000 0\nM  V30 6 O 5.448958 -4.069233 0.000000 0\nM  V30 7 C 4.092447 -2.481729 0.000000 0\nM  V30 8 C 3.594508 -3.347764 0.000000 0\nM  V30 9 C 3.685182 -1.568557 0.000000 0\nM  V30 10 N 4.426535 -0.897305 0.000000 0\nM  V30 11 C 2.706168 -1.360626 0.000000 0\nM  V30 12 C 2.397101 -0.409448 0.000000 0\nM  V30 13 C 2.984044 0.400593 0.000000 0\nM  V30 14 O 3.984844 0.399864 0.000000 0\nM  V30 15 N 2.396387 1.208752 0.000000 0\nM  V30 16 C 1.444409 0.900085 0.000000 0\nM  V30 17 C 0.580574 1.398624 0.000000 0\nM  V30 18 C -0.287591 0.900163 0.000000 0\nM  V30 19 C -0.286321 -0.099637 0.000000 0\nM  V30 20 C 0.578514 -0.600976 0.000000 0\nM  V30 21 C 1.446079 -0.099715 0.000000 0\nM  V30 22 S -1.137687 -0.589897 0.000000 0\nM  V30 23 O -0.636027 -1.429861 0.000000 0\nM  V30 24 O -1.642147 0.273868 0.000000 0\nM  V30 25 C -2.000251 -1.100557 0.000000 0\nM  V30 26 C -2.002980 -2.108758 0.000000 0\nM  V30 27 C -1.141344 -2.620697 0.000000 0\nM  V30 28 Cl -0.283377 -2.148236 0.000000 0\nM  V30 29 C -1.150273 -3.619097 0.000000 0\nM  V30 30 C -2.023839 -4.105959 0.000000 0\nM  V30 31 C -2.886875 -3.597220 0.000000 0\nM  V30 32 C -2.874745 -2.598819 0.000000 0\nM  V30 33 Cl -3.735981 -2.088479 0.000000 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 2 2 2 3\nM  V30 3 1 3 4\nM  V30 4 1 4 5\nM  V30 5 2 4 6\nM  V30 6 1 3 7\nM  V30 7 1 7 8\nM  V30 8 2 7 9\nM  V30 9 1 9 10\nM  V30 10 1 2 10\nM  V30 11 1 9 11\nM  V30 12 2 11 12\nM  V30 13 1 12 13\nM  V30 14 2 13 14\nM  V30 15 1 13 15\nM  V30 16 1 15 16\nM  V30 17 2 16 17\nM  V30 18 1 17 18\nM  V30 19 2 18 19\nM  V30 20 1 19 20\nM  V30 21 2 20 21\nM  V30 22 1 12 21\nM  V30 23 1 16 21\nM  V30 24 1 19 22\nM  V30 25 2 22 23\nM  V30 26 2 22 24\nM  V30 27 1 22 25\nM  V30 28 1 25 26\nM  V30 29 2 26 27\nM  V30 30 1 27 28\nM  V30 31 1 27 29\nM  V30 32 2 29 30\nM  V30 33 1 30 31\nM  V30 34 2 31 32\nM  V30 35 1 26 32\nM  V30 36 1 32 33\nM  V30 END BOND\nM  V30 END CTAB\nM  END"

    # Open the Compounds Panel & then the advanced search panel
    open_add_compounds_panel(selenium)
    open_advanced_search(selenium)

    # ----- Substructure search with Auto-update ON ----- #
    # Add compound query
    add_query_compound_structure(selenium, molv3=molv3_input)

    # Check auto-update results and click "Search for Compounds" button
    dom.click_element(selenium, AUTO_UPDATE_CHECKBOX)
    verify_is_visible(selenium, AUTO_UPDATE_CHECKED)

    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)
    # Verify 4 compounds are added to the LiveReport
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(4),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(5)
        })
    # Verify compound IDs are as expected
    verify_column_contents(selenium, 'ID', ['CRA-031137', 'CRA-031437', 'CRA-032627', 'CRA-032666'])

    # Halted the Auto update search and verified that the Compound count changes to zero.
    dom.click_element(selenium, ADV_QUERY_STOP_SEARCH)
    # verify LR is empty by checking the footer
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(0),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(5)
        })

    # ---- Similarity Search with Auto-Update ON ---- #
    # With auto update enabled ran an advanced search on similarity. (using the same smiles)
    set_similarity_percent_for_structure_search(selenium, tanimoto_score_threshold=0.60)
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)

    # Verified the compounds and columns returned and stopped the search.
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(4),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(6)
        })
    verify_column_contents(selenium, 'ID', ['CRA-031137', 'CRA-031437', 'CRA-032627', 'CRA-032666'])
    # Stop auto-update
    dom.click_element(selenium, ADV_QUERY_STOP_SEARCH)
    # verify LR is empty by checking the footer
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(0),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(6)
        })

    # ----- Similarity Search with Auto-update OFF ----- #
    # Disable the Auto-update Search and "Search for Compounds"
    dom.click_element(selenium, AUTO_UPDATE_CHECKBOX)
    verify_is_visible(selenium, AUTO_UPDATE_NOT_CHECKED)

    # Ran a normal search with similarity and verified the compounds returned.
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)
    # Verify 2 compounds are added to the LR
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(4),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(6)
        })
    verify_column_contents(selenium, 'ID', ['CRA-031137', 'CRA-031437', 'CRA-032627', 'CRA-032666'])
