import pytest

from helpers.selection.general import HELP_BUTTON
from helpers.verification.element import verify_is_visible
from library import dom, wait

help_button_label = 'Document'
help_button_link = 'https://www.google.com/'
help_link_page_title = 'Google'

LD_PROPERTIES = {
    'CUSTOM_HELP_BUTTON_LABEL': help_button_label,
    'CUSTOM_HELP_LINK': help_button_link,
    'DISPLAY_CUSTOM_HELP_BUTTON': 'true'
}


@pytest.mark.usefixtures('open_project')
@pytest.mark.usefixtures('customized_server_config')
def test_custom_help_button_label_and_custom_help_link(selenium):
    """
    Test CUSTOM_HELP_BUTTON_LABEL and CUSTOM_HELP_LINK FFs.
    1. Verify help button text
    2. verify help button link by navigating to opened tab

    :param selenium: selenium webdriver
    """
    # verify help button text
    verify_is_visible(selenium, HELP_BUTTON, selector_text=help_button_label)

    # Clicking Help link
    dom.click_element(selenium, HELP_BUTTON)

    # Switching to the new tab dom using selenium
    selenium.switch_to.window(selenium.window_handles[1])
    wait.until_page_title_is(selenium, help_link_page_title)

    # Validating tab url with help link
    assert help_button_link == selenium.current_url, "URL is not matched with expected"
