from helpers.selection.dropdown import DROPDOWN_QUERY_INPUT, DROPDOWN_HEADER_ITEM, \
    DROPDOWN_LIST_ITEM, DROPDOWN_LIST_CONTAINER, DROPDOWN_LIST_ITEM_CHECKBOX, \
    DROPDOWN_ITEMS_CONTAINER
from helpers.selection.filter_actions import HEADER_TITLE
from library import dom, utils, wait
from helpers.verification.element import verify_selected


def set_dropdown_items(dropdown_container_element, items, do_select=True):
    """
    Function to select/deselect checkboxes in a given autosuggest

    :param dropdown_container_element: The dropdown element or it's container
    :param items: item to select or deselect
    :param do_select: <bool> If False, action is deselect
    """
    driver = utils.get_driver_from_element(dropdown_container_element)

    initial_list_item_selector = '{} {}'.format(DROPDOWN_ITEMS_CONTAINER, DROPDOWN_LIST_ITEM)

    for item in items:
        # type the item and wait for item to appear in the multi-select
        dom.set_element_value(dropdown_container_element, DROPDOWN_QUERY_INPUT, item)
        wait.until_visible(dropdown_container_element, initial_list_item_selector, text=item)

        # add/remove the item in the query and wait for the change to occur
        selection_list = dom.get_element(dropdown_container_element, DROPDOWN_ITEMS_CONTAINER)
        dom.click_element(selection_list, DROPDOWN_LIST_ITEM, text=item, exact_text_match=True)

        if do_select:
            verify_selected(selection_list, DROPDOWN_ITEMS_CONTAINER + " " + DROPDOWN_LIST_ITEM_CHECKBOX, True)
        else:
            verify_selected(selection_list, DROPDOWN_ITEMS_CONTAINER + " " + DROPDOWN_LIST_ITEM_CHECKBOX, False)

    # Deselect dropdown-list by clicking elsewhere and wait for dropdown-list to disappear
    # NOTE (agupta): Tried using `dom.click_element` on body, but for some reason selenium does an actual click on
    # some random element on the screen. Instead, by using a dispatchEvent, we make sure that the click is still
    # processed without affecting any other elements.
    driver.execute_script('document.body.dispatchEvent(new Event("click", { bubbles: true }));')
    wait.until_not_visible(dropdown_container_element, DROPDOWN_LIST_CONTAINER)


def remove_dropdown_bubble_value(driver, element, bubble_to_remove):
    """
    Helper to remove dropdown values from filters.

    :param driver: webdriver instance
    :param element:  Box element (can be obtained from get_filter() or get_query())
    :param bubble_to_remove: str, value to be removed from the filter text area
    """

    matching_options = dom.get_elements(element, DROPDOWN_HEADER_ITEM, bubble_to_remove)
    dom.click_element(matching_options[0], 'span', text='x')

    # applying the change by clicking on header name
    dom.click_element(element, HEADER_TITLE)
    # wait for the loading mask to go away
    wait.until_loading_mask_not_visible(driver)
