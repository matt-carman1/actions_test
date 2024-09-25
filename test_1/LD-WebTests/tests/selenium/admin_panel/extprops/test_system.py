# ==============================================================================
# LEGACY ADMIN PANEL E2E TESTS
# ==============================================================================
# IMPORTANT: These tests are not up to standard with our best practices.
#            Please do not copy the test formats / development styles used here.
#
import re
import time
import uuid

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from helpers.change.live_report_picker import create_and_open_live_report
from helpers.change.project import open_project
from helpers.extraction import paths
from library.legacy_admin_panel import AdminSeleniumWebDriverTestCase
from library.url_endpoints import HOST
from tests.selenium.admin_panel.extprops.utils import (
    find_grid_cells,
    model_found_in_tree,
    find_model_in_tree_by_text,
    model_is_added_to_grid,
    value_in_grid,
    ExtpropSeleniumMixin,
)


class ExtpropSeleniumSystemTest(ExtpropSeleniumMixin, AdminSeleniumWebDriverTestCase):

    def setUp(self):
        # Always start from the landing page
        self.selenium.get(self.live_server_url)
        if not self.is_logged_in():
            self.login()

    def create_livereport(self, name):
        """ Creates a new LiveReport with the name passed in """
        open_project(self.selenium, project_name='JS Testing')
        create_and_open_live_report(self.selenium, report_name=name)

        # For some reason we are seeing a couple renders after creating a
        # LiveReport. Without this we could find the next elements we need
        # but it will inevitably render again and any clicks will be lost.
        time.sleep(2)
        url = self.selenium.current_url
        lrid_search = re.search('.*/4/livereports/([0-9]*)', url)
        if lrid_search is not None:
            return lrid_search.group(1)

    def navigate_livereport(self, lrid):
        """ Navigates to an existing live report by live report id """
        self.selenium.get('{}livedesign/#/projects/4/livereports/{}'.format(HOST, lrid))
        self.wait_until_visible('[class="tab tab-default tab-active"]')

    def add_compound(self, id):
        """ Adds a compound with the given ID to a LiveReport """

        self.wait_until_visible('#add-compound-button')
        self.selenium.find_element(By.ID, 'add-compound-button').click()
        self.wait_until_visible('#compounds-pane-container')

        # switch to Search tab and choose to search by ID
        self.selenium.find_element(By.CSS_SELECTOR, '#compounds-pane-container .tab-link[data-name="Search"]').click()
        self.wait_until_visible('#compounds-pane-container .active-tab-link[data-name="Search"]')
        self.selenium.find_element(By.CSS_SELECTOR,
                                   '#compounds-pane-container .sub-tab[data-type="CORPORATE_ID_SEARCH"]').click()
        self.wait_until_visible('#compounds-pane-container .sub-tab.active[data-type="CORPORATE_ID_SEARCH"]')

        text_input = self.selenium.find_element(By.CSS_SELECTOR, '#compounds-pane-container .search-textarea')
        text_input.send_keys(id)

        time.sleep(1)
        self.selenium.find_element(By.CSS_SELECTOR, '#compounds-pane-container .search-compounds').click()

    def add_model(self, model_name):
        """
        Adds a model with passed in model_name to the LiveReport. Returns
        a bool whether model was found or not.

        """
        self.selenium.find_element(By.ID, 'add-data-button').click()

        self.wait_until_visible('.column-tree-wrapper .search-input')
        column_tree = self.selenium.find_element(By.CSS_SELECTOR, 'column-tree-wrapper')
        search_input = column_tree.find_element(By.CLASS_NAME, 'search-input')
        search_input.send_keys(model_name)

        for _ in range(5):
            self.wait_until(model_found_in_tree(model_name))
            node = find_model_in_tree_by_text(self.selenium, model_name)
            if node is None:
                # it's expected find_model_in_tree_by_text will sometimes return None,
                # so we'll keep trying...
                continue

            node.click()
            add_button = self.selenium.find_element(By.CSS_SELECTOR,
                                                    '.column-tree-wrapper button.add-button-multi-select')
            add_button.click()
            return

        assert False  # find_model_in_tree_by_text returned None too many times :-(

    @pytest.mark.skip(reason="SS-31603: fails to create model")
    def test_add_model(self):
        """
        1) Create a new model that just returns the corporate ID
        2) Login to LiveDesign
        3) Create a new LiveReport
        4) Add a single compound
        5) Add the newly created model
        6) Verify that TE returns the corporate ID

        """
        model_name = str(uuid.uuid1())
        corporate_id = 'CRA-035001'
        file_path = paths.get_resource_path('example.py')
        model = {
            'name': model_name,
            'description': "Testing a model E2E",
            'folder': 'Testing',
            'parent': 'Schrodinger Python',
            'projects': ['Global'],
            'command_queue': 'Synchronous',
            'command_type': 'Realtime',
            'template_vars': [{
                'value': file_path,
                'field_name': 'python_script',
                'tag': 'READ_ONLY'
            }],
            'returns': [{
                'name': 'Result',
                'key': 'Result'
            }]
        }
        self.create_model(model)
        self.login_livedesign()
        self.create_livereport('Model System Test')
        self.add_compound(corporate_id)
        self.add_model(model_name)
        # Timeout if the column isn't added to the grid
        for return_data in model['returns']:
            self.wait_until(model_is_added_to_grid(model_name, return_data['name']))
            self.assert_column_found(model_name, return_data['name'])
        self.wait_until(value_in_grid(corporate_id, 2))
        self.assertEquals(2, len(find_grid_cells(self.selenium, corporate_id, 2)),
                          'There should be a corp ID for the new model and for the ID Column')

    @pytest.mark.skip(reason="SS-31603: fails to create model")
    def test_rename_model(self):
        """
        1) Create a new model that just returns the corporate ID
        2) Login to LiveDesign
        3) Create a new LiveReport
        4) Add a single compound
        5) Add the newly created model
        6) rename model return
        7) check to see if the column got changed in the LR

        """
        model_name = str(uuid.uuid1())
        corporate_id = 'CRA-035001'
        file_path = paths.get_resource_path('example.py')
        model = {
            'name': model_name,
            'description': "Testing renaming a model E2E",
            'folder': 'Testing',
            'parent': 'Schrodinger Python',
            'projects': ['Global'],
            'command_queue': 'Synchronous',
            'command_type': 'Realtime',
            'template_vars': [{
                'value': file_path,
                'field_name': 'python_script',
                'tag': 'READ_ONLY'
            }],
            'returns': [{
                'name': 'Result',
                'key': 'Result'
            }]
        }
        model_id = self.create_model(model)
        self.login_livedesign()
        lrid = self.create_livereport('Model System Test')
        self.add_compound(corporate_id)
        time.sleep(2)
        self.add_model(model_name)

        # Timeout if the column isn't added to the grid
        for return_data in model['returns']:
            self.wait_until(model_is_added_to_grid(model_name, return_data['name']))
            self.assert_column_found(model_name, return_data['name'])

        self.wait_until(value_in_grid(corporate_id, 2))
        self.assertEquals(2, len(find_grid_cells(self.selenium, corporate_id, 2)),
                          'There should be a corp ID for the new model and for the ID Column')
        self.rename_model_returns({'Result': 'Other Result'}, model_id)
        self.navigate_livereport(lrid)
        self.assert_column_found(model_name, 'Other Result')

    @pytest.mark.skip(reason="SS-31603: fails to create model")
    def test_parameterized(self):
        """
        Creates a protocol, model and parameterized model, then verifies
        the data
        """
        protocol_name = str(uuid.uuid1())
        command = ('/mnt/schrodinger/run '
                   '${Python Main File:FILE-INPUT} '
                   '-i ${SDF-FILE} '
                   '-result ${Result:TEXT-INPUT}')

        data = {
            'name': protocol_name,
            'description': 'Testing full parameterized',
            'projects': ['Global'],
            'commands': [command]
        }
        self.create_protocol(data)

        model_name = str(uuid.uuid1())
        parameterized_model_name = 'Copy of ' + model_name
        corporate_id = 'CRA-035001'
        file_path = paths.get_resource_path('parameterized_example.py')
        model = {
            'name': model_name,
            'description': 'Testing a model E2E',
            'folder': 'Testing',
            'parent': protocol_name,
            'projects': ['Global'],
            'command_queue': 'Synchronous',
            'command_type': 'Realtime',
            'template_vars': [{
                'value': file_path,
                'field_name': 'Python Main File',
                'tag': 'READ_ONLY'
            }],
            'returns': [{
                'name': 'Result',
                'key': 'Result'
            }]
        }
        self.create_model(model)
        self.login_livedesign()
        self.create_livereport('Parameterized Model System Test')
        self.add_compound(corporate_id)
        self.add_model(model_name)

        # Parameterized models make a BE call to populate the form. This happens
        # after the form is open.
        # TODO (williams): Move this over to an expectation
        time.sleep(3)

        # In LiveDesign the parameterized model dialog should show up now.
        # Add the result we want to see. The python script used here just
        # returns (the TE result) whatever you add in the form field.
        expected_result = str(uuid.uuid1())
        self.wait_until_visible('.bb-dialog-bottom .ok-button')
        dialog_rows = self.selenium.find_elements(By.CSS_SELECTOR, '.form-row')
        for row in dialog_rows:
            label = row.find_element(By.TAG_NAME, 'label')

            if label.text == 'Name:':
                input = row.find_element(By.TAG_NAME, 'input')
                input.send_keys(parameterized_model_name)

            if label.text == 'Result':
                textarea = row.find_element(By.TAG_NAME, 'textarea')
                textarea.send_keys(expected_result)

        ok_btn = self.selenium.find_element(By.CSS_SELECTOR, '.bb-dialog-bottom .ok-button')
        ok_btn.click()

        # Timeout if the column isn't added to the grid
        for return_data in model['returns']:
            self.wait_until(model_is_added_to_grid(parameterized_model_name, return_data['name']))

        try:
            self.wait_until(value_in_grid(expected_result), timeout=30)
        except TimeoutException as err:
            raise err

        self.assertEquals(1, len(find_grid_cells(self.selenium, expected_result)),
                          'There should be a single cell in the grid with the UUID')

        # Now go back to the admin site and verify the data is correct
        self.click_item_with_name('parameterized', parameterized_model_name)
        self.assert_template_var_found(expected_result)
