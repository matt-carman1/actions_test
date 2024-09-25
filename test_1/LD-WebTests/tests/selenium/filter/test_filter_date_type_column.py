import pytest

from helpers.selection.grid import Footer
from library import dom

from helpers.change import actions_pane
from helpers.change.filter_actions import add_filter
from helpers.change.filter_actions import set_filter_range, get_filter, change_filter_settings, \
     type_and_select_filter_item
from helpers.selection.filter_actions import FILTER_INVERT_BUTTON, FILTER_RANGE_SLIDER_INVERTED, \
     FILTER_INVERT_BUTTON_INVERTED
from helpers.verification.element import verify_is_visible
from helpers.verification.grid import verify_footer_values

live_report_to_duplicate = {'livereport_name': 'Test Date Assay Column', 'livereport_id': '2699'}
filter_name = 'Test Dates Assay (date)'


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_range_filter_date_type_column(selenium):
    """
    Adds range-based filter to a date type column and verifies the number of compounds for range filter and inverted
    range filter.

    1. Open filter panel
    2. Add filter for a date type column
    3. Set maximum & minimum limits on the slider to set a range filter
    4. Verify number of compounds in the footer
    5. Invert the range filter, verify inversion and number of compounds in the footer again

    :param selenium: Webdriver
    """

    # Open filter panel
    actions_pane.open_filter_panel(selenium)

    # Add filter on 'Test Dates Assay (date)’ column
    add_filter(selenium, filter_name)

    # Set upper & lower limits to create a range filter
    filter_element_range = get_filter(selenium, filter_name, filter_position=4)
    set_filter_range(selenium,
                     filter_element_range,
                     filter_position=4,
                     lower_limit='2009-01-01',
                     upper_limit='2009-12-01')

    # Verify values in the footer: total 4 & 2 after filter
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(4),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(2)
        })

    # Invert the range filter
    dom.click_element(filter_element_range, FILTER_INVERT_BUTTON)

    # Verify that the slider is inverted
    verify_is_visible(filter_element_range, FILTER_RANGE_SLIDER_INVERTED)

    # Verify footer values, values should be inverted
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(4),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(2)
        })


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_text_filter_date_type_column(selenium):
    """
    Adds a text-based filter to a date type column and verifies the number of compounds for text filter and
    inverted text filter

    1. Open filter panel
    2. Add filter for a date type column
    3. Switch to text filter & add value from the dropdown
    4. Verify the number of compounds in the footer
    5. Invert text filter, verify inversion and number of compounds in the footer again

    :param selenium: Webdriver
    """

    # Open filter panel
    actions_pane.open_filter_panel(selenium)

    # Add filter on 'Test Dates Assay (date)’ column
    add_filter(selenium, filter_name)

    # Convert into text filter
    filter_element_range = get_filter(selenium, filter_name, filter_position=4)
    change_filter_settings(filter_element_range, setting_text='Show as text', filter_position=4)
    filter_element_text = get_filter(selenium, filter_name, filter_position=4)

    # Add value/s & verify footer values: total 4 & 1 after filter
    type_and_select_filter_item(filter_element_text, item_name="2009-01-01")
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(4),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(1)
        })

    # Invert text filter
    dom.click_element(filter_element_text, FILTER_INVERT_BUTTON)

    # Verify that the filter is inverted
    verify_is_visible(filter_element_text, FILTER_INVERT_BUTTON_INVERTED)

    # Verify the footer values, values should be inverted
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(4),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(3)
        })
