from helpers.change.footer_actions import show_hidden_compounds, show_hidden_columns
from helpers.change.tile_view import switch_to_tile_view, select_tiles_and_click_context_menu_item
from helpers.selection.grid import Footer
from helpers.selection.modal import WINDOW_HEADER_TEXT, WINDOW_BODY
from helpers.selection.tile_view import TILE_HEADER
from helpers.verification.element import verify_is_not_visible, verify_is_visible
from helpers.verification.grid import verify_footer_values
from library import wait, base

# Set LiveReport to duplicate
live_report_to_duplicate = {'livereport_name': 'Test Reactants - Halides', 'livereport_id': '2554'}


def test_hide_show_remove_tiles_and_properties(selenium, duplicate_live_report, open_livereport):
    """
    Test to check Hide, Show and Remove functionality for tiles and Properties in tile view.
    1. Hide tiles and Verification
    2. Show Hidden tiles and Verification
    3. Show Hidden Properties from footer and Verification
    4. Remove Compounds and Verification

    :param selenium: Selenium Webdriver
    """
    # Navigate to tile view
    switch_to_tile_view(selenium)

    # ----- Hide tiles and Verification ----- #
    select_tiles_and_click_context_menu_item(selenium, ['V055824', 'V055826'], option_to_select="Hide")
    wait.until_loading_mask_not_visible(selenium)

    # verify tiles are hidden in footer and tile view
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(5),
            Footer.ROW_HIDDEN_COUNT_KEY: Footer.ROW_HIDDEN_COUNT_VALUE.format(2)
        })
    verify_is_not_visible(selenium, TILE_HEADER, selector_text='V055824')
    verify_is_not_visible(selenium, TILE_HEADER, selector_text='V055826')

    # ----- Show Hidden tiles and verification ----- #
    show_hidden_compounds(selenium, 2)
    # verify tiles are not hidden in footer & tile view
    verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(7)})
    verify_is_visible(selenium, TILE_HEADER, selector_text='V055824')
    verify_is_visible(selenium, TILE_HEADER, selector_text='V055826')

    # ----- Show Hidden Properties from footer and Verification ----- #
    show_hidden_columns(selenium, 1)
    verify_footer_values(selenium, {Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(5)})

    # ----- Remove Compounds and Verification ----- #
    select_tiles_and_click_context_menu_item(selenium, ['V055824', 'V055826'], option_to_select="Remove")
    # verify header and body text for confirmation message
    wait.until_visible(selenium, WINDOW_HEADER_TEXT, text='Remove Compounds')
    verify_is_visible(
        selenium, WINDOW_BODY,
        'Are you sure that you want to remove 2 compounds from the LiveReport "{}"?'.format(duplicate_live_report))
    # confirming remove compounds
    base.click_ok(selenium)
    wait.until_loading_mask_not_visible(selenium)

    # Verify tile count reduced in footer and tiles are not visible in tile view
    verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(5)})
    verify_is_not_visible(selenium, TILE_HEADER, selector_text='V055824')
    verify_is_not_visible(selenium, TILE_HEADER, selector_text='V055826')
