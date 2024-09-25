import pytest

from helpers.selection.project import THERAPEUTIC_AREA_SEARCH_INPUT, PROJECT_LIST_ITEMS, PROJECT_DETAILS_CONTENT
from helpers.verification.element import verify_is_visible, verify_is_not_visible
from library import dom, base


@pytest.mark.usefixtures("login_to_livedesign")
def test_project_picker_ui(selenium):
    """
    Tests project picker UI:
    1. Search and select 'Vaccines' in Therapeutic Area
    2. Verify correct projects show up in Project List:
        JS Testing
        NoMod Testing
    3. Verify empty details displayed in Project Details
    4. Select 'JS Testing' in Project List
    5. Verify correct details displayed in Project Details:
        Name: JS Testing
        Therapeutic Area: Vaccines
        Lead: Victoria Vaccinator MD PhD
        Description: For general JS testing.
        Links: View Project Landing Page

    :param selenium: Webdriver
    """
    # Search and select 'Vaccines' in Therapeutic Area
    project_modal = base.go_to_project_picker(selenium)
    dom.set_element_value(project_modal, THERAPEUTIC_AREA_SEARCH_INPUT, 'Vaccines')
    dom.click_element(project_modal, 'li', 'Vaccines')

    # Verify correct projects show up in Project List
    for expected_project in ['JS Testing', 'NoMod Testing']:
        verify_is_visible(selenium, selector=PROJECT_LIST_ITEMS, selector_text=expected_project)

    # Verify empty details displayed in Project Details
    for expected_empty_project_details in ['Name: ', 'Therapeutic Area:', 'Lead: ', 'Description']:
        verify_is_visible(selenium, selector=PROJECT_DETAILS_CONTENT, selector_text=expected_empty_project_details)

    verify_is_not_visible(selenium, selector=PROJECT_DETAILS_CONTENT, selector_text='Links:')

    # Select 'JS Testing' in Project List
    dom.click_element(project_modal, selector=PROJECT_LIST_ITEMS, text='JS Testing')

    # Verify correct details displayed in Project Details
    for expected_project_details_content in [
            'Name: ' + '\n' + 'JS Testing', 'Therapeutic Area:' + '\n' + 'Vaccines',
            'Lead: ' + '\n' + 'Victoria Vaccinator MD PhD ', 'Description' + '\n' + 'For general JS testing.',
            'Links:' + '\n' + 'View Project Landing Page'
    ]:
        verify_is_visible(selenium, selector=PROJECT_DETAILS_CONTENT, selector_text=expected_project_details_content)
