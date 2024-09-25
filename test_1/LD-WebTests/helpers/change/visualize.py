from helpers.change.grid_columns import get_cell
from helpers.selection.visualize import VISUALIZE_ICON
from library import dom


def click_visualize_icon(driver, column_name, structure_id):
    """
    Clicks the 3D Visualizer icon in the spreadsheet for the specified column_name and structure_id
    :param driver: webDriver
    :param column_name: str, column name the cell falls under
    :param structure_id: str, compound ID to identify row
    """
    eyeball_icon = get_cell(driver, compound_id=structure_id, column_title=column_name)
    dom.click_element(driver_or_parent_element=eyeball_icon, selector=VISUALIZE_ICON)
