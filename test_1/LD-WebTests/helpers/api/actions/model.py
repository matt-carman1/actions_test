from ldclient.models import Model, ModelRecursive


def create_model_via_api(ldclient,
                         name,
                         description,
                         folder=None,
                         is_archived=False,
                         is_published=True,
                         user='demo',
                         predictions=[],
                         parent=None,
                         template_vars=[],
                         project_ids=[],
                         batch_size=None,
                         command_type=ModelRecursive(tag='DEFAULT', value='NORMAL'),
                         command_queue=ModelRecursive(tag='DEFAULT', value='FAST'),
                         automatic_rerun=None):
    """
    Creates Model with mentioned field values

    :type ldclient:class:`LDClient`
    :param ldclient: ldclient object

    :type name: :class:`str`
    :param name: The name of the model.

    :type is_archived: :class:`bool`
    :param is_archived: Whether or not the model is archived.

    :type is_published: :class:`bool`
    :param is_published: Whether or not the model is published.

    :type user: :class:`str`
    :param user: The user that created the model.

    :type predictions: :class:`list` of :class:`ModelReturn`
    :param predictions: A list of what the model will return.

    :type folder: :class:`str`
    :param folder: The location of the model.

    :type project_ids: :class:`list` of :class:`int`
    :param project_ids: A list of what projects use the model.

    :type template_vars: :class:`list` of :class:`ModelTemplateVar`
    :param template_vars: A list of template variables

    :type description: :class:`str`
    :param description: A description of the model.

    :type parent: :class:`int`
    :param parent: The identifier for the parent model.

    :type batch_size: :class:`ModelRecursive`
    :param batch_size: The processing size of each model.

    :type command_type: :class:`ModelRecursive`
    :param command_type: The type of command to be run

    :type command_queue: :class:`ModelRecursive`
    :param command_queue: Specifies the task engine queue system

    :type automatic_rerun: :class:`ModelRecursive`
    :param automatic_rerun: The rerun type of the model

    :type id: :class:`str`
    :param id: The identifier for the model.

    :return: Created model object, ex: Model(name='protocol_name', description='description', project_ids='4',
                                            commands=[],folder='folder name',
                                            batch_size=ModelRecursive(tag='DEFAULT', value=100),
                                            command_queue=ModelRecursive(tag='DEFAULT', value='sync'),
                                            command_type=ModelRecursive(tag='DEFAULT', value='NORMAL'), archived=False,
                                             published=False, user='user',returns=[],template_vars=[],
                                             automatic_rerun=ModelRecursive(tag='DEFAULT', value=False))
    """
    model_def = Model(name=name,
                      description=description,
                      folder=folder,
                      archived=is_archived,
                      published=is_published,
                      user=user,
                      returns=predictions,
                      parent=parent,
                      template_vars=template_vars,
                      project_ids=project_ids,
                      batch_size=batch_size,
                      command_type=command_type,
                      command_queue=command_queue,
                      automatic_rerun=automatic_rerun)
    return ldclient.create_model(model_def)


def archive_models(ldclient, models_list):
    """
    Archive models for given model ids

    :param ldclient: LDClient, ldclient object
    :param models_list: list, list of model objects
    """
    for model in models_list:
        model.archived = True
        ldclient.update_model(model.id, model)


def update_protocol_via_api(ldclient, protocol_id, protocol_object):
    """
    Updates the protocol

    :param ldclient: LDClient, ldclient object
    :param protocol_id: str, id of the protocol to be updated
    :param protocol_object: Model, protocol object

    :rtype: :class:`models.Model`
    :return: The updated protocol, ex: Model(name='protocol_name', description='description', project_ids='4',
                                            commands=[],folder='folder name',
                                            batch_size=ModelRecursive(tag='DEFAULT', value=100),
                                            command_queue=ModelRecursive(tag='DEFAULT', value='sync'),
                                            command_type=ModelRecursive(tag='DEFAULT', value='NORMAL'), archived=False,
                                             published=False, user='user',returns=[],template_vars=[],
                                             automatic_rerun=ModelRecursive(tag='DEFAULT', value=False))
    """
    return ldclient.update_protocol(protocol_id, protocol_object)
