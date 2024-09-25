import pytest

from helpers.selection.grid import Footer
from library import dom, wait
from library import actions
from helpers.change import actions_pane, columns_action, \
    grid_columns, filter_actions
from helpers.flows import add_compound
from helpers.verification import grid
from helpers.selection.add_compound_panel import COMPOUND_SEARCH_SUB_TAB, COMPOUND_SEARCH_SUB_TAB_ACTIVE, \
    BASIC_SEARCH_SIMILARITY_SEARCH_SLIDER, BASIC_SEARCH_SIMILARITY_SEARCH_SLIDER_THRESHOLD_LABEL
from helpers.selection.filter_actions import FILTER_RANGE_UPPER_SLIDER,\
    FILTER_RANGE_LOWER_SLIDER


@pytest.mark.skip(reason="SS-36360: Change width and height of Maestro Sketcher")
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_drag_slider_helper(selenium):
    """
    Test helper functions for dragging elements by specific amount horizontally
    or vertically, to support e.g. sliders.
    1. Drag range filter slider.
    2. Drag Similarity Search slider.
    :param selenium: Webdriver
    :return:
    """
    # Assumption: We know the data to be filtered and thus the expected results.
    column = "AlogP"
    search_keyword = "CHEMBL105*,CHEMBL103*"

    # Search Compounds by ID
    actions_pane.open_add_compounds_panel(selenium)

    # Navigating to similarity search
    actions_pane.open_compound_search_panel(selenium)
    dom.click_element(selenium, COMPOUND_SEARCH_SUB_TAB, text='Structure', exact_text_match=True)
    wait.until_visible(selenium, COMPOUND_SEARCH_SUB_TAB_ACTIVE, text='Structure')

    dom.click_element(selenium, COMPOUND_SEARCH_SUB_TAB, text='Similarity', exact_text_match=True)
    wait.until_visible(selenium, COMPOUND_SEARCH_SUB_TAB_ACTIVE, text='Similarity')

    # DRAGGING SIMILARITY SEARCH SLIDER UNDER BASIC COMPOUND SEARCH
    similarity_slider = dom.get_element(selenium, BASIC_SEARCH_SIMILARITY_SEARCH_SLIDER)
    # Checking that the slider header shows 0.35 as the initial position
    wait.until_visible(selenium, BASIC_SEARCH_SIMILARITY_SEARCH_SLIDER_THRESHOLD_LABEL, text="Threshold \u2265 0.35")

    # Drag the slider horizontally by 50px
    actions.drag_and_drop_by_offset(similarity_slider, 150, 0)
    wait.until_visible(selenium, BASIC_SEARCH_SIMILARITY_SEARCH_SLIDER_THRESHOLD_LABEL, text="Threshold \u2265 0.70")

    # Drag the slider by 25px in reverse direction
    actions.drag_and_drop_by_offset(similarity_slider, -100, 0)
    wait.until_visible(selenium, BASIC_SEARCH_SIMILARITY_SEARCH_SLIDER_THRESHOLD_LABEL, text="Threshold \u2265 0.45")

    # DRAGGING FILTER RANGE SLIDERS
    # Add compounds
    add_compound.search_by_id(selenium, search_keyword)

    # Add a column to the LR
    actions_pane.open_add_data_panel(selenium)
    columns_action.add_column_by_name(selenium, column)

    # The added column on selenium-testserver are represented by column(column).
    # For e.g. "Alog (AlogP)", "H-Bond Donors (H-Bond Donors)"
    column_name = "{} ({})".format(column, column)

    # This function would check in a way that the column is added to the LR
    grid_columns.scroll_to_column_header(selenium, column_name)

    # Open the Filter Panel and Clear filters if there were some leftover ones
    actions_pane.open_filter_panel(selenium)
    filter_actions.remove_all_filters(selenium)

    # Add a filter from the dropdown
    filter_actions.add_filter(selenium, column_name)
    filter_element = filter_actions.get_filter(selenium, column_name, filter_position=3)

    right_slider = dom.get_element(filter_element, FILTER_RANGE_UPPER_SLIDER)
    left_slider = dom.get_element(filter_element, FILTER_RANGE_LOWER_SLIDER)

    # Dragging the lower range slider
    actions.drag_and_drop_by_offset(left_slider, 20, 0)
    wait.until_loading_mask_not_visible(selenium)

    # Dragging the upper range slider
    actions.drag_and_drop_by_offset(right_slider, -35, 0)
    wait.until_loading_mask_not_visible(selenium)

    # Verify footer values after dragging
    grid.verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(22),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(20)
        })
