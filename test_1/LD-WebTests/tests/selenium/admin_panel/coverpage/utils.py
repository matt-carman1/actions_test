# ==============================================================================
# LEGACY ADMIN PANEL E2E TESTS
# ==============================================================================
# IMPORTANT: These tests are not up to standard with our best practices.
#            Please do not copy the test formats / development styles used here.
#
from library.url_endpoints import ADMIN_COVERPAGE_URL


class CoverpageViewHelperMixin(object):
    """
    Helpers for the extprops selenium tests
    """
    summary_prefix = 'live_report_summaries'
    active_row = 0

    def set_active_row(self, row_index):
        """
        Set the active row index so we don't need to pass it into every helper
        """
        self.active_row = row_index

    def get_django_id(self, name, row_index=None):
        """
        Adds the generic django prefix to a given selector
        """
        return '#id_{prefix}-{row_index}-{name}'.format(prefix=self.summary_prefix,
                                                        row_index=row_index or self.active_row,
                                                        name=name)

    def get_project_id_of_coverpage(self):
        """
        Extracts the project id from the url
        """
        # NOTE: Every edit form is for a single coverpage, so the index is always 0
        selector = self.get_django_id('coverpage', 0)
        input_element = self.get_element(selector)
        return input_element.get_attribute('value')

    def create_new_coverpage(self):
        self.goto(ADMIN_COVERPAGE_URL)
        self.get_element('.object-tools .addlink').click()

    def click_dialog_ok(self):
        self.get_element('.ldadmin-dialog-buttons .ldadmin-dialog-submit').click()

    def select_live_report(self, title, row_index=None):
        """
        Set the dropdown value for the livereport at row_index
        """
        selector = self.get_django_id('live_report_id', row_index)
        self.select_option_by_text(selector, option_text=title)

    def click_summary_edit_button(self, row_index=None):
        """
        Click the edit button for a given row_index
        """
        selector = '#{prefix}-{row_index} .show-edit-dialog'.format(prefix=self.summary_prefix,
                                                                    row_index=row_index or self.active_row)
        self.get_element(selector).click()

    def set_summary_field(self, field_name, value, row_index=None):
        """
        Set the `date` value for a live report summary
        """
        selector = self.get_django_id(field_name, row_index)
        self.get_element(selector).send_keys(value)

    def click_save(self):
        """
        Click the save button
        """
        self.get_element('.submit-row input[name="_continue"]').click()

    def click_save_and_continue_editing(self):
        """
        Click the save and continue button
        """
        self.get_element('.submit-row input[name="_continue"]').click()

    def assert_flash_message(self, message):
        """
        Assert the message at the top of the screen shows correctly
        """
        banner = self.get_element('.messagelist')
        self.assertEqual(banner.text, message)

    def remove_all_coverpages(self):
        """
        Teardown task, to prevent test conflicts we must manually remove
        coverpages because we're modifying the live database on every run.

        TODO: use an ephmereal solution, similar to Django's StaticLiveServerTestCase
        """
        self.goto(ADMIN_COVERPAGE_URL)
        self.get_element('.action-checkbox-column').click()
        self.select_option_by_text('select[name="action"]', 'Delete selected Coverpages')
        self.get_element('.actions .button').click()
        self.get_element('input[type="submit"]').click()
