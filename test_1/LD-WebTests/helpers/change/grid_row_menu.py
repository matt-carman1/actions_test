from helpers.change.grid_row_actions import pick_row_context_menu_item
from helpers.change.live_report_picker import fill_details_for_new_livereport, open_live_report
from helpers.change.tile_view import click_tile_context_menu_item
from helpers.selection.grid import GRID_ALL_ROWS_CHECKBOX
from helpers.verification.grid import check_for_butterbar
from library.base import click_ok
from library import wait


def copy_compound_to_live_report(driver, entity_id, report_name, rationale='', new_report=False, grid_view=True):
    """
    Copies a structure to an existing or new LiveReport.
    :param driver: selenium driver
    :param entity_id: str, structure ID
    :param report_name: str, LiveReport name
    :param rationale: str, rationale the new livereport will have
    :param new_report: bool, True is we want to create a new LiveReport
    :param grid_view: bool, True as we're in Grid view, False for Tile view
    :return:
    """
    option = "Existing LiveReport..."
    if new_report:
        option = "New LiveReport..."
    if grid_view:
        # open row submenu and select the "LiveReport" option in the "Copy to" submenu
        pick_row_context_menu_item(driver, entity_id, option_to_select="Copy to", submenu_name=option)
    else:
        # same action for tile view
        click_tile_context_menu_item(driver, entity_id, "Copy to", option)
    if new_report:
        # when we click on New Livereport the Create New LiveReport dialog will appear directly
        report_name = fill_details_for_new_livereport(driver, report_name=report_name, rationale=rationale)
    else:
        open_live_report(driver, name=report_name)
    click_ok(driver)
    check_for_butterbar(driver, "Adding compound(s)...", visible=True)
    wait.until_loading_mask_not_visible(driver)
    # wait for all rows checkbox to appear to ensure LR loaded after mask has disppeared
    wait.until_visible(driver, GRID_ALL_ROWS_CHECKBOX)
    check_for_butterbar(driver, "Adding compound(s)...", visible=False)
    return report_name
