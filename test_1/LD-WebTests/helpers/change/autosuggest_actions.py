from helpers.selection.autosuggest_multiselect import AUTOSUGGEST_QUERY_INPUT, \
    MULTISELECT_ITEM_TEXT, MULTISELECT_PICKLIST, MULTISELECT_SELECTED_ITEMS_LIST, \
    MULTISELECT_UNSELECTED_ITEMS_LIST, MULTISELECT_UNSELECTED_ITEM
from helpers.selection.filter_actions import SELECTED_CONTAINER, HEADER_TITLE
from library import dom, utils, wait


def set_autosuggest_items(autosuggest_container_element, items, do_select=True):
    """
    Function to select/deselect checkboxes in a given autosuggest

    :param autosuggest_container_element: The autosuggest element or it's container
    :param items: item to select or deselect
    :param do_select: <bool> If False, action is deselect
    """
    driver = utils.get_driver_from_element(autosuggest_container_element)

    # Assign selectors depending on whether we are selecting or deselecting
    if not do_select:
        initial_list_selector = MULTISELECT_SELECTED_ITEMS_LIST
    else:
        initial_list_selector = MULTISELECT_UNSELECTED_ITEMS_LIST

    initial_list_item_selector = '{} {}'.format(initial_list_selector, MULTISELECT_ITEM_TEXT)

    for item in items:
        # type the item and wait for item to appear in the multi-select
        dom.set_element_value(autosuggest_container_element, AUTOSUGGEST_QUERY_INPUT, item)
        wait.until_visible(autosuggest_container_element, initial_list_item_selector, text=item)

        # add/remove the item in the query and wait for the change to occur
        selection_list = dom.get_element(autosuggest_container_element, initial_list_selector)
        dom.click_element(selection_list, MULTISELECT_UNSELECTED_ITEM, text=item, exact_text_match=True)
        wait.until_not_visible(autosuggest_container_element, initial_list_selector, text=item)

    # Deselect multi-select by clicking elsewhere and wait for muti-select to disappear
    # NOTE (pradeep): Tried using `dom.click_element` on body, but for some reason selenium does an actual click on
    # some random element on the screen. Instead, by using a dispatchEvent, we make sure that the click is still
    # processed without affecting any other elements.
    driver.execute_script('document.body.dispatchEvent(new Event("mousedown", { bubbles: true }));')
    wait.until_not_visible(autosuggest_container_element, MULTISELECT_PICKLIST)


def remove_autosuggest_bubble_value(driver, element, bubble_to_remove):
    """
    Helper to remove autosuggest values from advanced search/filters.

    :param driver: webdriver instance
    :param element:  Box element (can be obtained from get_filter() or get_query())
    :param bubble_to_remove: str, value to be removed from the filter text area
    """

    matching_options = dom.get_elements(element, SELECTED_CONTAINER, bubble_to_remove)
    dom.click_element(matching_options[0], 'span', text='x')

    # applying the change by clicking on header name. (both filter/advanced search)
    dom.click_element(element, HEADER_TITLE)
    # wait for the loading mask to go away
    wait.until_loading_mask_not_visible(driver)
