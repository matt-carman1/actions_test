from selenium.webdriver.common.by import By

from helpers.change import range_actions
from helpers.change.actions_pane import open_filter_panel
from helpers.selection.dropdown import DROPDOWN_QUERY_INPUT, \
    DROPDOWN_LIST_ITEM, DROPDOWN_LIST_CONTAINER, DROPDOWN_LIST_SELECTED_ITEMS_CONTAINER, \
    DROPDOWN_LIST_UNSELECTED_ITEMS_CONTAINER, DROPDOWN_HEADER, DROPDOWN_ITEMS_CONTAINER, \
    DROPDOWN_LIST_ITEM_CHECKBOX
from helpers.selection.filter_actions import FILTER_COLUMN_PICKER, FILTER_COLUMN_PICKER_DROPDOWN_LIST, \
    BOX_WIDGET, FILTERS_HEADER_RIGHT_BUTTON_CONTAINER, FILTER_HEADER_RIGHT_BUTTON, FILTER_HEADER_RIGHT_MENU_OPEN, \
    FILTER_RANGE_LOWER_VALUE_INPUT, FILTER_RANGE_UPPER_VALUE_INPUT, \
    FILTERS_HEADER_MENU_ITEM, \
    HEADER_TITLE, FILTER_GEAR_MENU_ITEM_SHOW_AS_TEXT, FILTER_GEAR_MENU_ITEM_SHOW_AS_RANGE, COMPOUND_TYPE_CHECKBOX
from helpers.selection.general import MENU_ITEM
from helpers.verification.element import verify_selected
from library import base, dom, simulate, utils, wait
from tests import selenium


def add_filter(driver, filter_name):
    """
    Adds the desired filter to the Filter panel
    :param driver: Selenium Webdriver
    :param filter_name: str, filter name to be added
    """
    dom.click_element(driver, FILTER_COLUMN_PICKER)

    wait.until_visible(driver, '.filter-column-picker-dropdown')
    dom.click_element(driver,
                      '{} li'.format(FILTER_COLUMN_PICKER_DROPDOWN_LIST),
                      text=filter_name,
                      exact_text_match=True)


def get_filter(driver, filter_name, filter_position):
    """
    Get filter by name. It does NOT adds the filter if the filter is not already present.

    :param driver: Selenium webdriver
    :param filter_name: str, Name of the filter to add
    :param filter_position: int, absolute position of the filter in the filter panel. This is done because we could
    add the same filter multiple times. The first filter has position 3. Also, the filters are sorted alphabetically.
    :return: filter box element
    """

    # Make sure filter panel is visible before proceeding
    open_filter_panel(driver)

    # check if filter already exists before creation
    # TODO: this might change in the future: the check is to just prevent adding multiple filters with the same name
    # in the future we'll extract some of the code to a separate add_filter method
    # hence get_filter will only retrieve an existing filter
    filter_box = dom.get_element(driver, '{}:nth-child({})'.format(BOX_WIDGET, filter_position), filter_name)
    if filter_box:
        return filter_box
    else:
        raise RuntimeError("Cannot find filter '{}'. get_element returned {}".format(filter_name, filter_box))


def remove_all_filters(driver):
    """
    Remove all filters in filter panel

    :param driver: Selenium webdriver
    """

    # Make sure filter panel is visible before proceeding
    open_filter_panel(driver)
    # TODO: Revisit this test after SS-26886 is resolved since currently filters_options is never disabled
    dom.click_element(driver, FILTERS_HEADER_RIGHT_BUTTON_CONTAINER)
    dom.click_element(driver, FILTERS_HEADER_MENU_ITEM, text='Remove All')
    base.click_ok(driver)


def select_filter_checkbox_item(filter_element, item_name, do_select=True):
    """
    Function to select/deselect a checkbox in a given filter

    :param filter_element: Filter element to select, or selenium webdriver
    :param item_name: item to select or deselect
    :param do_select: <bool> If False, action is deselect
    """

    driver = utils.get_driver_from_element(filter_element)

    # Wait for filter text auto-suggest to appear
    dom.click_element(filter_element, DROPDOWN_HEADER)
    wait.until_visible(filter_element, '{} {}'.format(DROPDOWN_ITEMS_CONTAINER, DROPDOWN_LIST_ITEM), text=item_name)

    selection_list = dom.get_element(filter_element, DROPDOWN_ITEMS_CONTAINER)
    wait.until_visible(selection_list, DROPDOWN_LIST_ITEM, text=item_name)

    # Select/deselect specific item and wait for change to occur
    dom.click_element(selection_list, DROPDOWN_LIST_ITEM, text=item_name, exact_text_match=True)
    item = dom.get_element(selection_list, DROPDOWN_LIST_ITEM_CHECKBOX)

    if do_select:
        verify_selected(selection_list, DROPDOWN_LIST_ITEM_CHECKBOX, True)
    else:
        verify_selected(selection_list, DROPDOWN_LIST_ITEM_CHECKBOX, False)

    # click outside to apply the filter
    # NOTE (pradeep): Tried using `dom.click_element` on body, but for some reason selenium does an actual click on
    # some random element on the screen. Instead, by using a dispatchEvent, we make sure that the click is still
    # processed without affecting any other elements.
    driver.execute_script('document.body.dispatchEvent(new Event("click", { bubbles: true }));')

    # wait for the loading mask to go away
    wait.until_loading_mask_not_visible(driver)


