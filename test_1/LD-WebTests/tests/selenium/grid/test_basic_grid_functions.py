"""
Selenium test for testing basic grid functions
"""
import pytest

from helpers.change.actions_pane import close_filter_panel, close_comments_panel
from helpers.change.footer_actions import show_hidden_compounds
from helpers.change.grid_row_actions import select_rows_and_pick_context_menu_item, select_rows, select_row
from helpers.selection.comments import COMMENTS_TEXTBOX, POST_COMMENT_BUTTON
from helpers.selection.dropdown import DROPDOWN_HEADER_ITEM
from helpers.selection.grid import FROZEN_ROWS_, Footer
from helpers.selection.rationale import RATIONALE_SAVE, RATIONALE_TEXTAREA
from helpers.verification.comments import verify_comment_added
from helpers.verification.element import verify_is_visible, verify_is_not_visible
from helpers.verification.grid import check_for_info_butterbar, verify_footer_values, verify_column_contents
from library import dom, base, wait, utils

# LiveReport to be duplicated for the test
live_report_to_duplicate = {'livereport_name': 'Test Reactants - Halides', 'livereport_id': '2554'}


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_basic_grid_functions(selenium):
    """
    Testing basic Grid functionality in LiveDesign.
    1.Hide/Show rows
    2.Freeze/Unfreeze rows
    3.Comment/Filter selected rows.
    4.Remove rows

    :param selenium: Selenium WebDriver
    """

    # -------- Hide two compounds and verify it -------- #
    select_rows_and_pick_context_menu_item(selenium, list_of_entity_ids=['V055824', 'V055826'], option_to_select='Hide')
    wait.until_loading_mask_not_visible(selenium)
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(5),
            Footer.ROW_HIDDEN_COUNT_KEY: Footer.ROW_HIDDEN_COUNT_VALUE.format(2)
        })
    # Shows two compounds and verifies it
    show_hidden_compounds(selenium, 2)
    wait.until_loading_mask_not_visible(selenium)
    verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(7)})

    # -------- Comment on two compounds -------- #
    select_rows_and_pick_context_menu_item(selenium,
                                           list_of_entity_ids=['V055824', 'V055825'],
                                           option_to_select='Comment')
    comment_1 = utils.make_unique_name('Comment: ')
    dom.set_element_value(selenium, COMMENTS_TEXTBOX, comment_1)
    dom.click_element(selenium, POST_COMMENT_BUTTON)

    # Verify butter bar goes away
    check_for_info_butterbar(selenium, 'Posting Comments', visible=False)

    # Verification that the comments are added for both these compounds
    select_row(selenium, entity_id='V055825')
    verify_comment_added(selenium, 'V055824', comment_1)
    select_rows(selenium, list_of_entity_ids=['V055824', 'V055825'])
    verify_comment_added(selenium, 'V055825', comment_1)
    close_comments_panel(selenium)

    # -------- Freeze two compounds --------- #
    select_rows_and_pick_context_menu_item(selenium, list_of_entity_ids=['V055824'], option_to_select='Freeze')

    # Wait until the viewport mask (ExtJS) is no longer visible
    wait.until_extjs_loading_mask_not_visible(selenium)

    # Verification that the compounds are frozen
    verify_is_visible(selenium, FROZEN_ROWS_.format('V055824'))
    verify_is_visible(selenium, FROZEN_ROWS_.format('V055825'))

    # -------- Unfreeze one compound and verify it -------- #
    select_rows_and_pick_context_menu_item(selenium, list_of_entity_ids=['V055824'], option_to_select='Unfreeze')

    # Wait until the viewport mask (ExtJS) is no longer visible
    wait.until_extjs_loading_mask_not_visible(selenium)

    # Verification that the compound is unfrozen
    verify_is_not_visible(selenium, FROZEN_ROWS_.format('V055824'))

    # -------- Remove two compounds from the LR ------- #
    # 'V055824' is already selected because of previous action
    select_rows_and_pick_context_menu_item(selenium, list_of_entity_ids=['V055826'], option_to_select='Remove')
    base.click_ok(selenium)

    # Verify that two compounds are deleted from the LR by verifying the footer value
    wait.until_loading_mask_not_visible(selenium)
    verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(5)})

    # Toggle selection of both rows
    select_rows(selenium, list_of_entity_ids=['V055825', 'V055827'])

    # ------- Apply Filter to one compound ------ #
    # Choosing 'V055827' to deselect
    select_rows_and_pick_context_menu_item(selenium,
                                           list_of_entity_ids=['V055825', 'V055827'],
                                           option_to_select='Filter to selected')

    # Verification that the filters are applied on the ID
    wait.until_loading_mask_not_visible(selenium)
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(5),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(1),
            Footer.ROW_SELECTED_COUNT_KEY: Footer.ROW_SELECTED_COUNT_VALUE.format(1)
        })
    verify_is_visible(selenium, DROPDOWN_HEADER_ITEM, selector_text='V055825')
    close_filter_panel(selenium)
