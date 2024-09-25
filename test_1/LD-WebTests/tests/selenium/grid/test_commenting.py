"""
Testing adding, modifying, and persistence of added compound comments.
"""
import pytest

from helpers.change import comments, actions_pane
from helpers.change.grid_row_actions import select_row
from helpers.change.live_report_picker import open_live_report
from helpers.change.project import open_project
from helpers.flows.add_compound import search_by_id
from helpers.selection.comments import COMMENTS_TEXTBOX, POST_COMMENT_BUTTON, EDIT_COMMENT_LINK, COMMENT_TEXTAREA, \
    EDIT_COMMENTBAR
from helpers.selection.grid import Footer
from helpers.selection.live_report_tab import TAB_ACTIVE
from helpers.verification.comments import verify_comment_added
from helpers.verification.grid import check_for_info_butterbar, verify_footer_values
from library import dom, simulate, utils, wait
from library.authentication import login, logout


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_commenting(selenium):
    """
    As demo user: make a new LR, add 2 compounds, add a comment to both compounds simultaneously, modify the last
    comment for the second compound, refresh page,
    verify comments are correct.
    Re-login as a seurat user and verify comments for all the compounds are correct.
    """

    # Test variables
    comment_1 = utils.make_unique_name('Comment: ')
    comment_modified = '{} Modified.'.format(comment_1)
    compound_ids = ['CHEMBL100', 'CHEMBL1000']

    # Opening the Compounds panel and Searching by IDs
    actions_pane.open_add_compounds_panel(selenium)
    search_by_id(selenium, ' '.join(compound_ids))
    # Closing the actions pane which takes up space unnecessarily
    actions_pane.close_add_compounds_panel(selenium)

    wait.until_live_report_loading_mask_not_visible(selenium)
    verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(2)})

    # Click on the compound's comment button
    comments.click_compound_comment_bubble(selenium, compound_ids[0])

    # Select 2nd compound row
    select_row(selenium, compound_ids[1])

    # Enter a comment & click "Post" button (will add 2 comments, 1 per row)
    dom.set_element_value(selenium, COMMENTS_TEXTBOX, comment_1)
    dom.click_element(selenium, POST_COMMENT_BUTTON)
    utils.request_animation_frame(selenium)

    # Verify comment exists 2 times (one for each compound)
    # Deselect row 2
    select_row(selenium, compound_ids[1])
    verify_comment_added(selenium, compound_ids[0], comment_1)
    # Deselect row 1 and select row 2
    select_row(selenium, compound_ids[0])
    select_row(selenium, compound_ids[1])
    verify_comment_added(selenium, compound_ids[1], comment_1)

    # Edit the last comment that was previously added
    edit_comment_bar = dom.get_elements(selenium, EDIT_COMMENTBAR)
    last_comment = edit_comment_bar[0] if len(edit_comment_bar) == 1 else edit_comment_bar[-1]
    simulate.click(selenium, last_comment)
    utils.request_animation_frame(selenium)

    # After action above, there should only be one edit link to change comment
    dom.click_element(selenium, EDIT_COMMENT_LINK)
    utils.request_animation_frame(selenium)
    dom.set_element_value(selenium, COMMENT_TEXTAREA, comment_modified)
    comments.click_comment_edit_button(selenium)

    # Verify butter bar goes away
    check_for_info_butterbar(selenium, 'Updating Comment', visible=False)

    # Verify comment is modified
    verify_comment_added(selenium, compound_ids[1], comment_modified)

    # Refresh page
    selenium.refresh()

    # Re-verify comments are correct after refresh
    comments.click_compound_comment_bubble(selenium, compound_ids[0])
    utils.request_animation_frame(selenium)
    verify_comment_added(selenium, compound_ids[0], comment_1)
    comments.click_compound_comment_bubble(selenium, compound_ids[1])
    utils.request_animation_frame(selenium)
    verify_comment_added(selenium, compound_ids[1], comment_modified)

    # Save Live Report name and logout of demo/demo
    live_report_name = dom.get_element(selenium, TAB_ACTIVE).text
    logout(selenium)

    # Log in as seurat user and open Live Report
    login(selenium, 'seurat', 'seurat')
    open_project(selenium, "JS Testing")
    open_live_report(selenium, name=live_report_name)

    # Verify persisting of comments when logged in as a different user
    comments.click_compound_comment_bubble(selenium, compound_ids[0])
    utils.request_animation_frame(selenium)
    verify_comment_added(selenium, compound_ids[0], comment_1)
    comments.click_compound_comment_bubble(selenium, compound_ids[1])
    utils.request_animation_frame(selenium)
    verify_comment_added(selenium, compound_ids[1], comment_modified)
