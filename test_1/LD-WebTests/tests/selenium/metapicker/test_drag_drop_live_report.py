from helpers.change.live_report_picker import close_metapicker
from helpers.verification.element import verify_is_visible
from library import dom, simulate, wait, actions
from helpers.change import live_report_picker
from helpers.selection.live_report_picker import REPORT_LIST_TITLE, REPORT_LIST_SELECTED_ITEM_TITLE, METAPICKER_FOLDER,\
    REPORT_LIST_SELECTED_FOLDER


def test_drag_drop_live_report(selenium, new_live_report, open_project):
    """
    Testing the helper functions for dragging elements.
    Drag and drop element X onto element Y,
    It has been tested here by dragging LRs to folders in metapicker
    :param selenium: Webdriver
    :param new_live_report: fixture to create new LiveReport. It returns the new LR name.
    """

    # ----- Create a new LR and search for LR in metapicker ----- #
    report_name = new_live_report

    # This opens metapicker and searches for newly created LR
    live_report_picker.search_for_live_report(selenium, name=report_name)

    # Click the report and then wait until it's selected before dragging and dropping
    dom.click_element(selenium, REPORT_LIST_TITLE, text=report_name)
    verify_is_visible(selenium, REPORT_LIST_SELECTED_ITEM_TITLE, selector_text=report_name)

    # ----- Drag and drop LR into MPO folder ----- #

    # Define element corresponding to LR in metapicker (this element will be dragged)
    source_element = dom.get_element(selenium, REPORT_LIST_TITLE, text=report_name)

    # Define MPO folder element (element where the LR will be dragged into)
    first_dest_element = dom.get_element(selenium, METAPICKER_FOLDER, text='MPO')

    # Perform drag and drop LR into MPO folder
    actions.drag_and_drop(selenium, source_element, first_dest_element)

    # ----- Ensure the selected LR in metapicker is in MPO folder ----- #
    # Select the source element, then make sure the selected report is in MPO
    simulate.click(selenium, source_element)
    wait.until_visible(selenium, REPORT_LIST_SELECTED_FOLDER, text="MPO")

    # ----- Drag and drop LR into Adv Search folder ----- #
    '''
    NOTE -- The second drag/drop simulation is to cover the following implementation detail:
    The helper injects JS the first time it is called on a page, but not subsequently.
    The reason that we do the second drag is that there is a risk that this logic could break the second time
    the helper is used.
    '''

    # Click the report and then wait until it's selected before dragging and dropping
    dom.click_element(selenium, REPORT_LIST_TITLE, text=report_name)
    wait.until_visible(selenium, REPORT_LIST_SELECTED_ITEM_TITLE, text=report_name)

    # Define Adv Search folder element (element where LR will be dragged into a second time)
    second_dest_element = dom.get_element(selenium, METAPICKER_FOLDER, text='Adv Search')

    # Perform drag and drop LR from MPO into Adv Search
    actions.drag_and_drop(selenium, source_element, second_dest_element)

    # ----- Ensure the selected LR in metapicker is in Adv Search folder ----- #
    # Select the source element, then make sure the selected report is in Adv Search
    simulate.click(selenium, source_element)
    wait.until_visible(selenium, REPORT_LIST_SELECTED_FOLDER, text="Adv Search")

    # Closing the metapicker for the test teardown(deleting the LR) to run
    close_metapicker(selenium)
