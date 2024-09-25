import time

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.remote.webdriver import WebDriver
from helpers.change.formula_actions import add_function_to_formula
from helpers.change.sketcher import import_structure_into_sketcher
from helpers.selection.formula import FORMULA_EXPRESSION, FORMULA_SKETCHER_ADD_BUTTON, \
    FORMULA_SUBSTRUCTURE_SEARCH_SKETCHER
from library import dom, simulate
from resources.structures.structures_test_substructure_formula import TEST_SUBSTRUCTURE_FORMULA


def select_function_import_sketcher(selenium):
    """
    Sets the expression to Formula expression by performing the following steps

    1. Adds the 'substructureSearch' function to the Formula expression.
    2. Imports the compound structure (molv3 or SMILES) into the sketcher using the provided Selenium Webdriver.
    3. Clicks the 'Add' button in the Formula sketcher.
    4. Waits for 5 seconds.
    5. Performs a backspace action seven times.
    6. Retrieves the Formula expression element.
    7. Simulates typing the expression "structure')" into the element.
    8. Maximizes the Selenium Webdriver window.
    :param selenium: The Selenium Webdriver used to interact with the web application
    :type selenium: WebDriver
    :return: None
    :rtype: None
    """

    add_function_to_formula(selenium, 'substructureSearch')

    import_structure_into_sketcher(selenium,
                                   molv3_or_smiles=TEST_SUBSTRUCTURE_FORMULA,
                                   sketcher_iframe_selector=FORMULA_SUBSTRUCTURE_SEARCH_SKETCHER)
    dom.click_element(selenium, selector=FORMULA_SKETCHER_ADD_BUTTON, text='Add')
    time.sleep(5)
    # If the output type is set to "Structure", the expected result should be a structure. However, when i entered an
    # expression in the expression box, it defaulted to the value "count" for the result. To rectify this, i used
    # backspace key to delete "count" and replaced it with "structure".
    ActionChains(selenium).send_keys(Keys.BACKSPACE * 7).perform()
    ele = dom.get_element(selenium, selector=FORMULA_EXPRESSION)
    time.sleep(2)
    simulate.typing(ele, "structure')")
    WebDriver.maximize_window(selenium)
