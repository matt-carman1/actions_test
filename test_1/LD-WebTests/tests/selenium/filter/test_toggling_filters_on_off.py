import pytest

from helpers.selection.grid import Footer
from library import dom
from helpers.change.grid_row_actions import select_multiple_continuous_rows, pick_row_context_menu_item
from helpers.change.filter_actions import add_filter, get_filter, select_filter_checkbox_item
from helpers.selection.filter_actions import FILTER_INVERT_BUTTON, TOGGLE_ALL_FILTERS_CONTAINER_ACTIVE, \
    TOGGLE_ALL_FILTERS_BUTTON
from helpers.verification.element import verify_is_not_visible, verify_is_visible
from helpers.verification.grid import verify_footer_values

live_report_to_duplicate = {'livereport_name': 'FFC - All types, published and unpublished', 'livereport_id': '1299'}


def test_toggling_filters_on_off(selenium, duplicate_live_report, open_livereport):
    """
    Test to toggle the filter slider on and off; Uncheck all filters
    and check footer values to verify

    :param selenium: Selenium Webdriver
    :param duplicate_live_report: fixture, Duplicates LR
    :param open_livereport: fixture, Opens LR
    """
    # Adding filter on All IDs column from row_context_menu_item by selecting first 8 rows
    select_multiple_continuous_rows(selenium, start_row="CRA-031137", end_row="CRA-032372")
    pick_row_context_menu_item(selenium, entity_id='CRA-032372', option_to_select='Filter')
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(116),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(8)
        })

    # Adding inverted filter on Boolean - published column
    boolean_filter_name = "Boolean - published"
    add_filter(selenium, filter_name=boolean_filter_name)
    boolean_filter_elem = get_filter(selenium, filter_name=boolean_filter_name, filter_position=4)
    select_filter_checkbox_item(filter_element=boolean_filter_elem, item_name="(undefined)")
    dom.click_element(driver_or_parent_element=boolean_filter_elem, selector=FILTER_INVERT_BUTTON)
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(116),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(3)
        })

    # Adding a range filter on Number - published column
    add_filter(selenium, filter_name="Number - published")
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(116),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(2)
        })

    # Toggling filter slider off
    dom.click_element(selenium, TOGGLE_ALL_FILTERS_BUTTON)
    verify_is_not_visible(selenium, TOGGLE_ALL_FILTERS_CONTAINER_ACTIVE)
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(116),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE_NONE
        })

    # Toggling filter slider on
    dom.click_element(selenium, TOGGLE_ALL_FILTERS_BUTTON)
    verify_is_visible(selenium, TOGGLE_ALL_FILTERS_CONTAINER_ACTIVE, custom_timeout=10)
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(116),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(2)
        })
