from library import dom, base
from helpers.selection.project import PROJECT_SEARCH_INPUT


def open_project(driver, project_name='JS Testing', click_ok_button=True):
    """
    Select a project and press OK to open it

    :param driver : Webdriver 
    :param project_name: str, name of project or therapeutic area
    :param click_ok_button : bool, variable which indicated whether to click ok button
                      in project picker page after project is selected
    """
    project_modal = base.go_to_project_picker(driver)
    dom.set_element_value(project_modal, PROJECT_SEARCH_INPUT, project_name)

    dom.click_element(project_modal, 'li', project_name)
    if click_ok_button:
        base.click_ok(project_modal)

    return project_modal
