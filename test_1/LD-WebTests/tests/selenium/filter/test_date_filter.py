import pytest

from helpers.change import actions_pane
from helpers.change.filter_actions import add_filter, get_filter, set_filter_range, change_filter_settings, \
    type_and_select_filter_item
from helpers.change.freeform_column_action import edit_ffc_cell
from helpers.selection.filter_actions import FILTER_INVERT_BUTTON, FILTER_RANGE_SLIDER_INVERTED
from helpers.selection.grid import Footer
from helpers.verification.element import verify_is_visible
from helpers.verification.grid import verify_footer_values
from library import dom

live_report_to_duplicate = {'livereport_name': 'FFC - All types, published and unpublished', 'livereport_id': '1299'}


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_date_filter(selenium):
    """
    Adds a date filter for an unpublished Date FFC column and then verifies the number of compounds
    for range type, text type, and inverted filters.

    1. Add filter for a published Date type FFC
    2. For a Range Filter, change the maximum and minimum values on the slider
    3. Verify the number of compounds
    4. Invert the Filter and verify
    5. Switch to Text Filter and select value(s) from the dropdown
    6. Verify the number of compounds
    7. Invert the filter and verify
    :param selenium: Webdriver
    :return:
    """
    # ----- Adding values to the column ----- #
    column_name = 'Date  - unpublished'
    edit_ffc_cell(selenium, column_name, 'CRA-031137', '2016-07-10', is_date=True)
    edit_ffc_cell(selenium, column_name, 'CRA-031437', '2016-07-05', is_date=True)
    edit_ffc_cell(selenium, column_name, 'CRA-031925', '2016-07-01', is_date=True)

    # ----- Inserting the Filter ----- #
    actions_pane.open_filter_panel(selenium)
    # Using "Data  - unpublished" as the column_name (two spaces before the " - ") and "Data - unpublished" as the
    # filter_name (single space before the " - ") as there is discrepancy with the column name that is stored in the db
    # and using the 'scroll_to _column_header' helper renders the attribute value of the column_name for the specific
    # HTML tag and not the inner text content whereas, adding filter_name from column dropdown takes into account the
    # the inner text content(single space before "-"). Uniform naming can be done once the issue is fixed in the
    # starter data.
    filter_name = 'Date - unpublished'
    add_filter(selenium, filter_name)
    # Set upper and lower limits on the slider
    filter_element = get_filter(selenium, filter_name, filter_position=3)
    set_filter_range(selenium, filter_element, filter_position=3, lower_limit='2016-07-05', upper_limit='2016-07-20')
    # Verify footer values: 116 Compounds 3 after filter
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(116),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(3)
        })
    # Invert range filter
    dom.click_element(filter_element, FILTER_INVERT_BUTTON)
    # Verify RC Slider is inverted
    verify_is_visible(filter_element, FILTER_RANGE_SLIDER_INVERTED)
    # Verify footer values: 116 Compounds, 1 after filter
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(116),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(1)
        })

    # ----- Converting to Text Filter ----- #
    change_filter_settings(filter_element, "Show as text", 3)
    filter_element = get_filter(selenium, filter_name, filter_position=3)
    # Select 'undefined' from the dropdown
    type_and_select_filter_item(filter_element, "(undefined)")
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(116),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(112)
        })
    # Invert Text Filter
    dom.click_element(filter_element, FILTER_INVERT_BUTTON)
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(116),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(4)
        })
