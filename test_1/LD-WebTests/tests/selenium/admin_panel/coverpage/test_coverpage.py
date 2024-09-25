# ==============================================================================
# LEGACY ADMIN PANEL E2E TESTS
# ==============================================================================
# IMPORTANT: These tests are not up to standard with our best practices.
#            Please do not copy the test formats / development styles used here.

#
# TODO: SS-29087
#

# class CoverpageSeleniumTest(CoverpageViewHelperMixin, AdminSeleniumWebDriverTestCase):
#     """
#     Tests for the Coverpage
#     """
#     def setUp(self):
#         if not self.is_logged_in():
#             self.goto(self.live_server_url)
#             self.login()

#     def tearDown(self):
#         self.remove_all_coverpages()

#     def test_empty_image(self):
#         """
#         Test that a summary created without an image does not render a thumbnail
#         """
#         self.create_new_coverpage()
#         # TODO: This should probably be considered a bug
#         self.wait(0.3)
#         self.click_dialog_ok()
#         self.select_option_by_text('#id_project_id', 'Project A')

#         self.select_live_report('Two Scaffolds')
#         self.click_summary_edit_button()
#         self.set_summary_field('date', '2019-01-01')
#         self.set_summary_field('designer', 'Susan')
#         self.set_summary_field('modeler', 'Sarah')

#         self.click_save_and_continue_editing()
#         self.assert_flash_message('The Coverpage for "Project A" was added successfully. You may edit it again below.')

#         project_id = self.get_project_id_of_coverpage()
#         self.goto(ADMIN_COVERPAGE_URL + project_id)

#         thumbnails = self.get_elements('.tile .thumbnail')
#         self.assertEqual(0, len(thumbnails))
