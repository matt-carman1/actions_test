from collections import OrderedDict

import pytest

from helpers.api.actions.livereport import export_live_report
from helpers.api.verification.file_contents import verify_csv_contents

live_report_id = '2048'
visible_columns_in_lr = [
    'Compound Structure', 'ID', 'All IDs', 'Rationale', 'Lot Scientist', 'PK_PO_RAT (AUC) [uM]',
    'PK_PO_RAT (Absorption) [uM]', 'DRC TEST ASSAY (IC50%) [uM]', 'Test RPE Formula', 'Test RPE MPO',
    'CorpID String (CorpID String)'
]
visible_rows_in_lr = ['V055682', 'V055683', 'V055685', 'V055691']


@pytest.mark.parametrize("ld_api_client", [('demo', 'demo'), ('userB', 'userB')], indirect=True)
def test_export_complete_live_report(ld_api_client):
    """
    Export an entire LiveReport to csv as admin and non-admin user and verify exported csv contents.

    :param ld_api_client: fixture that returns ldclient object
    """
    ld_api_client.execute_live_report(live_report_id)
    exported_live_report = export_live_report(ld_api_client, live_report_id)
    # verify column contents
    verify_csv_contents(
        exported_live_report,
        OrderedDict([
            ('Compound Structure', [
                'CCC1CCC(CC1)C1CCC(CC1)C1CCC(CC1)C1CCC(C)CC1', 'CC1CCC(CC1)C1CCC(CC1)C1CCC(CC1)C1CCC(CC1)C1=CC=CC=C1',
                'C1CC(CCC1C1CCC(CC1)C1CCC(CC1)C1=CC=CC=C1)C1CCC(CC1)C1=CC=CC=C1',
                'C(C1CCC(CC1)C1CCC(CC1)C1CCC(CC1)C1CCC(CC2=CC=CC=C2)CC1)C1=CC=CC=C1'
            ]), ('ID', ['V055682', 'V055683', 'V055685', 'V055691']),
            ('All IDs', ['V055682', 'V055683', 'V055685', 'V055691']), ('Rationale', ['', '', '', '']),
            ('Lot Scientist', ['LiveDesign;demo', 'LiveDesign;demo', 'LiveDesign;demo', 'LiveDesign;demo']),
            ('PK_PO_RAT (AUC) [uM]', ['20;10', '', '0.3;0.2;0.1', '100']),
            ('PK_PO_RAT (Absorption) [uM]', ['100;50', '', '3;2;1', '7000']),
            ('DRC TEST ASSAY (IC50%) [uM]', ['0.075', '0.22', '0.4', '1']), ('Test RPE Formula', ['', '', '', '200']),
            ('Test RPE MPO', ['', '', '', '1']),
            ('CorpID String (CorpID String)', [
                'This is a long string for corporate ID: V055682', 'This is a long string for corporate ID: V055683',
                'This is a long string for corporate ID: V055685', 'This is a long string for corporate ID: V055691'
            ])
        ]))


@pytest.mark.parametrize("ld_api_client", [('demo', 'demo'), ('userB', 'userB')], indirect=True)
def test_export_live_report_selected_compounds(ld_api_client):
    """
    Export only some compounds in a LiveReport to csv as admin and non-admin user and verify exported csv contents.

    :param ld_api_client: fixture that returns ldclient object
    """
    compounds_to_be_exported = ['V055683', 'V055691']
    exported_live_report = export_live_report(ld_api_client, live_report_id, entity_ids=compounds_to_be_exported)
    verify_csv_contents(
        exported_live_report,
        OrderedDict([
            ('Compound Structure', [
                'CC1CCC(CC1)C1CCC(CC1)C1CCC(CC1)C1CCC(CC1)C1=CC=CC=C1',
                'C(C1CCC(CC1)C1CCC(CC1)C1CCC(CC1)C1CCC(CC2=CC=CC=C2)CC1)C1=CC=CC=C1'
            ]), ('ID', ['V055683', 'V055691']), ('All IDs', ['V055683', 'V055691']), ('Rationale', ['', '']),
            ('Lot Scientist', ['LiveDesign;demo', 'LiveDesign;demo']), ('PK_PO_RAT (AUC) [uM]', ['', '100']),
            ('PK_PO_RAT (Absorption) [uM]', ['', '7000']), ('DRC TEST ASSAY (IC50%) [uM]', ['0.22', '1']),
            ('Test RPE Formula', ['', '200']), ('Test RPE MPO', ['', '1']),
            ('CorpID String (CorpID String)',
             ['This is a long string for corporate ID: V055683', 'This is a long string for corporate ID: V055691'])
        ]))


