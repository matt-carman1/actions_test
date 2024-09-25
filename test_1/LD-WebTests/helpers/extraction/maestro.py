from helpers.selection.sketcher import SKETCHER_IFRAME


def get_molv(driver, sketcher_iframe_selector=SKETCHER_IFRAME):
    """
    Use the Maestro Sketcher API to extract the molv3 represenation of the current structure.

    :param driver: selenium webdriver
    :param sketcher_iframe_selector: str, optional, the selector for the sketcher iframe.
                                     Defaults to '#design-pane-sketcher'
    :return: the molv3 string
    """

    molv3 = driver.execute_async_script(
        """
        var done = arguments[arguments.length - 1];
        function getRepresentation(selector) {
            var iframe = document.querySelector(selector);
            if (!iframe || !iframe.contentWindow || !iframe.contentWindow.Module || !iframe.contentWindow.Module.sketcher_export_text) {
                window.setTimeout(getRepresentation.bind(null, selector), 100);
            } else {
                var format = iframe.contentWindow.Module.Format.MDL_MOLV3000;
                var molv3 = iframe.contentWindow.Module.sketcher_export_text(format);
                done(molv3);
            }
        }
        getRepresentation(arguments[0]);
    """, sketcher_iframe_selector)

    return molv3 if molv3 else ''
