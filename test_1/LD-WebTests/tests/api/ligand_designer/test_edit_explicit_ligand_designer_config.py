import pytest

from requests import RequestException
from helpers.api.verification.general import verify_error_response
from library.utils import is_k8s


@pytest.mark.xfail(not is_k8s(), reason="SS-42724: Explicit config fails to create on Old Jenkins testserver")
@pytest.mark.smoke
def test_edit_explicit_ligand_designer_config(ld_api_client, create_explicit_lig_designer_config_via_api):
    """
    Edit an explicit ligand designer configuration created via api

    :param ld_api_client: fixture which creates api client
    :param create_explicit_lig_designer_config_via_api: fixture to create an explicit Ligand Designer configuration
    """
    test_ligand_designer_config = create_explicit_lig_designer_config_via_api

    # Update configuration by updating project_id list
    # valid update: Positive validation
    test_ligand_designer_config.project_ids.append('0')
    config_updated = ld_api_client.update_columnar_ligand_designer_configuration(test_ligand_designer_config.id,
                                                                                 test_ligand_designer_config)
    assert config_updated.project_ids == ['4', '0'], "Project id list not updated" \
                                                     "Projects IDs attached to the ligand designer configuration are {config_updated.project_ids}"

    # invalid update: Negative validation
    with pytest.raises(RequestException) as error_response:
        config_updated.project_ids = [-1]
        ld_api_client.update_columnar_ligand_designer_configuration(config_updated.id, config_updated)
    verify_error_response(error_response.value, expected_status_code='403', expected_error_message='Permission denied')

    # Update configuration by updating config name
    create_explicit_lig_designer_config_via_api.name = "Test Docking_updated"
    ld_api_client.update_columnar_ligand_designer_configuration(test_ligand_designer_config.id,
                                                                test_ligand_designer_config)
    column_list_updated = ld_api_client.get_addable_columns_by_ids([test_ligand_designer_config.addable_column_id])
    assert column_list_updated[0].name == "Test Docking_updated", "Configuration name not updated"
