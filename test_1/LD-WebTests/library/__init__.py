"""
Files in the `library` submodule underlie most operations in a test.

* utils.py - utility functions, e.g. for awaiting a screen refresh or generating
             a unique name, that don't have a better place to live. utils.py
             should not depend on anything else in the module.

* url.py - functions for manipulating the web-browser's location, e.g.
           navigating to a new page

* simulate.py - simulate certain user interactions with the page: currently,
                hover and click. Does not depend on anything else in the module.

* dom.py - functions here are used to select elements from the DOM. They block
           until their conditions are matched or a timeout duration is reached.
           The default timeout wait is 1 minute.

* authentication.py - functions for login and logout

* eventually.py - convenience wrappers that makes it easy to make assertions
                  that depend on the results of functions in dom.py.

* base.py - low-level, LiveDesign-specific site interactions. For example
            pressing "OK" in a modal dialog.

* iframe.py - a decorator that makes it very easy to work with the DOM inside an
              iframe

* scroll.py - functions useful for scrolling the page using mouse wheel events.
"""
