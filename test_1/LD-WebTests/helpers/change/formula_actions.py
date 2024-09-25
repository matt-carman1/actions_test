from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from helpers.change.actions_pane import open_add_data_panel
from helpers.change.grid_column_menu import open_edit_formula_window
from helpers.extraction.grid import wait_until_cells_are_loaded
from helpers.selection.column_tree import COLUMN_TREE_PICKER_CREATE_NEW_FORMULA_BUTTON
from helpers.selection.modal import WINDOW_HEADER_TEXT
from helpers.selection.formula import FORMULA_PICKER_COLUMNS_TAB, FORMULA_PICKER_COLUMNS_TAB_PICKER, \
    FORMULA_PICKER_DESCRIPTION, FORMULA_PICKER_FUNCTIONS_TAB, FORMULA_PICKER_FUNCTIONS_TAB_PICKER, \
    FORMULA_EXPRESSION, FORMULA_NAME_FIELD, FORMULA_SAVE_BUTTON, FORMULA_DESCRIPTION_FIELD, FORMULA_DATATYPE_FIELD, \
    FORMULA_PUBLISHED_CHECKBOX
from library import dom, wait, simulate


def add_column_to_formula(driver, column_to_add):
    """
    Double click on the desired column and adds it to the Formula expression. Make sure to click at the desired
    position in the expression box before adding the column.

    :param driver: Selenium Webdriver
    :param column_to_add: str, Column name to add to the formula expression
    :return:
    """
    dom.click_element(driver, FORMULA_PICKER_COLUMNS_TAB, text='Columns')

    select_element = dom.get_element(driver, FORMULA_PICKER_COLUMNS_TAB_PICKER)

    # Use webdriver Select object to scroll the correct option into view before dblclick
    select_helper = Select(select_element)
    select_helper.select_by_visible_text(column_to_add)
    option_element = dom.get_element(select_element, 'option', text=column_to_add, exact_text_match=True)

    simulate.double_click(option_element)


def add_function_to_formula(driver, function_to_add):
    """
    Double click on the desired function and adds it to the Formula expression. Make sure to click at the
    appropriate position in the expression box before adding the function.

    :param driver: Selenium Webdriver
    :param function_to_add: str, function to add to the formula expression
    :return: str, description of the function added to the formula
    """
    dom.click_element(driver, FORMULA_PICKER_FUNCTIONS_TAB, text='Functions')

    select_element = dom.get_element(driver, FORMULA_PICKER_FUNCTIONS_TAB_PICKER)

    # Use webdriver Select object to scroll the correct option into view before dblclick
    select_helper = Select(select_element)
    select_helper.select_by_visible_text(function_to_add)
    option_element = dom.get_element(select_element, 'option', text=function_to_add, exact_text_match=True)

    simulate.double_click(option_element)

    return dom.get_element(driver, FORMULA_PICKER_DESCRIPTION).text


def add_expression_to_formula(driver, expression_to_add):
    """
    Pastes an expression in the expression box. Make sure to click at the appropriate position in the expression box
    before adding this.

    :param driver: Selenium Webdriver
    :param expression_to_add: str, expression to add to the formula expression. For eg. operators '*', '+' or the
                              operands like '5', '10' or the 'combination of both
    :return:
    """
    expression_box_element = dom.click_element(driver, FORMULA_EXPRESSION)
    simulate.typing(expression_box_element, value=expression_to_add)


def add_name_to_formula(driver, formula_column_name):
    """
    Adds or Edits the Formula Column Name.

    :param driver: Selenium Webdriver
    :param formula_column_name: str, Formula Column name that would be displayed in the Livereport.
    :return:
    """
    dom.set_element_value(driver, FORMULA_NAME_FIELD, value=formula_column_name)


def add_description_to_formula(driver, description):
    """
    Adds or Edits the Formula Description.

    :param driver: Selenium Webdriver
    :param description: str, Formula description.
    :return:
    """
    dom.set_element_value(driver, FORMULA_DESCRIPTION_FIELD, value=description)


def add_data_type_to_formula(driver, output_data_type):
    """
    Adds or Edits formula output data type.

    :param driver: Selenium webdriver
    :param output_data_type: formula data type, values are Number, Datetime, String, Structure Image
    :return:
    """
    select_element = dom.get_element(driver, FORMULA_DATATYPE_FIELD)

    # Use webdriver Select object to scroll the correct option into view before dblclick
    select_helper = Select(select_element)
    select_helper.select_by_visible_text(output_data_type)


def open_create_formula_window(driver):
    """
    From the D&C tree click on the 'Create Formula' button and opens the Create and Add New Formula Column window.

    :param driver: Selenium Webdriver
    :return:
    """
    open_add_data_panel(driver)
    wait.until_loading_mask_not_visible(driver)
    # Click "New" button for Formulas
    dom.click_element(driver, COLUMN_TREE_PICKER_CREATE_NEW_FORMULA_BUTTON, text="NEW", exact_text_match=True)
    wait.until_visible(driver, WINDOW_HEADER_TEXT, text='Create and Add New Formula Column')


