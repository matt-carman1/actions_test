from ldclient.models import (ModelCommand, ModelTemplateVar)
from helpers.api.actions.model import create_model_via_api, archive_models, update_protocol_via_api
from library.utils import make_unique_name
from helpers.api.verification.general import verify_error_response
import pytest

# Protocol data
test_protocol_name = 'Protocol'
test_protocol_commands = [ModelCommand(command='${Length:TEXT-INPUT}', driver_id='1')]
test_protocol_template_vars = [
    ModelTemplateVar(tag='DEFAULT', type='STRING', name='Length', is_optional=False, data="template var data")
]
# the list of available projects in the server is [0, 1, 2, 3, 4, 5, 6, 7, 107]
test_protocol_projects = ['1', '2', '3']
ERROR_MESSAGE_INACCESSIBLE_PROJECT_ID = 'The project IDs provided to create this model [6] do not all exist or are' \
                                        ' not all accessible by the parent'


def test_project_access_for_models(ld_api_client, new_protocol_via_api):
    """
    API test to test project access for models

    a. Create a Protocol which has access to a fixed number of projects
    b. Create a Model using one of the projects and verify it.
    c. Update the Protocol with a new set of project ids.
    d. Update the model to use a new project id and verify.
    e. Update the model to have a project id not in the protocol project ids when the protocol has global project id
    e. Create a Model with invalid project id
    e. Create a Model with a valid project id but is not in the protocol list


    :param ld_api_client: LDClient, a fixture which creates ldclient object
    :param new_protocol_via_api: ldclient.models.Model, fixture which creates protocol
    """

    # Creating a Model based on the protocol with access to one of the projects defined above.
    model_with_project_access = create_model_via_api(ld_api_client,
                                                     make_unique_name('Model1'),
                                                     'description',
                                                     folder=new_protocol_via_api.folder,
                                                     parent=new_protocol_via_api.id,
                                                     project_ids=['2'])

    # Verification that the project id for models and protocols are similar
    model_project_id = model_with_project_access.project_ids
    assert [test_protocol_projects[1]] == model_project_id

    # Updating the protocol to have a new set of project ids now
    new_protocol_via_api.project_ids = ['0', '1', '2', '3', '4']
    update_protocol_via_api(ld_api_client, new_protocol_via_api.id, new_protocol_via_api)

    # Updating the models to now use a different project id
    model_with_project_access.project_ids = ['4']
    ld_api_client.update_model(model_with_project_access.id, model_with_project_access)

    # Verification that the project id for updated models and updated protocols are similar
    model_project_id = model_with_project_access.project_ids
    assert [new_protocol_via_api.project_ids[4]] == model_project_id

    # # Testing for Global ACL in the protocol project ID when the model project id isn't contained in protocol project id
    # # This shouldn't throw an error because if any protocol has Global ACL, it means it has access to every other
    # # project ID & models constructed from them can be assigned any valid project ID
    model_to_test_global_acl = create_model_via_api(ld_api_client,
                                                    make_unique_name('Model'),
                                                    'description',
                                                    folder=new_protocol_via_api.folder,
                                                    parent=new_protocol_via_api.id,
                                                    project_ids=['7'])
    model_project_id = model_to_test_global_acl.project_ids
    assert model_project_id not in new_protocol_via_api.project_ids
    archive_models(ld_api_client, [model_to_test_global_acl])

    # Negative validation for an invalid non-existent project id
    with pytest.raises(Exception) as error_response:
        create_model_via_api(ld_api_client,
                             make_unique_name('Model3'),
                             'description',
                             folder=new_protocol_via_api.folder,
                             parent=new_protocol_via_api.id,
                             project_ids=[10])
    verify_error_response(error_response.value, expected_status_code=403, expected_error_message="Permission denied")

    # NOTE(prakash): Updating the project IDs for the protocol to not contain the GLOBAL_PROJECT
    # SS-33340 : We no longer add global project [0] as the default project_id when no project_ids are specified
    new_protocol_via_api.project_ids = ['1', '2', '3', '4']
    update_protocol_via_api(ld_api_client, new_protocol_via_api.id, new_protocol_via_api)

    # Negative validation for an inaccessible project id
    with pytest.raises(Exception) as error_response:
        create_model_via_api(ld_api_client,
                             make_unique_name('Model4'),
                             'description',
                             folder=new_protocol_via_api.folder,
                             parent=new_protocol_via_api.id,
                             project_ids=[6])
    verify_error_response(error_response.value,
                          expected_status_code=400,
                          expected_error_message=ERROR_MESSAGE_INACCESSIBLE_PROJECT_ID)

    # Archiving the created models as the fixture also archives protocols and it cannot if there are dependent models
    archive_models(ld_api_client, [model_with_project_access])
