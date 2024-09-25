from helpers.change.grid_row_actions import pick_row_context_menu_item
from helpers.change.tile_view import click_tile_context_menu_item
from helpers.verification.sketcher import verify_if_sketcher_is_populated, verify_if_enumeration_is_populated
from library.wait import until_condition_met


def use_compound_in_sketcher_and_verify(driver,
                                        compound_id,
                                        enumeration_sketcher=False,
                                        tile_view=False,
                                        retries=3,
                                        interval=500):
    """
    Copies a compound to sketcher via grid submenu option 'Use in'.
    Verifies if the compound has been successfully copied over to sketcher.

    :param driver: selenium webdriver
    :param compound_id: str, ID of the compound to be copied over
    :param enumeration_sketcher: bool, True if copy to enumeration sketcher, otherwise design sketcher
    :param tile_view: bool, True if the copy operation happens in tile view
    :param retries: int, maximum # of retries the wait function checks if sketcher is populated
    :param interval: int, wait time in-between each attempt of execution of the wait function (in ms)
    """
    if tile_view:
        if enumeration_sketcher:
            click_tile_context_menu_item(driver, compound_id, "Use in", "Enumeration")
            until_condition_met(verify_if_enumeration_is_populated, retries=retries, interval=interval, driver=driver)
        else:
            click_tile_context_menu_item(driver, compound_id, "Use in", "Design Sketcher")
            until_condition_met(verify_if_sketcher_is_populated, retries=retries, interval=interval, driver=driver)
    else:
        if enumeration_sketcher:
            pick_row_context_menu_item(driver, compound_id, "Use in", "Enumeration")
            until_condition_met(verify_if_enumeration_is_populated, retries=retries, interval=interval, driver=driver)
        else:
            pick_row_context_menu_item(driver, compound_id, "Use in", "Design Sketcher")
            until_condition_met(verify_if_sketcher_is_populated, retries=retries, interval=interval, driver=driver)
