from ldclient import LDClient
from ldclient import enums
from ldclient.models import (Model, ModelCommand, ModelRecursive)

from library.utils import make_unique_name


def test_default_model_template_var_tag_for_abstract_protocol(ld_client: LDClient):
    command_text = "${Test:TEXT-INPUT}"
    command_text_2 = "${Test:TEXT-INPUT}  ${Test2:TEXT-INPUT}"
    command = ModelCommand(command=command_text, driver_id=1)
    command_2 = ModelCommand(command=command_text_2, driver_id=1)

    protocol_def = Model(name=make_unique_name('Protocol test_default_model_template_var_tag_for_abstract_protocol'),
                         commands=[command],
                         description='Tests tag inheritance for models on creation',
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

    protocol = ld_client.create_protocol(protocol_def)

    assert protocol.template_vars[0].type == enums.ModelTemplateVarType.STRING.name
    assert protocol.template_vars[0].tag == enums.RecursiveTag.ABSTRACT.name

    model = ld_client.create_model(
        model=Model(name=make_unique_name('test_default_model_template_var_tag_for_abstract_protocol: Child Model'),
                    archived=False,
                    published=True,
                    user='demo',
                    folder="Computational Models/User Defined/demo",
                    returns=[],
                    project_ids=None,
                    template_vars=None,
                    description='A child model for test_name',
                    parent=protocol.id,
                    commands=None,
                    batch_size=None,
                    command_type=protocol.command_type,
                    command_queue=protocol.command_queue))

    assert model.template_vars[0].type == protocol.template_vars[0].type
    assert model.template_vars[0].tag == enums.RecursiveTag.ABSTRACT.name

    protocol.commands = [command_2]

    protocol = ld_client.update_protocol(protocol.id, protocol)

    model = ld_client.model(model.id)

    assert model.template_vars[1].type == protocol.template_vars[0].type
    assert model.template_vars[1].tag == enums.RecursiveTag.PASS.name
