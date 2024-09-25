import pytest
import time

from helpers.change.grid_column_menu import toggle_show_smiles
from helpers.selection.grid import GRID_FIND_BUTTON, GRID_FIND_INPUT, GRID_FIND_MATCH_COUNT, \
    GRID_COMPOUND_STRUCTURE_SMILES
from helpers.verification.element import verify_is_visible
from helpers.verification.grid import verify_grid_matching_elements
from library import dom

live_report_to_duplicate = {'livereport_name': 'DRC Test Data', 'livereport_id': '897'}
COMPOUND_STRUCTURE_COLUMN_ID = '1228'


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_grid_find_for_smiles(selenium, ld_client):
    """
    Test Grid Find using:

    1. Toggle show smiles on Compound Structure column
    2. Set smiles substring as Grid Find text and Verify
    3. Set exact smiles as Grid Find text and Verify
    """
    # showing SMILES for compound structure
    toggle_show_smiles(selenium)

    dom.click_element(selenium, GRID_FIND_BUTTON)

    # ----- Set smiles substring as Grid Find text and Verify ----- #

    # NOTE(badlato): An attempt to generify this test so that it does not need to hard-code SMILES that will
    #  need to be updated with each preprocessor/registration config change
    smiles_list = [
        row['cells'][COMPOUND_STRUCTURE_COLUMN_ID]['values'][0]['value']
        for row in ld_client.execute_live_report(live_report_id='897')['rows'].values()
    ]
    # Find a SMILES that appears twice (once exact and once as a substring)
    smiles_text = None
    substring_smiles = None
    for s in smiles_list:
        matches = [match for match in smiles_list if s in match]
        if len(matches) == 2:
            substring_smiles = min(matches, key=len)
            smiles_text = max(matches, key=len)
            break
    if not (smiles_text and substring_smiles):
        assert False, "This test needs to be updated manually due to preprocessor/registration config changes"

    dom.set_element_value(selenium, GRID_FIND_INPUT, value=substring_smiles)

    # verify whether grid scrolled automatically to the matching element
    verify_is_visible(selenium, GRID_FIND_MATCH_COUNT, '1 of 2')
    verify_is_visible(selenium,
                      GRID_COMPOUND_STRUCTURE_SMILES,
                      selector_text=substring_smiles,
                      error_if_selector_matches_many_elements=False)

    # navigating to next selected element by Enter key
    dom.press_enter_key(selenium)

    # verify whether navigated to next element using count
    verify_is_visible(selenium, GRID_FIND_MATCH_COUNT, '2 of 2')
    # verifying matching elements count and text
    verify_grid_matching_elements(selenium, 1, expected_matching_text=substring_smiles, at_least=True)

    # ----- Set exact smiles as Grid Find text and Verify ----- #
    dom.set_element_value(selenium, GRID_FIND_INPUT, value=smiles_text)
    time.sleep(1)
    # verifying matching elements count and text
    verify_grid_matching_elements(selenium, 1, expected_matching_text=smiles_text)
