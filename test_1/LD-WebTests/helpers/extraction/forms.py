from helpers.selection.forms import FIELD_LIST, COLUMN_NAME, COLUMN_VALUE
from library import dom


#todo: move to a tileview file?
def get_list_widget_data(driver):
    """
    Gets the column names and data shown in the list widget

    :param driver, selenium webdriver
    :return dict[name: str] = value: str, dictionary with column name (key) and the content shown (value)
    """
    data = {}
    field_list = dom.get_elements(driver, FIELD_LIST)
    if not field_list:
        return data
    for item in field_list:
        column_name = dom.get_element(item, COLUMN_NAME).text
        column_value = dom.get_element(item, COLUMN_VALUE).text
        data[column_name] = column_value
    return data
