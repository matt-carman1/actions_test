import pytest
from selenium.webdriver.common.by import By

from library import wait, url
from library.dom import LiveDesignWebException
from library.url_endpoints import LOGIN_URL


def test_wait_with_nonexistent_element(selenium):
    with pytest.raises(LiveDesignWebException) as e_info:
        wait.until_visible(selenium, 'aside', timeout=1)

    assert 'No element matching css selector `aside` was found' \
           == e_info.value.msg


def test_wait_with_extant_element(selenium):
    with pytest.raises(LiveDesignWebException) as e_info:
        wait.until_not_visible(selenium, 'html', timeout=1)

    assert 'A visible element matching css selector `html` was found' == \
           e_info.value.msg


def test_page_title(selenium):
    url.go_to_url(selenium, LOGIN_URL)
    title_from_get_element = selenium.find_element(By.CSS_SELECTOR, 'title') \
        .get_attribute("textContent")
    title_from_driver = selenium.title
    assert title_from_get_element == title_from_driver, \
        "There are two ways of getting the same thing"
    wait.until_page_title_is(selenium, 'Log in to LiveDesign')
