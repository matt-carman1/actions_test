from helpers.change.grid_column_menu import open_coloring_rules
from helpers.selection.coloring_rules import SLIDER_MIN, SLIDER_MAX, \
    CONVERT_COLOR_RULES_WINDOW_HEADER, COLOR_WINDOW_OK_BUTTON, CONVERT_COLOR_RULES_WINDOW, \
    CONVERT_COLOR_RULES_WINDOW_BODY, CLEAR_RULES, \
    COLOR_RULES_MENU_CONTAINER, COLOR_RULES_MENU_ITEM, COLOR_RULE, COLOR_SELECTOR, GREEN, \
    CONVERT_DIALOG_WINDOW_OK_BUTTON, COLOR_RULE_INPUT, CELL_SELECTOR_LABEL
from helpers.verification.color import verify_column_color
from helpers.verification.element import verify_is_visible
from helpers.verification.grid import check_for_butterbar
from library import dom, wait

live_report_to_duplicate = {'livereport_name': 'Test Date Assay Column', 'livereport_id': '2699'}


def test_date_coloring_rules(selenium, duplicate_live_report, open_livereport):
    """
    Test to check coloring rules for date column.
    1. Apply Coloring rules with Range query
    2. Verify the color for Cells
    3. Convert Range query to Categorical and Apply coloring rules
    4. Verify the color for cells
    5. Clear all Coloring rules
    6. Verify the color for cells

    :param selenium: WebDriver, Selenium webdriver
    :param duplicate_live_report: LiveReport, fixture which duplicates and returns duplicated livereport
    :param open_livereport: LiveReport, fixture which open livereport
    """
    # column name
    date_column_name = "Test Dates Assay (date)"

    open_coloring_rules(selenium, date_column_name)

    # ----- Apply Coloring rules with Range query ----- #
    # Apply coloring rules
    dom.set_element_value(selenium, SLIDER_MIN, value='2009-01-01')
    dom.set_element_value(selenium, SLIDER_MAX, value='2009-01-02')

    # Save
    dom.click_element(selenium, COLOR_WINDOW_OK_BUTTON)

    # There should be a butter bar
    check_for_butterbar(selenium, 'Applying coloring rules', visible=True)
    # The butter bar should go away before we test colors
    check_for_butterbar(selenium, 'Applying coloring rules', visible=False)

    # ----- Verify the color for Cells ----- #
    verify_column_color(selenium,
                        date_column_name,
                        expected_colors=[(0, 0, 0, 0), (0, 0, 0, 0), (211, 211, 211, 1), (0, 0, 0, 0)])

    # ----- Convert Range query to Categorical and Apply coloring rules ----- #
    open_coloring_rules(selenium, date_column_name)

    # convert Range to Categorical
    dom.click_element(selenium, COLOR_RULES_MENU_CONTAINER)
    dom.click_element(selenium, COLOR_RULES_MENU_ITEM.format(1))
    wait.until_visible(selenium, CONVERT_COLOR_RULES_WINDOW)

    # verify confirmation Dialog
    verify_is_visible(selenium, CONVERT_COLOR_RULES_WINDOW_HEADER, selector_text='Convert Rule')
    verify_is_visible(
        selenium,
        CONVERT_COLOR_RULES_WINDOW_BODY,
        selector_text='Converting the rule types will reset all rules.\n\nAre you sure you wish to continue?')

    # click ok confirmation dialog
    dom.click_element(selenium, CONVERT_DIALOG_WINDOW_OK_BUTTON)

    # set range coloring rule
    dom.set_element_value(selenium, COLOR_RULE_INPUT.format(1), value='2009-02-01 16:00:00')
    dom.click_element(selenium, COLOR_RULE.format(1))
    dom.click_element(selenium, CELL_SELECTOR_LABEL, text='2009-02-01 16:00:00', exact_text_match=True)

    # click outside to close the dropdown
    selenium.execute_script('document.body.dispatchEvent(new Event("click", { bubbles: true }));')

    # select green
    dom.click_element(selenium, COLOR_SELECTOR.format(1))
    dom.click_element(selenium, GREEN)

    # save
    dom.click_element(selenium, COLOR_WINDOW_OK_BUTTON)

    # ----- Verify the color for cells ----- #
    verify_column_color(selenium,
                        date_column_name,
                        expected_colors=[(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 102, 0, 1)])

    # ----- Clear all Coloring rules ----- #
    open_coloring_rules(selenium, date_column_name)
    dom.click_element(selenium, CLEAR_RULES)
    dom.click_element(selenium, COLOR_WINDOW_OK_BUTTON)

    # There should be a butter bar
    check_for_butterbar(selenium, 'Applying coloring rules', visible=True)
    # The butter bar should go away before we test colors
    check_for_butterbar(selenium, 'Applying coloring rules', visible=False)

    # ----- Verify the color for Cells ----- #
    verify_column_color(selenium,
                        date_column_name,
                        expected_colors=[(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)])
