from helpers.change.live_report_picker import open_live_report
from helpers.change.project import open_project
from helpers.extraction.project_landing_page import find_bookmark
from helpers.selection.project_landing_page import PROJECT_LANDING_PAGE_URL, \
    DELETE_BOOKMARK_OPTION, LR_PICKER_LINK, BookmarkDialog, ACTIVE_TAB
from library import dom, base, ensure, wait


def open_project_landing_page(driver, project_name='JS Testing'):
    """
    Select a project and open project landing page

    :param driver: webdriver or parent element object
    :param project_name: str, name of the project to pick from project picker.Default project is "JS Testing"
    """
    project_modal = open_project(driver, project_name=project_name, click_ok_button=False)
    dom.click_element(project_modal, PROJECT_LANDING_PAGE_URL)


def switch_to_landing_page_bookmark_tab(driver):
    """
    Function checks if the current active tab in project landing page is bookmark tab by verifying if the
    active tab has Bookmarks text , if it's not then switch the tab to bookmark tab by clicking on the bookmark tab

    :param driver: webdriver or parent element object
    """

    ensure.element_visible(driver,
                           action_selector=BookmarkDialog.BOOKMARK_TAB,
                           action_selector_text='Bookmarks',
                           expected_visible_selector=ACTIVE_TAB,
                           expected_visible_selector_text='Bookmarks',
                           expected_visible_selector_exact_text_match=True,
                           action_selector_exact_text_match=True)


def click_add_bookmark_button(driver):
    """
    Function to click on add bookmark button in bookmark tab of project landing page

    :param driver : webdriver or parent element object
    """
    add_bookmark_button = dom.get_element(driver, BookmarkDialog.ADD_BOOKMARK_BUTTON)
    add_bookmark_button.click()


def add_new_bookmark(driver, bookmark_title, lr_name, label, description):
    """
    Function to add new bookmark

    :param driver: webdriver or parent element object
    :param bookmark_title : str, Title of that is to be shown on bookmark tile
    :param lr_name : str, Live report name
    :param label : str, label to enter in label field of bookmark
    :param description : str, description about bookmark
    """
    # Click on add bookmark button
    click_add_bookmark_button(driver)
    # fill the details required to create bookmark
    fill_bookmark_form(driver, bookmark_title, lr_name, label, description)
    # click on save button
    base.click_ok(driver)


def delete_bookmark(driver, bookmark_to_be_deleted):
    """
    Function to delete bookmark

    :param driver: webdriver or parent element object
    :param bookmark_to_be_deleted: str, title for bookmark that is to be deleted
    """
    # check if there is any bookmark with given title,if yes then get the web element for that bookmark
    bookmark_element = find_bookmark(driver, bookmark_to_be_deleted)
    dom.click_element(bookmark_element, BookmarkDialog.BOOKMARK_MORE_BUTTON)
    # click on delete option
    dom.click_element(bookmark_element, DELETE_BOOKMARK_OPTION, text='Delete')
    # click ok in dialog box to delete
    base.click_ok(driver)
    # wait until the bookmark element is not visible , this is required as after clicking delete ok button the
    # bookmark is shown for a second before deleted
    wait.until_not_visible(bookmark_element, BookmarkDialog.BOOKMARK_TITLE, text=bookmark_to_be_deleted)


def fill_bookmark_form(driver, bookmark_title, lr_name, label, description):
    """
    Function to fill the details requires to create a bookmark

    :param driver : webdriver or parent element object
    :param bookmark_title : str, Title that is to be shown on bookmark tile
    :param lr_name : str, Live report name
    :param label : str, label for bookmark
    :param description : str, description for bookmark
    """
    # enter bookmark title
    dom.set_element_value(driver, BookmarkDialog.BOOKMARK_TITLE_INPUT, bookmark_title)

    # choose the live report and click on OK button
    dom.click_element(driver, LR_PICKER_LINK)
    open_live_report(driver, name=lr_name)
    # click on dropdown and choose Type option
    dom.click_element(driver, BookmarkDialog.BOOKMARK_DESCRIPTION_TYPE_DROPDOWN)
    dom.click_element(driver,
                      BookmarkDialog.BOOKMARK_DESCRIPTION_TYPE_DROPDOWN_TEXT_OPTION,
                      text='Text',
                      exact_text_match=True)

    # Enter label and description for bookmark
    dom.set_element_value(driver, BookmarkDialog.BOOKMARK_DESCRIPTION_LABEL, label)
    dom.set_element_value(driver, BookmarkDialog.BOOKMARK_DESCRIPTION_INPUT, description)
