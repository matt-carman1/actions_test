from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.common import exceptions as selenium_exceptions


def element_is_scrolled_to_bottom(element):
    """
    Is the element scrolled to the bottom?
    :param element:
    :return: Boolean
    """
    # calculation from
    # https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollHeight
    scroll_height = int(element.get_property('scrollHeight'))
    scroll_top = int(element.get_property('scrollTop'))
    client_height = int(element.get_property('clientHeight'))

    return scroll_height - scroll_top == client_height


def get_all_ids(row_obj):
    id_objs = row_obj.find_elements(by=By.XPATH, value=".//div[contains(@class,'grid-cell-type-assay-subcell')]/span")
    all_id_list = [x.get_attribute("textContent") for x in id_objs]

    return all_id_list


def any_text_character_present(locator):

    def _predicate(driver):
        characters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        ele_text = driver.find_element(*locator).get_attribute("textContent")
        for letter in ele_text:
            if letter in characters:
                return True

    return _predicate


def main():
    driver = webdriver.Firefox()
    wait = WebDriverWait(driver, 20)

    driver.get("https://qa-demo-24-2.dev.bb.schrodinger.com/livedesign/static/login.html#/login")

    username = driver.find_element(by=By.XPATH, value="//input[@id='username']")
    username.send_keys("testadmin")
    password = driver.find_element(by=By.XPATH, value="//input[@id='password']")
    password.send_keys("ColorDreamBeing37!")
    password.send_keys(Keys.ENTER)

    project = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'A2A')]")))
    project.click()
    driver.find_element(by=By.XPATH, value="//button[contains(@class, 'ok-button')]").click()

    #driver.get("https://qa-demo-24-2.dev.bb.schrodinger.com/livedesign/#/projects/1351/livereports/125714")
    driver.get("https://qa-demo-24-2.dev.bb.schrodinger.com/livedesign/#/projects/1351/livereports/125394")

    WebDriverWait(driver, 20).until(any_text_character_present((By.XPATH, "//div[contains(@class, 'header-table grid-header')]")))
    #wait.until(EC.text_to_be_present_in_element((By.XPATH, "//div[contains(@class, 'header-table grid-header')]"), '*'))
    header_objs = driver.find_elements(by=By.XPATH, value="//div[@class='grid-header-complete-title']")
    header_name_values = ["Compound Structure" if x.text == "Entity" else x.text for x in header_objs]
    print(f"Header values: {header_name_values}")
    print("If 'Entity' is in the header values it will be replaced with 'Compound Structure' to match what would be exported")

    main_table = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'main-table')]")))
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'main-table')]/div/div[contains(@style, 'position:')]/div")))
    scroll_origin = ScrollOrigin.from_element(main_table)

    first_element_smiles_xpath = "//div[contains(@class,'main-table')]/div/div[2]/div[@class='fixedDataTableRowLayout_rowWrapper']//div[@class='structure-smiles']"
    # test_element_smiles2 = "c1ccccc1"
    # test_element_smiles = "COc1ccc(C(=O)NC/C=C/C(N)=O)cc1F"
    wait.until(any_text_character_present((By.XPATH, first_element_smiles_xpath)))
    #WebDriverWait(driver, 25).until(lambda x: x.find_element(by=By.XPATH, value=first_element_smiles_xpath).get_attribute("textContent") == test_element_smiles2)

    compounds = dict()
    while not element_is_scrolled_to_bottom(main_table):
        row_objects = main_table.find_elements(by=By.XPATH, value="./div/div[2]//div[@class='fixedDataTableRowLayout_rowWrapper']")
        for row in row_objects:
            if row.is_displayed() and row.is_enabled():
                row_info = []
                column_objects = row.find_elements(by=By.XPATH, value=".//div[@class='public_fixedDataTableCell_cellContent']")

                column_number = 0
                for column in column_objects:
                    # First three columns (row number, Entity, ID) use either a <span> or <div> to wrap the text content,
                    # and will only ever have a single value always visible.
                    if column_number <= 2:
                        row_info.append(column.get_attribute("textContent"))

                    # Columns after the first three (including the row number) wrap each text entry in a <span> and some are not always visible.
                    # Some, rationale, have some info in <b> and then a <div> doesn't seem like other do. Need to check
                    # in case the columns are somehow out of order.
                    else:
                        try:
                            column.find_element(by=By.XPATH, value=".//b")
                            column_info = [x.text.replace('\n', ' ') for x in column.find_elements(By.XPATH, value="./div")]
                            column_info.remove('')

                        except selenium_exceptions.NoSuchElementException:
                            column_info = [x.get_attribute("textContent") for x in column.find_elements(by=By.XPATH, value=".//span")]

                        column_info_len = len(column_info)
                        if column_info_len > 1:
                            row_info.append(';'.join(column_info))
                        elif column_info_len == 1:
                            row_info.append(column_info[0])
                        else:
                            row_info.append("")

                    column_number += 1

                if row_info[0] not in compounds:
                    compounds[row_info[0]] = dict(zip(header_name_values, row_info[1:]))

                # row_num = row.find_element(by=By.XPATH, value=".//div[@class='row-index']").text
                # if row_num not in compounds:
                #     compound_smiles = row.find_element(by=By.XPATH, value=".//div[@class='structure-smiles']").get_attribute("textContent")
                #     compound_id = row.find_element(by=By.XPATH, value=".//span[@class='ellipsisOverflow']").text
                #     compound_all_ids = get_all_ids(row)
                #     compound_rationale = row.find_element(by=By.XPATH, value=".//div[contains(@class, 'rationale-cell')]").get_attribute("textContent")
                #
                #     compounds[row_num] = [compound_smiles, compound_id, compound_all_ids, compound_rationale]

        ActionChains(driver).scroll_from_origin(scroll_origin, 0, 150).perform()

    for key, value in compounds.items():
        print(f"row:{key}   info:{value}")

    if input("driver quit:").lower() == 'y':
        driver.quit()


if __name__ == '__main__':
    main()
