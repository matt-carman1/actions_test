import pytest

from ldclient.models import ColumnGroup
from helpers.api.actions.column import add_columns_to_live_report, replace_column_groups, \
    get_column_groups_by_live_report_id
from helpers.api.verification.general import verify_error_response
from helpers.verification.grid import verify_column_group_contents

live_report_to_duplicate = {'livereport_name': 'RPE Test', 'livereport_id': 2048}
test_type = 'api'


def test_column_group(ld_api_client, duplicate_live_report):
    """
    Test grouping and ungrouping columns in a LiveReport

    :param ld_api_client: LDClient, ldclient object
    :param duplicate_live_report: fixture which duplicates livereport
    """
    # TODO: (kundu) May want to revisit this test and separate group & ungroup once QA-6231 is done
    # defining addable ids required throughout the test
    addable_column_id_to_add = ['3594']
    compound_structure_addable_id = ['1228']
    pk_group_addable_id = ['606', '159']
    assay_group_addable_id = ['3186', '16']
    ffc_mpo_group_addable_id = ['3594', '3938']

    live_report_id = duplicate_live_report.id

    # Adding ffc column to the LR to make the data more robust
    add_columns_to_live_report(ld_api_client, live_report_id, column_ids=addable_column_id_to_add)

    # Defining a column group with Compound Structure column
    # It was observed that the addable_column_id for a formula column varies (with builds) making the test flaky,
    # so I decided to not consider it for grouping.
    new_column_group_def = [
        ColumnGroup(name='Compound Structure',
                    frozen=False,
                    columns_order=compound_structure_addable_id,
                    limiting_condition=None),
        ColumnGroup(name='PK_group', frozen=False, columns_order=pk_group_addable_id, limiting_condition=None),
        ColumnGroup(name='Assay_group', frozen=False, columns_order=assay_group_addable_id, limiting_condition=None),
        ColumnGroup(name='FFC_MPO_group', frozen=False, columns_order=ffc_mpo_group_addable_id, limiting_condition=None)
    ]

    # Updating column groups in the duplicated LR.
    replace_column_groups(ld_api_client, live_report_id, list_of_column_groups=new_column_group_def, ungroup_mode=None)

    # Defining a fake column group without a compound structure column
    fake_column_group_def = new_column_group_def[2:]

    # Handling error where compound Structure has to be the first column of a column group
    with pytest.raises(Exception) as error_response:
        replace_column_groups(ld_api_client,
                              live_report_id,
                              list_of_column_groups=fake_column_group_def,
                              ungroup_mode=None)

    verify_error_response(error_response.value,
                          expected_status_code=400,
                          expected_error_message='The Compound Structure column must be the first column in the '
                          'LiveReport')

    # Verification that all the column orders and names are intact and as expected in the duplicated LR.
    list_of_column_groups = get_column_groups_by_live_report_id(ld_api_client, live_report_id)

    verify_column_group_contents(list_of_column_groups, new_column_group_def)

    # Ungrouping two of the four column groups
    ungrouped_columns_info = [
        ColumnGroup(name='Compound Structure',
                    frozen=False,
                    columns_order=compound_structure_addable_id,
                    limiting_condition=None),
        ColumnGroup(name=None, frozen=False, columns_order=['606'], limiting_condition=None),
        ColumnGroup(name=None, frozen=False, columns_order=['3186'], limiting_condition=None),
        ColumnGroup(name='FFC_MPO_group', frozen=False, columns_order=ffc_mpo_group_addable_id,
                    limiting_condition=None),
        ColumnGroup(name=None, frozen=False, columns_order=['159'], limiting_condition=None),
        ColumnGroup(name=None, frozen=False, columns_order=['16'], limiting_condition=None)
    ]

    # Updating the duplicate LR with ungrouped columns
    replace_column_groups(ld_api_client,
                          live_report_id,
                          list_of_column_groups=ungrouped_columns_info,
                          ungroup_mode=None)

    # Verification that all the column orders and names are intact and as expected after ungrouping column groups
    ungrouped_col_grp = get_column_groups_by_live_report_id(ld_api_client, live_report_id)

    verify_column_group_contents(ungrouped_col_grp, ungrouped_columns_info)
