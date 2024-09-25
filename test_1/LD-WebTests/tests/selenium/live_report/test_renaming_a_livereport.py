import pytest

from helpers.change.live_report_menu import rename_a_live_report
from helpers.verification.live_report_picker import verify_live_report_not_present, verify_live_report_present, \
    verify_live_report_tab_present
from helpers.verification.features_enabled_disabled import verify_live_report_menu_option_is_disabled
from helpers.change.project import open_project
from helpers.change.live_report_picker import open_live_report, close_metapicker
from library.authentication import logout, login


@pytest.mark.app_defect(reason="SS-37116")
def test_renaming_a_livereport(selenium, new_live_report, open_livereport):
    """
    Test Renaming a LR:
    1. Login with admin user (demo user)
    2. Rename the LR and verify the same.
    3. Logout and login with non-admin user.
    4. Try renaming the LR created initially (Only owner or Admin should be able to rename the LR.)
    :return:
    """

    initial_live_report_name = new_live_report

    lr_new_name = '{}-Avant-garde'.format(initial_live_report_name)

    # Renaming the LiveReport
    rename_a_live_report(selenium, live_report_name=initial_live_report_name, new_name_for_live_report=lr_new_name)

    # Verify LR tab with the new name is present
    verify_live_report_tab_present(selenium, lr_new_name)

    # Verifying that the LiveReport with the initial name is not found in the metapicker after renaming
    verify_live_report_not_present(selenium, live_report_name=initial_live_report_name)

    # Verifying that the LiveReport with the new name is found in the metapicker after renaming
    verify_live_report_present(selenium, live_report_name=lr_new_name)

    close_metapicker(selenium)

    logout(selenium)

    # Login with a non-admin user
    login(selenium, uname='userB', pword='userB')
    open_project(selenium)
    open_live_report(selenium, name=lr_new_name)

    # Check that the 'Rename…' option is disabled
    verify_live_report_menu_option_is_disabled(selenium,
                                               lr_new_name,
                                               'Rename…',
                                               dialog_header_text='Rename Live'
                                               'Report')

    logout(selenium)

    # Login with a different Admin user
    login(selenium, uname='seurat', pword='seurat')
    open_project(selenium)
    open_live_report(selenium, name=lr_new_name)

    # Renaming the LiveReport back to the inital name
    rename_a_live_report(selenium, live_report_name=lr_new_name, new_name_for_live_report=initial_live_report_name)

    # Verify LR tab with the changed name is present
    verify_live_report_tab_present(selenium, initial_live_report_name)
