"""
Testing that the Adv query defined feature works as expected
"""
import pytest

from helpers.change.advanced_search_actions import add_query, get_query, choose_adv_query_options
from helpers.change.autosuggest_actions import set_autosuggest_items
from helpers.change.actions_pane import open_add_compounds_panel, open_advanced_search
from helpers.selection.advanced_search import SEARCH_AND_ADD_COMPOUNDS_BUTTON
from helpers.selection.grid import Footer

from helpers.verification.grid import verify_column_contents, verify_footer_values
from helpers.verification.grid import check_for_butterbar
from library import dom


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_advanced_query_defined(selenium):
    """
    Testing that the Adv query defined feature works as expected. Details:

    a. Performed a Categorical Active Advanced search with "defined" on an assay column.
    b. Verified that the results show up as expected.
    :param selenium: Selenium webdriver
    """

    # Define test variables
    column_name = 'Ataxin-2 (Potency)'
    expected_ids = ['CHEMBL104', 'CHEMBL1089', 'CHEMBL1097', 'CHEMBL11']
    assay_values = ['25.12', '14.13', '25.12', '28.18']

    # Open the Advanced Query Tab
    open_add_compounds_panel(selenium)
    open_advanced_search(selenium)

    # Add range query and search
    add_query(selenium, column_name)
    choose_adv_query_options(selenium, query_name=column_name, option_to_choose='Show as Text Search')

    # Set value "(defined)" in text query
    query = get_query(selenium, column_name)
    set_autosuggest_items(query, ["(defined)"])
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)
    check_for_butterbar(selenium, notification_text='Searching for compounds...', visible=True)
    check_for_butterbar(selenium, notification_text='Searching for compounds...', visible=False)

    # Three way verification of the compounds returned
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(4),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(6)
        })
    verify_column_contents(selenium, 'ID', expected_ids)
    verify_column_contents(selenium, '{} [uM]'.format(column_name), assay_values)
