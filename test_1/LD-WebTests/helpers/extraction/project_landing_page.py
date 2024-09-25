from helpers.selection.project_landing_page import BookmarkDialog
from library import dom


def find_bookmark(driver, expected_bookmark_title, index_of_bookmark=''):
    """
    Checks if there is any bookmark with given bookmark title

    :param driver: Selenium Webdriver
    :param expected_bookmark_title : str, title of the bookmark that one want to check
    :param index_of_bookmark : str, When there are multiple bookmarks matching the same bookmark name if given 'all'
                               return all matching bookmarks,default value is '' which returns the first matched
                               bookmark
    :return : First web element which matches given bookmark name or list of all matched bookmark
              elements if user chooses index as 'all', returns None if there are no matching bookmarks
    """
    # get all bookmarks elements
    all_bookmarks_list = dom.get_elements(driver, BookmarkDialog.BOOKMARK_TILE, dont_raise=True, timeout=5)
    # handling edge case when there are no bookmarks and return none
    if not all_bookmarks_list:
        return None
    bookmark_element = None
    bookmark_list_with_expected_title = []
    # traverse through all bookmarks elements and find the bookmark with given name
    for bookmark in all_bookmarks_list:
        title_bookmark = dom.get_element(bookmark, BookmarkDialog.BOOKMARK_TITLE)
        if title_bookmark.text == expected_bookmark_title:
            bookmark_element = bookmark
            # If the index is ''(empty string) then return the first matched bookmark
            if index_of_bookmark == '':
                return bookmark_element
            # If the index is all then append the matched bookmark into result list
            if index_of_bookmark == 'all':
                bookmark_list_with_expected_title.append(bookmark_element)
    if bookmark_list_with_expected_title:
        return bookmark_list_with_expected_title
    return None
