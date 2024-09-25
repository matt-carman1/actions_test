from helpers.selection.sketcher import SKETCHER_IFRAME, RGROUP_SCAFFOLD_IFRAME


def verify_if_sketcher_is_empty(driver, sketcher_iframe_selector=SKETCHER_IFRAME):
    """
    Check if the sketcher is empty or not

    :param driver: selenium webdriver
    :param sketcher_iframe_selector: str, optional, the selector for the sketcher iframe.
                                     Defaults to '#sketcher-js'

    :rtype: :class:`bool`
    :return: True if sketcher is empty, False if it has a structure drawn in it
    """
    is_sketcher_empty = driver.execute_script(
        """
        function checkIfSketcherIsEmpty(selector) {
            var iframe = document.querySelector(selector);
            if (!iframe || !iframe.contentWindow || !iframe.contentWindow.Module) {
                window.setTimeout(checkIfSketcherIsEmpty.bind(null, selector), 100);
            } else {
                return iframe.contentWindow.Module.sketcher_is_empty();
            }
        }
        return checkIfSketcherIsEmpty(arguments[0]);
        """, sketcher_iframe_selector)
    return is_sketcher_empty


def verify_if_sketcher_is_populated(driver):
    """
    Verifies if the design sketcher is populated with compound structure

    :param driver: selenium webdriver
    """
    assert verify_if_sketcher_is_empty(driver, sketcher_iframe_selector=SKETCHER_IFRAME) is False


def verify_if_enumeration_is_populated(driver):
    """
    Verifies if the enumeration sketcher is populated with compound structure

    :param driver: selenium webdriver
    """
    assert verify_if_sketcher_is_empty(driver, sketcher_iframe_selector=RGROUP_SCAFFOLD_IFRAME) is False
