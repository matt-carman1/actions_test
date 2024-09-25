import pytest

from helpers.change.actions_pane import close_comments_panel
from helpers.change.comments import add_a_comment
from helpers.change.grid_row_actions import select_row
from helpers.change.live_report_menu import copy_live_report_to_project
from helpers.selection.actions_pane import COMMENTS_BUTTON
from helpers.selection.grid import GRID_ROW_ID_
from helpers.verification.comments import verify_comment_added
from library import dom, wait, utils

# LiveReport to be duplicated for the test
live_report_to_duplicate = {'livereport_name': 'Test Reactants - Halides', 'livereport_id': '2554'}


def test_copy_lr_with_comment_to_new_project(selenium, duplicate_live_report, open_livereport):
    """
    Test for copy Livereport with Comments to new Project.

    1. Add comments to compounds
    2. Copy the LiveReport to new project
    3. Verify comments are copied to new project

    :param selenium: Selenium Webdriver
    :return:
    """

    duplicate_lr_name = duplicate_live_report
    copy_to_project_name = 'Project A'

    # Add comments to compounds
    comment = utils.make_unique_name('Comment: ')
    add_a_comment(selenium, list_of_entity_ids=['V055824', 'V055825'], comment=comment)

    # Copy the LiveReport to a project
    copy_live_report_to_project(selenium, copy_to_project_name, duplicate_lr_name, open_lr=True)

    # Verify comments are copied to new project
    wait.until_visible(selenium, GRID_ROW_ID_.format('V055824'))
    select_row(selenium, 'V055824')
    dom.click_element(selenium, COMMENTS_BUTTON)
    verify_comment_added(selenium, 'V055824', comment)
    select_row(selenium, 'V055825')
    verify_comment_added(selenium, 'V055825', comment)
    close_comments_panel(selenium)
