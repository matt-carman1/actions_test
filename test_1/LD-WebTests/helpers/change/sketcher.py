from helpers.selection.sketcher import SKETCHER_IFRAME
from library import iframe, wait


def import_structure_into_sketcher(driver, molv3_or_smiles, sketcher_iframe_selector=SKETCHER_IFRAME):
    """
    Given an open sketcher, paste in a molv3 string representing a new
    compound and confirm the import. This will add the compound, if not already
    present, to the active live report.

    :param driver: selenium webdriver
    :param molv3_or_smiles: str, molv3 or SMILES string to be added to the sketcher and imported
    :param sketcher_iframe_selector: str, optional, the selector for the sketcher iframe.
                                     Defaults to '#design-pane-sketcher'
    """

    @iframe.within_iframe(sketcher_iframe_selector)
    def wait_for_maestro_sketcher_to_load(_driver):
        wait.until_visible(_driver, '#qtcanvas')

    wait_for_maestro_sketcher_to_load(driver)

    driver.execute_async_script(
        """
        var done = arguments[arguments.length - 1];
        function importStructureIntoSketcher(selector, representation, val) {
            var iframe = document.querySelector(selector);
            if (!iframe || !iframe.contentWindow || !iframe.contentWindow.Module || !iframe.contentWindow.Module.sketcher_import_text) {
                window.setTimeout(importStructureIntoSketcher.bind(null, selector, representation), 100);
            } else {
                iframe.contentWindow.Module.sketcher_import_text(representation);
                done();
            }
        }
        importStructureIntoSketcher(arguments[0], arguments[1]);
    """, sketcher_iframe_selector, molv3_or_smiles)


def clear_structure_from_sketcher(driver, sketcher_iframe_selector=SKETCHER_IFRAME):
    """
    Clear the contents of an open sketcher.

    :param driver: selenium webdriver
    :param sketcher_iframe_selector: str, optional, the selector for the sketcher iframe.
                                     Defaults to '#sketcher-js'
    """

    driver.execute_async_script(
        """
        var done = arguments[arguments.length - 1];
        function clearStructureFromSketcher(selector) {
            var iframe = document.querySelector(selector);
            if (!iframe || !iframe.contentWindow || !iframe.contentWindow.Module || !iframe.contentWindow.Module.sketcher_clear) {
                window.setTimeout(clearStructureFromSketcher.bind(null, selector), 100);
            } else {
                iframe.contentWindow.Module.sketcher_clear();
                done()
            }
        }
        clearStructureFromSketcher(arguments[0]);
    """, sketcher_iframe_selector)
