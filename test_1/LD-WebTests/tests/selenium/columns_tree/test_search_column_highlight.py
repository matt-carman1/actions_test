import pytest
from helpers.flows.columns_tree import search_in_columns_tree_and_check_highlight

live_report_to_duplicate = {'livereport_name': 'RPE Test', 'livereport_id': '2048'}


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_search_column_highlight(selenium):
    """
    This test searches for column name in D&C Tree and verifies the highlighted text matches the search string or not
    1. Search text matches exactly to a single column
    2. Search text matches to multiple columns
    3. Search text matches no column
    4. Search text matches columns as well as folders
    :param selenium: Selenium webdriver
    """
    # Search text matches exactly to a single column
    search_in_columns_tree_and_check_highlight(selenium,
                                               search_term='Random integer (Result)',
                                               expected=['Random integer (Result)'])
    # Search text matches to multiple columns
    search_in_columns_tree_and_check_highlight(selenium,
                                               search_term='Molecular',
                                               expected=['Molecular Weight', 'Molecular Formula', 'Molecular Weight'],
                                               only_expected=False)
    # Search text matches no column
    search_in_columns_tree_and_check_highlight(selenium, search_term='abc', expected=[])
    # Search text matches columns as well as folders
    search_in_columns_tree_and_check_highlight(selenium,
                                               search_term='enzyme',
                                               expected=[
                                                   'Acyl coenzyme A:cholesterol acyltransferase 1 (IC50)',
                                                   'DNA dC->dU-editing enzyme APOBEC-3G (Potency)',
                                                   'Glycogen debranching enzyme (IC50)', 'Enzyme'
                                               ],
                                               only_expected=False)
