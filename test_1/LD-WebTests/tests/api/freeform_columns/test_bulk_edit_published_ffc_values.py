import time

import pytest

from helpers.api.actions.column import add_freeform_values
from helpers.api.actions.freeform_column import bulk_delete_ffc_values, create_bulk_ffc_observations, \
    bulk_edit_ffc_values
from helpers.api.verification.freeform_columns import verify_bulk_ffc_values
from library.utils import is_k8s

live_report_to_duplicate = {'livereport_name': 'FFC - All types, published and unpublished', 'livereport_id': '1299'}
test_type = 'api'


@pytest.mark.serial
@pytest.mark.xfail(not is_k8s(),
                   reason="api call for inserting FFC values are appending to existing value in cell "
                   "for few cells in old jenkins")
def test_bulk_edit_published_ffc_values(ld_api_client, duplicate_live_report):
    """
    Test bulk edit on published FFC columns

    :param ld_api_client: LDClient object
    :param duplicate_live_report: fixture to duplicate an existing LiveReport
    """
    lr_id = duplicate_live_report.id
    lr_compound_ids = [
        'CRA-031137', 'CRA-031437', 'CRA-031925', 'CRA-031965', 'CRA-031978', 'CRA-032348', 'CRA-032370', 'CRA-032372',
        'CRA-032373', 'CRA-032411', 'CRA-032412', 'CRA-032428', 'CRA-032429', 'CRA-032430', 'CRA-032431', 'CRA-032432',
        'CRA-032433', 'CRA-032434', 'CRA-032435', 'CRA-032436', 'CRA-032458', 'CRA-032459', 'CRA-032474', 'CRA-032479',
        'CRA-032481'
    ]

    # Addable Column id of Text type published FFC column: "Text  - published"
    text_type_published_ffc_id = '3594'
    # Bulk add/edit the FFC value
    bulk_edit_ffc_values(ld_api_client, lr_id, text_type_published_ffc_id, lr_compound_ids, ffc_value="FFC Value")

    expected_cell_values = ['FFC Value']
    # verify if the FFC values show up in duplicated LR
    verify_bulk_ffc_values(ld_api_client, duplicate_live_report.id, [text_type_published_ffc_id], lr_compound_ids,
                           expected_cell_values)
    # verify if the FFC values show up in the original LR
    verify_bulk_ffc_values(ld_api_client, live_report_to_duplicate['livereport_id'], [text_type_published_ffc_id],
                           lr_compound_ids, expected_cell_values)

    # Bulk delete the added ffc values
    bulk_delete_ffc_values(ld_api_client, lr_id, text_type_published_ffc_id, lr_compound_ids)
    # verify if the FFC values are deleted in duplicated LR
    verify_bulk_ffc_values(ld_api_client,
                           duplicate_live_report.id, [text_type_published_ffc_id],
                           lr_compound_ids,
                           expected_cell_values=[''])
    # verify if the FFC values are deleted in the original LR
    verify_bulk_ffc_values(ld_api_client,
                           live_report_to_duplicate['livereport_id'], [text_type_published_ffc_id],
                           lr_compound_ids,
                           expected_cell_values=[''])
