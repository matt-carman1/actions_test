"""
Manipulate the URL of the site under test
"""


def go_to_url(driver, url):
    try:
        driver.get(url)
    except Exception:
        print("Could not navigate to {}".format(url))
        raise


def get_page_hash(driver):
    return driver.execute_script('return window.location.hash')


def set_page_hash(driver, new_hash):
    driver.execute_script('window.location.hash = arguments[0]', new_hash)
