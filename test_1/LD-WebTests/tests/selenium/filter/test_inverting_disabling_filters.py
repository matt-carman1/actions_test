import pytest

from helpers.change.filter_actions import remove_all_filters, get_filter, set_filter_range, add_filter
from helpers.change.grid_column_menu import sort_grid_by
from helpers.selection.filter_actions import FILTER_INVERT_BUTTON, FILTER_ENABLE_BUTTON, \
    FILTER_RANGE_SLIDER_INVERTED, FILTER_RANGE_SLIDER_DISABLED, TOGGLE_ALL_FILTERS_BUTTON, \
    TOGGLE_ALL_FILTERS_CONTAINER_ACTIVE
from helpers.selection.grid import Footer
from helpers.verification.element import verify_is_not_visible, verify_is_visible
from helpers.verification.grid import verify_footer_values, verify_column_contents
from library import dom

live_report_to_duplicate = '5 Compounds 4 Assays'
live_report_to_duplicate = {'livereport_name': '5 Compounds 4 Assays', 'livereport_id': '882'}


@pytest.mark.app_defect(reason="SS-32648: Flaky Test on master")
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_inverting_disabling_filters(selenium):
    """
    Test LD inverting and disabling of filters.

    :param selenium: Selenium Webdriver
    """

    # Remove any existing filters from the duplicated LR
    remove_all_filters(selenium)
    sort_grid_by(selenium, 'ID')

    # Add filter on column "Clearance (undefined)". Leave min-value at auto, set max to 10
    add_filter(selenium, 'Clearance (undefined)')
    clearance_filter_element = get_filter(selenium, 'Clearance (undefined)', filter_position=3)
    set_filter_range(selenium, clearance_filter_element, filter_position=3, upper_limit=10)

    # Verify RC Slider is not inverted
    verify_is_not_visible(clearance_filter_element, FILTER_RANGE_SLIDER_INVERTED)

    # Verify footer values: 5 Compounds, 3 after filter
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(5),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(3)
        })

    # Verify ids in the grid
    verify_column_contents(selenium, 'ID', ['CRA-032662', 'CRA-032664', 'CRA-032703'])

    # Click "invert" button
    dom.click_element(clearance_filter_element, FILTER_INVERT_BUTTON)

    # Verify RC Slider is inverted
    verify_is_visible(clearance_filter_element, FILTER_RANGE_SLIDER_INVERTED)

    # Verify footer values: 5 Compounds, 2 after filter
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(5),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(2)
        })

    # Verify ids in the grid
    verify_column_contents(selenium, 'ID', ['CRA-032913', 'CRA-035608'])

    # Add filter on column "STABILITY-PB-PH 7.4 (%Rem@2hr) [%]". Leave min-value at auto, set max to 80
    add_filter(selenium, 'STABILITY-PB-PH 7.4 (%Rem@2hr)')
    stability_filter_element = get_filter(selenium, 'STABILITY-PB-PH 7.4 (%Rem@2hr)', filter_position=4)
    set_filter_range(selenium, stability_filter_element, filter_position=4, upper_limit=80)

    # Verify RC Slider is not disabled
    verify_is_not_visible(stability_filter_element, FILTER_RANGE_SLIDER_DISABLED)

    # Verify footer values: 5 Compounds, 1 after filter
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(5),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(1)
        })

    # Click checkbox to disable "STABILITY-PB-PH 7.4 (%Rem@2hr) [%]".
    dom.click_element(stability_filter_element, FILTER_ENABLE_BUTTON)

    # Verify RC Slider is disabled
    verify_is_visible(stability_filter_element, FILTER_RANGE_SLIDER_DISABLED)

    # Verify footer values: 5 Compounds, 2 after filter
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(5),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(2)
        })

    # Toggle the Filter ON/OFF to Off.
    dom.click_element(selenium, TOGGLE_ALL_FILTERS_BUTTON)

    # Verify 5 Compounds.
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(5),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE_NONE
        })

    # Verify the button to toggle all filters is OFF (not active)
    verify_is_not_visible(selenium, TOGGLE_ALL_FILTERS_CONTAINER_ACTIVE)
