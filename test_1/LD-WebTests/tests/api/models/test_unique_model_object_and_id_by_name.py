from ldclient.models import ModelReturn, Model, ModelRecursive, ModelTemplateVar


def test_unique_model_object_and_id_by_name(ld_api_client):
    """
    Test to get model objects and ids by name for model with unique name
    using two ldclient methods and verify them.
    i) get_model_by_name()
    ii) get_model_id_by_name()

    :param ld_api_client: LDClient, ldclient object
    """
    returns = [
        ModelReturn(id='2901',
                    key='MW',
                    type='REAL',
                    units='',
                    display_name='MW',
                    tag='DEFAULT',
                    precision=1,
                    addable_column_id='1258')
    ]
    template_vars = [
        ModelTemplateVar(id='3451',
                         tag='READ_ONLY',
                         type='STRING',
                         name='Property Argument',
                         data='MW',
                         is_optional=False)
    ]
    commands = ld_api_client.get_protocol_by_id(351).commands
    expected_model_object = Model(id='2801',
                                  parent=351,
                                  name='MW',
                                  archived=False,
                                  published=True,
                                  user='demo',
                                  created_at=1431388800000,
                                  updated_at=1431388800000,
                                  folder='Computed Properties/Physicochemical Descriptors',
                                  returns=returns,
                                  template_vars=template_vars,
                                  batch_size=ModelRecursive(tag='PASS', value=None),
                                  description="Calculate MW  using Schrodinger's Canvas software",
                                  command_type=ModelRecursive(tag='DEFAULT', value='REALTIME'),
                                  command_queue=ModelRecursive(tag='DEFAULT', value='sync'),
                                  commands=[],
                                  project_ids=[0],
                                  automatic_rerun={
                                      'tag': 'PASS',
                                      'value': None
                                  },
                                  as_merged=Model(id='2801',
                                                  parent=351,
                                                  name='MW',
                                                  archived=False,
                                                  published=True,
                                                  user='demo',
                                                  created_at=1431388800000,
                                                  updated_at=1431388800000,
                                                  folder='Computed Properties/Physicochemical Descriptors',
                                                  returns=returns,
                                                  template_vars=[
                                                      ModelTemplateVar(id='1401',
                                                                       tag='ABSTRACT',
                                                                       type='SDF_FILE',
                                                                       name='SDF-FILE',
                                                                       is_optional=False), template_vars[0]
                                                  ],
                                                  batch_size=ModelRecursive(tag='DEFAULT', value=100),
                                                  description="Calculate MW  using Schrodinger's Canvas software",
                                                  command_type=ModelRecursive(tag='DEFAULT', value='REALTIME'),
                                                  command_queue=ModelRecursive(tag='DEFAULT', value='sync'),
                                                  commands=commands,
                                                  project_ids=[0],
                                                  automatic_rerun={
                                                      'tag': 'DEFAULT',
                                                      'value': True
                                                  }))
    # Using get_model_by_name() method
    model_name = 'MW'
    actual_model_object = ld_api_client.get_model_by_name(model_name)
    assert expected_model_object.as_dict() == actual_model_object.as_dict(), \
        'Expected model object {} but got {}'.format(expected_model_object, actual_model_object)

    # Using get_model_id_by_name() method
    expected_model_id = 2801
    actual_model_id = ld_api_client.get_model_id_by_name(model_name)
    assert expected_model_id == actual_model_id, \
        'Expected model ID {} but got {}'.format(expected_model_id, actual_model_id)
