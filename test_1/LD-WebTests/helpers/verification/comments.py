"""
Click actions specific to the commenting workflow.
"""

from library import dom, utils
from helpers.change import comments
from helpers.selection.comments import COMMENT_CONTENT


def verify_comment_added(driver, entity_id, expected_comment):
    """
    Verifies last comment added for a structure is the expected_comment.

    :param driver: webdriver
    :param entity_id: str, structure ID from the ID column in the LR
    :param expected_comment: str, last added comment for the structure
    :return: None
    """

    comments.click_comments_radio(driver)
    utils.request_animation_frame(driver)
    comment_elements = dom.get_elements(driver, COMMENT_CONTENT)
    structure_comments = [element.text for element in comment_elements]

    assert len(structure_comments) > 0, "No comments for {}." \
        .format(entity_id)
    assert expected_comment in structure_comments, ("Comment '{}' "
                                                    "not found for {}").format(expected_comment, entity_id)
