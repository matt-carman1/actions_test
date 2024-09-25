import pytest
from requests import RequestException
from helpers.api.verification.general import verify_error_response
from helpers.api.verification.model import verify_expected_protocols_names_exists_in_protocols_found

# Logging in as userA
test_username = 'userA'
test_password = 'userA'


def test_get_and_verify_protocols_by_project_id(ld_api_client):
    """
    Test to get protocols by project ids and verify them.

    :param ld_api_client: LDClient, ldclient object
    """
    # Protocols associated with project_id: 0, project_name: 'Global'
    protocols_global = ld_api_client.get_protocols_by_project_id(project_ids=['0'])
    expected_protocol_names = [
        'Realtime 3D Protocol With Overlay', 'Jchem cxcalc', 'JChem LIBMCS', 'CTR Schrodinger Python', 'Canvas KMeans',
        'Glide 3D Builder', 'Fake 3D Model with 2 Poses', 'canvasMolDescriptors', 'Schrodinger Python', 'LigPrep',
        'Fake 3D Model', 'KNIME HTVS 3D', 'Realtime 3D Protocol Without Overlay', 'Test Async Template',
        'Test Schrodinger Empty Python Template', 'Test Schrodinger Python Template', 'JS Test Sleep and Fail',
        'JS Test Model Pending', 'JS Test Realtime', 'Schrodinger Python w/ Column Data', 'GUI_DeepQSAR',
        'JS Test Cat Python 3 Results', 'Generic Entity Protocol'
    ]
    verify_expected_protocols_names_exists_in_protocols_found(protocols_global, expected_protocol_names)

    # TODO: Currently, all protocols mentioned above are the only protocols available in the starter data
    #  and are associated with project_id: 0, project_name: 'Global'
    #  Once, protocols based on project_id: 6 is added, multi-project protocol verification can be added.

    # Attempting to get protocols for project_id: '4', project_name:'JS Testing', non-accessible to userA
    with pytest.raises(RequestException) as error:
        ld_api_client.get_protocols_by_project_id(project_ids=['4'])
    verify_error_response(error.value, '400', 'ACLs missing for requested project: [4]')

    # Invalid Project IDs
    with pytest.raises(RequestException) as error:
        ld_api_client.get_protocols_by_project_id(project_ids=['-1'])
    verify_error_response(error.value, '400', 'ACLs missing for requested project: [-1]')

    with pytest.raises(RequestException) as error:
        ld_api_client.get_protocols_by_project_id(project_ids=['12043'])
    verify_error_response(error.value, '400', 'ACLs missing for requested project: [12043]')
