import logging

import pytest

from requests import RequestException

from helpers.api.actions.compound import load_compounds_from_csv
from helpers.api.actions.row import add_rows_to_live_report
from helpers.api.verification.live_report import verify_live_report_columns, verify_live_report_compounds
from helpers.api.verification.general import verify_error_response
from helpers.extraction import paths
from library.utils import is_k8s

logger = logging.getLogger(__name__)

data_path = paths.get_resource_path("api/")

test_type = 'api'


@pytest.mark.xfail(not is_k8s(), reason="SS-43040: Old data dump in old jenkins causes test to fail")
def test_import_compounds_only_with_load_csv(ld_api_client, new_live_report):
    """
    Test import compounds only

    :param ld_api_client: LDClient, ldclient object
    :param new_live_report: LiveReport, fixture which created livereport
    """
    lr_id = new_live_report.id
    # Import columns only without publishing data
    compound_ids = load_compounds_from_csv(ld_api_client,
                                           lr_id,
                                           filename='{}/test_load_csv.csv'.format(data_path),
                                           project_name='JS Testing',
                                           is_compounds_only=True)

    # verify compounds and columns
    assert ['V046171', 'V055836'] == sorted(compound_ids)
    verify_live_report_compounds(ld_api_client, lr_id, expected_compound_ids=compound_ids)
    verify_live_report_columns(ld_api_client, lr_id, expected_column_count=8)

    # Import columns only with publish data
    compound_ids = load_compounds_from_csv(ld_api_client,
                                           lr_id,
                                           filename='{}/test_load_csv.csv'.format(data_path),
                                           project_name='JS Testing',
                                           is_published=True)

    # verify columns and compounds
    assert ['V046171', 'V055836'] == sorted(compound_ids)
    verify_live_report_compounds(ld_api_client, lr_id, expected_compound_ids=compound_ids)
    verify_live_report_columns(ld_api_client, lr_id, expected_column_count=8)


@pytest.mark.xfail(not is_k8s(), reason="SS-43040: Old data dump in old jenkins causes test to fail")
def test_import_compounds_and_columns_with_load_csv(ld_api_client, new_live_report):
    """
    Test load compounds with columns data using load_csv

    :param ld_api_client: LDClient, ldclient object
    :param new_live_report: LiveReport, fixture which creates livereport
    """
    lr_id = new_live_report.id
    # Import compounds and columns without publishing data
    compound_ids = load_compounds_from_csv(ld_api_client,
                                           lr_id,
                                           filename='{}/test_load_csv.csv'.format(data_path),
                                           is_columns_only=False,
                                           is_compounds_only=False,
                                           project_name='JS Testing')

    assert ['V046171', 'V055836'] == sorted(compound_ids)
    verify_live_report_compounds(ld_api_client, lr_id, expected_compound_ids=compound_ids)
    verify_live_report_columns(ld_api_client, lr_id, expected_column_count=14)

    # Import compounds and columns with publishing data
    compound_ids = load_compounds_from_csv(ld_api_client,
                                           lr_id,
                                           filename='{}/test_load_csv.csv'.format(data_path),
                                           is_columns_only=False,
                                           is_compounds_only=False,
                                           project_name='JS Testing',
                                           is_published=True)
    # validating compounds and columns
    assert ['V046171', 'V055836'] == sorted(compound_ids)
    verify_live_report_compounds(ld_api_client, lr_id, expected_compound_ids=compound_ids)
    verify_live_report_columns(ld_api_client, lr_id, expected_column_count=14)


@pytest.mark.app_defect(reason="SS-37664: Adding rows times out")
def test_import_columns_only_with_load_csv(ld_api_client, new_live_report):
    """
    Test import columns only with load_csv method

    :param ld_api_client: LDClient, ldclient object
    :param new_live_report: LiveReport, fixture which creates livereport
    """
    lr_id = new_live_report.id
    # Import columns only to empty livereport
    compound_ids = load_compounds_from_csv(ld_api_client,
                                           lr_id,
                                           filename='{}/test_load_csv.csv'.format(data_path),
                                           is_columns_only=True,
                                           is_compounds_only=False,
                                           project_name='JS Testing')
    # validating no columns, compounds added to lr
    assert [] == sorted(compound_ids)
    verify_live_report_compounds(ld_api_client, lr_id, expected_compound_ids=compound_ids)
    verify_live_report_columns(ld_api_client, lr_id, expected_column_count=8)

    # adding compound to LR to test columns only import
    add_rows_to_live_report(ld_api_client, live_report_id=lr_id, corporate_ids=['V055836'])
    # Import columns only to live report
    compound_ids = load_compounds_from_csv(ld_api_client,
                                           lr_id,
                                           filename='{}/test_load_csv.csv'.format(data_path),
                                           is_columns_only=True,
                                           is_compounds_only=False,
                                           project_name='JS Testing',
                                           column_identifier='ID',
                                           compound_identifier_type='CSV_CORP_ID')
    # verify whether columns only added to live report
    assert ['V055836'] == sorted(compound_ids)
    verify_live_report_compounds(ld_api_client, lr_id, expected_compound_ids=compound_ids)
    verify_live_report_columns(ld_api_client, lr_id, expected_column_count=14)


