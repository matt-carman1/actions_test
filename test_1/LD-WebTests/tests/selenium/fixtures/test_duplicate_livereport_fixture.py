import time

from helpers.selection.live_report_tab import TAB_ACTIVE
from helpers.verification.element import verify_is_visible
from helpers.verification.grid import verify_visible_columns_in_live_report, verify_grid_contents
from library import wait

live_report_to_duplicate = {'livereport_name': '4 Compounds 3 Formulas', 'livereport_id': '890'}
entity_ids_subset = ['V035625']
column_ids_subset = ['1226', '813']


def test_duplicate_livereport_fixture(selenium, duplicate_live_report, open_livereport):
    """
    A simple test to check if the duplicate_live_report fixture works.

    :param selenium: Selenium Webdriver
    """
    time.sleep(2)
    verify_is_visible(selenium, selector=TAB_ACTIVE, selector_text=duplicate_live_report)
    wait.until_live_report_loading_mask_not_visible(selenium)
    verify_visible_columns_in_live_report(selenium,
                                          ['Compound Structure', 'ID', 'Rationale', 'Lot Scientist', 'A3 (undefined)'])
    verify_grid_contents(selenium, {'ID': ['V035625'], 'A3 (undefined)': ['92']})
