import time
import pytest

from library import utils

from ldclient.models import FreeformColumn, LiveReport
from helpers.api.actions.freeform_column import create_freeform_column_using_ffc_object
from helpers.api.flows.freeform_columns import add_values_for_ffcs
from helpers.api.extraction.livereport import get_column_ids_by_name
from helpers.api.verification.live_report import verify_column_values_for_compounds

live_report_to_duplicate = {'livereport_name': 'Compound', 'livereport_id': '1548'}
test_type = 'api'


def test_compare_ffc_value_changes_between_original_and_duplicate_lrs(ld_api_client, duplicate_live_report):
    """
    Test to verify published and unpublished FFC value changes on original LR based on the changes made in duplicate LR
    Steps Involved:
        i) Duplicating an existing LR with atleast one compound
        ii) Create/Add a Published and Unpublished FFC into the LR and verify
        iii) Create/Add observations (values) for both the columns for one row and verify
        iv) Duplicate the LR
        v) Create/Add new observations (values) for the columns in duplicate LR and verify
        vi) Verify that the observation related to published FFC has changed but not for unpublished FFC

    :param ld_api_client: Fixture which creates API Client
    :param duplicate_live_report: Fixture which duplicated an existing LR
    """
    entity_id = 'V055812'
    original_lr_id = duplicate_live_report.id
    project_id = duplicate_live_report.project_id

    # Creating a published FFC
    published_ffc_name = utils.make_unique_name('PublishedFFC')
    published_ffc_object = FreeformColumn(name=published_ffc_name,
                                          type=FreeformColumn.COLUMN_TEXT,
                                          description='Published FFC created with API Test',
                                          project_id=project_id,
                                          live_report_id=original_lr_id,
                                          published=True)
    published_ffc = create_freeform_column_using_ffc_object(ld_api_client, ffc_obj=published_ffc_object)

    # Creating an unpublished FFC
    unpublished_ffc_name = utils.make_unique_name('UnpublishedFFC')
    unpublished_ffc_object = FreeformColumn(name=unpublished_ffc_name,
                                            type=FreeformColumn.COLUMN_TEXT,
                                            description='Unpublished FFC created with API Test',
                                            project_id=project_id,
                                            live_report_id=original_lr_id,
                                            published=False)
    unpublished_ffc = create_freeform_column_using_ffc_object(ld_api_client, ffc_obj=unpublished_ffc_object)

    # Adding both FFCs into LR
    original_lr_ffc_ids = [published_ffc.id, unpublished_ffc.id]
    ld_api_client.add_columns(live_report_id=original_lr_id, addable_columns=original_lr_ffc_ids)

    # Adding and verifying values for both FFCs
    add_values_for_ffcs(ld_api_client,
                        project_id,
                        original_lr_id,
                        input_info={
                            original_lr_ffc_ids[0]: {
                                entity_id: 'TestString#010'
                            },
                            original_lr_ffc_ids[1]: {
                                entity_id: '92.221'
                            }
                        })

    time.sleep(2)

    expected_original_lr_values = {entity_id: ['TestString#010', '92.221']}
    verify_column_values_for_compounds(ld_api_client,
                                       livereport_id=original_lr_id,
                                       column_ids=original_lr_ffc_ids,
                                       expected_values=expected_original_lr_values)

    # Duplicate/Copy the LR
    lr_obj = LiveReport(title=utils.make_unique_name(duplicate_live_report.title), project_id=project_id)
    duplicate_lr = ld_api_client.copy_live_report(template_id=original_lr_id, live_report=lr_obj)
    duplicate_lr_id = duplicate_lr.id

    # Retrieving columns ids for specific column names in the LR
    duplicate_lr_ffc_ids = get_column_ids_by_name(ld_api_client,
                                                  duplicate_lr_id,
                                                  column_names=[published_ffc_name, unpublished_ffc_name])

    # Creating and adding values for both FFCs
    add_values_for_ffcs(ld_api_client,
                        project_id,
                        duplicate_lr_id,
                        input_info={
                            duplicate_lr_ffc_ids[0]: {
                                entity_id: 'RandomValue@339'
                            },
                            duplicate_lr_ffc_ids[1]: {
                                entity_id: '34.67'
                            }
                        })

    time.sleep(2)

    expected_duplicate_lr_values = {entity_id: ['RandomValue@339', '34.67']}
    verify_column_values_for_compounds(ld_api_client,
                                       livereport_id=duplicate_lr_id,
                                       column_ids=duplicate_lr_ffc_ids,
                                       expected_values=expected_duplicate_lr_values)

    time.sleep(2)

    # Checking FFC value changes on original LR based on the changes made in duplicate LR
    expected_final_lr_values = {entity_id: ['RandomValue@339', '92.221']}
    verify_column_values_for_compounds(ld_api_client,
                                       livereport_id=original_lr_id,
                                       column_ids=original_lr_ffc_ids,
                                       expected_values=expected_final_lr_values)

    # Deleting duplicated LR at the end
    ld_api_client.delete_live_report(duplicate_lr_id)
