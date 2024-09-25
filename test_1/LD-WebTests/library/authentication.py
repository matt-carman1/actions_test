from helpers.selection.authentication import USERNAME_INPUT, PASSWORD_INPUT, LOGIN_BUTTON, USER_NAME_ELEMENT
from library import dom, url, wait, ensure
from helpers.selection.general import MENU_ITEM
from library.url_endpoints import LOGIN_URL


def login(driver, uname='demo', pword='demo'):
    """
    Log into LD with provided username
    """

    do_login(driver, uname, pword)
    wait.until_page_title_is(driver, 'LiveDesign')


def do_login(driver, user_name, password):
    """
    Enter the username, password and do click login button
    """
    url.go_to_url(driver, LOGIN_URL)
    wait.until_page_title_is(driver, 'Log in to LiveDesign')

    dom.set_element_value(driver, USERNAME_INPUT, user_name)
    dom.set_element_value(driver, PASSWORD_INPUT, password)
    dom.click_element(driver, LOGIN_BUTTON)


def logout(driver):
    """
    Log out of LD via logout dropdown
    """
    ensure.element_visible(driver, USER_NAME_ELEMENT, MENU_ITEM, expected_visible_selector_text='Log Out')
    dom.click_element(driver, MENU_ITEM, text='Log Out')
    wait.until_page_title_is(driver, 'Log in to LiveDesign')
