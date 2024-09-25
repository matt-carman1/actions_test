import pytest
import random

from ldclient import LDClient
from ldclient import enums
from ldclient.models import (Model, ModelCommand, ModelRecursive, ModelReturn)
from library.utils import make_unique_name
from textwrap import dedent

COMMAND_TEXT = '''
   ${param1:TEXT-INPUT}
   ${param2:TEXT-INPUT}
   ${param3:TEXT-INPUT}
   '''
COMMAND_TEXT = dedent(COMMAND_TEXT)
COMMAND = ModelCommand(command=COMMAND_TEXT, driver_id=1)
TEMPLATE_VAR_NAME = "param4"
COMMAND_TEXT_2 = "${" + TEMPLATE_VAR_NAME + ":TEXT-INPUT}"
COMMAND_2 = ModelCommand(command=COMMAND_TEXT_2, driver_id=1)
TEMPLATE_VAR_DATA_1 = "data1"
TEMPLATE_VAR_DATA_2 = "data2"


def test_create_protocol_tag(ld_client: LDClient):
    protocol = create_protocol(ld_client)
    for template_var in protocol.template_vars:
        assert template_var.tag == enums.RecursiveTag.ABSTRACT.name


def test_create_model_tag(ld_client: LDClient):
    protocol = create_protocol(ld_client)
    updated_protocol = update_protocol_template_vars(
        ld_client, protocol, [enums.RecursiveTag.DEFAULT.name, enums.RecursiveTag.READ_ONLY.name],
        [TEMPLATE_VAR_DATA_1, TEMPLATE_VAR_DATA_2], [0, 1])
    model = create_model(ld_client, updated_protocol)
    for template_var in protocol.template_vars:
        model_template_var = next((model_template_var for model_template_var in model.template_vars
                                   if model_template_var.name == template_var.name), None)
        if template_var.tag == enums.RecursiveTag.ABSTRACT.name:
            assert model_template_var.tag == enums.RecursiveTag.ABSTRACT.name
        if template_var.tag == enums.RecursiveTag.DEFAULT.name:
            assert model_template_var.tag == enums.RecursiveTag.READ_ONLY.name
        if template_var.tag == enums.RecursiveTag.READ_ONLY.name:
            assert model_template_var.tag == enums.RecursiveTag.PASS.name


def test_add_new_template_var_to_existing_protocol(ld_client: LDClient):
    protocol = create_protocol(ld_client)
    updated_commands = [COMMAND, COMMAND_2]
    updated_protocol = update_protocol_commands(ld_client, protocol, updated_commands)
    for template_var in updated_protocol.template_vars:
        if template_var.name == TEMPLATE_VAR_NAME:
            assert template_var.tag == enums.RecursiveTag.ABSTRACT.name


def test_add_new_default_template_var_to_existing_protocol_and_model(ld_client: LDClient):
    protocol = create_protocol(ld_client)
    model_id = create_model(ld_client, protocol).id
    updated_commands = [COMMAND, COMMAND_2]
    updated_protocol = update_protocol_commands(ld_client, protocol, updated_commands)
    for template_var in updated_protocol.template_vars:
        if template_var.name == TEMPLATE_VAR_NAME:
            template_var.tag = enums.RecursiveTag.DEFAULT.name
            template_var.data = TEMPLATE_VAR_DATA_1
    ld_client.update_protocol(protocol.id, updated_protocol)
    model = ld_client.model(model_id)
    for template_var in model.template_vars:
        if template_var.name == TEMPLATE_VAR_NAME:
            assert template_var.tag == enums.RecursiveTag.READ_ONLY.name


def test_add_new_template_var_to_existing_protocol_and_model(ld_client: LDClient):
    protocol = create_protocol(ld_client)
    model_id = create_model(ld_client, protocol).id
    updated_commands = [COMMAND, COMMAND_2]
    update_protocol_commands(ld_client, protocol, updated_commands)
    model = ld_client.model(model_id)
    for template_var in model.template_vars:
        if template_var.name == TEMPLATE_VAR_NAME:
            assert template_var.tag == enums.RecursiveTag.PASS.name


def create_protocol(ld_client: LDClient, protocol_def=None):
    if not protocol_def:
        protocol_def = Model(name=make_unique_name('Protocol test_create'),
                             commands=[COMMAND],
                             description='create protocol',
                             archived=False,
                             published=False,
                             folder="Computational Models/User Defined/demo",
                             user="demo",
                             project_ids=['0'],
                             template_vars=[],
                             returns=[],
                             batch_size=ModelRecursive(tag=enums.RecursiveTag.DEFAULT, value=100),
                             command_type=ModelRecursive(tag=enums.RecursiveTag.READ_ONLY, value='NORMAL'),
                             command_queue=ModelRecursive(tag=enums.RecursiveTag.READ_ONLY, value='sync'))

    return ld_client.create_protocol(protocol_def)


def create_model(ld_client: LDClient, protocol):
    returns = [
        ModelReturn(key="return1",
                    type="STRING",
                    units="",
                    precision=0,
                    tag=enums.RecursiveTag.DEFAULT,
                    display_name="return1")
    ]
    model_def = Model(name=make_unique_name('test_name: Child Model'),
                      archived=False,
                      published=True,
                      user='demo',
                      folder="Computational Models/User Defined/demo",
                      returns=returns,
                      project_ids=None,
                      template_vars=None,
                      description='A child model for test_name',
                      parent=protocol.id,
                      commands=None,
                      batch_size=None,
                      command_type=protocol.command_type,
                      command_queue=protocol.command_queue)

    return ld_client.create_model(model_def)


def update_protocol_template_vars(ld_client: LDClient,
                                  protocol,
                                  tags: list = [],
                                  data: list = [],
                                  template_var_indexes: list = []):
    for index in template_var_indexes:
        if tags[index] is not None:
            protocol.template_vars[index].tag = tags[index]
        if data[index] is not None:
            protocol.template_vars[index].data = data[index]

    ld_client.update_protocol(protocol.id, protocol)
    return ld_client.get_protocol_by_id(protocol.id)


def update_protocol_commands(ld_client: LDClient, protocol, commands: list = []):
    if commands is not None:
        protocol.commands = commands
    ld_client.update_protocol(protocol.id, protocol)
    return ld_client.get_protocol_by_id(protocol.id)
