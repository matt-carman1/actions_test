import pytest
from requests import RequestException

from helpers.api.actions.compound import register_compounds_from_csv
from helpers.api.verification.general import verify_error_response
from helpers.api.verification.live_report import verify_live_report_columns
from helpers.extraction import paths
from library.utils import is_k8s

data_path = paths.get_resource_path("api/")


def test_register_compounds_via_csv_with_invalid_lr(ld_api_client):
    """
    Test check register compounds via csv method with invalid livereport

    :param ld_api_client: LDClient, ldclient object
    """
    # passing invalid string for livereport id and check whether we are getting proper error message.
    with pytest.raises(RequestException):
        response = register_compounds_from_csv(ld_api_client,
                                               project_name='JS Testing',
                                               lr_id='Invalid string',
                                               file_name='{}/test_register_compounds_via_csv.csv'.format(data_path))
        verify_error_response(response,
                              expected_status_code='400',
                              expected_error_message='Must pass valid data import settings')

    # passing invalid int(-1) for livereport id and check whether we are getting proper error message.
    with pytest.raises(RequestException):
        response = register_compounds_from_csv(ld_api_client,
                                               project_name='JS Testing',
                                               lr_id='-1',
                                               file_name='{}/test_register_compounds_via_csv.csv'.format(data_path))
        verify_error_response(response,
                              expected_status_code='400',
                              expected_error_message='One or more of the specified LiveReports do not exist')


test_type = 'api'


def test_register_compounds_via_csv_with_invalid_project(ld_api_client, new_live_report):
    """
    Test check register compounds via csv method with invalid project

    :param ld_api_client: fixture to create LDClient object
    :param new_live_report: fixture to create livereport
    """
    lr_id = new_live_report.id
    project_name = "Invalid Project"

    # passing invalid project name and check whether we are getting proper error message.
    with pytest.raises(RequestException):
        response = register_compounds_from_csv(ld_api_client,
                                               project_name=project_name,
                                               lr_id=lr_id,
                                               file_name='{}/test_register_compounds_via_csv.csv'.format(data_path))
        verify_error_response(response,
                              expected_status_code='400',
                              expected_error_message='Project {} does not exist'.format(project_name))


def test_register_compounds_with_unsupported_file(ld_api_client, new_live_report):
    """
    Register compounds with unsupported(txt) file.

    :param ld_api_client: LDClient, ldclient object
    :param new_live_report: fixture which creates livereport
    """
    lr_id = new_live_report.id
    with pytest.raises(RequestException):
        response = register_compounds_from_csv(ld_api_client,
                                               project_name='JS Testing',
                                               lr_id=lr_id,
                                               file_name='{}/test_invalid_file_format.pptx'.format(data_path))
        verify_error_response(response, expected_status_code='400', expected_error_message='Selected file must be CSV')


register_with_str_file_contents = ('{}/test_register_compounds_via_csv.csv'.format(data_path), 'file contents', [])
register_with_file_contents_differ_from_filename = (
    '{}/test_register_compounds_via_csv.csv'.format(data_path),
    'Compound Structure,ID,All IDs,Rationale\nCC(C)NC1=CC=C(C=O)C=N1,CRA-035001,ISOSORBIDE '
    'DINITRATE;V61522;CRA-035001', ['CRA-035001'])


@pytest.mark.skip(reason='SS-33612 ')
@pytest.mark.parametrize('file_name, file_contents_input, expected_compound_ids',
                         [register_with_str_file_contents, register_with_file_contents_differ_from_filename])
def test_register_compounds_via_csv_with_different_file_contents(ld_api_client, new_live_report, file_name,
                                                                 file_contents_input, expected_compound_ids):
    """
    Test register_compounds_via_csv method with various types of files and file contents

    :param ld_api_client: LDClient, ldclient object
    :param new_live_report: LiveReport, fixture for create livereport
    :param file_name: str, name of the file
    :param file_contents_input: str/None, None if you want to use mentioned file_name contents
    :param expected_compound_ids: list, compound ids list
    """
    lr_id = new_live_report.id
    response = register_compounds_from_csv(ld_api_client,
                                           project_name='JS Testing',
                                           lr_id=lr_id,
                                           file_name=file_name,
                                           file_contents_input=file_contents_input)
    # verify compounds and columns
    assert expected_compound_ids == sorted(response)
    verify_live_report_columns(ld_api_client, lr_id, expected_column_count=8)


@pytest.mark.skip(reason='SS-33612')
@pytest.mark.parametrize('column_identifier, expected_compound_ids',
                         [('Compound Structure', ['V047518', 'V047755', 'V055820']), ('invalid', []),
                          ('ID', ['V047518', 'V047755', 'V055820']), ('All IDs', ['V047518', 'V047755', 'V055820'])])
def test_register_compounds_via_csv_with_different_identifiers(ld_api_client, new_live_report, column_identifier,
                                                               expected_compound_ids):
    """
    Test register compounds with different column identifiers

    :param ld_api_client: LDClient
    :param new_live_report: fixture which creates live report
    :param column_identifier: Column identifier
    :param expected_compound_ids: error message for negative test data, list of compound ids for positive test data
    """
    lr_id = new_live_report.id
    compound_ids = register_compounds_from_csv(ld_api_client,
                                               project_name='JS Testing',
                                               lr_id=lr_id,
                                               column_identifier=column_identifier,
                                               file_name='{}/test_register_compounds_via_csv.csv'.format(data_path))

    # verify compounds and columns
    assert expected_compound_ids == sorted(compound_ids)
    verify_live_report_columns(ld_api_client, lr_id, expected_column_count=8)


@pytest.mark.xfail(not is_k8s(), reason="SS-43040: Old data dump in old jenkins causes test to fail")
def test_register_compounds_via_csv_with_import_data(ld_api_client, new_live_report):
    """
    Test register_compounds_via_csv with includes importing data

    :param ld_api_client: LDClient
    :param new_live_report: fixture which creates live report
    """
    lr_id = new_live_report.id
    # registering compounds and columns without publishing data
    compound_ids = register_compounds_from_csv(ld_api_client,
                                               project_name='JS Testing',
                                               lr_id=lr_id,
                                               file_name='{}/test_register_compounds_via_csv.csv'.format(data_path),
                                               import_assay_data=True,
                                               published=False)

    # verify columns and compounds
    assert ['V047518', 'V047755', 'V055820'] == sorted(compound_ids)
    verify_live_report_columns(ld_api_client, lr_id, expected_column_count=11)

    # registering compounds and columns with publishing data
    response = register_compounds_from_csv(ld_api_client,
                                           project_name='JS Testing',
                                           lr_id=lr_id,
                                           file_name='{}/test_register_compounds_via_csv.csv'.format(data_path),
                                           import_assay_data=True,
                                           published=True)

    # verify compounds and columns
    assert ['V047518', 'V047755', 'V055820'] == sorted(response)
    verify_live_report_columns(ld_api_client, lr_id, expected_column_count=11)
