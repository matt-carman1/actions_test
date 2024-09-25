import pytest

from helpers.change.freeform_column_action import create_ffc, edit_picklist_ffc_cell, add_remove_picklist_ffc_item
from helpers.verification.grid import verify_column_contents

# Set LiveReport to duplicate
live_report_to_duplicate = {'livereport_name': 'Test Reactants - Nitriles', 'livereport_id': '2553'}


@pytest.mark.app_defect(reason="SS-34048")
@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_ffc_unpublished_multiselect_picklist(selenium):
    """
    Test creation, cell selection, and editing of multiselect picklist type freeform column.

    :param selenium: Webdriver
    :return:
    """
    description = 'This is a multiselect picklist text FFC'
    multiselect_picklist_text_ffc = 'Multiselect picklist FFC'
    values = ['multiselect1', 'multiselect2', 'multiselect3', 'multiselect4', 'multiselect5']

    # Creating an FFC of multiselect picklist type
    create_ffc(selenium,
               multiselect_picklist_text_ffc,
               description,
               allow_any_value=False,
               picklist_values=values[0:4],
               multiselect_in_picklist=True,
               publish=False)

    # Selecting multiple values at once from the picklist type FFC
    edit_picklist_ffc_cell(selenium, multiselect_picklist_text_ffc, 'V047518', values=values[0:2], multiselect=True)
    edit_picklist_ffc_cell(selenium, multiselect_picklist_text_ffc, 'V055820', values=values[1:4], multiselect=True)

    # Verifying contents of the column after editing the FFC
    verify_column_contents(selenium, multiselect_picklist_text_ffc,
                           ['multiselect1\nmultiselect2', '', 'multiselect2\nmultiselect3\nmultiselect4', '', '', ''])

    # Editing the existing picklist definition to remove one value and add another value
    add_remove_picklist_ffc_item(selenium,
                                 multiselect_picklist_text_ffc,
                                 value_to_remove=values[0],
                                 value_to_add=values[4])

    # Selecting new values from the edited picklist
    edit_picklist_ffc_cell(selenium, multiselect_picklist_text_ffc, 'V055821', values=values[3:], multiselect=True)
    # Verifying contents of the column after editing.
    # Note this also checks that the old value is not deleted and is placed at the end of the list
    verify_column_contents(selenium, multiselect_picklist_text_ffc, [
        'multiselect2\nmultiselect1', '', 'multiselect2\nmultiselect3\nmultiselect4', 'multiselect4\nmultiselect5', '',
        ''
    ])
