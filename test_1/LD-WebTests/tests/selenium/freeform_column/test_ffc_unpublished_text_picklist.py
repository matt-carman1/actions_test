import pytest

from helpers.change.freeform_column_action import create_ffc, add_remove_picklist_ffc_item, edit_picklist_ffc_cell
from helpers.verification.data_and_columns_tree import verify_no_column_exists_in_column_tree
from helpers.verification.grid import verify_column_contents

# Set LiveReport to duplicate
live_report_to_duplicate = {'livereport_name': 'FFC Selenium Test LR', 'livereport_id': '2304'}


@pytest.mark.k8s_defect(reason="SS-42609: Newly added picklist item doesn't appear as an option")
@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_ffc_unpublished_text_picklist(selenium):
    """
    Test creation, cell selection, and editing of unpublished picklist text type freeform column.

    :param selenium: Webdriver
    :return:
    """
    description = 'This is a picklist text FFC'
    unpublished_picklist_text_ffc = 'FFC 1'
    values = ['Text1', 'Text2', 'Text3']
    # Creating an FFC of picklist type
    create_ffc(selenium,
               unpublished_picklist_text_ffc,
               description,
               allow_any_value=False,
               picklist_values=values,
               publish=False)

    # Selecting values from the picklist type FFC
    edit_picklist_ffc_cell(selenium, unpublished_picklist_text_ffc, 'CRA-031437', values=values[0])
    edit_picklist_ffc_cell(selenium, unpublished_picklist_text_ffc, 'CRA-035504', values=values[2])

    # Verifying contents of the column after editing the FFC
    verify_column_contents(selenium, unpublished_picklist_text_ffc, ['Text1', '', 'Text3', '', ''])

    # Editing the existing picklist definition to remove one value and add another value
    add_remove_picklist_ffc_item(selenium, unpublished_picklist_text_ffc, value_to_remove='Text1', value_to_add='Text4')

    # Selecting new values from the edited picklist
    edit_picklist_ffc_cell(selenium, unpublished_picklist_text_ffc, 'CRA-035503', values='Text4')
    verify_column_contents(selenium, unpublished_picklist_text_ffc, ['Text1', 'Text4', 'Text3', '', ''])

    # Search D&C tree for FFC column name (Since this is unpublished, it should only exist in the context of the LR
    verify_no_column_exists_in_column_tree(selenium, unpublished_picklist_text_ffc)
