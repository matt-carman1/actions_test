import time

from helpers.change.plots import add_rule_nth_child_shape_selection
from helpers.selection.modal import MODAL_OK_BUTTON
from helpers.selection.plots import PLOT_OPTIONS_ADD_RULE, PLOT_OPTION_SHAPE_LAST_CHILD_MIN, \
    PLOT_OPTION_SHAPE_LAST_CHILD_MAX
from helpers.verification.plots import verify_scatter_point_count, verify_scatter_shape_point_count
from library import dom


def add_rule_with_data_and_verify_shape_counts(selenium, data_shape, min_value, max_value, expected_value_count):
    """
    Function to click on add_rule to select ShapesBy and provide values of minimum and maximum

    :param selenium: selenium Webdriver
    :data_shape: shape selection(diamond, square, right-triangle..etc)
    :type data_shape: str
    :min_value: minimum value
    :type min_value: str
    :max_value: maximum value
    :type max_value: str
    :expected_value_count: expected value
    :type expected_value_count: int
    """
    dom.click_element(selenium, PLOT_OPTIONS_ADD_RULE)
    time.sleep(1)
    # Shape selection
    add_rule_nth_child_shape_selection(selenium, data_shape)
    dom.set_element_value(selenium, selector=PLOT_OPTION_SHAPE_LAST_CHILD_MIN, value=min_value)
    dom.set_element_value(selenium, selector=PLOT_OPTION_SHAPE_LAST_CHILD_MAX, value=max_value)
    dom.click_element(selenium, MODAL_OK_BUTTON)
    verify_scatter_point_count(selenium, expected_value_count)
    verify_scatter_shape_point_count(selenium, expected_value_count)
