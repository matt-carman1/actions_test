import pytest

from helpers.selection.filter_actions import FILTER_RANGE_LOWER_AUTO_BUTTON, \
    FILTER_RANGE_UPPER_AUTO_BUTTON, FILTER_RANGE_LOWER_SLIDER, \
    FILTER_RANGE_UPPER_SLIDER
from helpers.change.filter_actions import set_filter_range
from helpers.change.range_actions import set_range_to_auto_or_infinity
from helpers.selection.grid import Footer
from helpers.verification.grid import verify_footer_values
from library import dom, wait, actions
from library.utils import is_k8s


@pytest.mark.xfail(not is_k8s(), reason="SS-40265: RMQ issues in Old Jenkins")
@pytest.mark.smoke
def test_range_filter(selenium, prepare_live_report_filter):
    """
    Test LD range filters.
    We are applying range filters on compounds retrieved by ID
    search on "CHEMBL105*,CHEMBL103*", for AlogP.

    :param selenium: Selenium Webdriver
    :param prepare_live_report_filter: A fixture to prepare LR for filter tests.
    """

    # ----- Test basic range (2 to 5) ----- #
    set_filter_range(selenium, prepare_live_report_filter, filter_position=3, lower_limit=2, upper_limit=5)
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(22),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(12)
        })

    # ----- Test inverted range (4 to 1) ----- #
    # should be automatically corrected to 1 to 4
    set_filter_range(selenium, prepare_live_report_filter, filter_position=3, lower_limit=4, upper_limit=1)
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(22),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(11)
        })

    # ----- Test "Auto" to "Auto" range ----- #
    # "Auto" button appears only when hovering over, but we don't require
    # it to be visible when executing click_element
    set_range_to_auto_or_infinity(selenium, prepare_live_report_filter, FILTER_RANGE_LOWER_AUTO_BUTTON)
    set_range_to_auto_or_infinity(selenium, prepare_live_report_filter, FILTER_RANGE_UPPER_AUTO_BUTTON)
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(22),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(22)
        })

    # ----- Test range sliders ----- #
    right_slider = dom.get_element(prepare_live_report_filter, FILTER_RANGE_UPPER_SLIDER)
    left_slider = dom.get_element(prepare_live_report_filter, FILTER_RANGE_LOWER_SLIDER)
    # drag the lower range slider
    actions.drag_and_drop_by_offset(left_slider, 20, 0)
    wait.until_loading_mask_not_visible(selenium)
    # drag the upper range slider
    actions.drag_and_drop_by_offset(right_slider, -35, 0)
    wait.until_loading_mask_not_visible(selenium)
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(22),
            Footer.ROW_FILTERED_COUNT_KEY: Footer.ROW_FILTERED_COUNT_VALUE.format(20)
        })
