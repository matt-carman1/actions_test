"""
Verifications for project landing pages
"""
from helpers.extraction.project_landing_page import find_bookmark


def verify_is_bookmark_present(driver, expected_bookmark_title):
    """
    Function to verify if bookmark with given name is present in list of bookmarks available

    :param driver : webdriver
    :param expected_bookmark_title : str, name of the bookmark
    """
    # find the bookmark
    bookmark_element = find_bookmark(driver, expected_bookmark_title)
    # check if bookmark is saved
    assert bookmark_element is not None, "Bookmark with title : {} is not present".format(expected_bookmark_title)


def verify_is_bookmark_absent(driver, expected_bookmark_title):
    """
    Function to verify if bookmark with given name is not present in the list of bookmarks available

    :param driver : webdriver
    :param expected_bookmark_title : str, name of the bookmark
    """
    # find the bookmark
    bookmark_element = find_bookmark(driver, expected_bookmark_title)
    # check if bookmark is saved
    assert bookmark_element is None, "Bookmark with title : {} is present".format(expected_bookmark_title)
