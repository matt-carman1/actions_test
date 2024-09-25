from helpers.selection.grid import GRID_ICON, GRID_ICON_ACTIVE
from library import ensure


def switch_to_grid_view(driver):
    """
    Opens grid view.

    :param driver: selenium webdriver
    """
    ensure.element_visible(driver, action_selector=GRID_ICON, expected_visible_selector=GRID_ICON_ACTIVE)
