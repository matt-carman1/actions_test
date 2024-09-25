"""
Selenium test to show and hide columns
"""

from helpers.change.footer_actions import show_hidden_compounds
from helpers.change.grid_row_actions import select_rows_and_pick_context_menu_item, pick_row_context_menu_item, \
    select_multiple_rows, select_multiple_continuous_rows
from helpers.selection.grid import Footer
from helpers.verification.grid import verify_footer_values
from library import wait

live_report_to_duplicate = {'livereport_name': 'Test Reactants - Halides', 'livereport_id': '2554'}


def test_show_hide_compounds(selenium, duplicate_live_report, open_livereport):
    """
    Test hiding and showing compounds in the grid
    :param selenium: Selenium WebDriver
    :param duplicate_live_report: Fixture to duplicate the Livereport
    """

    # Hide a compound by right click and verify compound is hidden and then un-hide them.
    select_rows_and_pick_context_menu_item(selenium, list_of_entity_ids=['V055824'], option_to_select='Hide')
    wait.until_loading_mask_not_visible(selenium)
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(6),
            Footer.ROW_HIDDEN_COUNT_KEY: Footer.ROW_HIDDEN_COUNT_VALUE.format(1)
        })
    show_hidden_compounds(selenium, 1)
    verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(7)})

    # Hide multiple compounds by ctrl+click selection and verify that the compounds are hidden and then un-hide them.
    select_multiple_rows(selenium, 'V055824', 'V055826', 'V055828')
    pick_row_context_menu_item(selenium, entity_id='V055828', option_to_select='Hide')
    wait.until_loading_mask_not_visible(selenium)
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(4),
            Footer.ROW_HIDDEN_COUNT_KEY: Footer.ROW_HIDDEN_COUNT_VALUE.format(3)
        })
    show_hidden_compounds(selenium, 3)
    verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(7)})

    # Hide multiple compounds by shift+click selection and verify that compounds are hidden.
    select_multiple_continuous_rows(selenium, start_row='V055824', end_row='V055827')
    pick_row_context_menu_item(selenium, entity_id='V055827', option_to_select='Hide')
    wait.until_loading_mask_not_visible(selenium)
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(3),
            Footer.ROW_HIDDEN_COUNT_KEY: Footer.ROW_HIDDEN_COUNT_VALUE.format(4)
        })
