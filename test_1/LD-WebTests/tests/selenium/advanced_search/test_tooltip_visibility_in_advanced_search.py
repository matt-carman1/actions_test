import pytest

from helpers.change.actions_pane import open_add_compounds_panel, open_advanced_search
from helpers.selection.advanced_search import ADVANCED_QUERY_COLUMN_SELECTOR, CLEAR_ADVANCED_QUERY_SEARCH
from helpers.selection.column_tree import COLUMN_TREE_PICKER_TEXT_NODE, COLUMN_TREE_PICKER_TOOLTIP_HEADER_TEXT, \
    COLUMN_TREE_PICKER_TOOLTIP_BODY_TEXT, ColumnTreeSectionTooltip
from helpers.verification.advanced_search import verify_column_searched_tooltip_in_advanced_query
from helpers.verification.element import verify_is_visible
from library import simulate, dom


def test_tooltip_visibility_in_advanced_search(selenium, new_live_report, open_livereport):
    """
    Checks the tooltip visibility of different sections, parent folder and columns in D&C tree of Advanced Search
    :param selenium: selenium webdriver
    :param new_live_report: LiveReport Model object, fixture that creates a new livereport via ldclient api
    :param open_livereport: LiveReport Model object, fixture that opens the newly created livereport
    """
    # Open advanced search panel
    open_add_compounds_panel(selenium)
    open_advanced_search(selenium)
    # Open D&C tree in advanced search
    dom.click_element(selenium, ADVANCED_QUERY_COLUMN_SELECTOR)

    # Define test variables
    assay_section_header = ColumnTreeSectionTooltip().ASSAYS_HEADER
    assay_section_description = ColumnTreeSectionTooltip().ASSAYS_DESC
    ffc_section_header = ColumnTreeSectionTooltip().FFC_HEADER
    ffc_section_description = ColumnTreeSectionTooltip().FFC_DESC

    # Hovers over the section nodes mentioned above and verifies the tooltip header and description
    # Tooltip header is the section name i.e. 'Computed Properties'
    simulate.hover(selenium, dom.get_element(selenium, COLUMN_TREE_PICKER_TEXT_NODE, text=assay_section_header))
    verify_is_visible(selenium,
                      COLUMN_TREE_PICKER_TOOLTIP_HEADER_TEXT,
                      selector_text=assay_section_header,
                      exact_selector_text_match=True)
    verify_is_visible(selenium,
                      COLUMN_TREE_PICKER_TOOLTIP_BODY_TEXT,
                      selector_text=assay_section_description,
                      exact_selector_text_match=True)
    simulate.hover(selenium, dom.get_element(selenium, COLUMN_TREE_PICKER_TEXT_NODE, text=ffc_section_header))
    verify_is_visible(selenium,
                      COLUMN_TREE_PICKER_TOOLTIP_HEADER_TEXT,
                      selector_text=ffc_section_header,
                      exact_selector_text_match=True)
    verify_is_visible(selenium,
                      COLUMN_TREE_PICKER_TOOLTIP_BODY_TEXT,
                      selector_text=ffc_section_description,
                      exact_selector_text_match=True)

    # Define test variables
    computed_column_header = '"Random integer (Result)"'
    computed_column_body = 'Output a random integer'
    model_folder_header = '"[Clustering] Canvas KMeans"'
    model_folder_body = "Run Canvas's KMeans Clustering over the LiveReport"

    # Search & hover over the column name mentioned above and verifies the tooltip header and description
    verify_column_searched_tooltip_in_advanced_query(selenium,
                                                     search_term=computed_column_header,
                                                     tooltip_body=True,
                                                     tooltip_body_text=computed_column_body)
    # Need to clear search box for next search query
    dom.click_element(selenium, CLEAR_ADVANCED_QUERY_SEARCH)
    # Search box is out of focus, so click again
    dom.click_element(selenium, ADVANCED_QUERY_COLUMN_SELECTOR)
    # Search & hover over the folder name mentioned above and verifies the tooltip header and description
    verify_column_searched_tooltip_in_advanced_query(selenium,
                                                     search_term=model_folder_header,
                                                     tooltip_body=True,
                                                     tooltip_body_text=model_folder_body)
