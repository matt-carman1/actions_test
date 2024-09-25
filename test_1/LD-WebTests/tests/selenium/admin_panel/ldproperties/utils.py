# ==============================================================================
# LEGACY ADMIN PANEL E2E TESTS
# ==============================================================================
# IMPORTANT: These tests are not up to standard with our best practices.
#            Please do not copy the test formats / development styles used here.
#
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from library import dom, selenium_jenkins, simulate
from library.url_endpoints import ADMIN_LD_PROPERTY_URL
from library.utils import is_k8s
from tests.selenium.admin_panel.ldproperties import selectors
from urllib.parse import urljoin


class LDPropertiesReactViewHelperMixin(object):
    """
    Helpers for the extprops selenium tests
    """

    def assert_category_title(self, title):
        """
        Verify the provided title is present in the page Category Header & breadcrumb navigation
        """
        category_title = self.selenium.find_element(By.CSS_SELECTOR, selectors.CATEGORY_HEADER)
        breadcrumbs = self.selenium.find_element(By.CSS_SELECTOR, selectors.BREADCRUMBS)

        self.assertEqual(category_title.text.strip(), title)
        self.assertIn(title, breadcrumbs.text.strip())

    def assert_search_input(self, search_value, expected_tab_counts=[]):
        """
        Set a search input, and verify the tab counts
        """
        self.set_search_filter(search_value)
        self.assert_search_tab_counts(expected_tab_counts)

    def set_search_filter(self, search_value):
        """
        Set the search input and wait for 100ms to allow time for the reducers to propagate
        """
        search_field = self.selenium.find_element(By.CSS_SELECTOR, selectors.SEARCH_INPUT)
        search_field.send_keys(search_value)
        self.wait(0.1)

    def clear_search_filter(self):
        """
        Clear the search input and wait for 100ms to allow time for the reducers to propagate
        """
        clear_button = self.selenium.find_element(By.CSS_SELECTOR, selectors.SEARCH_INPUT_CLEAR_BUTTON)
        clear_button.click()
        self.wait(0.1)  # Allow the redux selector time to propagate

    def assert_search_tab_counts(self, expected_tab_counts=[]):
        """
        Collects the match count for each tab, and asserts they match our expectation
        """
        for tab in self.selenium.find_elements(By.CSS_SELECTOR, selectors.CATEGORY_NAVIGATION_TABS):
            tab_category = tab.find_element(By.CSS_SELECTOR, selectors.CATEGORY).text.strip()

            try:
                tab_count = int(tab.find_element(By.CSS_SELECTOR, selectors.MATCH_COUNT_ICON).text.strip())
            except NoSuchElementException:
                tab_count = 0

            self.assertEqual(tab_count, expected_tab_counts[tab_category],
                             "{cat} tab has incorrect match count icon".format(cat=tab_category))

    def count_overriddens(self):
        """
        Crawls through each tab and collects the number of properties that are
        marked overridden / not overridden
        """
        overridden = {}
        unoverridden = {}

        for tab in self.selenium.find_elements(By.CSS_SELECTOR, selectors.CATEGORY_NAVIGATION_TABS):
            tab.click()
            category = self.selenium.find_element(By.CSS_SELECTOR, selectors.CATEGORY_HEADER).text.strip()
            overridden[category] = len(self.selenium.find_elements(By.CSS_SELECTOR, selectors.OVERRIDE_ACTIVE))
            unoverridden[category] = len(self.selenium.find_elements(By.CSS_SELECTOR, selectors.OVERRIDE_INACTIVE))

        return (overridden, unoverridden)

    def get_matched_phrases(self):
        """
        Crawls through each tab and collects the highlighted texts
        """
        matched_phrases = []
        for tab in self.selenium.find_elements(By.CSS_SELECTOR, selectors.CATEGORY_NAVIGATION_TABS):
            tab.click()
            highlighted_elements = self.selenium.find_elements(By.CSS_SELECTOR, selectors.HIGHLIGHT)
            matched_phrases += [h.text.strip().lower() for h in highlighted_elements if h.is_displayed()]

        return matched_phrases

    def click_tab(self, name):
        """
        Clicks on the category tab matching `name`
        Scrolls the page to the top so the tab will be on screen
        """
        content_elem = dom.get_element(self.selenium, 'body')
        ActionChains(self.selenium).move_to_element(content_elem).click().send_keys(Keys.HOME).perform()
        dom.click_element(self.selenium, f'{selectors.CATEGORY_NAVIGATION_TABS} {selectors.CATEGORY}', text=name)

    def assert_active_tab(self, name):
        """
        Assert that the given tab is active
        """
        active_tabs = self.selenium.find_elements(By.CSS_SELECTOR, selectors.ACTIVE_CATEGORY_NAVIGATION_TAB)
        active_tab_names = [t.text.strip() for t in active_tabs]
        self.assertEqual(active_tab_names, [name])

    def get_properties_list(self):
        """
        Gets a list of all the visible properties on a given tab. Useful for asserting filters.
        """
        results = {}
        for tab in self.selenium.find_elements(By.CSS_SELECTOR, selectors.CATEGORY_NAVIGATION_TABS):
            tab.click()
            category = tab.find_element(By.CSS_SELECTOR, selectors.CATEGORY).text.strip()
            properties = self.selenium.find_elements(By.CSS_SELECTOR, selectors.PROPERTY_KEY)
            results[category] = [prop.text.strip() for prop in properties]

        return results

    def assert_no_results_found(self):
        """
        Assert that the property table reads "No Properties Found."
        """
        tables = self.selenium.find_elements(By.CSS_SELECTOR, selectors.PROPERTIES_TABLE)

        results = [t.text.strip() for t in tables]
        for result in results:
            self.assertEqual(result, 'No Properties Found.')

    def get_element_by_property_key(self, property_key, element):
        """
        Shortcut selector for accessing a PropertyCell, since we rely on data-property-key
        """
        selector = selectors.PROPERTY_ELEMENT.format(element=element, property_key=property_key)
        return self.selenium.find_element(By.CSS_SELECTOR, selector)

    def click_property_edit_button(self, property_key):
        """
        Opens an edit form for a given property key
        """
        edit_selector = selectors.PROPERTY_VALUE_ROW.format(property_key=property_key)
        value_selector = selectors.PROPERTY_VALUE_BY_KEY.format(property_key=property_key)

        value_element = dom.get_element(self.selenium, value_selector)
        simulate.hover(self.selenium, value_element)
        dom.click_element(self.selenium, edit_selector)

        expected_url = '{domain}{path}{key}/change/'.format(domain=self.live_server_url,
                                                            path=ADMIN_LD_PROPERTY_URL,
                                                            key=property_key)
        self.assertEqual(self.selenium.current_url, expected_url)
        self.assert_property_being_edited(property_key)

    def set_property_value(self, property_key, value):
        """
        Enters text into an OPEN EDIT FORM for a property
        """
        selector = selectors.PROPERTY_VALUE_TEXTAREA.format(property_key=property_key)
        dom.set_element_value(self.selenium, selector, value)

    def click_property_save_edit_button(self, property_key):
        """
        Click the save button on an OPEN EDIT FORM for a property
        """
        selector = selectors.PROPERTY_VALUE_SAVE_BUTTON.format(property_key=property_key)
        dom.click_element(self.selenium, selector)
        self.wait(0.1)

    def click_property_cancel_edit_button(self, property_key):
        """
        Click the cancel button on an OPEN EDIT FORM for a property
        """
        selector = selectors.PROPERTY_VALUE_CANCEL_BUTTON.format(property_key=property_key)
        self.selenium.find_element(By.CSS_SELECTOR, selector).click()

    def click_property_restore_default_value_button(self, property_key):
        """
        Click the restore default button on an OPEN EDIT FORM for a property
        """
        property = self.get_element_by_property_key(property_key, selectors.PROPERTY_VALUE)
        property.find_element(By.CSS_SELECTOR, selectors.DEFAULT_VALUE_SPAN).click()

    def assert_property_being_edited(self, property_key):
        """
        Verifies the active property being edited is the one we expect
        """
        property = dom.get_element(self.selenium, selectors.PROPERTY_VALUE_EDITING)
        self.assertEqual(property.get_attribute('data-property-key'), property_key)

    def choose_a_property_key(self, index=0, unchanged_only=False):
        """
        Returns a property key from the page to work with

        :param index: select a specific property by index
        :param unchanged_only: only return properties that haven't been overridden
        """
        properties = self.selenium.find_elements(By.CSS_SELECTOR, selectors.OVERRIDE_COLLAPSED)
        self.assertTrue(0 <= abs(index) < len(properties))

        if unchanged_only:
            properties = [p for p in properties if not p.find_elements(By.CSS_SELECTOR, '.fa-circle.active')]

        return properties[index].get_attribute('data-property-key')

    def get_property_value(self, property_key):
        """
        Gets the value for a given property key
        """
        property = self.get_element_by_property_key(property_key, selectors.PROPERTY_VALUE)
        return property.find_element(By.CSS_SELECTOR, '.value').text.strip()

    def get_property_textarea_value(self, property_key):
        """
        Gets the value for a given property key
        """
        selector = selectors.PROPERTY_VALUE_TEXTAREA.format(property_key=property_key)
        property = self.selenium.find_element(By.CSS_SELECTOR, selector)
        return property.text.strip()

    def get_property_default_value(self, property_key):
        """
        Gets the value for a given property key
        """
        self.expand_property_row(property_key)
        property = self.get_element_by_property_key(property_key, selectors.PROPERTY_VALUE)
        return property.find_element(By.CSS_SELECTOR, selectors.DEFAULT_VALUE_SPAN).text.strip()

    def expand_property_row(self, property_key):
        """
        Expands a collapsed property row
        """
        property = self.get_element_by_property_key(property_key, selectors.KEY)
        self.assertTrue('collapsed' in property.get_attribute('class'))

        property.find_element(By.CSS_SELECTOR, selectors.PROPERTY_KEY).click()

    def assert_edit_dialog(self, property_key, property_value):
        """
        Asserts the property edit dialog is displayed, showing the given property key / value
        """
        dialog = self.selenium.find_element(By.CSS_SELECTOR, selectors.CONFIRM_EDIT_IN_PROGRESS)
        dialog_property_key = dialog.find_element(By.CSS_SELECTOR, selectors.PROPERTY_KEY).text.strip()
        dialog_property_value = dialog.find_element(By.CSS_SELECTOR, selectors.NEW_VALUE).text.strip()

        self.assertEqual(dialog_property_key, property_key)
        self.assertEqual(dialog_property_value, property_value)

    def click_dialog_ok_button(self):
        """
        Click the dialog ok button
        """
        self.selenium.find_element(By.CSS_SELECTOR, selectors.DIALOG_CONFIRM).click()
        self.wait(0.1)

    def click_dialog_cancel_button(self):
        """
        Click the dialog cancel button
        """
        self.selenium.find_element(By.CSS_SELECTOR, selectors.DIALOG_CANCEL).click()
        self.wait(0.1)

    def hover_over_element(self, element):
        hover = ActionChains(self.selenium).move_to_element(element)
        hover.perform()

    def assert_validation_errors(self, property_key, expected_errors):
        """
        Assert that validation errors are present for the given property key
        """
        selector = selectors.PROPERTY_VALUE_VALIDATION_ERROR.format(property_key=property_key)
        actual_errors = dom.get_elements(self.selenium, selector)

        self.assertEqual(len(expected_errors), len(actual_errors))
        for error_element in actual_errors:
            self.assertIn(error_element.text, expected_errors)

    def clear_property_key_value(self, property_key):
        """
        Clear the text in a property key
        """
        selector = selectors.PROPERTY_VALUE_TEXTAREA.format(property_key=property_key)
        element = dom.set_element_value(self.selenium, selector, '')

    def get_logout_url(self):
        HOST = os.getenv('NODE_NAME', '').strip()
        if HOST and not is_k8s():
            print('Getting jenkins node running the build')
            HOST = 'http://' + HOST + ':8080/'
        else:
            HOST = os.getenv('LD_SERVER', '').strip()
            if HOST:
                if not HOST.startswith('http'):
                    raise ValueError(
                        'LD_SERVER must include protocol, i.e. it should start with http:// for local developer '
                        'environments and nodes on jenkins server, and spinner machines (hopefully also everything '
                        'else) are https://')
                print('Using HOST from LD_SERVER env param')
            else:
                print('Getting HOST from Jenkins...')
                HOST = selenium_jenkins.get_host()
                print('')
        return urljoin(HOST, 'livedesign/static/login.html')
