import pytest

from helpers.api.actions.ligand_designer import create_explicit_ligand_designer_config
from helpers.api.extraction.ligand_designer_attachment_id import get_attachment_id
from requests import RequestException
from helpers.api.verification.general import verify_error_response
from library.utils import make_unique_name
from library.utils import is_k8s

# Using the following credentials to create an ldclient obj(login) as it has access to JS Testing project(Project ID: 4)
# This user does not have access to "RestrictedAB" Project (Project ID: 6)
test_username = 'userC'
test_password = 'userC'


@pytest.mark.xfail(not is_k8s(), reason="SS-42724: Explicit config fails to create on Old Jenkins testserver")
@pytest.mark.smoke
@pytest.mark.parametrize("ref_ligand_file, ref_grid_file",
                         [('ligand0.pse', 'thrombin_grid.zip'),
                          ('thrombin_reference_modified.mae', 'glide-grid_4eiy_2Waters.zip'),
                          ('ligand.maegz', 'thrombin_grid.zip')])
def test_create_lig_designer_config_valid_cases(ld_api_client, ref_ligand_file, ref_grid_file):
    """
    create explicit ligand designer configuration with valid reference ligands and grid files: Positive validation

    :param ld_api_client: fixture which creates api client
    :param ref_ligand_file: reference ligand object
    :param ref_grid_file: grid file object
    """
    ref_ligand_obj = get_attachment_id(ld_api_client, filename=ref_ligand_file, attachment_type='THREE_D')
    grid_file_obj = get_attachment_id(ld_api_client, filename=ref_grid_file, attachment_type='ATTACHMENT')

    # Step 1: Use attachments, name & project ids to create the explicit configuration
    explicit_test_config = create_explicit_ligand_designer_config(ld_api_client,
                                                                  name=make_unique_name('Test Docking'),
                                                                  ref_ligand=ref_ligand_obj,
                                                                  grid_file=grid_file_obj,
                                                                  project_ids=[4])
    # Step 2: Validating creation of explicit configuration
    # addable_column_id can also be verified with name of column and column_type
    # explicit configs have unique column_type 'ligand_designer'
    column_list = ld_api_client.get_addable_columns_by_ids([explicit_test_config.addable_column_id])
    assert len(column_list) == 1, "addable_column_id not unique"
    assert column_list[0].name == explicit_test_config.name, "configuration name is not matching"
    assert str(column_list[0].column_type) == 'ligand_designer', "Column type is incorrect"


# Defining Test inputs for Negative validation
# Error thrown for incorrect grid file type is:
# 'Protein extraction from grid file failed. Reason: {"error":"Only zip file is allowed"}'
grid_file_error = 'Only zip file is allowed'
# Error thrown for incorrect ref. ligand file type is: 'The attachment <filename> has unsupported file type'
ref_ligand_error = 'unsupported file type'

unsupported_ref_ligand_file_supported_grid_file = ('valid_sdf_real.sdf', 'thrombin_grid.zip', [4], '400',
                                                   ref_ligand_error)
supported_ref_ligand_file_unsupported_grid_file = ('thrombin_reference_modified.mae',
                                                   'test_register_compounds_via_csv.txt', [4], '400', grid_file_error)
supported_ref_ligand_file_supported_grid_file_invalid_project_id = ('thrombin_reference_modified.mae',
                                                                    'thrombin_grid.zip', [-1
                                                                                         ], '403', 'Permission denied')
supported_ref_ligand_file_supported_grid_file_inaccessible_project = ('thrombin_reference_modified.mae',
                                                                      'thrombin_grid.zip', [6], '403',
                                                                      'Permission denied')


@pytest.mark.xfail(not is_k8s(), reason="SS-42724: Explicit config fails to create on Old Jenkins testserver")
@pytest.mark.smoke
@pytest.mark.parametrize("ref_ligand_file, ref_grid_file, project_id_to_register, error_code, error_message", [
    unsupported_ref_ligand_file_supported_grid_file, supported_ref_ligand_file_unsupported_grid_file,
    supported_ref_ligand_file_supported_grid_file_invalid_project_id,
    supported_ref_ligand_file_supported_grid_file_inaccessible_project
])
def test_create_lig_designer_config_invalid_cases(ld_api_client, ref_ligand_file, ref_grid_file, project_id_to_register,
                                                  error_code, error_message):
    """
    Test create explicit Ligand Designer configuration function : Negative validation

    :param ld_api_client: fixture which creates api client
    :param ref_ligand_file: reference ligand object
    :param ref_grid_file: grid file object
    :param project_id_to_register: list of project ids
    :param error_code: expected error code
    :param error_message: error thrown when configuration fails to create
    """
    ref_ligand_obj = get_attachment_id(ld_api_client, filename=ref_ligand_file, attachment_type='THREE_D')
    grid_file_obj = get_attachment_id(ld_api_client, filename=ref_grid_file, attachment_type='ATTACHMENT')

    with pytest.raises(RequestException) as error_response:
        create_explicit_ligand_designer_config(ld_api_client,
                                               name=make_unique_name('Test Docking'),
                                               ref_ligand=ref_ligand_obj,
                                               grid_file=grid_file_obj,
                                               project_ids=project_id_to_register)
    verify_error_response(error_response.value, expected_status_code=error_code, expected_error_message=error_message)
