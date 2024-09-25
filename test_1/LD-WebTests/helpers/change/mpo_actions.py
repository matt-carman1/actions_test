from helpers.selection.column_tree import COLUMN_TREE_PICKER_TEXT_NODE, COLUMN_TREE_PICKER_TOOLTIP_HEADER_TEXT
from library import dom, wait, simulate
from helpers.selection.mpo import MPO_GENERAL_SETTINGS_FORM, MPO_NAME_FIELD, MPO_DESCRIPTION_FIELD, \
    MPO_CONSTITUENT_PICKER, MPO_CONSTITUENT_PICKER_VALUE, MPO_CONSTITUENT_FORM, MPO_VALUE_DISTRIBUTION_DROPDOWN, \
    MPO_CONSTITUENT_FIELD, MPO_DROPDOWN_INPUT, MPO_CONSTITUENT_BUTTON, MPO_PROPERTY_WEIGHTS, \
    MPO_PROPERTY_WEIGHTS_FORM, MPO_CONSTITUENT_WEIGHT_EDITOR, MPO_DELETE_CONSTITUENT, MPO_CLONE_BUTTON
from helpers.change.actions_pane import open_add_data_panel
from helpers.change.data_and_columns_tree import search_column_tree
from helpers.change.dropdown_actions import set_dropdown_items
from helpers.verification.element import verify_is_not_visible, verify_is_visible


def open_mpo_create_window(driver, column_name, description=None):
    """
    Opens Create MPO window and sets name + description

    :param driver: webdriver
    :param column_name: name of the MPO
    :type column_name: <str>
    :param description: description of the MPO
    :type description: <str>
    """
    # open the "Add Data" action panel, if it is not already open
    open_add_data_panel(driver)

    # Click "Define new MP Profile" button
    dom.click_element(driver, 'div.action.mpo', text="NEW")

    # Ensure that the MPO window is open before choosing settings (This is necessary because the opening of the
    # window is slow and sometimes it is not ready when choose_ffc_settings() starts running.)
    wait.until_visible(driver, MPO_GENERAL_SETTINGS_FORM)

    # Add unique name
    dom.set_element_value(driver, MPO_NAME_FIELD, column_name)

    # Add description
    if description:
        dom.set_element_value(driver, MPO_DESCRIPTION_FIELD, description)


def add_in_live_report_constituent(driver, column_name, distribution_type, values):
    """
    Add a constituent (that is already in the LR) to currently open MPO create/edit dialog

    :param driver: webdriver
    :param column_name: name of the MPO
    :param distribution_type: distribution type of MPO constituent
    :param values: list of distribution values, expected to match the given distribution type
    """

    # Add unique name
    dom.click_element(driver, 'button', '+ Add Constituent')
    wait.until_visible(driver, MPO_CONSTITUENT_PICKER)

    dom.click_element(driver, MPO_CONSTITUENT_PICKER_VALUE, column_name, exact_text_match=True)
    wait.until_visible(driver, MPO_CONSTITUENT_FORM)
    set_constituent_form_values(driver, distribution_type, values)


def edit_constituent(driver, column_name, distribution_type, values):
    """
    Edits an existing MPO constituent

    :param driver: webdriver
    :param column_name: name of the constituent
    :param distribution_type: distribution type of MPO constituent
    :param values: list of distribution values, expected to match the given distribution type
    """

    # Add unique name
    dom.click_element(driver, MPO_CONSTITUENT_BUTTON, column_name)
    wait.until_visible(driver, MPO_CONSTITUENT_FORM)
    set_constituent_form_values(driver, distribution_type, values)


def set_constituent_form_values(driver, distribution_type, values):
    """
    Sets the settings for a MPO constituent

    :param driver: webdriver
    :param column_name: name of the constituent
    :param distribution_type: distribution type of MPO constituent
    :param values: list of distribution values, expected to match the given distribution type
    """
    # Select distribution type
    dropdown = dom.click_element(driver, MPO_VALUE_DISTRIBUTION_DROPDOWN)
    dom.click_element(dropdown, 'li', distribution_type)

    # Set distribution values.  Categorical uses autosuggest and needs to set in a different way
    if distribution_type == 'Categorical (Text)':
        valueFields = dom.get_elements(driver, MPO_DROPDOWN_INPUT)
        for (valueField, value) in zip(valueFields, values):
            set_dropdown_items(valueField, value, do_select=True)
    else:
        valueFields = dom.get_elements(driver, MPO_CONSTITUENT_FIELD)
        for (valueField, value) in zip(valueFields, values):
            valueField.send_keys(value)


def add_constituent_weight(driver, column_name, value):
    """
    Sets the weights for a MPO constituent

    :param driver: webdriver
    :param column_name: str, name of the constituent for which the weight needs to be added.
    :param value: str, weight to be added to the constituent column.
    :return:
    """
    dom.click_element(driver, MPO_PROPERTY_WEIGHTS)
    wait.until_visible(driver, MPO_PROPERTY_WEIGHTS_FORM)
    constituent_weight_editor = dom.get_element(driver, MPO_CONSTITUENT_WEIGHT_EDITOR, column_name)
    dom.set_element_value(constituent_weight_editor, 'input', value)


def remove_constituent(driver, column_name):
    """
    Removes the MPO constituent. Make sure to open the MPO dialog.

    :param driver: Selenium Webdriver
    :param column_name: str, Constituent Column to be removed from MPO.
    """

    mpo_constituent = dom.get_element(driver, '.mpo-added-constituent', text=column_name)
    simulate.hover(driver, mpo_constituent)
    dom.click_element(mpo_constituent, MPO_DELETE_CONSTITUENT, text='X', exact_text_match=True)
    verify_is_not_visible(driver, '.mpo-added-constituent', selector_text=column_name)


def clone_mpo(driver, mpo_to_clone):
    """
    Cloning an MPO using 'Clone' button on the tooltip.

    :param driver: webdriver
    :param mpo_to_clone: str, MPO which needs to be cloned
    """
    open_add_data_panel(driver)
    search_column_tree(driver, mpo_to_clone)
    simulate.hover(driver,
                   dom.get_element(driver, COLUMN_TREE_PICKER_TEXT_NODE, text=mpo_to_clone, exact_text_match=True))
    verify_is_visible(driver,
                      COLUMN_TREE_PICKER_TOOLTIP_HEADER_TEXT,
                      selector_text=mpo_to_clone,
                      exact_selector_text_match=True)
    dom.click_element(driver, MPO_CLONE_BUTTON, text='Duplicate', exact_text_match=True)
