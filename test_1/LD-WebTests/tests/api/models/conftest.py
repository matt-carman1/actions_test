import pytest
from ldclient.models import ModelRecursive, Model

from helpers.api.actions.model import create_model_via_api, archive_models
from library import utils
from library.api.exceptions import LiveDesignAPIException


@pytest.fixture(scope='function')
def new_protocol_via_api(request, ld_api_client, create_model_or_protocol_object):
    """
    Creates protocol with different parameters

    1. Name of the protocol is set by defining variable 'test_protocol_name' before calling this fixture.
    2. If protocol name should be same as test_protocol_name variable, set 'is_unique_name_required' variable as False.
        For example, to create a protocol with name "Test Protocol"

            test_protocol_name = 'Test Protocol'
            is_unique_name_required = False
            @pytest.mark.usefixtures("new_protocol_via_api")

    :param request: request object with test metadata (from pytest fixture)
    :param ld_api_client: LDClient, ldclient object
    :param create_model_or_protocol_object: Model, fixture which creates protocol object

    :rtype: :class:`models.Model`
    :return: The newly created protocol, ex: Model(name='protocol_name', description='description', project_ids='4',
                                            commands=[ModelCommand(command='', driver_id='1')],folder='folder name',
                                            batch_size=ModelRecursive(tag='DEFAULT', value=100),
                                            command_queue=ModelRecursive(tag='DEFAULT', value='sync'),
                                            command_type=ModelRecursive(tag='DEFAULT', value='NORMAL'), archived=False,
                                             published=False, user='user',returns=[],template_vars=[],
                                             automatic_rerun=ModelRecursive(tag='DEFAULT', value=False))
    """
    # creating protocol using ldclient method
    protocol = ld_api_client.create_protocol(create_model_or_protocol_object)
    archive_protocol_after_test = getattr(request.module, 'archive_after_test', True)

    def finalizer():
        if archive_protocol_after_test:
            protocol.archived = True
            ld_api_client.update_protocol(protocol_id=protocol.id, protocol=protocol)

    request.addfinalizer(finalizer)
    return protocol


@pytest.fixture(scope="function")
def create_models_under_protocol(request, ld_api_client, new_protocol_via_api):
    """
    Creates 2 models(with static data) under the newly created protocol

    :param request: request object with test metadata (from pytest fixture)
    :param ld_api_client: LDClient, a fixture which creates ldclient object
    :param new_protocol_via_api: ldclient.models.Model, a fixture which creates protocol
    """
    # ----- Create models under protocol, by giving parent_id as protocol id ----- #
    first_model = create_model_via_api(ld_api_client,
                                       utils.make_unique_name('Model2'),
                                       'description',
                                       folder=new_protocol_via_api.folder,
                                       parent=new_protocol_via_api.id)
    second_model = create_model_via_api(ld_api_client,
                                        utils.make_unique_name('Model3'),
                                        'description',
                                        folder=new_protocol_via_api.folder,
                                        parent=new_protocol_via_api.id)

    def finalizer():
        # archiving models as protocol will not archive until all dependent models are archived
        archive_models(ld_api_client, [first_model, second_model])

    request.addfinalizer(finalizer)

    return new_protocol_via_api, first_model, second_model


@pytest.fixture(scope='function')
def create_model_or_protocol_object(request):
    """
    Creates protocol/model object which can be used for both model and protocol methods, with given parameters

    1. Name of the protocol/model is set by defining variable 'test_protocol_name' before calling this fixture.
    2. If protocol/model name should be same as test_protocol_name variable, set 'is_unique_name_required' variable as False.
        For example, to create a protocol with name "Test Protocol"

            test_protocol_name = 'Test Protocol'
            is_unique_name_required = False
            @pytest.mark.usefixtures("new_protocol_via_api")

    :param request: request object with test metadata (from pytest fixture)

    :rtype: :class:`models.Model`
    :return: protocol or model object, ex: Model(name='protocol_name', description='description', project_ids='4',
                                            commands=[ModelCommand(command='', driver_id='1')],folder='folder name',
                                            batch_size=ModelRecursive(tag='DEFAULT', value=100),
                                            command_queue=ModelRecursive(tag='DEFAULT', value='sync'),
                                            command_type=ModelRecursive(tag='DEFAULT', value='NORMAL'), archived=False,
                                             published=False, user='user',returns=[],template_vars=[],
                                             automatic_rerun=ModelRecursive(tag='DEFAULT', value=False))
    """
    try:
        name = getattr(request.module, 'test_protocol_name', None)
        assert name
    except AssertionError:
        raise LiveDesignAPIException('Variable "test_protocol_name" must be defined to use protocol_via_api fixture')

    unique_name = getattr(request.module, 'is_unique_name_required', True)
    protocol_name = utils.make_unique_name(name) if unique_name else name
    description = getattr(request.module, 'test_protocol_description', 'API Protocol description')
    project_ids = getattr(request.module, 'test_protocol_projects', ['4'])
    commands = getattr(request.module, 'test_protocol_commands', None)
    folder = getattr(request.module, 'test_protocol_folder', 'Computational Models/User Defined/demo')
    batch_size = getattr(request.module, 'test_protocol_batch_size', ModelRecursive(tag='DEFAULT', value=100))
    command_queue = getattr(request.module, 'test_protocol_comd_queue', ModelRecursive(tag='DEFAULT', value='sync'))
    command_type = getattr(request.module, 'test_protocol_command_type', ModelRecursive(tag='DEFAULT', value='NORMAL'))
    is_archived = getattr(request.module, 'test_protocol_is_archived', False)
    is_published = getattr(request.module, 'test_protocol_is_published', False)
    user = getattr(request.module, 'test_protocol_user', 'demo')
    predictions = getattr(request.module, 'test_protocol_predictions', [])
    template_vars = getattr(request.module, 'test_protocol_template_vars', [])
    is_automatic_rerun = getattr(request.module, 'test_protocol_automatic_rerun',
                                 ModelRecursive(tag='DEFAULT', value=False))

    return Model(name=protocol_name,
                 description=description,
                 project_ids=project_ids,
                 commands=commands,
                 folder=folder,
                 batch_size=batch_size,
                 command_queue=command_queue,
                 command_type=command_type,
                 archived=is_archived,
                 published=is_published,
                 user=user,
                 returns=predictions,
                 template_vars=template_vars,
                 automatic_rerun=is_automatic_rerun)
