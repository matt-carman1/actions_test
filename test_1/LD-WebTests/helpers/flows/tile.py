from helpers.selection.rationale import RATIONALE_TEXTAREA, RATIONALE_SAVE
from helpers.selection.tile_view import RATIONALE_CELL, RATIONALE_CELL_EDIT_BUTTON
from library import simulate, dom
from library.dom import set_element_value, click_element


def edit_rationale_in_tile_view(driver, rationale_text, compound_id):
    """
    Edits rationale in tile view for a given compound

    :param driver: selenium webdriver
    :param rationale_text: text input for rationale
    :param compound_id: compound id to edit/add rationale for
    """
    simulate.hover(driver, dom.get_element(driver, RATIONALE_CELL.format(compound_id)))
    simulate.click(driver, dom.get_element(driver, RATIONALE_CELL_EDIT_BUTTON.format(compound_id)))
    set_element_value(driver, RATIONALE_TEXTAREA, rationale_text)
    click_element(driver, RATIONALE_SAVE)
