# ==============================================================================
# LEGACY ADMIN PANEL E2E TESTS
# ==============================================================================
# IMPORTANT: These tests are not up to standard with our best practices.
#            Please do not copy the test formats / development styles used here.
#
import logging
import pytest
import time
from unittest import TestCase
from urllib.parse import urljoin, urlencode

from selenium.common.exceptions import (NoSuchElementException, TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote import remote_connection
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

from library import dom, utils, wait
from library.authentication import login
from library.url_endpoints import (ADMIN_URL, ADMIN_LOGIN_URL, LOGIN_URL)

# NOTE: This is a hack to force the Admin Panel tests to run serially, as a
# workaround for the lack of support for simultaneous sessions being logged in
# Otherwise, all tests will race to negate one another, leaving the last standing
DEFAULT_TIMEOUT = 60


@pytest.mark.usefixtures('selenium_class')
class AdminSeleniumWebDriverTestCase(TestCase):
    live_server_url = ADMIN_URL
    login_url = ADMIN_LOGIN_URL

    # Override to
    webdriver_class = 'selenium.webdriver.chrome.webdriver.WebDriver'

    # Set the default selenium logging level
    selenium_logging_level = logging.WARNING

    def __init__(self, *args, **kwargs):
        # Set the selenium logging level
        remote_connection.LOGGER.setLevel(self.selenium_logging_level)

        super(AdminSeleniumWebDriverTestCase, self).__init__(*args, **kwargs)

    def goto(self, path, domain=None, url_params=None):
        """ Go to a path and then wait for page to load """
        if path.startswith('/'):
            # Strip leading forward slash to ensure path is a RELATIVE url so we
            # may guarantee, or omit, the LD Admin URL_PATH_PREFIX when necessary.
            # ADMIN_URL is the source of truth, and already has /admin if needed.
            path = path[1:]

        if url_params:
            path += "?{querystring}".format(querystring=urlencode(url_params))

        self.selenium.get(urljoin(domain or ADMIN_URL, path))
        self.wait_until_present('body')

    def login_livedesign(self, username='demo', password='demo'):
        """ Logs into the LiveDesign app and waits for the project picker """
        login(self.selenium, username, password)

    def login(self, username='demo', password='demo'):
        """ Helper method to log in """
        self.selenium.get(LOGIN_URL)
        wait.until_page_title_is(self.selenium, 'Log in to LiveDesign')

        dom.set_element_value(self.selenium, 'input[name="username"]', username)
        dom.set_element_value(self.selenium, 'input[name="password"]', password)

        dom.click_element(self.selenium, '#loginButton')
        self.wait(5)
        self.goto(ADMIN_URL)
        wait.until_visible(self.selenium, '.section', text='MODEL AND PROTOCOL CONFIGURATION')

    def logout(self):
        """ Helper method to log out """
        user_tools = self.selenium.find_element(By.ID, 'user-tools')
        user_tools.find_element(By.LINK_TEXT, 'LOG OUT').click()

        wait.until_page_title_is(self.selenium, 'Log in | LiveDesign Admin')

    def is_logged_in(self):
        """
        Determine if we are logged in or not. This is useful in a setUpClass
        or setUp method since we don't need to continually log in.

        FIXME: This is a hack that is needed so we don't continually log in
        for each test since we have a timed wait on the login.
        """
        # Navigate to the main page, if we are logged in we won't be on the
        # login page
        self.selenium.get(ADMIN_URL)
        wait.sleep_if_k8s(3)
        try:
            self.selenium.find_element(By.NAME, 'username')
            self.selenium.find_element(By.NAME, 'password')
            return False
        except NoSuchElementException:
            return True

    def wait(self, timeout):
        """
        Runs a conditional wait that will never resolve, resulting in a simple wait until the timeout expires
        """
        try:
            self.wait_until(lambda selenium: True == False, timeout=timeout)
        except TimeoutException:
            pass

    def wait_until(self, callback, timeout=DEFAULT_TIMEOUT):
        """
        Block testing until condition returned by callback is not false.
        See: selenium.webdriver.support.wait.WebDriverWait
        """
        WebDriverWait(self.selenium, timeout).until(callback)

    def wait_until_not(self, callback, timeout=DEFAULT_TIMEOUT):
        """
        Block testing until condition returned by callback is false.
        See: selenium.webdriver.support.wait.WebDriverWait
        """
        WebDriverWait(self.selenium, timeout).until_not(callback)

    def wait_until_present(self, selector, timeout=DEFAULT_TIMEOUT):
        """
        Helper function that will wait until a selector is found in the DOM
        """
        self.wait_until(ec.visibility_of_element_located((By.CSS_SELECTOR, selector)), timeout)

    def wait_until_visible(self, selector, timeout=DEFAULT_TIMEOUT):
        """
        Helper function that will wait until a selector is found and visible
        """
        self.wait_until(ec.visibility_of_element_located((By.CSS_SELECTOR, selector)), timeout)

    def wait_until_not_visible(self, selector, timeout=DEFAULT_TIMEOUT):
        """ Waits until text is present in given selector """
        self.wait_until_not(ec.visibility_of_element_located((By.CSS_SELECTOR, selector)), timeout)

    def wait_until_text(self, selector, text, timeout=DEFAULT_TIMEOUT):
        """ Waits until text is present in given selector """
        self.wait_until(ec.text_to_be_present_in_element((By.CSS_SELECTOR, selector), text), timeout)

    def get_element(self, selector):
        """ Shorthand for finding an element by CSS Selector """
        return self.selenium.find_element(By.CSS_SELECTOR, selector)(selector)

    def get_elements(self, selector):
        """ Shorthand for finding multiple elements by CSS Selector """
        return self.selenium.find_elements(By.CSS_SELECTOR, selector)

    def select_option_by_text(self, select_selector, option_text):
        """
        Helper to select an option on a select element, with some added robustness against redraws

        :param select_selector: The selector for the select element
        :param option_text: The text of the option to select
        :return:
        """
        select_element = Select(self.get_element(select_selector))
        select_element.select_by_visible_text(option_text)
        time.sleep(.5)
