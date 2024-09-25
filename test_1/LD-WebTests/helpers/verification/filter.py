from helpers.selection.filter_actions import FILTERS_BOX_WIDGET_HEADER_NAME
from library import dom


def verify_added_columns_in_filter_panel(driver, expected_column_names):
    """
    Verify columns which are in visible range in filter panel.

    :param driver: Selenium Webdriver
    :param expected_column_names: list, list of string(s) of expected column names in filter panel
    """

    widget_elems = dom.get_elements(driver, FILTERS_BOX_WIDGET_HEADER_NAME, dont_raise=True)
    column_names = [widget.text for widget in widget_elems]
    assert column_names == expected_column_names, \
        'Actual column names:{}, expected column names:{}'.format(column_names, expected_column_names)
