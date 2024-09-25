import pytest

from helpers.change.data_and_columns_tree import clear_column_tree_search
from helpers.flows.columns_tree import search_in_columns_tree_and_check_highlight

test_livereport = 'Plots test LR'


@pytest.mark.parametrize('customized_server_config', [{
    'COLUMN_TREE_SEARCH_LENGTH': 2
}, {
    'COLUMN_TREE_SEARCH_LENGTH': 5
}, {
    'COLUMN_TREE_SEARCH_LENGTH': 1
}],
                         indirect=True)
@pytest.mark.parametrize('login_to_livedesign', [("demo", "demo")], indirect=True)
@pytest.mark.usefixtures("open_livereport")
def test_column_tree_search_length(driver, customized_server_config, login_to_livedesign):
    """
    Test for FF COLUMN_TREE_SEARCH_LENGTH
    1.Set value in feature flag(FF) -> Example, LD_PROPERTIES = {COLUMN_TREE_SEARCH_LENGTH: '2'}
    2.Open existing livereport -> test_livereport = 'Plots test LR'
    3.Search in column tree picker search
    4.verify the search term
    """
    search_term = ":cholester"
    column_search_size = int(customized_server_config.get('COLUMN_TREE_SEARCH_LENGTH'))

    # positive case -> set expected value in FF
    search_in_columns_tree_and_check_highlight(driver,
                                               search_term=search_term[:column_search_size],
                                               expected=["Acyl coenzyme A:cholesterol acyltransferase 1 (IC50)"])
    clear_column_tree_search(driver)

    # Another check to set value more than FF
    search_in_columns_tree_and_check_highlight(driver,
                                               search_term=search_term[:column_search_size + 1],
                                               expected=["Acyl coenzyme A:cholesterol acyltransferase 1 (IC50)"])
    clear_column_tree_search(driver)

    # Negative case -> set less than expected value in FF
    search_in_columns_tree_and_check_highlight(driver, search_term=search_term[:column_search_size - 1], expected=[])