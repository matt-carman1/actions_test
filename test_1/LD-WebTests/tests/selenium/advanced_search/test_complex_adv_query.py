from helpers.selection.advanced_search import SEARCH_AND_ADD_COMPOUNDS_BUTTON, ADVANCED_SEARCH_TEXTBOX,\
    COMPLEX_ADV_SEARCH_TEXT_NODE, COMPLEX_ADV_QUERY_RANGE_1, COMPLEX_ADV_SEARCH_FOCUSED_QUERY, \
    ADV_QUERY_COG_ICON, COMPLEX_ADV_QUERY_DATABASE_DATASET, COMPLEX_ADV_QUERY_RANGE_2
from helpers.selection.add_compound_panel import COMPOUNDS_PANE_ACTIVE_TAB
from helpers.selection.general import MENU_ITEM
from helpers.change.advanced_search_actions import add_query, open_complex_advanced_search_panel
from helpers.change.live_report_picker import create_and_open_live_report
from helpers.change.live_report_menu import switch_to_live_report
from helpers.change.columns_action import search_and_selecting_column_in_columns_tree
from helpers.selection.grid import Footer
from helpers.verification.grid import verify_grid_contents, verify_footer_values, verify_is_visible
from library import dom, base


def test_complex_adv_query(selenium, new_live_report, open_livereport):
    """
    Test for complex advanced search. The four objectives covered are:
        1. Adding conditions to form an expression.
            a. Run an active advanced search
            b. Verify the results.
        2. Deleting a part of the expression, by interacting with it.
            a. Deleted an expression
        3. Switch between LRs
        4. Verify that that the expression is still intact

    :param selenium: Selenium Webdriver
    :param new_live_report: Fixture to create a new live report
    :param open_livereport: Fixture to open a live report
    """
    # Defining data required throughout the test
    model_column = "Random integer (Result)"
    assay_column = "Brain (Drug uptake)"
    database_query = "Database/Dataset"
    list_of_ids = ['CHEMBL1034']
    assay_values = ['=2.7']
    model_values = ['11.0']

    # Opening the Advanced Search panel and switching to Complex view mode
    open_complex_advanced_search_panel(selenium)

    # Objective 1 : Adding conditions to form an expression
    # adding a model column
    search_and_selecting_column_in_columns_tree(selenium, model_column, ADVANCED_SEARCH_TEXTBOX)
    # adding an assay column
    search_and_selecting_column_in_columns_tree(selenium, assay_column, ADVANCED_SEARCH_TEXTBOX)
    # adding a database/dataset column
    add_query(selenium, database_query, text_search=False)

    # Note that dom.set_element_value cannot be used for the above selector since its not an input element,
    # so Niranjan helped me come up with a workaround using JS.
    # Placing the 'and' in between the model and assay column
    adv_input_text_element = dom.click_element(selenium, COMPLEX_ADV_SEARCH_TEXT_NODE)
    selenium.execute_script("""
            arguments[0].innerText = 'and';
            """, adv_input_text_element)

    dom.click_element(selenium, COMPOUNDS_PANE_ACTIVE_TAB)

    # Searching for compounds
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)

    # Verify footer values and compound ids in grid
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(1),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(7)
        })

    # Verification that IDs's, assay and model columns are populated as expected
    verify_grid_contents(selenium, {
        'ID': list_of_ids,
        'Brain (Drug uptake) [uM]': assay_values,
        model_column: model_values
    })

    # Objective 2: Deleting a part of the expression. Note this can be extracted to a helper if required.
    # Deleting the model column here
    dom.click_element(selenium, COMPLEX_ADV_QUERY_RANGE_1)

    query = dom.get_element(selenium, COMPLEX_ADV_SEARCH_FOCUSED_QUERY)

    dom.click_element(query, ADV_QUERY_COG_ICON)
    dom.click_element(query, MENU_ITEM, text="Delete")

    base.click_ok(selenium)

    # Objective 3: Switching to a different LR
    create_and_open_live_report(selenium, report_name="test_switching", lr_type="Compounds")

    switch_to_live_report(selenium, live_report_name=new_live_report)

    # Objective 4: Verify that the expression still exists after switching the LR
    verify_is_visible(selenium, COMPLEX_ADV_QUERY_RANGE_2, custom_timeout=5)
    verify_is_visible(selenium, COMPLEX_ADV_QUERY_DATABASE_DATASET)
