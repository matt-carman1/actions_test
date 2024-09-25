import pytest
from helpers.change.advanced_search_actions import add_query_compound_structure
from helpers.selection.advanced_search import SEARCH_AND_ADD_COMPOUNDS_BUTTON, AUTO_UPDATE_CHECKBOX, \
    ADV_QUERY_STOP_SEARCH, AUTO_UPDATE_CHECKED
from helpers.change.actions_pane import open_add_compounds_panel, open_advanced_search
from helpers.selection.grid import Footer
from helpers.verification.grid import verify_footer_values, verify_is_visible
from library import dom, utils


@pytest.mark.app_defect(reason='SS-42693')
@pytest.mark.smoke
@pytest.mark.require_webgl
@pytest.mark.xfail(utils.is_k8s(), reason="SS-42730: Unknown failure reason on New Jenkins")
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_advanced_substructure(selenium):
    """
    Adding a compound to the LR using Advanced Substructure Compound Search.

    :param selenium: Selenium Webdriver
    """
    substructure = '\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 15 15 0 0 1\nM  V30 BEGIN ATOM\nM  V30 1 C 6.153428 -0.001143 0.000000 0\nM  V30 2 S 4.913714 -0.711143 0.000000 0\nM  V30 3 O 5.623429 -1.950857 0.000000 0\nM  V30 4 O 4.204000 0.528571 0.000000 0\nM  V30 5 C 3.674000 -1.420857 0.000000 0\nM  V30 6 C 2.439428 -0.702286 0.000000 0\nM  V30 7 O 2.444571 0.726286 0.000000 0\nM  V30 8 N 1.199714 -1.412000 0.000000 0\nM  V30 9 C -0.034857 -0.693429 0.000000 0\nM  V30 10 C -0.030000 0.735143 0.000000 0\nM  V30 11 C -1.264286 1.454000 0.000000 0\nM  V30 12 C -2.504286 0.744000 0.000000 0\nM  V30 13 C -2.509143 -0.684286 0.000000 0\nM  V30 14 F -3.749143 -1.394286 0.000000 0\nM  V30 15 C -1.274571 -1.403429 0.000000 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 2 2 2 3\nM  V30 3 2 2 4\nM  V30 4 1 2 5\nM  V30 5 1 5 6\nM  V30 6 2 6 7\nM  V30 7 1 6 8\nM  V30 8 1 8 9\nM  V30 9 2 9 10\nM  V30 10 1 10 11\nM  V30 11 2 11 12\nM  V30 12 1 12 13\nM  V30 13 1 13 14\nM  V30 14 2 13 15\nM  V30 15 1 9 15\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n'

    ### ADD COMPOUND STRUCTURE QUERY ###
    # Opening the Compounds Panel & then the advanced search panel
    open_add_compounds_panel(selenium)
    open_advanced_search(selenium)
    # Add compound query
    add_query_compound_structure(selenium, molv3=substructure)

    ### AUTO-UPDATE SEARCH ###
    # Click the "Search for Compounds" button
    dom.click_element(selenium, AUTO_UPDATE_CHECKBOX)
    verify_is_visible(selenium, AUTO_UPDATE_CHECKED)

    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)
    # Verify 1 compound is added to the LR
    verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(1)})
    # Stop the search
    dom.click_element(selenium, ADV_QUERY_STOP_SEARCH)
    # Verify LR is empty by checking the footer
    verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(0)})

    ### SEARCH FOR COMPOUNDS (NOT AUTO-UPDATED) ###
    # Click the "Search for Compounds" button
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)
    # Verify 1 compound is added to the LR
    verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(1)})