def select_all_filter_checkbox_items(filter_element, do_select=True):
    """
    Function to select/deselect all filter checkbox items

    :param filter_element: Filter element to select, or selenium webdriver
    :param do_select: <bool> if False, action is deselect
    """

    # selected/deselected item selectors
    selected_selector = DROPDOWN_LIST_SELECTED_ITEMS_CONTAINER
    unselected_selector = DROPDOWN_LIST_UNSELECTED_ITEMS_CONTAINER

    # Assign selectors depending on whether we are selecting or deselecting
    if not do_select:
        initial_selected_state = selected_selector
        final_selected_state = unselected_selector
    else:
        initial_selected_state = unselected_selector
        final_selected_state = selected_selector

    # Wait for filter text autosuggest to appear
    dom.click_element(filter_element, DROPDOWN_HEADER)
    wait.until_visible(filter_element, DROPDOWN_LIST_CONTAINER)

    selection_list = dom.get_element(filter_element, initial_selected_state)
    # Note: Need to use native webdriver command to avoid calling is_displayed
    # on (possibly) very many items, which is really slow.
    list_items = selection_list.find_elements(By.TAG_NAME, "li")

    # Handle case where we select/deselect all items
    for item in list_items:
        simulate.click(filter_element, item)
    dom.click_element(filter_element, DROPDOWN_HEADER)
    wait.until_not_visible(filter_element, final_selected_state)

    driver = utils.get_driver_from_element(filter_element)
    wait.until_loading_mask_not_visible(driver)


def type_and_select_filter_item(filter_element, item_name):
    """
    Type in the name of a filter and select checkbox item

    Note: Does not support deselecting

    :param filter_element: Element corresponding to filter of choice
    :param item_name: <str> item to be selected
    TODO:
        Improve this function to have list passed to "item_name". This
        would help us select or deselect single or multiple items at once.
        Thus, making the code faster and reducing the lines of code.
    """
    dom.click_element(filter_element, DROPDOWN_HEADER)
    wait.until_visible(filter_element, DROPDOWN_LIST_CONTAINER)

    dom.set_element_value(filter_element, DROPDOWN_QUERY_INPUT, item_name)

    select_filter_checkbox_item(filter_element, item_name)


def paste_to_filter(filter_element):
    """
    Send paste event to the input of the filter element

    :param filter_element: the filter element
    """
    autosuggest_input = dom.click_element(filter_element, DROPDOWN_QUERY_INPUT)
    dom.paste(autosuggest_input)


def change_filter_settings(filter_element, setting_text, filter_position, confirm_dialog=True):
    """
    To change filter settings like converting to range,text, quick filters,
    reset the filters etc.
    :param filter_element: WebElement for the filter condition
    :param setting_text: Visible text for the setting. range,text,
    quick filters, reset the filters etc.
    :param filter_position: int, position of the filter in the filter panel. This is done because we could add the
    same filter multiple times. The first filter has position 3. Also, the filters are sorted alphabetically.
    :param confirm_dialog: Click OK if changing the setting requires a confirmation. Pass
                  False if there is no confirmation box for the setting change
    :return: filter box element
    """
    driver = utils.get_driver_from_element(filter_element)
    filter_name = dom.get_element(filter_element, HEADER_TITLE).text

    dom.click_element(filter_element, FILTER_HEADER_RIGHT_BUTTON)
    wait.until_visible(filter_element, FILTER_HEADER_RIGHT_MENU_OPEN)
    dom.click_element(filter_element, MENU_ITEM, text=setting_text)
    # Do we want to get the driver from element
    if confirm_dialog:
        base.click_ok(driver)

    # convert actions on a filter might change the DOM reference, so we wait until the current filter is removed
    # from the DOM, and then reselect the newer one
    if setting_text in [FILTER_GEAR_MENU_ITEM_SHOW_AS_TEXT, FILTER_GEAR_MENU_ITEM_SHOW_AS_RANGE]:
        wait.until_not_visible(filter_element, HEADER_TITLE)
        return get_filter(driver, filter_name, filter_position)

    return filter_element


def set_filter_range(driver, filter_element, filter_position, lower_limit=None, upper_limit=None):
    """
    Adjust a filter's range based on upper and lower limit

    NOTE: This is similar to the advanced_search_actions.set_query_range,
    but unlike that function this resets the filter before setting the values

    :param driver: selenium webdriver
    :param filter_element: filter element to work on
    :param filter_position: int, absolute position of the filter in the filter panel. This is done because we could
    add the same filter multiple times. The first filter has position 3. Also, the filters are sorted alphabetically.
    :param lower_limit: lower range limit value
    :param upper_limit: upper range limit value
    """

    change_filter_settings(filter_element, "Reset", filter_position)

    if lower_limit is not None:
        range_actions.set_range_limit_value_in_filter_query(driver, filter_element, FILTER_RANGE_LOWER_VALUE_INPUT,
                                                            lower_limit)

    if upper_limit is not None:
        range_actions.set_range_limit_value_in_filter_query(driver, filter_element, FILTER_RANGE_UPPER_VALUE_INPUT,
                                                            upper_limit)


def set_filter_for_r_groups(driver):
    """
    Apply R-group filter by deselecting COMPOUND(s)
    :param driver: selenium webdriver
    """
    dom.click_element(driver, COMPOUND_TYPE_CHECKBOX, text="COMPOUND")

    # Utility function for waiting till the loading mask goes away
    wait.until_loading_mask_not_visible(driver)