@pytest.mark.parametrize("ld_api_client", [('demo', 'demo'), ('userB', 'userB')], indirect=True)
def test_export_live_report_selected_columns(ld_api_client):
    """
    Export only some columns in a LiveReport to csv as admin and non-admin user and verify exported csv contents.

    :param ld_api_client: fixture that returns ldclient object
    """
    # Column ids for 'ID', 'All IDs', 'Compound structure', 'PK_PO_RAT (AUC) [uM]',
    # 'DRC TEST ASSAY (IC50%) [uM]', 'Test RPE Formula', 'CorpID String (CorpID String)' respectively
    column_ids = ['1226', '1227', '1228', '606', '3186', '3937', '16']
    exported_live_report = export_live_report(ld_api_client, live_report_id, column_ids=column_ids)
    verify_csv_contents(
        exported_live_report,
        OrderedDict([
            ('Compound Structure', [
                'CCC1CCC(CC1)C1CCC(CC1)C1CCC(CC1)C1CCC(C)CC1', 'CC1CCC(CC1)C1CCC(CC1)C1CCC(CC1)C1CCC(CC1)C1=CC=CC=C1',
                'C1CC(CCC1C1CCC(CC1)C1CCC(CC1)C1=CC=CC=C1)C1CCC(CC1)C1=CC=CC=C1',
                'C(C1CCC(CC1)C1CCC(CC1)C1CCC(CC1)C1CCC(CC2=CC=CC=C2)CC1)C1=CC=CC=C1'
            ]), ('ID', ['V055682', 'V055683', 'V055685', 'V055691']),
            ('All IDs', ['V055682', 'V055683', 'V055685', 'V055691']),
            ('PK_PO_RAT (AUC) [uM]', ['20;10', '', '0.3;0.2;0.1', '100']),
            ('DRC TEST ASSAY (IC50%) [uM]', ['0.075', '0.22', '0.4', '1']), ('Test RPE Formula', ['', '', '', '200']),
            ('CorpID String (CorpID String)', [
                'This is a long string for corporate ID: V055682', 'This is a long string for corporate ID: V055683',
                'This is a long string for corporate ID: V055685', 'This is a long string for corporate ID: V055691'
            ])
        ]))


@pytest.mark.parametrize("ld_api_client", [('demo', 'demo'), ('userB', 'userB')], indirect=True)
def test_export_live_report_selected_columns_selected_compounds(ld_api_client):
    """
    Test export live report with selected columns and selected compounds as admin and non-admin user and verify exported csv contents.

    :param ld_api_client: fixture that returns ldclient object
    """
    compounds_to_be_exported = ['V055682', 'V055691']
    columns_to_be_exported = ['1226', '1227', '1228', '606', '3186', '3937', '16']
    exported_live_report = export_live_report(ld_api_client,
                                              live_report_id,
                                              column_ids=columns_to_be_exported,
                                              entity_ids=compounds_to_be_exported)
    verify_csv_contents(
        exported_live_report,
        OrderedDict([
            ('Compound Structure', [
                'CCC1CCC(CC1)C1CCC(CC1)C1CCC(CC1)C1CCC(C)CC1',
                'C(C1CCC(CC1)C1CCC(CC1)C1CCC(CC1)C1CCC(CC2=CC=CC=C2)CC1)C1=CC=CC=C1'
            ]), ('ID', ['V055682', 'V055691']), ('All IDs', ['V055682', 'V055691']),
            ('PK_PO_RAT (AUC) [uM]', ['20;10', '100']), ('DRC TEST ASSAY (IC50%) [uM]', ['0.075', '1']),
            ('Test RPE Formula', ['', '200']),
            ('CorpID String (CorpID String)',
             ['This is a long string for corporate ID: V055682', 'This is a long string for corporate ID: V055691'])
        ]))
