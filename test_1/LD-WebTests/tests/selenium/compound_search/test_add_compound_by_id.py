import pytest

from helpers.flows.add_compound import open_search_add_compound_by_id
from helpers.selection.grid import Footer
from helpers.verification.grid import verify_footer_values, verify_column_contents

commound_id_set = set()


@pytest.mark.smoke
@pytest.mark.parametrize(
    "seperator_symbol, actual_input, expected_output",
    [("Semicolon", "CRA-032553; CRA-032554; CRA-032557; CRA-032560",
      ['CRA-032553', 'CRA-032554', 'CRA-032557', 'CRA-032560']),
     ("None", "CRA-031137, CRA-032370; CRA-032372 CRA-032661", []),
     ("Comma", "CRA-032666, CRA-032670, CRA-032671, CRA-032672",
      ['CRA-032666', 'CRA-032670', 'CRA-032671', 'CRA-032672']),
     ("White space", "CRA-032432 CRA-032433 CRA-032434 CRA-032435",
      ['CRA-032432', 'CRA-032433', 'CRA-032434', 'CRA-032435']),
     ("Semicolon", "CRA-00000; Invalid123; Nonexistent123; CRA-032554; CRA-032557", ['CRA-032554', 'CRA-032557'])])
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_add_compound_by_id(selenium, seperator_symbol, actual_input, expected_output):
    """
    Test create a LR:
    1. Create a new LR.
    2.Opening the compounds panel and searching for the ID tab
    3.Verifying the number of compounds on footer.
    4.Verifying compound ID's on columns.
    param selenium: Selenium webdriver
    param seperated_symbol: seperated symbol from parametrize data
    param actual_input: Actual compounds from parametrize data as a String
    param expected_output: expected compounds from parametrize data as a List
    """
    open_search_add_compound_by_id(selenium, seperator_symbol, actual_input)
    # verifying the number of compounds added
    verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(len(expected_output))})
    verify_column_contents(selenium, 'ID', expected_content=expected_output)
