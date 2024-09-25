from ldclient.models import (ModelCommand, ModelRecursive)
from helpers.api.actions.model import create_model_via_api, archive_models
from library.utils import make_unique_name

# Protocol data
test_protocol_name = 'Protocol'
test_protocol_commands = [ModelCommand(command='${Hello:NUMERIC-INPUT}', driver_id='1')]
test_protocol_command_type = ModelRecursive(tag='DEFAULT', value='NORMAL')


def test_model_command_type(ld_api_client, new_protocol_via_api):
    """
    API test to test model command types:

    a. Create a Protocol where command type is NORMAL.
    b. Create a Model with command type NORMAL and verify it.
    c. Create a Model with command type CLICK_TO_RUN and verify it.
    d. Create a Model with command type CLUSTERING and verify it.
    e. Create a Model with command type REALTIME and verify it.

    :param ld_api_client: LDClient, a fixture which creates ldclient object
    :param new_protocol_via_api: ldclient.models.Model, fixture which creates protocol
    """

    # Creating a normal Model based on the protocol defined by the fixture
    protocol_command_type = new_protocol_via_api.command_type
    normal_model_command_type = ModelRecursive(tag='DEFAULT', value='NORMAL')
    normal_model = create_model_via_api(ld_api_client,
                                        make_unique_name('Normal_Model'),
                                        'description',
                                        folder=new_protocol_via_api.folder,
                                        parent=new_protocol_via_api.id,
                                        command_type=normal_model_command_type)

    # Fetching the command_type for model
    created_normal_model_command_type = normal_model.command_type

    # Ensuring that the command_type for protocol and model are similar and as expected
    assert str(created_normal_model_command_type) == str(protocol_command_type)
    assert str(created_normal_model_command_type) == str(normal_model_command_type)

    # Creating a CTR model based on the protocol defined by the fixture
    ctr_model_command_type = ModelRecursive(tag='DEFAULT', value='CLICK_TO_RUN')
    ctr_model = create_model_via_api(ld_api_client,
                                     make_unique_name('CTR_Model'),
                                     'description',
                                     folder=new_protocol_via_api.folder,
                                     parent=new_protocol_via_api.id,
                                     command_type=ctr_model_command_type)

    # Fetching the command_type for ctr model
    created_ctr_model_command_type = ctr_model.command_type

    # Verification that models can be created with ctr command type.
    assert str(created_ctr_model_command_type) == str(ctr_model_command_type)

    # Creating a clustering model based on the protocol defined by the fixture.
    clustering_model_command_type = ModelRecursive(tag='DEFAULT', value='CLUSTERING')
    clustering_model = create_model_via_api(ld_api_client,
                                            make_unique_name('Clustering_Model'),
                                            'description',
                                            folder=new_protocol_via_api.folder,
                                            parent=new_protocol_via_api.id,
                                            command_type=clustering_model_command_type)

    # Fetching the command_type for models
    created_clustering_model_command_type = clustering_model.command_type

    # Verification that models can be created with clustering command type.
    assert str(created_clustering_model_command_type) == str(clustering_model_command_type)

    # Creating a realtime model based on the protocol defined by the fixture.
    realtime_model_command_type = ModelRecursive(tag='DEFAULT', value='REALTIME')
    realtime_model = create_model_via_api(ld_api_client,
                                          make_unique_name('Clustering_Model'),
                                          'description',
                                          folder=new_protocol_via_api.folder,
                                          parent=new_protocol_via_api.id,
                                          command_type=realtime_model_command_type)

    # Fetching the command_type for models
    created_realtime_model_command_type = realtime_model.command_type

    # Verification that models can be created with realtime command type.
    assert str(created_realtime_model_command_type) == str(realtime_model_command_type)

    # Archiving the created models as the fixture also archives protocols and it cannot if there are dependent models
    archive_models(ld_api_client, [normal_model, ctr_model, clustering_model, realtime_model])