def create_a_custom_formula(driver,
                            formula_name,
                            create_expression_callback,
                            description=None,
                            output_data_type=None,
                            is_publish=False):
    """
    creating a formula with a custom expression.

    :param driver: Selenium Webdriver
    :param formula_name: str, Formula Column Name
    :param create_expression_callback: function which will set expression in Expression text box
    :param description: str, formula description
    :param output_data_type: str, formula data type, values are Number, Datetime, String, Structure Image
    :param is_publish: boolean, will create published formula if it is True, non-published formula for False
    :return str, final formula expression
    """

    # Open create formula window
    open_create_formula_window(driver)

    # Add name to the formula
    add_name_to_formula(driver, formula_name)

    # Add description to formula
    if description:
        add_description_to_formula(driver, description)

    # Add output data type to the formula
    if output_data_type:
        add_data_type_to_formula(driver, output_data_type)

    # creating expression by calling expression call back
    create_expression_callback(driver)
    formula_expression = dom.get_element(driver, FORMULA_EXPRESSION).text
    # With the new formula Editor Quill, the color is also return in text of the element. So, removing it.
    final_formula_expression = formula_expression.replace('\ufeff', '')

    # Add publish state to the formula
    if is_publish:
        dom.click_element(driver, selector=FORMULA_PUBLISHED_CHECKBOX)

    dom.click_element(driver, FORMULA_SAVE_BUTTON, text='Add to LiveReport', exact_text_match=True)

    return final_formula_expression


def create_formula_and_wait_for_cells_to_load(selenium, formula_name, expression_function, is_publish):
    """
    Create a custom formula and wait for cells to be loaded in the specified column.

    :param selenium: Selenium WebDriver instance.
    :type selenium: selenium.webdriver.WebDriver
    :param formula_name: Name of the formula to be created.
    :type formula_name: str
    :param expression_function: Expression function for the formula.
    :type expression_function: callable
    :param is_publish: Flag indicating whether the formula should be published.
    :type is_publish: bool
    """
    create_a_custom_formula(selenium,
                            formula_name,
                            expression_function,
                            description='description for formula testing',
                            output_data_type='Number',
                            is_publish=is_publish)
    wait_until_cells_are_loaded(selenium, column_title=formula_name)


def make_custom_edit_to_formula(driver,
                                formula_column_name,
                                new_formula_name=None,
                                formula_function=None,
                                formula_column=None,
                                expression=None,
                                is_only_expression=False,
                                is_exp_box_clear=False,
                                characters_to_remove=None):
    """
    Making a custom edit to an existing formula in the LR.

    :param driver:Selenium WebDriver instance
    :type driver:selenium.webdriver.WebDriver
    :param formula_column_name:The name of the existing formula column
    :type formula_column_name:str
    :param new_formula_name:The new formula column name. Defaults to None
    :type new_formula_name:str
    :param formula_function:The name of the function to be added to the formula. Defaults to None.
    :type formula_function:str
    :param formula_column:The name of the column to be added to the formula. Defaults to None.
    :type formula_column:str
    :param is_only_expression: Adding expression to the formula expression box. Defaults to False
    :type is_only_expression:
    :param expression:The expression to be added to the formula. Defaults to None.
    :type expression:str
    :param is_exp_box_clear:Whether to clear the formula expression box. Defaults to False.
    :type is_exp_box_clear:bool
    :param characters_to_remove:The number of characters to remove from the formula expression box.Defaults to None.
    :type characters_to_remove:int
    """
    # Opening the Formula Edit Window
    open_edit_formula_window(driver, formula_column_name)

    # Changing the formula name
    if new_formula_name:
        add_name_to_formula(driver, new_formula_name)

    # Clear the formula expression box
    if is_exp_box_clear:
        dom.click_element(driver, FORMULA_EXPRESSION)
        ActionChains(driver).send_keys(Keys.BACKSPACE * characters_to_remove).perform()

    # Edit the formula
    if formula_function and formula_column and expression:
        create_expression(driver, formula_function, formula_column, expression)

    # Adding expression to formula
    if is_only_expression:
        add_expression_to_formula(driver, expression)

    formula_expression = dom.get_element(driver, FORMULA_EXPRESSION).text

    # Saving the formula post editing
    dom.click_element(driver, FORMULA_SAVE_BUTTON, text='Save')

    # With the new formula Editor Quill, the color is also returned in the text of the element. So, removing it.
    final_formula_expression = formula_expression.replace('\ufeff', '')

    return final_formula_expression


def create_expression(driver, function_name, column_name, expression):
    """
    Sets a custom expression for a formula in a Live Report.
    This function is specific to testing and is intended to be passed to the `create_a_custom_formula` helper.

    :param driver: Selenium Webdriver
    :type driver:selenium.webdriver.WebDriver
    :param function_name: The name of the function to be added to the formula.
    :type function_name:str
    :param column_name: The name of the column to be added to the formula.
    :type column_name:str
    :param expression: The expression to be added to the formula.
    :type expression:str
    """
    add_function_to_formula(driver, function_name)
    add_column_to_formula(driver, column_name)
    add_expression_to_formula(driver, expression)