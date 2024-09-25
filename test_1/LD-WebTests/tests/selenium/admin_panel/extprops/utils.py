# ==============================================================================
# LEGACY ADMIN PANEL E2E TESTS
# ==============================================================================
# IMPORTANT: These tests are not up to standard with our best practices.
#            Please do not copy the test formats / development styles used here.
#
import re
import logging
import time

from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from library.url_endpoints import ADMIN_PROTOCOL_URL, ADMIN_LDMODEL_URL
from helpers.selection.grid import GRID_HEADER_TOP_CELLS

from library import legacy_admin_panel_utils as utils, dom, wait

# Get an instance of a logger
logger = logging.getLogger(__name__)


def find_inline_section(driver, title):
    """ Finds the inline section based on title """
    fieldsets = driver.find_elements(By.TAG_NAME, 'fieldset')
    for fieldset in fieldsets:
        try:
            headers = fieldset.find_elements(By.TAG_NAME, 'h2')
        except NoSuchElementException:
            headers = []

        for h in headers:
            # User lower since CSS can change anything
            if h.text.strip().lower() == title.lower():
                return fieldset


def find_grid_cells(driver, value, max_count=1):
    """
    Finds the cells in the grid with given value.
    If max count is passed in we will only grab `max_count` occurrences. This
    is a perf issue if you have a grid with tons of cells.
    """
    cells = []
    spans = driver.find_elements(By.CSS_SELECTOR, '.public_fixedDataTableCell_cellContent span')
    for span in spans:
        if span.text == value:
            cells.append(span)
            if len(cells) == max_count:
                break

    return cells


def find_column(driver, model_name, column_name):
    """ Finds the column in the grid """
    header_text = '{0} ({1})'.format(model_name, column_name)

    headers = driver.find_elements(By.CSS_SELECTOR, GRID_HEADER_TOP_CELLS)
    for header in headers:
        if header.text == header_text:
            return header

    return False


def find_button_by_text(driver, text):
    """ Find's a button with text """
    buttons = driver.find_elements(By.TAG_NAME, 'button')
    for button in buttons:
        if button.text == text:
            return button


def find_model_in_tree_by_text(driver, text):
    """ Find's a model with text in the column tree """
    nodes = driver.find_elements(By.CLASS_NAME, 'column-folder-multi-select')
    for node in nodes:
        try:
            if node.text.strip().startswith(text):
                return node
        # This is easy to hit. The tree will render a couple times,
        # even in the middle of this loop.
        except StaleElementReferenceException as err:
            return None


class inline_is_available():
    """ An expectation for checking the inline fieldset is available. """

    def __init__(self, title):
        self.title = title

    def __call__(self, driver):
        success = find_inline_section(driver, self.title)
        return success


class model_is_added_to_grid():
    """ An expectation for checking that the model was added to grid. """

    def __init__(self, model_name, column_name):
        self.model_name = model_name
        self.column_name = column_name

    def __call__(self, driver):
        return find_column(driver, self.model_name, self.column_name)


class value_in_grid():
    """
    An expectation for checking that a value is in the grid. Passing in
    `count` will make sure it's there at least `count` times.
    """

    def __init__(self, value, count=1):
        self.value = value
        self.count = count

    def __call__(self, driver):
        cells = find_grid_cells(driver, self.value, max_count=self.count)
        return len(cells) == self.count


class button_found():
    """
    An expectation for checking that a button with text is present
    """

    def __init__(self, text):
        self.text = text

    def __call__(self, driver):
        return bool(find_button_by_text(driver, self.text))


class model_found_in_tree():
    """
    An expectation for checking that a model is found in the column tree
    """

    def __init__(self, text):
        self.text = text

    def __call__(self, driver):
        return bool(find_model_in_tree_by_text(driver, self.text))


