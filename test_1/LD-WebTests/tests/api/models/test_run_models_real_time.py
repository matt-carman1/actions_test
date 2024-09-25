from ldclient import LDClient
from ldclient.models import (LiveReport, Model, ModelCommand, ModelRecursive, ModelReturn)
from ldclient import enums
import json
from textwrap import dedent
from library.utils import make_unique_name

COMMAND_TEXT = '''
   touch ${SDF-FILE} && $SCHRODINGER/run python3 <<'EOF'
   import sys
   import csv
   from rdkit import Chem
   from schrodinger.structure import StructureReader
   fname = 'input'
   fname += '.sdf'
   corp = 'Corporate ID'
   writer = csv.DictWriter(open('results.csv', 'w'), fieldnames=['Corporate ID', 'corp_id'])
   print('Corporate ID,corp_id')
   writer.writeheader()
   suppl = Chem.SDMolSupplier(fname)
   for i,mol in enumerate(suppl):
       if not mol:
           continue                
       writer.writerow({'Corporate ID': mol.GetProp(corp), 'corp_id': mol.GetProp(corp) })
       print(mol.GetProp(corp)+\',\'+mol.GetProp(corp))
   EOF
   '''
COMMAND_TEXT = dedent(COMMAND_TEXT)
COMMAND = ModelCommand(command=COMMAND_TEXT, driver_id=1)

MOL = """"
     RDKit          2D

  0  0  0  0  0  0  0  0  0  0999 V3000
M  V30 BEGIN CTAB
M  V30 COUNTS 52 58 0 0 0
M  V30 BEGIN ATOM
M  V30 1 C -4.685714 0.485714 0.000000 0
M  V30 2 C -3.675562 -0.524438 0.000000 0
M  V30 3 C -2.246990 -0.524438 0.000000 0
M  V30 4 C -1.236838 0.485714 0.000000 0
M  V30 5 C -1.236838 1.914286 0.000000 0
M  V30 6 C -2.246990 2.924438 0.000000 0
M  V30 7 C -3.675562 2.924438 0.000000 0
M  V30 8 C -4.685714 1.914286 0.000000 0
M  V30 9 C -5.695867 -0.524438 0.000000 0
M  V30 10 C -7.124438 -0.524438 0.000000 0
M  V30 11 C -8.134591 0.485714 0.000000 0
M  V30 12 C -8.134591 1.914286 0.000000 0
M  V30 13 C -7.124438 2.924438 0.000000 0
M  V30 14 C -5.695867 2.924438 0.000000 0
M  V30 15 C -9.144743 2.924438 0.000000 0
M  V30 16 C -10.573315 2.924438 0.000000 0
M  V30 17 C -11.583467 1.914286 0.000000 0
M  V30 18 C -11.583467 0.485714 0.000000 0
M  V30 19 C -10.573315 -0.524438 0.000000 0
M  V30 20 C -9.144743 -0.524438 0.000000 0
M  V30 21 C -0.226685 2.924438 0.000000 0
M  V30 22 C 1.201886 2.924438 0.000000 0
M  V30 23 C 2.212039 1.914286 0.000000 0
M  V30 24 C 2.212039 0.485714 0.000000 0
M  V30 25 C 1.201886 -0.524438 0.000000 0
M  V30 26 C -0.226685 -0.524438 0.000000 0
M  V30 27 C -8.134591 -1.534591 0.000000 0
M  V30 28 C -8.134591 -2.963162 0.000000 0
M  V30 29 C -7.124438 -3.973315 0.000000 0
M  V30 30 C -5.695867 -3.973315 0.000000 0
M  V30 31 C -4.685714 -2.963162 0.000000 0
M  V30 32 C -4.685714 -1.534591 0.000000 0
M  V30 33 C -5.400000 -1.257143 0.000000 0
M  V30 34 C -4.389847 -2.267295 0.000000 0
M  V30 35 C -2.961276 -2.267295 0.000000 0
M  V30 36 C -1.951123 -1.257143 0.000000 0
M  V30 37 C -1.951123 0.171429 0.000000 0
M  V30 38 C -2.961276 1.181581 0.000000 0
M  V30 39 C -4.389847 1.181581 0.000000 0
M  V30 40 C -5.400000 0.171429 0.000000 0
M  V30 41 C -4.685714 -4.983467 0.000000 0
M  V30 42 C -4.685714 -6.412039 0.000000 0
M  V30 43 C -5.695867 -7.422191 0.000000 0
M  V30 44 C -7.124438 -7.422191 0.000000 0
M  V30 45 C -8.134591 -6.412039 0.000000 0
M  V30 46 C -8.134591 -4.983467 0.000000 0
M  V30 47 C -3.675562 -7.422191 0.000000 0
M  V30 48 C -2.246990 -7.422191 0.000000 0
M  V30 49 C -1.236838 -6.412039 0.000000 0
M  V30 50 C -1.236838 -4.983467 0.000000 0
M  V30 51 C -2.246990 -3.973315 0.000000 0
M  V30 52 C -3.675562 -3.973315 0.000000 0
M  V30 END ATOM
M  V30 BEGIN BOND
M  V30 1 1 1 2
M  V30 2 1 2 3
M  V30 3 1 3 4
M  V30 4 1 4 5
M  V30 5 1 5 6
M  V30 6 1 6 7
M  V30 7 1 7 8
M  V30 8 1 8 1
M  V30 9 1 1 9
M  V30 10 1 9 10
M  V30 11 1 10 11
M  V30 12 1 11 12
M  V30 13 1 12 13
M  V30 14 1 13 14
M  V30 15 1 14 8
M  V30 16 1 12 15
M  V30 17 1 15 16
M  V30 18 1 16 17
M  V30 19 1 17 18
M  V30 20 1 18 19
M  V30 21 1 19 20
M  V30 22 1 20 11
M  V30 23 1 5 21
M  V30 24 1 21 22
M  V30 25 1 22 23
M  V30 26 1 23 24
M  V30 27 1 24 25
M  V30 28 1 25 26
M  V30 29 1 26 4
M  V30 30 1 10 27
M  V30 31 1 27 28
M  V30 32 1 28 29
M  V30 33 1 29 30
M  V30 34 1 30 31
M  V30 35 1 31 32
M  V30 36 1 32 9
M  V30 37 1 33 34
M  V30 38 1 34 35
M  V30 39 1 35 36
M  V30 40 1 36 37
M  V30 41 1 37 38
M  V30 42 1 38 39
M  V30 43 1 39 40
M  V30 44 1 40 33
M  V30 45 1 30 41
M  V30 46 1 41 42
M  V30 47 1 42 43
M  V30 48 1 43 44
M  V30 49 1 44 45
M  V30 50 1 45 46
M  V30 51 1 46 29
M  V30 52 1 42 47
M  V30 53 1 47 48
M  V30 54 1 48 49
M  V30 55 1 49 50
M  V30 56 1 50 51
M  V30 57 1 51 52
M  V30 58 1 52 41
M  V30 END BOND
M  V30 END CTAB
M  END
$$$$
    """


