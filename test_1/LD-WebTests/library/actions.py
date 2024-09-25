"""
Emulate drag and drop using a javascript library. Native drag and drop in
selenium is broken in my hands and according to this ticket:

https://github.com/seleniumhq/selenium-google-code-issue-archive/issues/3604

Instead we are using a MIT-licensed javascript library to emulate drag/drop
behavior:

https://github.com/andywer/drag-mock

Note that I copied the latest minified version as of 2018-04-24 into this repo.

"""

import base64

from selenium.webdriver import ActionChains

from library import utils
"""
Get script contents once on module load

TODO: Generalize this for arbitrary javascript code that needs to be injected.
"""
with open('injectable_js/drag-mock.min.js') as script_reader:
    source_code = script_reader.read()

encoded_source = base64.b64encode(source_code.encode('utf-8')).decode('utf-8')

drag_drop_library_element_script = """
    var done = arguments[0];
    if (!window.dragMock) {{
        var scriptEl = document.createElement('script');
        scriptEl.onload = done;
        scriptEl.src = 'data:text/javascript;base64,{}'
        document.body.appendChild(scriptEl);
    }}
    else {{
        done();
    }}
""".format(encoded_source)


def _ensure_library_is_in_page(driver):
    driver.execute_async_script(drag_drop_library_element_script)


def drag_and_drop(driver, source_element, destination_element):
    """
    Drag a source element X onto the target element Y.
    :param driver: Webdriver
    :param source_element: the element to be dragged
    :param destination_element: the element onto which the source_element will be dragged and dropped.
    """
    _ensure_library_is_in_page(driver)
    driver.execute_script("""
        dragMock.dragStart(arguments[0]).drop(arguments[1]);
    """, source_element, destination_element)


def drag_dragover_and_drop(driver, source_element, destination_element):
    """
    Drag a source element X onto the target element Y. The only difference between this helper and the drag_and_drop()
    is that this trigger an additional event called dragOver that makes it work for Columns Management UI. Currently
    this does not work for other drag drop tests like metapicker and there is a ticket LDIDEAS-4174 for it to understand
    the reason for it.
    :param driver: Webdriver
    :param source_element: the element to be dragged
    :param destination_element: the element onto which the source_element will be dragged and dropped.
    """
    _ensure_library_is_in_page(driver)
    driver.execute_script(
        """
        dragMock.dragStart(arguments[0])
        .dragOver(arguments[1])
        .delay(1000)
        .drop(arguments[1]);
    """, source_element, destination_element)


def drag_and_drop_by_offset(element, element_horz_displacement=None, element_vert_displacement=None):
    """
    Performs drag and drop by some offset using the functions of the Action
    Chains class of Selenium Webdriver. Drag and drop horizontally or
    vertically with some displacement. For e.g. Range and Similarity Sliders.
    :param element: Slider Web Element
    :param element_horz_displacement: horizontal displacement in pixels
    :param element_vert_displacement: vertical displacement in pixels
    :return: No returns
    """

    if element_horz_displacement or element_vert_displacement:
        slide = ActionChains(utils.get_driver_from_element(element))
        slide.click_and_hold(element).move_by_offset(element_horz_displacement,
                                                     element_vert_displacement). \
            release().perform()