class ExtpropSeleniumMixin():
    """
    Helpers for the extprops selenium tests
    """

    def goto_asyncdriver_id_2(self, path):
        self.goto(path.format(model_id=2))
        expected_name = 'JS Test Async Driver'
        self.wait_until_text('[name="name"]', expected_name)
        return expected_name

    def assert_projects(self, projects):
        """
        Pass in a list of project names to verify they are selected in the form
        """
        chosen_projects = self.selenium.find_element(By.NAME, 'projects')
        project_names = [opt.text for opt in chosen_projects.find_elements(By.TAG_NAME, 'option')]
        self.assertEqual(project_names, projects)

    def assert_commands_exact(self, commands):
        """
        Asserts all commands are present in the form. The commands must be
        present and in order.
        """
        for i, command in enumerate(commands):
            el_name = 'commands-{0}-command'.format(str(i))
            command_field = self.selenium.find_element(By.NAME, el_name)
            self.assertEqual(command_field.get_attribute('value'), command)

    def assert_command_found(self, command):
        """
        Asserts commands are present in the form. It will test for
        the presence of any commands passed in.
        """
        all_commands = []
        command_inputs = self.selenium.find_element(By.CSS_SELECTOR, '.field-command textarea')
        for command_field in command_inputs:
            all_commands.append(command_field.get_attribute('value'))

        self.assertIn(command, all_commands)

    def assert_template_var_found(self, data):
        """
        Asserts "data" is found in a template var's data
        """
        self.wait_until_visible('#template_vars-group')
        all_data = []
        template_vars_group = self.selenium.find_element(By.ID, 'template_vars-group')
        inputs = template_vars_group.find_elements(By.CSS_SELECTOR, '.field-data input')
        for input in inputs:
            all_data.append(input.get_attribute('value'))

        self.assertIn(data, all_data)

    def assert_column_found(self, model_name, column_name):
        """ Asserts that we find the column """
        self.assertIsNot(False, find_column(self.selenium, model_name, column_name))

    def click_item_with_name(self, model, name):
        """
        Will navigate to the model's list url, search by the name passed in,
        then click the link when found. The return value indicates if the link
        was found and clicked.

        """
        path = '/extprops/{0}/?q={1}'.format(model, name.replace(' ', '+'))
        self.goto(path)

        field_selector = 'field-detailed_name' if model == 'parameterized' else 'field-name'
        self.wait_until_visible('.{}'.format(field_selector))
        name_fields = self.selenium.find_elements(By.CLASS_NAME, field_selector)
        for field in name_fields:
            anchor = field.find_element(By.TAG_NAME, 'a')
            if anchor.text == name or (model == 'parameterized' and anchor.text.startswith(name)):
                anchor.click()
                return True

        return False

    def add_project(self, name):
        """ We need this method since after adding the els will be stale """
        add_project_btn = self.selenium.find_element(By.ID, 'id_projects_add_link')
        available_projects = self.selenium.find_element(By.NAME, 'projects_old')
        options = available_projects.find_elements(By.TAG_NAME, 'option')
        for opt in options:
            if opt.text == name:
                opt.click()
                add_project_btn.click()
                return

    def create_protocol(self, data):
        """
        Creates a protocol with the passed in data. Here is the expected data
        format:

          data = {
            'name': 'My Protocol',
            'description': 'Testing creation of protocols',
            'projects': ['Global'],
            'commands': ['Some command']
          }

        """
        self.goto(ADMIN_PROTOCOL_URL + 'add/')
        self.wait_until_visible('[name="name"]')
        inputs = ['name', 'description']
        for input_name in inputs:
            input = self.selenium.find_element(By.NAME, input_name)
            input.send_keys(data[input_name])

        for project in data['projects']:
            self.add_project(project)

        # Add all the empty commands needed for this protocol
        total_commands = len(data['commands'])
        commands_group = self.selenium.find_element(By.ID, 'commands-group')
        if (total_commands > 1):
            add_btn = commands_group.find_element(By.CSS_SELECTOR, '.add-row a')
            for x in range(0, total_commands - 1):
                add_btn.click()

        for i, command in enumerate(data['commands']):
            el_name = 'commands-{0}-command'.format(str(i))
            command_field = self.selenium.find_element(By.NAME, el_name)
            self.selenium.execute_script("arguments[0].innerHTML = '%s';" % command, command_field)

        save_btn = self.selenium.find_element(By.NAME, '_continue')
        self.selenium.execute_script("arguments[0].scrollIntoView();", save_btn)
        save_btn.click()

    def assert_protocol(self, data):
        """
        Asserts that the protocol in the view matches the data passed in. See
        `create_protocol` for the data format.

        """
        # Find the protocol with the given name in the list and navigate to it
        self.click_item_with_name('protocol', data['name'])
        self.wait_until_visible('[name="name"]')
        inputs = ['name', 'description']
        for input_name in inputs:
            input = self.selenium.find_element(By.NAME, input_name)
            self.assertEqual(input.get_attribute('value'), data[input_name])

        self.assert_projects(data['projects'])
        self.assert_commands_exact(data['commands'])

    def create_model(self, data):
        """
        Creates a model with the passed in data. Here is the expected data
        format:

          data = {
            'name': 'My Name',
            'description': 'My Description',
            'folder': 'User Defined/My Folder',
            'parent': <protocol name>,
            'projects': ['Global'],
            'command_queue': 'Synchronous',
            'command_type': 'Realtime',
            'template_vars': [{
              'value': <input value>,
              'field_name': <name of the var>,
              'tag': READONLY
            }],
            'returns': [{
                'name': 'Result',
                'key': 'Result'
            }]
          }

        Note that the files['file_name'] must be in extprops/test/file_uploads/.

        Returns: the id of the model that was created
        """
        self.goto(ADMIN_LDMODEL_URL + 'add/')
        self.wait_until_visible('[name="name"]')
        inputs = ['name', 'description', 'folder']
        for input_name in inputs:
            input = self.selenium.find_element(By.NAME, input_name)
            input.send_keys(data[input_name])

        self.select_parent_option_by_text(data['parent'])

        # Need to continue before filling out the rest
        save_continue_btn = self.selenium.find_element(By.NAME, '_continue')
        save_continue_btn.click()

        # The Model Data section is available only after saving the first time
        self.wait_until(inline_is_available('Model Data'))
        model_data = find_inline_section(self.selenium, 'Model Data')
        template_vars = model_data.find_elements(By.CLASS_NAME, 'dynamic-template_vars')
        url = self.selenium.current_url
        id_search = re.search('.*/ldmodel/([0-9]*)/change/', url)
        if id_search is not None:
            id = id_search.group(1)
        else:
            logger.error('Failed to extract a model id from the URL "{}"'.format(url))
            assert False
        for var in data['template_vars']:
            field_name = var['field_name']
            value = var['value']
            tag_value = var['tag']
            for i, row in enumerate(template_vars):
                name = row.find_element(By.CSS_SELECTOR, '.field-name p')
                if name.text == field_name:
                    el_basename = 'template_vars-{0}'.format(str(i))
                    input = row.find_element(By.NAME, el_basename + '-data')
                    input.send_keys(value)
                    tag = row.find_element(By.NAME, el_basename + '-tag')
                    for opt in tag.find_elements(By.TAG_NAME, 'option'):
                        if opt.get_attribute('value') == tag_value:
                            opt.click()

        # Add all the empty returns needed for this protocol
        total_returns = len(data['returns'])
        returns_group = self.selenium.find_element(By.ID, 'returns-group')
        if (total_returns > 1):
            add_command_btn = returns_group.find_element(By.CSS_SELECTOR, '.add-row a')
            for x in range(0, total_returns - 1):
                add_command_btn.click()

        for i, returns in enumerate(data['returns']):
            return_display = self.selenium.find_element(By.NAME, 'returns-{0}-display_name'.format(str(i)))
            return_display.send_keys(returns['name'])
            return_key = self.selenium.find_element(By.NAME, 'returns-{0}-key'.format(str(i)))
            return_key.send_keys(returns['key'])

        save_btn = self.selenium.find_element(By.NAME, '_continue')
        save_btn.click()
        return id

    def rename_model_returns(self, name_map, model_id):
        """
        updates a model returns, renaming them according to the map
        """
        self.goto(ADMIN_LDMODEL_URL + '{model_id}/change'.format(model_id=model_id))
        self.wait_until_visible('[name="name"]')
        # Add all the empty returns needed for this protocol
        count = self.selenium.find_element(By.NAME, 'returns-TOTAL_FORMS').get_attribute('value')
        for i in range(int(count)):
            return_display = self.selenium.find_element(By.NAME, 'returns-{0}-display_name'.format(str(i)))
            if return_display is None:
                break
            text = return_display.text
            if text not in name_map:
                continue
            new_text = name_map.get(text)
            return_display.clear()
            return_display.send_keys(new_text)

        save_btn = self.selenium.find_element(By.NAME, '_continue')
        save_btn.click()
        return id

    def select_parent_option_by_text(self, text):
        parent_select = self.selenium.find_element(By.NAME, 'parent')
        parent_select.click()
        time.sleep(1)

        parent_opts = parent_select.find_elements(By.TAG_NAME, 'option')
        for opt in parent_opts:
            # We use a regex here b/c the ID is appended to the option name
            match = re.match(r'{0} \(\d+\)'.format(text), opt.text)
            if match:
                ret = opt.click()
                break
        else:
            # we didn't hit the break statement above!
            logger.error('Did not find a match & failed to click anything!')
            assert False  # This should never happen

    def click_model_continue_button(self):
        save_continue_btn = self.selenium.find_element(By.NAME, '_continue')
        save_continue_btn.click()

    def set_input_value(self, input_name, text, make_unique_name=True, separator=' '):
        input_text = utils.make_unique_name(text, separator=separator) if make_unique_name else text
        dom.set_element_value(self.selenium, input_name, input_text)

    def get_command_type_options_for_new_model(self):
        self.goto(ADMIN_LDMODEL_URL + 'add/')
        wait.until_page_title_is(self.selenium, 'Add Model | LiveDesign Admin')

        self.set_input_value('#id_name', 'Test Command Type')
        self.set_input_value('#id_description',
                             'Assert that the realtime command_type is only available for privileged users')

        self.select_parent_option_by_text('JS Test Model Pending')
        self.click_model_continue_button()

        wait.until_page_title_is(self.selenium, 'Change Model | LiveDesign Admin')
        self.wait_until(inline_is_available('Model Execution Options'))

        command_type_select = self.selenium.find_element(By.NAME, 'command_type')
        available_options = [opt.text.lower() for opt in command_type_select.find_elements(By.TAG_NAME, 'option')]

        return available_options
