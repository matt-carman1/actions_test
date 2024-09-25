from collections import Counter
from helpers.extraction.forms import get_list_widget_data
from helpers.selection.forms import TAB_TITLE
from library import dom
from library.eventually import eventually_equal


def verify_list_widget_contents(driver_or_container_element, expected_content):
    """
    Verifies content in a List container matches the provided expected_content

    :param driver_or_container_element: webdriver or container element object
    :param expected_content: dict[name: str] = value: str, dictionary with column name (key) & the content shown (value)
    """

    def get_actual_contents(driver):
        return get_list_widget_data(driver_or_container_element)

    assert eventually_equal(driver_or_container_element, get_actual_contents,
                            expected_content), 'List Tile did not have expected contents `{}`'.format(expected_content)


def verify_forms_tabs_exist(driver, *tab_names):
    """
    Confirms whether the provided *tab_names all exist in the forms view loaded.

    :param driver: webdriver
    :param tab_names: str, names of tabs expected to exist
    """
    # Variable for the assert message at end of helper, indicating which of the expected *tabs_names are missing
    missing_tabs = {}
    # Create a dict to containing the count of each *tab_names provided
    # Used a dict to more efficiently track multiple tabs with the same name
    expected_tabs = Counter(tab_names)

    def check_tabs(driver):
        """
        Returns False if all/some tab names are missing from the layout, else True
        """
        # Return True if no tabs are expected
        if not expected_tabs:
            return True

        # Grab all the tab names loaded and store as a dict, actual_tabs
        actual_tabs = Counter([elem.text for elem in dom.get_elements(driver, TAB_TITLE)])

        nonlocal missing_tabs
        missing_tabs = expected_tabs - actual_tabs

        # missing_tabs should be empty if all the tabs expected were found from the dom
        return False if missing_tabs else True

    assert eventually_equal(driver, check_tabs,
                            True), "Forms view is missing tab names by count:\n{}".format(missing_tabs)
