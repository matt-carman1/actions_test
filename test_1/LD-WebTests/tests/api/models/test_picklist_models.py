import pytest
import random

from ldclient import LDClient
from ldclient import enums
from ldclient.models import (LiveReport, Model, ModelCommand, ModelRecursive, ModelReturn, ModelPicklistItem)
from library.utils import make_unique_name
from library.api.wait import wait_until_condition_met
from textwrap import dedent

COMMAND_TEXT = '''
    export SCHRODINGER=/mnt/suites/suite2021-1 && echo ${picklist:LIST-INPUT} && touch ${SDF-FILE} && $SCHRODINGER/run python3 <<'EOF'
    import sys
    import csv
    from schrodinger.structure import StructureReader
    fname = 'input'
    fname += '.sdf'
    writer = csv.DictWriter(open('results.csv', 'w'), fieldnames=['Corporate ID', 'PicklistData'])
    writer.writeheader()
    for st in StructureReader(fname):
        writer.writerow({'Corporate ID': st.title, 'PicklistData': '${picklist:LIST-INPUT}' })
    EOF
    '''
COMMAND_TEXT = dedent(COMMAND_TEXT)
COMMAND_TEXT_2 = 'cat results.csv'
COMMAND = ModelCommand(command=COMMAND_TEXT, driver_id=1)
COMMAND_2 = ModelCommand(command=COMMAND_TEXT_2, driver_id=1)
STRING_PICKLIST_VALUE_ARRAY = ["String 1", "String 2", "3"]
NUMERIC_PICKLIST_VALUE_ARRAY = ["1", "2", "3"]
LIVE_REPORT_ROWS = ["CRA-031137", "CRA-031437"]
TEST_LR_ID = 0

