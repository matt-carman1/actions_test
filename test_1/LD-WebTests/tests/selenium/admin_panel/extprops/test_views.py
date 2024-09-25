# ==============================================================================
# LEGACY ADMIN PANEL E2E TESTS
# ==============================================================================
# IMPORTANT: These tests are not up to standard with our best practices.
#            Please do not copy the test formats / development styles used here.
#
import pytest
from selenium.webdriver.common.by import By

from library.legacy_admin_panel import AdminSeleniumWebDriverTestCase
from library.url_endpoints import ADMIN_ASYNCDRIVER_URL, OLD_ADMIN_ASYNCDRIVER_URL
from tests.selenium.admin_panel.extprops.utils import ExtpropSeleniumMixin


class ExtpropSeleniumViewTest(ExtpropSeleniumMixin, AdminSeleniumWebDriverTestCase):

    def setUp(self):
        # Always start from the landing page
        self.goto(self.live_server_url)
        if not self.is_logged_in():
            self.login()

    def test_landing(self):
        """
        Test the landing page to make sure we have the correct Site Name
        """
        site_name = self.selenium.find_element(By.ID, 'site-name')
        anchor = site_name.find_element(By.TAG_NAME, 'a')
        self.assertEqual(anchor.text.strip(), 'LiveDesign Admin')

    def test_default_asyncdriver(self):
        """
        Test the fields for one of the default async drivers
        """
        # Open a page that has the standard asyncdriver item
        try:
            path = ADMIN_ASYNCDRIVER_URL + '{model_id}/change/'
            expected_name = self.goto_asyncdriver_id_2(path)
        except Exception as e:
            print(f"An enception occurred: {e}, the tests are running on the old admin panel.")
            path = OLD_ADMIN_ASYNCDRIVER_URL + '{model_id}/change/'
            expected_name = self.goto_asyncdriver_id_2(path)

        name_input = self.selenium.find_element(By.NAME, 'name')
        self.assertEqual(name_input.get_attribute('value'), expected_name)

        job_id_regex = self.selenium.find_element(By.NAME, 'job_id_regex')
        self.assertEqual(job_id_regex.get_attribute('value'), r'^JobId: ([^\s]+)')

        job_status = self.selenium.find_element(By.NAME, 'job_status')
        self.assertEqual(
            job_status.get_attribute('value'),
            r"/mnt/schrodinger/run fake_jobcontrol.py {job_id} -list | tail -1 | tr -s ' ' | cut -d ' ' -f 3 | sed 's/launched\|submitted\|started\|exited/running/ig;s/stranded\|killed\|died\|fizzled/failed/ig'"
        )

    @pytest.mark.skip(reason="SS-31605: Created protocol is incorrect")
    def test_add_protocol(self):
        """  Creates a protocols then verifies the data """
        command = ('/mnt/schrodinger/run '
                   '${Python Main File:FILE-INPUT} '
                   '-i ${SDF-FILE} '
                   '-l ${Password Length:NUMERIC-INPUT} '
                   '-score_file ${Python Score Module:FILE-INPUT} '
                   '-c ${Column:COLUMN-INPUT} '
                   '${Extra CL Args:TEXT-INPUT}')

        data = {
            'name': 'My Protocol',
            'description': 'Testing creation of protocols',
            'projects': ['Global'],
            'commands': [command]
        }
        self.create_protocol(data)
        self.assert_protocol(data)

    @pytest.mark.skip(reason="SS-31607: protocol name is not visible")
    def test_default_protocol(self):
        """
        Test the fields for one of the default protocols
        """
        protocol_name = 'Schrodinger Python'
        self.click_item_with_name('protocol', protocol_name)
        self.wait_until_visible('[name="name"]')
        name_input = self.selenium.find_element(By.NAME, 'name')
        self.assertEqual(name_input.get_attribute('value'), protocol_name)

    @pytest.mark.skip(reason="SS-31606: model name is not visible")
    def test_default_model(self):
        """
        Test the fields for one of the default protocols
        """
        model = {
            'name': 'Ring Count',
            'description': "Calculate Ring Count using Schrodinger's Canvas software",
            'folder': 'Computed Properties/Physicochemical Descriptors',
            'parent': 'canvasMolDescriptors',
            'projects': ['JS Testing'],
            'command_queue': 'Synchronous',
            'command_type': 'Realtime'
        }

        self.click_item_with_name('ldmodel', model['name'])
        self.wait_until_visible('[name="name"]')
        inputs = ['name', 'description', 'folder']
        for input_name in inputs:
            input = self.selenium.find_element(By.NAME, input_name)
            self.assertEqual(input.get_attribute('value'), model[input_name])

        chosen_projects = self.selenium.find_element(By.NAME, 'projects')
        project_names = [opt.text for opt in chosen_projects.find_elements(By.TAG_NAME, 'option')]
        self.assertEqual(project_names, model['projects'])

        selects = ['command_queue', 'command_type']
        for select_name in selects:
            select = self.selenium.find_element(By.NAME, select_name)
            for opt in select.find_elements(By.TAG_NAME, 'option'):
                if opt.get_attribute('selected') == 'selected':
                    self.assertEqual(opt.get_attribute('value'), model[select])

    @pytest.mark.skip(reason="SS-31604: Unexpected html page title")
    def test_realtime_modification(self):
        """
        The 'realtime' option should not be allowed for unprivileged users
        """
        available_options = self.get_command_type_options_for_new_model()
        self.assertIn('realtime', available_options)

        self.logout()
        self.login(username='userB', password='userB')
        available_options = self.get_command_type_options_for_new_model()
        self.assertNotIn('realtime', available_options)

        self.logout()