def test_run_realtime_with_terminated_mol_structure(ld_client: LDClient):
    model_column_id = str(ld_client.model(3451).returns[0].addable_column_id)
    payload = {'mol': MOL, 'addable_column_ids': [model_column_id]}

    results = ld_client.client.post(service_path='/property_calculation', path='/search', data=json.dumps(payload))
    assert results[0]['mol'] == MOL  # Ensures we return the same mol sent
    assert results[0]['return_display_name'] == 'AlogP'
    assert results[0]['addable_column_id'] == model_column_id
    assert results[0]['status'] != 'failed'
    assert results[0]['value'] is not None


def test_run_realtime_with_terminated_mol_structure_custom_command(ld_client: LDClient):
    protocol_def = Model(
        name=make_unique_name('Protocol test_run_realtime_with_terminated_mol_structure_custom_command'),
        commands=[COMMAND],
        description='run a python file that requires the schrodinger python library',
        archived=False,
        published=False,
        folder="Computational Models/User Defined/demo",
        user="demo",
        project_ids=['0'],
        template_vars=[],
        returns=[],
        batch_size=ModelRecursive(tag=enums.RecursiveTag.DEFAULT, value=100),
        command_type=ModelRecursive(tag=enums.RecursiveTag.DEFAULT, value='REALTIME'),
        command_queue=ModelRecursive(tag=enums.RecursiveTag.READ_ONLY, value='sync'))

    protocol = ld_client.create_protocol(protocol_def)

    returns = [
        ModelReturn(key="corp_id",
                    type="STRING",
                    units="",
                    precision=0,
                    tag=enums.RecursiveTag.DEFAULT,
                    display_name="corp_id")
    ]
    model_def = Model(name=make_unique_name(make_unique_name('test_name: Child Model')),
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
    model = ld_client.create_model(model_def)

    payload = {'mol': MOL, 'addable_column_ids': [model.returns[0].addable_column_id]}

    results = ld_client.client.post(service_path='/property_calculation', path='/search', data=json.dumps(payload))
    assert results[0]['mol'] == MOL  # Ensures we return the same mol sent
    assert results[0]['addable_column_id'] == model.returns[0].addable_column_id
    assert results[0]['status'] == 'complete'
    assert results[0]['value'] is not None
    assert results[0]['value'] != ''
