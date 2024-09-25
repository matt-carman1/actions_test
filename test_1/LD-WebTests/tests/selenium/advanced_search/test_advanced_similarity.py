import pytest
from helpers.change.advanced_search_actions import add_query_compound_structure, \
    set_similarity_percent_for_structure_search
from helpers.change.grid_column_menu import sort_grid_by
from helpers.selection.advanced_search import SEARCH_AND_ADD_COMPOUNDS_BUTTON
from helpers.change.actions_pane import open_add_compounds_panel, open_advanced_search
from helpers.selection.grid import Footer
from helpers.verification.grid import verify_footer_values, verify_grid_contents, check_for_butterbar
from library import dom


@pytest.mark.app_defect(reason='SS-38009')
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
@pytest.mark.require_webgl
def test_advanced_similarity(selenium):
    """
    Add compounds using Advanced Similarity Compound Search and verifies correct:
        1. count of compounds returned in LR
        2. Tanimoto score of each compound

    Note: This Selenium test replicates Javascript system test feature.AdvQuerySimilarity,
          which tests advanced searching for compounds at Similarity score of 0.90 and 0.30.
    :param selenium: Selenium Webdriver
    """
    # ----- Add Advanced Search Compound Structure Query ----- #
    molv3 = "Advanced_similarity\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 12 12 0 0 1\nM  V30 BEGIN ATOM\nM  V30 1 C -0.067213 3.814338 0.000000 0\nM  V30 2 C 0.286500 2.878956 0.000000 0\nM  V30 3 C 1.273388 2.717510 0.000000 0\nM  V30 4 N -0.346872 2.105053 0.000000 0\nM  V30 5 C 0.006841 1.169672 0.000000 0\nM  V30 6 C 0.993532 1.008259 0.000000 0\nM  V30 7 C 1.347245 0.072877 0.000000 0\nM  V30 8 C 0.714070 -0.701059 0.000000 0\nM  V30 9 C 1.067586 -1.636408 0.000000 0\nM  V30 10 O 2.054474 -1.797854 0.000000 0\nM  V30 11 C -0.272818 -0.539613 0.000000 0\nM  V30 12 N -0.626531 0.395769 0.000000 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 2 1 2 3\nM  V30 3 1 2 4\nM  V30 4 1 4 5\nM  V30 5 2 5 6\nM  V30 6 1 6 7\nM  V30 7 2 7 8\nM  V30 8 1 8 9\nM  V30 9 1 9 10\nM  V30 10 1 8 11\nM  V30 11 2 11 12\nM  V30 12 1 5 12\nM  V30 END BOND\nM  V30 END CTAB\nM  END"
    # Open the Compounds Panel & then the advanced search panel
    open_add_compounds_panel(selenium)
    open_advanced_search(selenium)
    # Add compound query
    add_query_compound_structure(selenium, molv3)
    set_similarity_percent_for_structure_search(selenium, tanimoto_score_threshold=0.90)

    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)

    check_for_butterbar(selenium, notification_text='Adding compound(s)...', visible=True)
    check_for_butterbar(selenium, notification_text='Adding compound(s)...', visible=False)
    sort_grid_by(selenium, column_name='ID')
    # Verify compound is added to the LR
    verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(1)})
    verify_grid_contents(selenium, {'ID': ['CRA-035002'], 'Similarity Score (CC(C)Nc1ccc(CO)cn1)': ['1']})

    # ----- Validate compounds returned at Tanimoto score threshold-0.30 ----- #
    set_similarity_percent_for_structure_search(selenium, tanimoto_score_threshold=0.30)
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)
    check_for_butterbar(selenium, notification_text='Adding compound(s)...', visible=True)
    check_for_butterbar(selenium, notification_text='Adding compound(s)...', visible=False)

    # Verify compounds are added to the LR
    verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(4)})
    verify_grid_contents(
        selenium, {
            'ID': ["CRA-035001", "CRA-035002", "V039318", "V046264"],
            'Similarity Score (CC(C)Nc1ccc(CO)cn1)': ['0.543', '1', '0.319', '0.304']
        })