PROTOCOL_DEF = Model(name='Protocol test_create_picklist %s' % random.random(),
                     commands=[COMMAND, COMMAND_2],
                     description='run a python file that requires the schrodinger python library',
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


def test_create_untyped_list(ld_client: LDClient):
    protocol = create_protocol(ld_client)
    assert protocol.template_vars[0].model_picklist is not None
    assert protocol.template_vars[0].model_picklist.id is not None
    assert protocol.template_vars[0].model_picklist.data_type == enums.ModelPicklistType.UNTYPED
    assert not protocol.template_vars[0].model_picklist.picklist_item_choices
    for choice in protocol.template_vars[0].model_picklist.picklist_item_choices:
        assert choice.id is not None


def test_add_items_to_untyped_list(ld_client: LDClient):
    protocol = create_protocol(ld_client)
    with pytest.raises(Exception):
        update_protocol_list_type_and_items(ld_client=ld_client,
                                            protocol=protocol,
                                            new_values=STRING_PICKLIST_VALUE_ARRAY)
    updated_protocol = ld_client.get_protocol_by_id(protocol.id)

    assert updated_protocol.template_vars[0].model_picklist.data_type == enums.ModelPicklistType.UNTYPED
    assert not updated_protocol.template_vars[0].model_picklist.picklist_item_choices


def test_change_empty_list_typing_and_add_items(ld_client: LDClient):
    protocol = create_protocol(ld_client)
    updated_protocol = update_protocol_list_type_and_items(ld_client=ld_client,
                                                           protocol=protocol,
                                                           type=enums.ModelPicklistType.STRING,
                                                           new_values=STRING_PICKLIST_VALUE_ARRAY)

    assert updated_protocol.template_vars[0].model_picklist.data_type == enums.ModelPicklistType.STRING
    assert updated_protocol.template_vars[0].model_picklist.picklist_item_choices
    assert_picklist_items_equal_to_values(updated_protocol.template_vars[0].model_picklist.picklist_item_choices,
                                          STRING_PICKLIST_VALUE_ARRAY)


def test_change_list_type_for_non_empty_list(ld_client: LDClient):
    protocol = create_protocol_with_type_and_value(ld_client=ld_client,
                                                   type=enums.ModelPicklistType.STRING,
                                                   picklist_value_arr=STRING_PICKLIST_VALUE_ARRAY)
    with pytest.raises(Exception) as e_info:
        update_protocol_list_type_and_items(ld_client=ld_client,
                                            protocol=protocol,
                                            type=enums.ModelPicklistType.NUMERIC)


def test_add_multiple_picklist_items_to_non_empty_list(ld_client: LDClient):
    protocol = create_protocol_with_type_and_value(ld_client=ld_client,
                                                   type=enums.ModelPicklistType.STRING,
                                                   picklist_value_arr=STRING_PICKLIST_VALUE_ARRAY)
    new_str_array = ["String 4", "String 5", "String 6"]
    updated_protocol = update_protocol_list_type_and_items(
        ld_client=ld_client,
        protocol=protocol,
        new_values=new_str_array,
        existing_values=protocol.template_vars[0].model_picklist.picklist_item_choices)
    assert len(
        updated_protocol.template_vars[0].model_picklist.picklist_item_choices) == len(STRING_PICKLIST_VALUE_ARRAY +
                                                                                       new_str_array)
    assert_picklist_items_equal_to_values(updated_protocol.template_vars[0].model_picklist.picklist_item_choices,
                                          STRING_PICKLIST_VALUE_ARRAY + new_str_array)


def test_create_model_and_picklist_propagates(ld_client: LDClient):
    protocol = create_protocol_with_type_and_value(ld_client=ld_client,
                                                   type=enums.ModelPicklistType.STRING,
                                                   picklist_value_arr=STRING_PICKLIST_VALUE_ARRAY)
    model = create_model(ld_client, protocol)
    assert model.template_vars[0].model_picklist.data_type == enums.ModelPicklistType.STRING
    assert_picklist_items_equal(protocol.template_vars[0].model_picklist.picklist_item_choices,
                                model.template_vars[0].model_picklist.picklist_item_choices)


def test_update_list_type_and_items_of_non_empty_list(ld_client: LDClient):
    protocol_with_str_list = create_protocol_with_type_and_value(ld_client=ld_client,
                                                                 type=enums.ModelPicklistType.STRING,
                                                                 picklist_value_arr=STRING_PICKLIST_VALUE_ARRAY)
    model_with_str_list = create_model(ld_client, protocol_with_str_list)

    protocol_with_numeric_list = update_protocol_list_type_and_items(ld_client=ld_client,
                                                                     protocol=protocol_with_str_list,
                                                                     type=enums.ModelPicklistType.NUMERIC,
                                                                     new_values=NUMERIC_PICKLIST_VALUE_ARRAY)
    assert protocol_with_str_list.id == protocol_with_numeric_list.id
    assert protocol_with_numeric_list.template_vars[0].model_picklist.data_type == enums.ModelPicklistType.NUMERIC
    assert_picklist_items_equal_to_values(
        protocol_with_numeric_list.template_vars[0].model_picklist.picklist_item_choices, NUMERIC_PICKLIST_VALUE_ARRAY)

    model_with_numeric_list = ld_client.model(model_with_str_list.id)

    assert model_with_numeric_list.id == model_with_str_list.id
    assert model_with_numeric_list.template_vars[0].model_picklist.data_type == enums.ModelPicklistType.NUMERIC
    assert_picklist_items_equal_to_values(
        protocol_with_numeric_list.template_vars[0].model_picklist.picklist_item_choices, NUMERIC_PICKLIST_VALUE_ARRAY)


def test_delete_inputs_from_list_and_it_propagates(ld_client: LDClient):
    protocol_with_str_list = create_protocol_with_type_and_value(ld_client=ld_client,
                                                                 type=enums.ModelPicklistType.STRING,
                                                                 picklist_value_arr=STRING_PICKLIST_VALUE_ARRAY)
    model_with_str_list = create_model(ld_client, protocol_with_str_list)
    assert_picklist_items_equal(protocol_with_str_list.template_vars[0].model_picklist.picklist_item_choices,
                                model_with_str_list.template_vars[0].model_picklist.picklist_item_choices)

    updated_protocol_with_str_list = update_protocol_list_type_and_items(ld_client=ld_client,
                                                                         protocol=protocol_with_str_list,
                                                                         new_values=STRING_PICKLIST_VALUE_ARRAY[:-1])
    updated_model_with_str_list = ld_client.model(model_with_str_list.id)

    assert_picklist_items_equal_to_values(
        updated_protocol_with_str_list.template_vars[0].model_picklist.picklist_item_choices,
        STRING_PICKLIST_VALUE_ARRAY[:-1])
    assert_picklist_items_equal(updated_protocol_with_str_list.template_vars[0].model_picklist.picklist_item_choices,
                                updated_model_with_str_list.template_vars[0].model_picklist.picklist_item_choices)


def test_try_to_remove_picklist_choice_on_model(ld_client: LDClient):
    protocol = create_protocol_with_type_and_value(ld_client=ld_client,
                                                   type=enums.ModelPicklistType.STRING,
                                                   picklist_value_arr=STRING_PICKLIST_VALUE_ARRAY)
    model = create_model(ld_client=ld_client, protocol=protocol)
    model.template_vars[0].model_picklist.picklist_item_choices = model.template_vars[
        0].model_picklist.picklist_item_choices[:-1]
    with pytest.raises(Exception) as e_info:
        ld_client.update_model(model.id, model)
    print(e_info)


def test_try_to_edit_picklist_choice_on_model(ld_client: LDClient):
    protocol = create_protocol_with_type_and_value(ld_client=ld_client,
                                                   type=enums.ModelPicklistType.STRING,
                                                   picklist_value_arr=STRING_PICKLIST_VALUE_ARRAY)
    model = create_model(ld_client=ld_client, protocol=protocol)
    model.template_vars[0].model_picklist.picklist_item_choices = model.template_vars[
        0].model_picklist.picklist_item_choices[:-1]
    with pytest.raises(Exception) as e_info:
        ld_client.update_model(model.id, model)
    print(e_info)


def test_set_single_data_value_on_protocol_non_multi_data_field(ld_client: LDClient):
    protocol = create_protocol_with_type_and_value(ld_client=ld_client,
                                                   type=enums.ModelPicklistType.STRING,
                                                   picklist_value_arr=STRING_PICKLIST_VALUE_ARRAY)

    assert not protocol.template_vars[0].model_picklist.allow_multiple
    assert protocol.template_vars[0].data is None
    data = protocol.template_vars[0].model_picklist.picklist_item_choices[0].id
    updated_protocol = update_protocol_data(ld_client=ld_client,
                                            protocol=protocol,
                                            tag=enums.RecursiveTag.DEFAULT,
                                            data=data)
    assert updated_protocol.template_vars[0].data == data


def test_parameterizable_model_creation(ld_client):
    protocol = create_protocol_with_type_and_value(ld_client=ld_client,
                                                   type=enums.ModelPicklistType.STRING,
                                                   picklist_value_arr=STRING_PICKLIST_VALUE_ARRAY)

    model = create_model(ld_client=ld_client, protocol=protocol)
    data = model.template_vars[0].model_picklist.picklist_item_choices[0].id
    updated_model = update_model_data(ld_client=ld_client, model=model, tag=enums.RecursiveTag.DEFAULT, data=data)
    assert updated_model.template_vars[0].data == data
    assert updated_model.template_vars[0].tag == enums.RecursiveTag.DEFAULT.name

    updated_model_2 = create_model(ld_client=ld_client, protocol=updated_model)

    assert updated_model_2.template_vars[0].data is None
    assert updated_model_2.template_vars[0].tag == enums.RecursiveTag.ABSTRACT.name


def test_set_multi_data_value_on_protocol_non_multi_data_field(ld_client: LDClient):
    protocol = create_protocol_with_type_and_value(ld_client=ld_client,
                                                   type=enums.ModelPicklistType.STRING,
                                                   picklist_value_arr=STRING_PICKLIST_VALUE_ARRAY)

    assert protocol.template_vars[0].model_picklist.allow_multiple == False
    assert protocol.template_vars[0].data is None
    data = [choice.id for choice in protocol.template_vars[0].model_picklist.picklist_item_choices]
    data = ','.join(data)
    with pytest.raises(Exception) as e_info:
        update_protocol_data(ld_client=ld_client, protocol=protocol, tag=enums.RecursiveTag.DEFAULT, data=data)
    print(e_info)


def test_set_multi_data_value_on_protocol_and_model(ld_client: LDClient):
    protocol = create_protocol_with_type_and_value(ld_client=ld_client,
                                                   type=enums.ModelPicklistType.STRING,
                                                   picklist_value_arr=STRING_PICKLIST_VALUE_ARRAY)
    data = [choice.id for choice in protocol.template_vars[0].model_picklist.picklist_item_choices]
    data = ','.join(data)
    updated_protocol = update_protocol_data(ld_client=ld_client,
                                            protocol=protocol,
                                            tag=enums.RecursiveTag.DEFAULT,
                                            allow_multiple=True,
                                            data=data)
    assert updated_protocol.template_vars[0].tag == enums.RecursiveTag.DEFAULT.name
    assert updated_protocol.template_vars[0].data == data

    model = create_model(ld_client=ld_client, protocol=protocol)
    expected_model_data = ','.join(
        [choice.id for choice in model.template_vars[0].model_picklist.picklist_item_choices])

    assert model.template_vars[0].data == expected_model_data
    assert model.template_vars[0].tag == enums.RecursiveTag.READ_ONLY.name

    new_model_data = ','.join(
        [choice.id for choice in model.template_vars[0].model_picklist.picklist_item_choices[:-1]])

    updated_model = update_model_data(ld_client=ld_client,
                                      model=model,
                                      tag=enums.RecursiveTag.READ_ONLY,
                                      data=new_model_data)

    assert updated_model.template_vars[0].tag == enums.RecursiveTag.READ_ONLY.name
    assert updated_model.template_vars[0].data == new_model_data


def test_delete_inputs_from_list_that_are_in_data(ld_client: LDClient):
    protocol = create_protocol_with_type_and_value(ld_client=ld_client,
                                                   type=enums.ModelPicklistType.STRING,
                                                   picklist_value_arr=STRING_PICKLIST_VALUE_ARRAY)
    data = ','.join([choice.id for choice in protocol.template_vars[0].model_picklist.picklist_item_choices])
    updated_protocol = update_protocol_data(ld_client=ld_client,
                                            protocol=protocol,
                                            tag=enums.RecursiveTag.DEFAULT,
                                            allow_multiple=True,
                                            data=data)
    with pytest.raises(Exception) as e_info:
        update_protocol_list_type_and_items(ld_client=ld_client,
                                            protocol=updated_protocol,
                                            new_values=STRING_PICKLIST_VALUE_ARRAY[:-1])
    print(e_info)


def test_set_invalid_ids_as_data(ld_client: LDClient):
    protocol = create_protocol_with_type_and_value(ld_client=ld_client,
                                                   type=enums.ModelPicklistType.STRING,
                                                   picklist_value_arr=STRING_PICKLIST_VALUE_ARRAY)
    data = ','.join([choice.id + '1' for choice in protocol.template_vars[0].model_picklist.picklist_item_choices])
    with pytest.raises(Exception) as e_info:
        update_protocol_data(ld_client=ld_client,
                             protocol=protocol,
                             tag=enums.RecursiveTag.DEFAULT,
                             allow_multiple=True,
                             data=data)
    print(e_info.value)


def test_set_invalid_string_as_data(ld_client: LDClient):
    protocol = create_protocol_with_type_and_value(ld_client=ld_client,
                                                   type=enums.ModelPicklistType.STRING,
                                                   picklist_value_arr=STRING_PICKLIST_VALUE_ARRAY)
    data = "I am text"
    with pytest.raises(Exception) as e_info:
        update_protocol_data(ld_client=ld_client,
                             protocol=protocol,
                             tag=enums.RecursiveTag.DEFAULT,
                             allow_multiple=True,
                             data=data)
    print(e_info.value)


def test_create_protocol_with_empty_optional_param_data(ld_client: LDClient):
    name = "I am an optional parameter name"
    protocol = create_protocol_with_type_items_data(ld_client=ld_client,
                                                    type=enums.ModelPicklistType.STRING,
                                                    picklist_value_arr=STRING_PICKLIST_VALUE_ARRAY,
                                                    tag=enums.RecursiveTag.ABSTRACT,
                                                    is_optional=True,
                                                    optional_name=name,
                                                    template_var_index=0)
    assert protocol.template_vars[0].is_optional
    assert protocol.template_vars[0].optional_parameter_name == name + " "
    # NOTE(Alajmi): To allow the name to fit in the generated command we add an extra space after the name


def test_add_new_picklist_to_existing_protocol_with_model(ld_client: LDClient):
    protocol_def = PROTOCOL_DEF
    protocol_def.commands = [protocol_def.commands[1]]
    protocol = create_protocol(ld_client, protocol_def)

    create_model(ld_client=ld_client, protocol=protocol)
    protocol.commands.append(ModelCommand(command="echo ${mypicklist:LIST-INPUT} && ", driver_id=1))
    protocol = ld_client.update_protocol(protocol.id, protocol)
    string_picklist_choices = [ModelPicklistItem(value=val) for val in STRING_PICKLIST_VALUE_ARRAY]

    protocol.template_vars[-1].model_picklist.picklist_item_choices = string_picklist_choices
    protocol.template_vars[-1].model_picklist.data_type = enums.ModelPicklistType.STRING
    protocol = ld_client.update_protocol(protocol.id, protocol)
    print(protocol)


def test_duplicate_protocol_with_picklist(ld_client: LDClient):
    protocol = create_protocol(ld_client=ld_client)
    duped_protocol = duplicate_protocol(ld_client=ld_client, protocol=protocol)
    print(duped_protocol)
    # Verify correct values and non null IDs
    assert duped_protocol.id != protocol.id
    assert duped_protocol.template_vars[0].id != protocol.template_vars[0].id
    assert duped_protocol.template_vars[0].name == protocol.template_vars[0].name
    assert duped_protocol.template_vars[0].tag == protocol.template_vars[0].tag
    assert duped_protocol.template_vars[0].type == protocol.template_vars[0].type
    assert_picklist_items_equal(duped_protocol.template_vars[0].model_picklist.picklist_item_choices,
                                protocol.template_vars[0].model_picklist.picklist_item_choices)


@pytest.mark.app_defect(reason="SS-40265: Taskengine related flakiness on jenkins")
def test_create_and_run_model_with_data_set_on_model(ld_client: LDClient):
    protocol = create_protocol_with_type_items_data(ld_client=ld_client,
                                                    type=enums.ModelPicklistType.STRING,
                                                    picklist_value_arr=STRING_PICKLIST_VALUE_ARRAY,
                                                    allow_multiple=True)

    model = create_model(ld_client=ld_client, protocol=protocol)
    data = ','.join([choice.id for choice in model.template_vars[0].model_picklist.picklist_item_choices])
    updated_model = update_model_data(ld_client=ld_client, model=model, tag=enums.RecursiveTag.READ_ONLY, data=data)
    lr_id = create_liverport_for_model_testing(ld_client)
    ld_client.add_columns(lr_id, [model.returns[0].addable_column_id])
    wait_until_condition_met(lambda: model_finished_executing(ld_client, updated_model.returns[0].addable_column_id),
                             retries=50,
                             interval=2000)

    executed_lr = ld_client.execute_live_report(lr_id)
    model_result_values = [
        executed_lr['rows'][x]['cells'][updated_model.returns[0].addable_column_id]['values']
        for x in executed_lr['rows']
    ]

    for result in model_result_values:
        # The value set on the model
        expected_value = ','.join(STRING_PICKLIST_VALUE_ARRAY)
        assert result[0]['value'] == expected_value


@pytest.mark.app_defect(reason="SS-40265: Taskengine related flakiness on jenkins")
def test_create_and_run_model_with_data_set_on_protocol(ld_client):
    protocol = create_protocol_with_type_and_value(ld_client=ld_client,
                                                   type=enums.ModelPicklistType.STRING,
                                                   picklist_value_arr=STRING_PICKLIST_VALUE_ARRAY)

    data = [choice.id for choice in protocol.template_vars[0].model_picklist.picklist_item_choices]
    data = ','.join(data)
    updated_protocol = update_protocol_data(ld_client=ld_client,
                                            protocol=protocol,
                                            tag=enums.RecursiveTag.DEFAULT,
                                            data=data,
                                            allow_multiple=True)

    model = create_model(ld_client=ld_client, protocol=updated_protocol)
    lr_id = create_liverport_for_model_testing(ld_client)
    ld_client.add_columns(lr_id, [model.returns[0].addable_column_id])
    wait_until_condition_met(lambda: model_finished_executing(ld_client, model.returns[0].addable_column_id),
                             retries=50,
                             interval=2000)

    executed_lr = ld_client.execute_live_report(lr_id)

    model_result_values = [
        executed_lr['rows'][x]['cells'][model.returns[0].addable_column_id]['values'] for x in executed_lr['rows']
    ]

    for result in model_result_values:
        # The value defaulted by the protocol
        expected_value = ','.join(STRING_PICKLIST_VALUE_ARRAY)
        assert result[0]['value'] == expected_value


@pytest.mark.app_defect(reason="SS-40265: Taskengine related flakiness on jenkins")
def test_create_and_run_model_with_empty_optional_param_data(ld_client: LDClient):
    name = "I am an optional parameter name"
    protocol = create_protocol_with_type_items_data(ld_client=ld_client,
                                                    type=enums.ModelPicklistType.NUMERIC,
                                                    picklist_value_arr=NUMERIC_PICKLIST_VALUE_ARRAY,
                                                    tag=enums.RecursiveTag.ABSTRACT,
                                                    is_optional=True,
                                                    optional_name=name,
                                                    template_var_index=0)
    model = create_model(ld_client=ld_client, protocol=protocol)
    lr_id = create_liverport_for_model_testing(ld_client)
    ld_client.add_columns(lr_id, [model.returns[0].addable_column_id])
    wait_until_condition_met(lambda: model_finished_executing(ld_client, model.returns[0].addable_column_id),
                             retries=50,
                             interval=2000)

    executed_lr = ld_client.execute_live_report(lr_id)

    model_result_values = [
        executed_lr['rows'][x]['cells'][model.returns[0].addable_column_id]['values'] for x in executed_lr['rows']
    ]

    for result in model_result_values:
        # The value defaulted by the protocol
        expected_value = ''
        assert result[0]['value'] == expected_value


@pytest.mark.app_defect(reason="SS-40265: Taskengine related flakiness on jenkins")
def test_create_and_run_model_with_non_empty_optional_param_data(ld_client: LDClient):

    name = "I am an optional parameter name"
    protocol = create_protocol_with_type_items_data(ld_client=ld_client,
                                                    type=enums.ModelPicklistType.NUMERIC,
                                                    picklist_value_arr=NUMERIC_PICKLIST_VALUE_ARRAY,
                                                    tag=enums.RecursiveTag.ABSTRACT,
                                                    is_optional=True,
                                                    optional_name=name,
                                                    template_var_index=0)
    model = create_model(ld_client=ld_client, protocol=protocol)
    updated_model = update_model_data(ld_client=ld_client,
                                      model=model,
                                      tag=enums.RecursiveTag.READ_ONLY,
                                      data=model.template_vars[0].model_picklist.picklist_item_choices[0].id)
    lr_id = create_liverport_for_model_testing(ld_client)

    ld_client.add_columns(lr_id, [updated_model.returns[0].addable_column_id])
    wait_until_condition_met(lambda: model_finished_executing(ld_client, model.returns[0].addable_column_id),
                             retries=50,
                             interval=2000)

    executed_lr = ld_client.execute_live_report(lr_id)

    model_result_values = [
        executed_lr['rows'][x]['cells'][model.returns[0].addable_column_id]['values'] for x in executed_lr['rows']
    ]

    for result in model_result_values:
        expected_value = name + ' 1'
        assert result[0]['value'] == expected_value


def create_protocol(ld_client: LDClient, protocol_def=None):
    if not protocol_def:
        protocol_def = Model(name=make_unique_name('Protocol test_create_picklist %s' % random.random()),
                             commands=[COMMAND, COMMAND_2],
                             description='run a python file that requires the schrodinger python library',
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


def create_model(ld_client: LDClient, protocol, model_def=None):
    if not model_def:
        returns = [
            ModelReturn(key="PicklistData",
                        type="STRING",
                        units="",
                        precision=0,
                        tag=enums.RecursiveTag.DEFAULT,
                        display_name="PicklistData")
        ]
        model_def = Model(name=make_unique_name('test_name: Child Model %s' % random.random()),
                          archived=False,
                          published=True,
                          user='demo',
                          folder="Picklist Models",
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


def update_protocol_list_type_and_items(ld_client: LDClient,
                                        protocol,
                                        type: enums.ModelPicklistType = None,
                                        new_values: [] = None,
                                        existing_values: [] = None):
    if type:
        protocol.template_vars[0].model_picklist.data_type = type
    if new_values:
        new_values = [ModelPicklistItem(value=value) for value in new_values]
        if existing_values:
            protocol.template_vars[0].model_picklist.picklist_item_choices = existing_values + new_values
        else:
            protocol.template_vars[0].model_picklist.picklist_item_choices = new_values

    ld_client.update_protocol(protocol.id, protocol)
    return ld_client.get_protocol_by_id(protocol.id)


def update_protocol_data(ld_client: LDClient,
                         protocol,
                         tag: enums.RecursiveTag = None,
                         data: str = None,
                         template_var_index=0,
                         allow_multiple: bool = None,
                         is_optional: bool = None,
                         optional_name: str = None):
    if tag is not None:
        protocol.template_vars[template_var_index].tag = tag
    if data is not None:
        protocol.template_vars[template_var_index].data = data
    if allow_multiple is not None:
        protocol.template_vars[template_var_index].model_picklist.allow_multiple = allow_multiple
    if is_optional is not None:
        protocol.template_vars[template_var_index].is_optional = is_optional
    if optional_name is not None:
        protocol.template_vars[template_var_index].optional_parameter_name = optional_name

    ld_client.update_protocol(protocol.id, protocol)
    return ld_client.get_protocol_by_id(protocol.id)


def update_model_data(ld_client: LDClient,
                      model,
                      tag: enums.RecursiveTag = None,
                      data: str = None,
                      template_var_index=0):
    if tag is not None:
        model.template_vars[template_var_index].tag = tag
    if data is not None:
        model.template_vars[template_var_index].data = data

    ld_client.update_model(model.id, model)
    return ld_client.model(model.id)


def create_protocol_with_type_and_value(ld_client: LDClient,
                                        protocol_def=None,
                                        type: enums.ModelPicklistType = None,
                                        picklist_value_arr: [] = None):
    protocol = create_protocol(ld_client, protocol_def)
    return update_protocol_list_type_and_items(ld_client=ld_client,
                                               protocol=protocol,
                                               type=type,
                                               new_values=picklist_value_arr)


def create_protocol_with_type_items_data(ld_client: LDClient,
                                         protocol_def=None,
                                         type: enums.ModelPicklistType = None,
                                         picklist_value_arr: [] = None,
                                         tag: enums.RecursiveTag = None,
                                         data: str = None,
                                         template_var_index=0,
                                         allow_multiple: bool = None,
                                         is_optional: bool = None,
                                         optional_name: str = None):
    protocol = create_protocol(ld_client, protocol_def)
    protocol = update_protocol_list_type_and_items(ld_client=ld_client,
                                                   protocol=protocol,
                                                   type=type,
                                                   new_values=picklist_value_arr)

    return update_protocol_data(ld_client=ld_client,
                                protocol=protocol,
                                tag=tag,
                                data=data,
                                template_var_index=template_var_index,
                                allow_multiple=allow_multiple,
                                is_optional=is_optional,
                                optional_name=optional_name)


def create_liverport_for_model_testing(ld_client: LDClient):
    global TEST_LR_ID
    if TEST_LR_ID != 0:
        return TEST_LR_ID
    live_report = LiveReport(title='LR to test picklist models',
                             description='some',
                             update_policy='by_cachebuilder',
                             default_rationale='Default rationale description',
                             owner='demo',
                             template=False,
                             shared_editable=True,
                             active=True,
                             project_id="0")

    created_live_report = ld_client.create_live_report(live_report)
    ld_client.add_rows(created_live_report.id, LIVE_REPORT_ROWS)
    TEST_LR_ID = created_live_report.id
    return TEST_LR_ID


def duplicate_protocol(ld_client: LDClient, protocol):
    protocol.id = None
    protocol.template_vars[0].model_picklist.id = None
    cleaned_temp_vars = []
    for temp_var in protocol.template_vars:
        temp_var.id = None
        cleaned_temp_vars.append(temp_var)
    for item in protocol.template_vars[0].model_picklist.picklist_item_choices:
        item.id = None
    for command in protocol.commands:
        command.id = None
    protocol.as_merged = None
    protocol.name = make_unique_name('Duped Protocol')

    return ld_client.create_protocol(protocol=protocol)


def assert_picklist_items_equal(picklist_items_1: list, picklist_items_2: list):
    assert len(picklist_items_1) == len(picklist_items_2)
    for i in range(len(picklist_items_1)):
        assert picklist_items_1[i].value == picklist_items_2[i].value
        assert picklist_items_1[i].id is not None
        assert picklist_items_2[i].id is not None


def assert_picklist_items_equal_to_values(picklist_items: list, values: list):
    assert len(picklist_items) == len(values)
    for i in range(len(picklist_items)):
        assert picklist_items[i].value == values[i]
        assert picklist_items[i].id is not None


def model_finished_executing(ld_client, addable_column_id):
    executed_lr = ld_client.execute_live_report(TEST_LR_ID)
    columns_have_values = containsValuesInLRRow(executed_lr, LIVE_REPORT_ROWS[0], addable_column_id)
    assert columns_have_values


def containsValuesInLRRow(lr, compound_id, addable_col_id):
    # Make a list in order of the values that should be accessed from the LR
    to_access = ['rows', compound_id, 'cells', addable_col_id, 'values']
    copy = lr
    for x in to_access:
        if x in copy and copy[x]:
            copy = copy[x]
        else:
            return False

    return True
