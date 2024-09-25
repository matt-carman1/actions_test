import pytest

from helpers.change.freeform_column_action import create_ffc, edit_ffc_cell
from helpers.change.live_report_menu import delete_open_live_report
from helpers.change.project import open_project
from helpers.flows.grid import hide_columns_contiguously
from helpers.flows.live_report_management import duplicate_livereport
from helpers.selection.live_report_tab import TAB_ACTIVE
from helpers.verification.data_and_columns_tree import verify_no_column_exists_in_column_tree, \
    verify_column_exists_in_column_tree
from helpers.verification.grid import verify_column_contents
from library import utils, wait

live_report_to_duplicate = {'livereport_name': 'Compound', 'livereport_id': '1548'}


@pytest.mark.smoke
@pytest.mark.app_defect(reason="SS-31685")
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures('duplicate_live_report')
def test_ffc_published_columns(selenium):
    """
    Test for Published FFC Columns.
    1. Create published FFC in restricted project
    2. Verification of restricted FFC column not in Global project
    3. Create published FFC in Global project.
    4. Verification of Global FFC column in restricted project
    :param selenium: a fixture that returns Selenium Webdriver
    :return:
    """

    # to avoid duplicate FFC names(as test may run several times in jenkins node), making FFC names unique.
    restricted_ffc_column_name = utils.make_unique_name('Text_published_FFC')

    # ----- Create published FFC in restricted project ----- #
    create_ffc(selenium, column_name=restricted_ffc_column_name, column_type='Text', publish=True)

    # adding values to FFC columns
    restricted_ffc_column_values = ['FFC_Text', '']
    edit_ffc_cell(selenium, restricted_ffc_column_name, 'V055812', restricted_ffc_column_values[0])

    # verification of FFC values
    verify_column_contents(selenium, restricted_ffc_column_name, restricted_ffc_column_values)

    #  ----- Verification of restricted FFC column not in Global project ----- #
    # opening Global project and opening duplicated livereport
    open_project(selenium, project_name='Global')
    lr_name = duplicate_livereport(selenium, livereport_name='Realtime 3D Test')

    # hiding unnecessary columns
    hide_columns_contiguously(selenium, "Lot Scientist", "Rationale")

    # checking restricted FFC column not present in Global project by checking in Freeform Columns section.
    verify_no_column_exists_in_column_tree(selenium, restricted_ffc_column_name)

    # ----- Create unpublished FFC in Global project and make it published ----- #
    # creating published Numeric FFC column
    global_ffc_column_name = utils.make_unique_name('Numeric_FFC')
    create_ffc(selenium, column_name=global_ffc_column_name, column_type='Number', publish=True)

    # # making unpublished FFC to published FFC
    # make_ffc_published(selenium, global_ffc_column_name)

    # adding values to Numeric FFC
    global_ffc_actual_column_values = ['12', '']
    edit_ffc_cell(selenium, global_ffc_column_name, 'V048220', global_ffc_actual_column_values[0])

    # verification of FFC values
    verify_column_contents(selenium,
                           global_ffc_column_name,
                           global_ffc_actual_column_values,
                           match_length_to_expected=True)
    delete_open_live_report(selenium, lr_name)

    # ----- Verification of Global FFC column in restricted project ----- #
    open_project(selenium, project_name='JS Testing')
    wait.until_visible(selenium, TAB_ACTIVE)
    verify_column_exists_in_column_tree(selenium, '(Global) {}'.format(global_ffc_column_name), search_retries=3)
