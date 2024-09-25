"""
To test for tooltips & Add To Favourites in Data and columns tree
"""

import pytest

from helpers.change.actions_pane import open_add_data_panel
from helpers.change.data_and_columns_tree import clear_column_tree_search, search_column_tree
from helpers.change.freeform_column_action import create_ffc
from helpers.selection.column_tree import (COLUMN_TREE_PICKER_TEXT_NODE, COLUMN_TREE_PICKER_TOOLTIP_HEADER_TEXT,
                                           COLUMN_TREE_PICKER_TOOLTIP_BODY_TEXT, COLUMN_TREE_PICKER_NODE_TEXT_AREA,
                                           PROJECT_FAVORITE_COLUMN_NODE,
                                           COLUMN_TREE_PICKER_TOOLTIP_REMOVE_FAVORITE_ICON,
                                           COLUMN_TREE_PICKER_NODE_ICON_AREA,
                                           COLUMN_TREE_PICKER_TOOLTIP_ADD_FAVORITE_ICON, COLUMN_TREE_PICKER_TOOLTIP)
from helpers.verification.data_and_columns_tree import verify_column_visible_in_column_tree_by_searching
from helpers.verification.element import verify_is_visible, verify_is_not_visible
from library import dom, simulate, utils
from library.wait import until_condition_met


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_tooltips_descriptions_and_favorites_in_column_tree(selenium):
    """
    * Creates a new livereport
    * Creates a new ffc
    * Verifies tooltip header and description for the ffc
    * Favorites the column
    * Verifies that favorited column appears under Project Favourites

    :param selenium: Selenium Webdriver
    """
    # Defining test variables
    tooltip_header = 'Freeform Columns'
    tooltip_description = ("Freeform columns allow you to enter custom data for any compound by typing "
                           "directly into a spreadsheet cell.\n"
                           "The column can optionally be 'published' to make it available and editable "
                           "across many LiveReports.\n"
                           "Use these to to track compound state for workflows, bin compounds into groups, collect "
                           "structured comments, and more.")
    ffc_name = utils.make_unique_name('Test_ffc')

    # opens the D&C Tree
    open_add_data_panel(selenium)

    # Hovers over the 'Freeform columns' node and verifies the tooltip header and description for it.
    # Tooltip header is the column name for parent node ie. 'Freeform Columns')
    simulate.hover(selenium, dom.get_element(selenium, COLUMN_TREE_PICKER_TEXT_NODE, text=tooltip_header))
    verify_is_visible(selenium,
                      COLUMN_TREE_PICKER_TOOLTIP_HEADER_TEXT,
                      selector_text=tooltip_header,
                      exact_selector_text_match=True)
    verify_is_visible(selenium,
                      COLUMN_TREE_PICKER_TOOLTIP_BODY_TEXT,
                      selector_text=tooltip_description,
                      exact_selector_text_match=True)

    # Creates a new ffc
    create_ffc(selenium,
               ffc_name,
               description='Testing tooltip description for ffc',
               column_type='Text',
               allow_any_value=True,
               picklist_values=None,
               publish=True)

    # Opens column tree, searches for the new ffc
    open_add_data_panel(selenium)
    verify_column_visible_in_column_tree_by_searching(selenium, ffc_name, retries=3)

    # ----- Hovers over column and verifies tooltip header and description -----
    # Verifying the header and description for new ffc
    simulate.hover(selenium,
                   dom.get_element(selenium, COLUMN_TREE_PICKER_NODE_TEXT_AREA, text=ffc_name, exact_text_match=True))
    verify_is_visible(selenium,
                      COLUMN_TREE_PICKER_TOOLTIP_HEADER_TEXT,
                      selector_text=ffc_name,
                      exact_selector_text_match=True)
    verify_is_visible(selenium,
                      COLUMN_TREE_PICKER_TOOLTIP_BODY_TEXT,
                      selector_text='Testing tooltip description for ffc',
                      exact_selector_text_match=True)

    # Note (absingh): move to the center of the tooltip first so that the tooltip doesn't disappear while the cursor is
    # travelling
    simulate.hover(selenium, dom.get_element(selenium, COLUMN_TREE_PICKER_TOOLTIP))
    # ----- Adds column to Project Favorites, verifies it and then unfavorites the column ----- #
    # Adding column to Project Favorites and verifying
    dom.click_element(selenium, "{} {}".format(COLUMN_TREE_PICKER_TOOLTIP,
                                               COLUMN_TREE_PICKER_TOOLTIP_ADD_FAVORITE_ICON))

    def search_column_tree_for_favorited_ffc():
        search_column_tree(selenium, ffc_name)
        visible = verify_is_visible(selenium,
                                    COLUMN_TREE_PICKER_TEXT_NODE,
                                    selector_text='Project Favorites',
                                    exact_selector_text_match=True)
        assert visible

    until_condition_met(search_column_tree_for_favorited_ffc, 3)

    # Closing the Project Favorites node
    dom.click_element(selenium, COLUMN_TREE_PICKER_TEXT_NODE, text='Project Favorites', exact_text_match=True)

    # Verifying that the column is favorited in FFC accordion
    verify_is_visible(selenium, PROJECT_FAVORITE_COLUMN_NODE)
    # Closing accordion node
    dom.click_element(selenium, COLUMN_TREE_PICKER_TEXT_NODE, text='Freeform Columns', exact_text_match=True)

    # Opening Project Favorites and checking for favorited column in project Favorites
    dom.click_element(selenium, COLUMN_TREE_PICKER_TEXT_NODE, text='Project Favorites', exact_text_match=True)
    verify_is_visible(selenium,
                      COLUMN_TREE_PICKER_NODE_TEXT_AREA,
                      selector_text=ffc_name,
                      exact_selector_text_match=True)

    # ----- Removes column from Project Favorites, verifies it and then verifies it in Project Favorites ----- #
    # Hovering over the tooltip and removing the favorited column
    simulate.hover(selenium,
                   dom.get_element(selenium, COLUMN_TREE_PICKER_NODE_TEXT_AREA, text=ffc_name, exact_text_match=True))

    # Note (absingh): move to the center of the tooltip first so that the tooltip doesn't disappear while the cursor is
    # travelling
    simulate.hover(selenium, dom.get_element(selenium, COLUMN_TREE_PICKER_TOOLTIP))
    dom.click_element(selenium, "{} {}".format(COLUMN_TREE_PICKER_TOOLTIP,
                                               COLUMN_TREE_PICKER_TOOLTIP_REMOVE_FAVORITE_ICON))
    # Closing the Project Favorites node
    # Note: Commenting this line out as removing the favorite is quick and takes Project Favorites out of the picture
    # and thus, we do not need to perform this action any more.
    # dom.click_element(selenium, COLUMN_TREE_PICKER_TEXT_NODE, text='Project Favorites', exact_text_match=True)
    clear_column_tree_search(selenium)
    # Reopening Project Favorites and verifying that column is not in Project favorites
    dom.click_element(selenium, COLUMN_TREE_PICKER_TEXT_NODE, text='Project Favorites', exact_text_match=True)
    verify_is_not_visible(selenium, COLUMN_TREE_PICKER_NODE_ICON_AREA, selector_text=ffc_name, custom_timeout=5)
