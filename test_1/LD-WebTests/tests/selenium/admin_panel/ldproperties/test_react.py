# ==============================================================================
# LEGACY ADMIN PANEL E2E TESTS
# ==============================================================================
# IMPORTANT: These tests are not up to standard with our best practices.
#            Please do not copy the test formats / development styles used here.
#
from selenium.webdriver.common.by import By

from library.legacy_admin_panel import AdminSeleniumWebDriverTestCase
from tests.selenium.admin_panel.ldproperties.utils import LDPropertiesReactViewHelperMixin
from library.url_endpoints import ADMIN_LD_PROPERTY_URL
from tests.selenium.admin_panel.ldproperties import selectors
from helpers.verification.element import verify_is_visible
import pytest


class LDPropertiesSeleniumViewTest(LDPropertiesReactViewHelperMixin, AdminSeleniumWebDriverTestCase):
    """
    Tests for the React Property Admin

    TODO: Test coverage for INTERNAL_PROPERTIES.UKNOWN category, which should only be present if
          there are properties that have no category and/or subcategory
    """

    def setUp(self):
        if not self.is_logged_in():
            self.selenium.get(self.live_server_url)
            self.login()

        self.goto(ADMIN_LD_PROPERTY_URL)
        # Always ensure we're on the react version, and properties are loaded
        self.selenium.find_element(By.ID, 'react-root')
        self.wait_until_present('.properties-table > .key')

    def test_logout(self):
        """
        Test logout link, since the header is not provided by Django Admin
        """
        user_tools = self.selenium.find_element(By.ID, 'user-tools')
        user_tools.find_element(By.LINK_TEXT, 'LOG OUT').click()
        self.assertEqual(self.selenium.current_url, self.get_logout_url())

    def test_navigation(self):
        """
        Test navigation tabs route properly
        """
        self.click_tab('Development Flags')
        self.assert_category_title('Development Flags')
        self.assert_active_tab('Development Flags')

        self.click_tab('Configurations')
        self.assert_category_title('Configurations')
        self.assert_active_tab('Configurations')

        self.click_tab('Internal Properties')
        self.assert_category_title('Internal Properties')
        self.assert_active_tab('Internal Properties')

        self.click_tab('Settings')
        self.assert_category_title('Settings')
        self.assert_active_tab('Settings')

    def test_collapsing_headers(self):
        """
        Test collapsing sub categories
        """
        self.assert_category_title('Settings')

        subcategories = self.selenium.find_elements(By.CSS_SELECTOR, '.subcategory.active')
        subcategy_headings = self.selenium.find_elements(By.CSS_SELECTOR, '.subcategory > h2')
        subcategory_descriptions = [el.text.strip() for el in subcategories]
        subcategory_titles = [el.text.strip() for el in subcategy_headings]

        property_tables = self.selenium.find_elements(By.CSS_SELECTOR, '.properties-table')

        self.assertEqual(len(subcategories), len(property_tables))

        for heading in subcategories:
            heading.click()
            self.assertNotIn('active', heading.get_attribute('class'))

            # Nothing other than the heading text should be visible when collapsed
            self.assertIn(heading.text.strip(), subcategory_titles)

            property_tables = self.selenium.find_elements(By.CSS_SELECTOR, '.properties-table')
            self.assertEqual(len(property_tables), len(subcategories) - 1)

            heading.click()
            property_tables = self.selenium.find_elements(By.CSS_SELECTOR, '.properties-table')
            self.assertEqual(len(property_tables), len(subcategories))

            # Heading descriptions (if originally present) should be restored
            self.assertIn(heading.text.strip(), subcategory_descriptions)

    def test_filtering(self):
        """
        Test filtering a property

        TODO: This test is completely reliant on specific values being present in the starter data
        We should find a way to mock the requests to ldproxy.post and return reliable test data
        """
        self.assert_search_input('OBSERVATION_ATTACHMENT_URL_CACHE_EXPIRATION_TIMEOUT_MINUTES', {
            'Settings': 0,
            'Configurations': 1,
            'Development Flags': 0,
            'Internal Properties': 0,
        })

        self.assertEqual(
            self.get_properties_list(), {
                'Configurations': ['OBSERVATION_ATTACHMENT_URL_CACHE_EXPIRATION_TIMEOUT_MINUTES'],
                'Development Flags': [],
                'Internal Properties': [],
                'Settings': []
            })

    def test_clearing_filter(self):
        """
        Test filtering properties

        TODO: This test is completely reliant on specific values being present in the starter data
        We should find a way to mock the requests to ldproxy.post and return reliable test data
        """
        self.assert_search_input('OBSERVATION_ATTACHMENT_URL_CACHE_EXPIRATION_TIMEOUT_MINUTES', {
            'Settings': 0,
            'Configurations': 1,
            'Development Flags': 0,
            'Internal Properties': 0,
        })

        self.clear_search_filter()

        # Clearing the input should reset results
        self.assert_search_tab_counts({
            'Settings': 0,
            'Configurations': 0,
            'Development Flags': 0,
            'Internal Properties': 0,
        })

    def test_filtering_vague_match_tokens(self):
        """
        Test filtering properties

        RULE: A space should match each word individually, with order independence

        TODO: This test is completely reliant on specific values being present in the starter data
        We should find a way to mock the requests to ldproxy.post and return reliable test data
        """
        self.assert_search_input('EXPIRATION ATTACHMENT TIMEOUT OBSERVATION CACHE URL MINUTES', {
            'Settings': 0,
            'Configurations': 1,
            'Development Flags': 0,
            'Internal Properties': 0,
        })

        self.assertEqual(
            self.get_properties_list(), {
                'Configurations': ['OBSERVATION_ATTACHMENT_URL_CACHE_EXPIRATION_TIMEOUT_MINUTES'],
                'Development Flags': [],
                'Internal Properties': [],
                'Settings': []
            })

    def test_filtering_exact_match_tokens(self):
        """
        Test filtering properties

        RULE: Exact phrases should be order dependent
             (note the double quotations in the search filter, and incorrect word ordering)

        TODO: This test is completely reliant on specific values being present in the starter data
        We should find a way to mock the requests to ldproxy.post and return reliable test data
        """
        self.assert_search_input('"EXPIRATION ATTACHMENT TIMEOUT OBSERVATION CACHE URL MINUTES"', {
            'Settings': 0,
            'Configurations': 0,
            'Development Flags': 0,
            'Internal Properties': 0,
        })

        self.assertEqual(self.get_properties_list(), {
            'Configurations': [],
            'Development Flags': [],
            'Internal Properties': [],
            'Settings': []
        })

    def test_filtering_exact_and_vague_match_tokens(self):
        """
        Test filtering properties

        RULE: Combined exact and vague queries should match

        TODO: This test is completely reliant on specific values being present in the starter data
        We should find a way to mock the requests to ldproxy.post and return reliable test data
        """
        self.assert_search_input('EXPIRATION "TIMEOUT MINUTES" CACHE "OBSERVATION ATTACHMENT" URL', {
            'Settings': 0,
            'Configurations': 1,
            'Development Flags': 0,
            'Internal Properties': 0,
        })

        self.assertEqual(
            self.get_properties_list(), {
                'Configurations': ['OBSERVATION_ATTACHMENT_URL_CACHE_EXPIRATION_TIMEOUT_MINUTES'],
                'Development Flags': [],
                'Internal Properties': [],
                'Settings': []
            })

    def test_filtering_with_partial_matches(self):
        """
        Test filtering properties

        RULE: Partial words should match

        TODO: This test is completely reliant on specific values being present in the starter data
        We should find a way to mock the requests to ldproxy.post and return reliable test data
        """
        self.assert_search_input('EXPIR TIME OBSERV ATTACH CACH', {
            'Settings': 0,
            'Configurations': 1,
            'Development Flags': 0,
            'Internal Properties': 0,
        })

        self.assertEqual(
            self.get_properties_list(), {
                'Configurations': ['OBSERVATION_ATTACHMENT_URL_CACHE_EXPIRATION_TIMEOUT_MINUTES'],
                'Development Flags': [],
                'Internal Properties': [],
                'Settings': []
            })

    def test_filtering_case_insensitivity(self):
        """
        Test filtering properties

        RULE: Case should not matter

        TODO: This test is completely reliant on specific values being present in the starter data
        We should find a way to mock the requests to ldproxy.post and return reliable test data
        """
        self.assert_search_input('ObservatION_ATTachment "UrL CacHE" tImEoUt minutes EXPIRATION ', {
            'Settings': 0,
            'Configurations': 1,
            'Development Flags': 0,
            'Internal Properties': 0,
        })

        self.assertEqual(
            self.get_properties_list(), {
                'Configurations': ['OBSERVATION_ATTACHMENT_URL_CACHE_EXPIRATION_TIMEOUT_MINUTES'],
                'Development Flags': [],
                'Internal Properties': [],
                'Settings': []
            })

    def test_filtering_multiple_matches(self):
        """
        Test filtering properties

        RULE: Multiple results should match

        TODO: This test is completely reliant on specific values being present in the starter data
        We should find a way to mock the requests to ldproxy.post and return reliable test data
        """
        self.assert_search_input('bbchem_', {
            'Settings': 8,
            'Configurations': 1,
            'Development Flags': 0,
            'Internal Properties': 4,
        })

    def test_filtering_without_match(self):
        """
        Test filtering properties

        RULE: Invalid queries should not show any results
        """

        self.set_search_filter('iB7pboz1vY23gLfv4m-tb!TJjMGzQ@n6IERaqUhF2OUaRjgDKKQ4XOl-JJVF')
        self.assert_no_results_found()

    # TODO: FIGURE OUT WHAT IS WRONG WITH THIS TEST!
    #       Passes locally, Jenkins says it can't find the match icon during
    #       assert_search_tab_counts. If you print match_icon.screenshot_as_base64
    #       during the test and convert it, you can see the icon does exist..
    #
    # def test_override_filter(self):
    #     """
    #     Test the override filter
    #     """
    #     (overridden, unoverridden) = self.count_overriddens()
    #     overridden_original_counts = overridden
    #
    #     self.assertGreater(sum(overridden.values()), 0)
    #     self.assertGreater(sum(unoverridden.values()), 0)
    #
    #     self.selenium.find_element(By.CSS_SELECTOR, '.override-option').click()
    #     self.wait_until_present(selectors.MATCH_COUNT_ICON)
    #
    #     (overridden, unoverridden) = self.count_overriddens()
    #
    #     self.assertEqual(overridden, overridden_original_counts)
    #     self.assertEqual(unoverridden, {
    #         'Settings': 0,
    #         'Configurations': 0,
    #         'Development Flags': 0,
    #         'Internal Properties': 0,
    #     })
    #
    #     self.assert_search_tab_counts(overridden_original_counts)

    def test_filter_highlighting(self):
        """
        Test filter match highlighting
        """
        self.set_search_filter('true')
        matched_phrases = self.get_matched_phrases()
        self.assertGreater(len(matched_phrases), 0)

        for phrase in matched_phrases:
            self.assertEqual(phrase, 'true')

    def test_filter_highlighting_individual_words(self):
        """
        Test filter with multiple vague match queries highlights individual words
        """
        self.set_search_filter('live report')
        matched_phrases = self.get_matched_phrases()
        self.assertGreater(len(matched_phrases), 0)

        for phrase in matched_phrases:
            self.assertIn(phrase, ['live', 'report'])

    def test_filter_highlighting_exact_matches(self):
        """
        Test filter with exact match matches phrases correctly

        RULE: An exact match containing spaces should optionally match
              underscores, and maintain word order dependence
        """
        self.set_search_filter('"live report"')
        matched_phrases = self.get_matched_phrases()
        self.assertGreater(len(matched_phrases), 0)

        # Ensure underscores and spaces are present
        self.assertIn('live_report', matched_phrases)
        # self.assertIn('live report', matched_phrases)

        # Ensure only the expected phrases are present
        for phrase in matched_phrases:
            self.assertIn(phrase, ['live report', 'live_report'])

    def test_filter_highlighting_with_underscores(self):
        """
        Test filter with exact match matches phrases correctly

        RULE: An underscore should ONLY match underscores
             (ie, the reverse of test_filter_highlighting_exact_matches is not true)
        """
        self.set_search_filter('live_report')
        matched_phrases = self.get_matched_phrases()
        self.assertGreater(len(matched_phrases), 0)

        # Ensure only the expected phrases are present
        for phrase in matched_phrases:
            self.assertEqual(phrase, 'live_report')

    def test_collapsing_property_rows(self):
        """
        Test expanding property rows, and verify they remain open through navigation / filtering
        """
        self.assert_category_title('Settings')

        collapsed_properties = self.selenium.find_elements(By.CSS_SELECTOR, '.property-key.collapsed')[:3]

        open_settings_properties = []
        for property in collapsed_properties:
            property.click()
            self.assertNotIn('collapsed', property.get_attribute('class'))
            open_settings_properties += [property.text.strip()]

        self.click_tab('Configurations')

        collapsed_properties = self.selenium.find_elements(By.CSS_SELECTOR, '.property-key.collapsed')[:5]

        open_configurations_properties = []
        for property in collapsed_properties:
            property.click()
            self.assertNotIn('collapsed', property.get_attribute('class'))
            open_configurations_properties += [property.text.strip()]

        self.click_tab('Settings')
        properties = self.selenium.find_elements(By.CSS_SELECTOR, '.property-key:not(.collapsed)')
        self.assertEqual(sorted(open_settings_properties), sorted([p.text.strip() for p in properties]))

        for property in properties:
            property.click()
            self.assertIn('collapsed', property.get_attribute('class'))

        self.click_tab('Configurations')
        properties = self.selenium.find_elements(By.CSS_SELECTOR, '.property-key:not(.collapsed)')
        self.assertEqual(sorted(open_configurations_properties), sorted([p.text.strip() for p in properties]))

        self.set_search_filter('Q8CzVACoPMLFg@7NEdgD12G!vaOCG~')
        self.assert_no_results_found()
        self.clear_search_filter()

        properties = self.selenium.find_elements(By.CSS_SELECTOR, '.property-key:not(.collapsed)')
        self.assertEqual(sorted(open_configurations_properties), sorted([p.text.strip() for p in properties]))

    @pytest.mark.app_defect(reason="SS-42895: Flaky, fails to locate validation errors")
    def test_edit_property(self):
        """
        Test editing a property value

        NOTE: This test takes adavantage of the fact that all value types are stored as strings and
              does not attempt to set a sane values for any given property.
        """
        property_key = 'BINDING_SITE_STICK_RADIUS'
        initial_value = self.get_property_value(property_key)

        self.click_property_edit_button(property_key)

        self.set_property_value(property_key, 'UNSAVED VALUE')
        self.click_property_cancel_edit_button(property_key)

        self.assertEqual(initial_value, self.get_property_value(property_key))

        # invalid value testing
        self.click_property_edit_button(property_key)
        self.set_property_value(property_key, 'INVALID VALUE')
        self.click_property_save_edit_button(property_key)
        self.assertEqual('INVALID VALUE', self.get_property_textarea_value(property_key))
        self.assert_validation_errors(property_key, ['Could not parse "INVALID VALUE" to float.'])
        self.click_property_cancel_edit_button(property_key)

        # valid value testing
        self.click_property_edit_button(property_key)
        self.set_property_value(property_key, '0.5')
        self.click_property_save_edit_button(property_key)

        self.assertEqual(self.get_property_value(property_key), '0.5')

        # RESTORE INITIAL VALUE AS TEAR DOWN
        self.click_property_edit_button(property_key)
        self.set_property_value(property_key, initial_value)
        self.click_property_save_edit_button(property_key)

    def test_edit_property_form_stays_open(self):
        """
        Test opening an edit form persists through actions like filtering and changing tabs

        NOTE: This test takes adavantage of the fact that all value types are stored as strings and
              does not attempt to set a sane values for any given property.
        """
        property_key = self.choose_a_property_key()

        self.click_property_edit_button(property_key)

        self.set_search_filter('6f*y+nRfFGnSbdwu+8JRJEnK,wNPmn')
        self.assert_no_results_found()
        self.clear_search_filter()

        property = self.selenium.find_element(By.CSS_SELECTOR, '.property-value.editing')
        self.assertEqual(property.get_attribute('data-property-key'), property_key)

        self.click_tab('Development Flags')
        self.wait(0.3)
        self.click_tab('Settings')

        property = self.selenium.find_element(By.CSS_SELECTOR, '.property-value.editing')
        self.assertEqual(property.get_attribute('data-property-key'), property_key)

    @pytest.mark.app_defect(reason="SS-42747, SS-42895: Flaky, fails to locate validation errors")
    def test_edit_property_dialog(self):
        """
        Test editing multiple property values and asserting proper confirmation dialog behavior:

        RULES:
          * Dialog should only be triggered when editing another property, if changes were present
          * Clicking cancel in the dialog should not change any value
          * Clicking ok in the dialog should update the first properties value
          * Dialog should be triggered even through navigation

        NOTE: This test takes adavantage of the fact that all value types are stored as strings and
              does not attempt to set a sane values for any given property.
        """
        float_property_key = 'BINDING_SITE_STICK_RADIUS'
        initial_value = self.get_property_value(float_property_key)

        # Clicking another property without any unsaved changes should not trigger a dialog
        self.click_property_edit_button(float_property_key)
        self.click_tab('Development Flags')
        second_property_key = self.choose_a_property_key()
        self.click_property_edit_button(second_property_key)
        dialogs = self.selenium.find_elements(By.ID, 'confirm-edit-in-progress')
        self.assertEqual(len(dialogs), 0)

        # Clicking to edit another property while this one has changes should display a dialog
        self.click_tab('Settings')
        self.click_property_edit_button(float_property_key)
        self.set_property_value(float_property_key, 'UNSAVED VALUE')
        self.click_tab('Development Flags')
        self.click_property_edit_button(second_property_key)
        self.assert_edit_dialog(float_property_key, 'UNSAVED VALUE')

        # Clicking cancel should not make changes
        self.click_dialog_cancel_button()
        self.click_tab('Settings')
        self.assertEqual(initial_value, self.get_property_value(float_property_key))

        # Clicking ok should throw error for invalid value
        self.click_property_edit_button(float_property_key)
        self.set_property_value(float_property_key, 'INVALID VALUE')
        self.click_tab('Development Flags')
        self.click_property_edit_button(second_property_key)
        self.assert_edit_dialog(float_property_key, 'INVALID VALUE')
        self.click_dialog_ok_button()
        self.assert_validation_errors(float_property_key, ['Could not parse "INVALID VALUE" to float.'])
        self.assertEqual('INVALID VALUE', self.get_property_textarea_value(float_property_key))
        self.click_property_cancel_edit_button(float_property_key)

        # Clicking ok should persist changes for valid value
        self.click_property_edit_button(float_property_key)
        self.set_property_value(float_property_key, '0.5')
        self.click_tab('Development Flags')
        self.click_property_edit_button(second_property_key)
        self.wait_until_visible(selectors.CONFIRM_EDIT_IN_PROGRESS)
        self.assert_edit_dialog(float_property_key, '0.5')
        self.click_dialog_ok_button()
        self.wait_until_not_visible(selectors.CONFIRM_EDIT_IN_PROGRESS)
        self.click_tab('Settings')
        self.assertEqual('0.5', self.get_property_value(float_property_key))

        # RESTORE INITIAL VALUE AS TEAR DOWN
        self.click_property_edit_button(float_property_key)
        self.set_property_value(float_property_key, initial_value)
        self.click_property_save_edit_button(float_property_key)

    def test_tooltip_hover(self):
        """
        Ensure the search tooltip is displayed
        """
        tooltip = self.selenium.find_element(By.CSS_SELECTOR, '.tooltip-hint')
        tooltip_icon = self.selenium.find_element(By.CSS_SELECTOR, '.tooltip i')
        self.assertFalse(tooltip.is_displayed())
        self.hover_over_element(tooltip_icon)
        verify_is_visible(self.selenium, '.tooltip')

    @pytest.mark.app_defect(reason="SS-42895: Flaky, fails to locate property textarea")
    def test_empty_property_validation(self):
        """
        Ensure the search tooltip is displayed
        """
        first_property_key = 'BINDING_SITE_STICK_RADIUS'

        # Clicking another property without any unsaved changes should not trigger a dialog
        self.click_property_edit_button(first_property_key)
        self.set_property_value(first_property_key, '        ')
        self.click_property_save_edit_button(first_property_key)

        self.assert_validation_errors(first_property_key, ['Could not parse " " to float.'])

        self.clear_property_key_value(first_property_key)
        self.click_property_save_edit_button(first_property_key)

        self.wait(0.1)
        self.assert_validation_errors(first_property_key, ['Could not parse "" to float.'])

    def test_edit_property_navigation(self):
        """
        Ensure direct navigation to a url property path
        """
        path = ADMIN_LD_PROPERTY_URL + '{property_key}/change'

        self.click_tab('Development Flags')
        property_key = self.choose_a_property_key(index=2)
        self.goto(path.format(property_key=property_key))
        self.wait(0.1)
        self.assert_property_being_edited(property_key)

        self.click_tab('Configurations')
        property_key = self.choose_a_property_key(index=1)
        self.goto(path.format(property_key=property_key))
        self.wait(0.1)
        self.assert_property_being_edited(property_key)

    def test_restore_default_value(self):
        """
        Test restoring the default value for a property

        NOTE: This test could be super flaky because of SS-28710, since it scrapes
        the default value out of the page content instead of relying on known values.
        SS-28710 causes the default value to not be present after an edit. We attempt
        to mitigate this by only choosing a property key that hasn't been changed.
        """
        property_key = self.choose_a_property_key(unchanged_only=True)
        initial_value = self.get_property_value(property_key)
        default_value = self.get_property_default_value(property_key)

        self.click_property_edit_button(property_key)
        self.set_property_value(property_key, 'Anything')
        self.assertEqual(self.get_property_textarea_value(property_key), 'Anything')

        self.click_property_restore_default_value_button(property_key)
        self.assertEqual(self.get_property_textarea_value(property_key), default_value)

        # RESTORE INITIAL VALUE AS TEAR DOWN
        self.set_property_value(property_key, initial_value)
        self.click_property_save_edit_button(property_key)
