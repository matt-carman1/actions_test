"""

Verification for all MPO related stuff

"""

from helpers.change.grid_columns import get_cell, scroll_to_column_header
from helpers.extraction.grid import get_color_tuple, wait_until_cells_are_loaded
from helpers.selection.mpo import MPO_CELLTIP
from helpers.verification.element import verify_is_visible
from library import dom, simulate, wait


def verify_mpo_tooltip(driver, compound_id, mpo_name, expected_tooltip_values, expected_tooltip_colors):
    """
    This function achieves the following objectives:
    a. Hovers over the MPO value in the cell
    b. Verifies that the tooltip shows up.
    c. Verifies that the constituent in the tooltip are as expected.

    :param driver: Selenium webdriver
    :param compound_id: str, Entity Id of the Compound.
    :param mpo_name: str, the name of the mpo to be verified.
    :param expected_tooltip_values: dict, expected values with constituents
    :param expected_tooltip_colors: a list of tuples where each tuple represent color in the format (2, 255, 0, 1)
    :return:
    """

    scroll_to_column_header(driver, mpo_name)
    wait_until_cells_are_loaded(driver, mpo_name)

    mpo_cell = get_cell(driver, compound_id, mpo_name)
    simulate.hover(driver, mpo_cell)
    tooltip = dom.get_element(driver, MPO_CELLTIP)
    verify_is_visible(tooltip, '.header', selector_text=mpo_name)
    tooltip_constituents = dom.get_elements(tooltip, 'li')
    # First element of list is the header, the constituents are the
    # rest of the items in the list
    tooltip_constituents = tooltip_constituents[1:]
    for constituent in tooltip_constituents:
        name = dom.get_element(constituent, 'label').text
        value = dom.get_element(constituent, '.value').text
        color = get_color_tuple('.color-square', constituent)
        assert value == expected_tooltip_values[name]
        assert color == expected_tooltip_colors[name]