@pytest.mark.parametrize('identifier, expected_compound_ids, expected_column_count',
                         [('ID', ['V046171', 'V055836'], 14), ('All IDs', ['CRA-035000', 'CRA-035001'], 14),
                          ('Boolean - Published', [], 8)])
@pytest.mark.app_defect(reason="SS-37463")
def test_import_with_different_identifiers(ld_api_client, new_live_report, identifier, expected_compound_ids,
                                           expected_column_count):
    """
    Test import compounds with different column identifiers.

    :param ld_api_client: LDClient, ldclient object
    :param new_live_report: LiveReport, fixtures which creates Livereport
    :param identifier: str, column identifier
    :param expected_compound_ids: list, list of expected compound ids
    :param expected_column_count:int, expected number of columns present in lr after loading compounds
    """
    lr_id = new_live_report.id

    logger.info("Import compounds and columns with identifier : {}".format(identifier))
    # import compounds and columns with identifier
    compound_ids = load_compounds_from_csv(ld_api_client,
                                           lr_id,
                                           filename='{}/test_load_csv.csv'.format(data_path),
                                           is_columns_only=False,
                                           is_compounds_only=False,
                                           project_name='JS Testing',
                                           column_identifier=identifier,
                                           compound_identifier_type='CSV_CORP_ID')
    # verify whether compounds registered into live report
    assert sorted(expected_compound_ids) == sorted(compound_ids)
    verify_live_report_compounds(ld_api_client, lr_id, expected_compound_ids=compound_ids)
    verify_live_report_columns(ld_api_client, lr_id, expected_column_count=expected_column_count)


def test_load_csv_with_negative_data(ld_api_client, new_live_report):
    """
    Test load csv with negative test samples.

    :param ld_api_client: LDClient, ldclient object
    :param new_live_report: LiveReport, fixture which creates livereport
    """
    lr_id = new_live_report.id

    # Test import compounds by choosing compounds_only=True and columns_only=True
    with pytest.raises(RequestException):
        error_response = load_compounds_from_csv(ld_api_client,
                                                 lr_id,
                                                 filename='{}/test_load_csv.csv'.format(data_path),
                                                 is_columns_only=True,
                                                 is_compounds_only=True,
                                                 project_name='JS Testing')
        verify_error_response(error_response,
                              expected_status_code='400',
                              expected_error_message='Must choose either compounds only or columns only import')

    # Test import compounds with invalid lr(integer)
    with pytest.raises(RequestException):
        inv_lr_error_response = load_compounds_from_csv(ld_api_client,
                                                        '-1',
                                                        filename='{}/test_load_csv.csv'.format(data_path),
                                                        is_compounds_only=True,
                                                        project_name='JS Testing')
        verify_error_response(inv_lr_error_response,
                              expected_status_code='400',
                              expected_error_message='One or more of the specified LiveReports do not exist')

    # Test import compounds with invalid lr(string)
    with pytest.raises(RequestException):
        inv_str_lr_error_response = load_compounds_from_csv(ld_api_client,
                                                            'invalid',
                                                            filename='{}/test_load_csv.csv'.format(data_path),
                                                            is_compounds_only=True,
                                                            project_name='JS Testing')
        verify_error_response(inv_str_lr_error_response,
                              expected_status_code='400',
                              expected_error_message='Must pass valid data import settings')

    # Test import with invalid file type
    with pytest.raises(RequestException):
        inv_file_error_response = load_compounds_from_csv(ld_api_client,
                                                          lr_id,
                                                          filename='{}/stereo_reals.sdf'.format(data_path),
                                                          is_compounds_only=True,
                                                          project_name='JS Testing')
        verify_error_response(inv_file_error_response,
                              expected_status_code='400',
                              expected_error_message='Must pass valid data import settings')

    # Test import with invalid project name
    with pytest.raises(RequestException):
        inv_project_error_response = load_compounds_from_csv(ld_api_client,
                                                             lr_id,
                                                             filename='{}/test_load_csv.csv'.format(data_path),
                                                             is_compounds_only=True,
                                                             project_name='-1')
        verify_error_response(inv_project_error_response,
                              expected_status_code='400',
                              expected_error_message='Must pass valid data import settings')
