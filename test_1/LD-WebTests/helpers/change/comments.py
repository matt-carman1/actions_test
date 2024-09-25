"""
Click actions specific to the commenting workflow.
"""
from helpers.change.grid_row_actions import select_rows_and_pick_context_menu_item
from helpers.selection.comments import COMMENT_SCOPE_RADIO_GROUP, EDIT_COMMENT_BUTTON, \
    COMMENT_SELECTED_ENTITIES_RADIO_BUTTON, \
    COMMENT_ALL_ENTITIES_RADIO_BUTTON, COMMENTS_TEXTBOX, POST_COMMENT_BUTTON
from helpers.selection.comments import ZOOM_IMAGE_COMMENT_BUBBLE
from helpers.selection.grid import GRID_COMPOUND_IMAGE_SELECTOR_, GRID_ROW_ID_
from library import dom, simulate, utils, wait


def click_compound_comment_bubble(driver, entity_id):
    """
    Click the comment bubble for a Compound ID.

    :param driver: webdriver
    :param entity_id: str, Compound ID from ID column
    """
    # Expand the compound image and then click on the comments bubble button
    compound_img = dom.get_element(driver, GRID_COMPOUND_IMAGE_SELECTOR_.format(entity_id))
    simulate.hover(driver, compound_img)
    dom.click_element(driver, ZOOM_IMAGE_COMMENT_BUBBLE)


def click_comments_radio(driver, select_all=False):
    """
    Selects the comments radio to view either
    "Selected Compound(s)" or "All Compounds"

    :param driver: webdriver
    :param select_all: boolean, False for "Selected Compound(s)" radio,
                                True for "All Compounds" radio
    :return: None
    """
    assert select_all is True or select_all is False, \
        "select_all must be either True of False"

    radio_group = dom.get_element(driver, COMMENT_SCOPE_RADIO_GROUP)

    radio_selector = COMMENT_ALL_ENTITIES_RADIO_BUTTON if select_all else COMMENT_SELECTED_ENTITIES_RADIO_BUTTON
    dom.click_element(radio_group, radio_selector)


def click_comment_edit_button(driver, action_name='Save'):
    edit_comment_button = dom.get_element(driver, EDIT_COMMENT_BUTTON, action_name)
    simulate.click(driver, edit_comment_button)
    utils.request_animation_frame(driver)


def add_a_comment(driver, list_of_entity_ids, comment):
    """
    Add a comment on selected compound IDs

    :param driver: webdriver
    :param list_of_entity_ids: List of entity ids to be selected
    :param comment: str, Comment to be added
    """
    wait.until_visible(driver, GRID_ROW_ID_.format(list_of_entity_ids[0]))
    select_rows_and_pick_context_menu_item(driver, list_of_entity_ids, option_to_select='Comment')
    dom.set_element_value(driver, COMMENTS_TEXTBOX, comment)
    dom.click_element(driver, POST_COMMENT_BUTTON)
