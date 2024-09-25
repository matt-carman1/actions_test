import pytest

from helpers.api.verification.live_report import wait_until_models_successfully_run
from ldclient import LDClient
from ldclient import enums
from ldclient.models import (LiveReport, Model, ModelCommand, ModelRecursive, ModelReturn)
from library.utils import make_unique_name, is_k8s
from textwrap import dedent


@pytest.mark.xfail(not is_k8s(), reason="SS-40265: RMQ issues in Old Jenkins")
def test_getting_model_results_with_empty_ligand(ld_client: LDClient):
    command_text = '''
    touch ${SDF-FILE} && $SCHRODINGER/run python3 <<'EOF'
    from schrodinger.structure import StructureReader
    fname = 'input'
    fname += '.sdf'
    print("Corporate ID,Result,Ligand")
    for st in StructureReader(fname):
        print("%s,%s,%s" % (st.title, '10', ''))
    EOF
    '''
    command_text = dedent(command_text)
    command = ModelCommand(command=command_text, driver_id=1)
    protocol_def = Model(name=make_unique_name('Protocol that returns empty ligand'),
                         commands=[command],
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
    protocol = ld_client.create_protocol(protocol_def)

    return_1 = ModelReturn(key="Result",
                           type="STRING",
                           units="",
                           precision=0,
                           tag=enums.RecursiveTag.DEFAULT,
                           display_name="result")
    return_2 = ModelReturn(key="Ligand",
                           type=enums.ModelReturnType.LIGAND.name,
                           units="",
                           precision=0,
                           tag=enums.RecursiveTag.DEFAULT,
                           display_name="ligand")
    created_model = ld_client.create_model(model=Model(name=make_unique_name('Model that returns an empty ligand'),
                                                       archived=False,
                                                       published=True,
                                                       user='demo',
                                                       folder="Computational Models/User Defined/demo",
                                                       returns=[return_1, return_2],
                                                       project_ids=None,
                                                       template_vars=None,
                                                       description='A child model for test_name',
                                                       parent=protocol.id,
                                                       commands=None,
                                                       batch_size=None,
                                                       command_type=protocol.command_type,
                                                       command_queue=protocol.command_queue))

    live_report = LiveReport(title='LR to test ' + created_model.name,
                             description='some',
                             update_policy='by_cachebuilder',
                             default_rationale='Default rationale description',
                             owner='demo',
                             template=False,
                             shared_editable=True,
                             active=True,
                             project_id="0")

    created_live_report = ld_client.create_live_report(live_report)
    rows = ["CRA-031137", "CRA-031437"]

    ld_client.add_rows(created_live_report.id, rows)
    all_addable_column_ids = [created_model.returns[0].addable_column_id, created_model.returns[1].addable_column_id]
    ld_client.add_columns(created_live_report.id, all_addable_column_ids)
    wait_until_models_successfully_run(ld_client, created_live_report.id, all_addable_column_ids, rows)

    executed_lr = ld_client.execute_live_report(created_live_report.id)

    model_return_1_values = [
        executed_lr['rows'][x]['cells'][created_model.returns[0].addable_column_id]['values']
        for x in executed_lr['rows']
    ]
    model_return_2_values = [
        executed_lr['rows'][x]['cells'][created_model.returns[1].addable_column_id]['values']
        for x in executed_lr['rows']
    ]

    for result in model_return_1_values:
        assert result[0]['value'] == '10'

    for result in model_return_2_values:
        assert result[0]['value'] == ''
