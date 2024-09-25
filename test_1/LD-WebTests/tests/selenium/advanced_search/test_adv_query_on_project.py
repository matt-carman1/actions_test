import pytest

from helpers.change.actions_pane import open_advanced_search, open_add_compounds_panel
from helpers.change.advanced_search_actions import add_query, get_query, set_query_range
from helpers.change.live_report_menu import delete_open_live_report
from helpers.change.live_report_picker import create_and_open_live_report
from helpers.change.project import open_project
from helpers.selection.advanced_search import PROJECT_LINK, SEARCH_AND_ADD_COMPOUNDS_BUTTON, \
    ADV_PROJECT_QUERY_DROPDOWN, ADV_PROJECT_QUERY_DROPDOWN_ELEMS
from helpers.selection.grid import Footer
from helpers.verification.grid import verify_footer_values, verify_column_contents, check_for_butterbar
from library import dom


@pytest.mark.usefixtures('open_livereport')
@pytest.mark.usefixtures('new_live_report')
def test_adv_query_on_project(selenium):
    """
    Test for create advanced search on project query for restricted and unrestricted projects

    1. Advanced search with unrestricted project on restricted Project.
    2. Advanced search with Global project on Unrestricted Project.

    :param selenium: Selenium webdriver
    """
    # open advanced search panel
    open_add_compounds_panel(selenium)
    open_advanced_search(selenium)

    # ----- Advanced search with Restricted project on non restricted project ----- #
    # add project query using bottom link in adv query panel
    add_query(selenium, query_name=PROJECT_LINK, text_search=False)

    # opening project query dropdown
    dom.click_element(selenium, ADV_PROJECT_QUERY_DROPDOWN, 'Choose Project')

    # Verifying unrestricted projects and selected restricted project available in the dropdown
    project_elems = dom.get_elements(selenium, ADV_PROJECT_QUERY_DROPDOWN_ELEMS)
    project_names = [elem.text for elem in project_elems]
    expected_project_names = ['CMET', 'Global', 'JS Testing', 'Project A', 'Project B']
    assert expected_project_names == project_names, "Project names are not matched with expected."

    # Select unrestricted project from Project query dropdown
    dom.click_element(selenium, ADV_PROJECT_QUERY_DROPDOWN_ELEMS, 'Project A')
    # search CB-RAMOS-CA-FLUX (IC50)
    add_query(selenium, 'CB-RAMOS-CA-FLUX (IC50)')
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)
    check_for_butterbar(selenium, notification_text='Adding compound(s)...', visible=True)
    check_for_butterbar(selenium, notification_text='Adding compound(s)...', visible=False)

    # Verify footer values and compound ids in grid
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(3),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(6)
        })
    verify_column_contents(selenium, 'ID', ['CRA-032665', 'CRA-032718', 'CRA-032845'])

    # Select restricted project additionally from Project query dropdown
    dom.click_element(selenium, ADV_PROJECT_QUERY_DROPDOWN, 'Project A')
    dom.click_element(selenium, ADV_PROJECT_QUERY_DROPDOWN_ELEMS, 'JS Testing')
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)
    check_for_butterbar(selenium, notification_text='Adding compound(s)...', visible=True)
    check_for_butterbar(selenium, notification_text='Adding compound(s)...', visible=False)

    # Verify footer values and compound ids in grid
    verify_footer_values(selenium, {'row_all_count': '6 Total Compounds', 'column_all_count': '6 Columns'})
    verify_column_contents(selenium, 'ID',
                           ['CRA-032665', 'CRA-032718', 'CRA-032772', 'CRA-032845', 'CRA-032913', 'CRA-033227'])

    # ----- Advanced search with Global project on Restricted Project ----- #
    # open unrestricted project and create live report
    open_project(selenium, 'Project A')
    lr_name = create_and_open_live_report(selenium,
                                          report_name='test_adv_query_on_project',
                                          folder_name='Project A Home')
    # Open advanced search panel
    open_add_compounds_panel(selenium)
    open_advanced_search(selenium)

    add_query(selenium, query_name=PROJECT_LINK, text_search=False)
    # opening project query dropdown
    dom.click_element(selenium, ADV_PROJECT_QUERY_DROPDOWN, 'Choose Project')

    # verify only unrestricted project names available in query dropdown
    project_elems = dom.get_elements(selenium, ADV_PROJECT_QUERY_DROPDOWN_ELEMS)
    project_names = [elem.text for elem in project_elems]
    expected_project_names = ['CMET', 'Global', 'Project A', 'Project B']
    assert expected_project_names == project_names, "Project names are not matched with expected."

    # selecting global project from unrestricted project
    dom.click_element(selenium, ADV_PROJECT_QUERY_DROPDOWN_ELEMS, 'Global')

    # adding column with range query
    add_query(selenium, 'CMET-TRFRET (Ki)')
    column_query = get_query(selenium, 'CMET-TRFRET (Ki)')
    set_query_range(column_query, lower_limit=0.0003, upper_limit=0.003)

    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)
    check_for_butterbar(selenium, notification_text='Adding compound(s)...', visible=True)
    check_for_butterbar(selenium, notification_text='Adding compound(s)...', visible=False)
    # Verify footer values and compound ids in grid
    verify_footer_values(selenium, {'row_all_count': '4 Total Compounds', 'column_all_count': '6 Columns'})
    verify_column_contents(selenium, 'ID', ['CRA-032665', 'CRA-032675', 'CRA-032718', 'CRA-032913'])

    # deleting LR and navigating to JS Testing project to make sure to delete the created LR
    delete_open_live_report(selenium, lr_name)
    open_project(selenium, 'JS Testing')
