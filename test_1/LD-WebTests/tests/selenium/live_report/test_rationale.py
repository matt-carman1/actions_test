"""
Selenium Test for testing Rationale functionality (QA-3141).

"""
import pytest

from helpers.change.actions_pane import open_add_compounds_panel, close_add_compounds_panel
from helpers.change.grid_columns import get_cell
from helpers.change.live_report_menu import switch_to_live_report, click_live_report_menu_item
from helpers.change.live_report_picker import create_and_open_live_report
from helpers.flows import add_compound
from helpers.selection.data_and_columns import RATIONALE_EDIT_ICON
from helpers.selection.rationale import RATIONALE_SAVE, EDIT_DEFAULT_RATIONALE_WINDOW_TEXTBOX, RATIONALE_TEXTAREA
from helpers.verification.grid import verify_grid_contents, verify_column_contents
from library import dom, base, simulate


@pytest.mark.usefixtures("open_project")
def test_rationale(selenium):
    """
     Testing basic Rationale functionality in LiveDesign.

     :param selenium: Selenium WebDriver

    """
    # --------- Creating a new LR with a default rationale --------- #
    lr_one = create_and_open_live_report(selenium,
                                         report_name='Test_Default_Rationale',
                                         rationale='LR with a default rationale')

    # Adding three compounds and checking the desired rationale is applied
    open_add_compounds_panel(selenium)
    idlist_test_rationale = 'CHEMBL1051,CRA-035507,CHEMBL1031'
    add_compound.search_by_id(selenium, idlist_test_rationale)

    close_add_compounds_panel(selenium)

    # Verification that the default rationale is applied
    rationale_one = 'demo:\nLR with a default rationale'
    verify_grid_contents(selenium, {'Rationale': [rationale_one] * 3})

    # -------- Edit the Default Rationale for the first row -------- #
    # Extract this section into a helper in future if more tests require this functionality
    rationale_cell = get_cell(selenium, 'CHEMBL1031', 'Rationale')
    simulate.click(selenium, rationale_cell)
    dom.click_element(selenium, RATIONALE_EDIT_ICON)
    dom.set_element_value(selenium, RATIONALE_TEXTAREA, 'The default rationale has been changed now')
    dom.click_element(selenium, RATIONALE_SAVE)

    # Verification that the rationale is edited
    rationale_two = 'demo:\nThe default rationale has been changed now'
    verify_column_contents(selenium, 'Rationale', [rationale_two, rationale_one, rationale_one])
    click_lr_dropdown_and_edit_rationale(selenium,
                                         lr_one,
                                         rationale_text='Default rationale cannot be changed from LR dropdown')

    # Verification that the edited rationale is not updated in any of the cells
    verify_column_contents(selenium, 'Rationale', [rationale_two, rationale_one, rationale_one])

    # ------- Create a new LR and edit the default rationale -------- #
    lr_second = create_and_open_live_report(selenium, report_name='Default_Rationale_2')
    open_add_compounds_panel(selenium)
    id_list_test_edit_rationale = 'CHEMBL1069,CHEMBL1072'
    add_compound.search_by_id(selenium, id_list_test_edit_rationale)
    click_lr_dropdown_and_edit_rationale(selenium, lr_second, rationale_text='These are random compounds used for test')

    # Verification that the edit Default Rationale from LR dropdown works
    rationale_three = 'demo:\nThese are random compounds used for test'
    verify_column_contents(selenium, 'Rationale', [rationale_three] * 2)


def click_lr_dropdown_and_edit_rationale(driver, live_report_name, rationale_text=''):
    """
    From the LR dropdown clicks on Edit Default Rationale.
    Then applies a default rationale for the LR.

    :param driver: WebDriver
    :param live_report_name: str, Live Report Name
    :param rationale_text: str, the text for the edit default rationale box

    """
    switch_to_live_report(driver, live_report_name)
    click_live_report_menu_item(driver, live_report_name, 'Edit Default Rationale…')
    dom.set_element_value(driver, EDIT_DEFAULT_RATIONALE_WINDOW_TEXTBOX, rationale_text)
    base.click_ok(driver)
