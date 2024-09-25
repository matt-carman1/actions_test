import pytest

from helpers.api.actions.livereport import export_live_report
from helpers.api.verification.file_contents import verify_sdf_contents

live_report_id = '2048'
HIDDEN_COLUMN_IN_LR_2048 = '29'


@pytest.mark.parametrize("ld_api_client", [('demo', 'demo'), ('userB', 'userB')], indirect=True)
def test_export_complete_live_report(ld_api_client):
    """
    Export an entire LiveReport to sdf as admin and non-admin user and verify exported sdf contents.

    :param ld_api_client: fixture that returns ldclient object
    """
    expected_columns = [
        'ID', 'All IDs', 'Lot Scientist', 'PK_PO_RAT (AUC) [uM]', 'PK_PO_RAT (Absorption) [uM]',
        'DRC TEST ASSAY (IC50%) [uM]', 'Test RPE Formula', 'Test RPE MPO', 'CorpID String (CorpID String)'
    ]

    expected_data = {
        'ID': ['V055682', 'V055683', 'V055685', 'V055691'],
        'All IDs': ['V055682', 'V055683', 'V055685', 'V055691'],
        'Lot Scientist': ['LiveDesign\ndemo', 'LiveDesign\ndemo', 'LiveDesign\ndemo', 'LiveDesign\ndemo'],
        'PK_PO_RAT (AUC) [uM]': ['20\n10', '0.3\n0.2\n0.1', '100'],
        'PK_PO_RAT (Absorption) [uM]': ['100\n50', '3\n2\n1', '7000'],
        'DRC TEST ASSAY (IC50%) [uM]': ['0.075', '0.22', '0.4', '1'],
        'Test RPE Formula': ['200'],
        'Test RPE MPO': ['1'],
        'CorpID String (CorpID String)': [
            'This is a long string for corporate ID: V055682', 'This is a long string for corporate ID: V055683',
            'This is a long string for corporate ID: V055685', 'This is a long string for corporate ID: V055691'
        ]
    }

    # export complete livereport in sdf format
    exported_live_report = export_live_report(ld_api_client, live_report_id, export_type='sdf')
    # verify exported file contents
    verify_sdf_contents(expected_columns, expected_data, exported_live_report)


@pytest.mark.parametrize("ld_api_client", [('demo', 'demo'), ('userB', 'userB')], indirect=True)
def test_export_live_report_with_selected_columns(ld_api_client):
    """
    Export LiveReport with selected columns to sdf as admin and non-admin user and verify exported sdf contents.

    :param ld_api_client: fixture that returns ldclient object
    """
    expected_data = {
        'ID': ['V055682', 'V055683', 'V055685', 'V055691'],
        'All IDs': ['V055682', 'V055683', 'V055685', 'V055691'],
        'PK_PO_RAT (AUC) [uM]': ['20\n10', '0.3\n0.2\n0.1', '100'],
        'PK_PO_RAT (Absorption) [uM]': ['100\n50', '3\n2\n1', '7000'],
        'DRC TEST ASSAY (IC50%) [uM]': ['0.075', '0.22', '0.4', '1'],
        'Test RPE Formula': ['200'],
        'CorpID String (CorpID String)': [
            'This is a long string for corporate ID: V055682', 'This is a long string for corporate ID: V055683',
            'This is a long string for corporate ID: V055685', 'This is a long string for corporate ID: V055691'
        ]
    }
    expected_columns = [
        'ID', 'All IDs', 'PK_PO_RAT (AUC) [uM]', 'DRC TEST ASSAY (IC50%) [uM]', 'Test RPE Formula',
        'CorpID String (CorpID String)'
    ]
    column_ids_to_export = ['1226', '1227', '1228', '606', '3186', '3937', '16']

    # Export livereport with selected columns to sdf format.
    exported_live_report = export_live_report(ld_api_client,
                                              live_report_id,
                                              column_ids=column_ids_to_export,
                                              export_type='sdf')
    # Verify exported file contents
    verify_sdf_contents(expected_columns, expected_data, exported_live_report)


@pytest.mark.parametrize("ld_api_client", [('demo', 'demo'), ('userB', 'userB')], indirect=True)
def test_export_live_report_with_selected_compounds(ld_api_client):
    """
    Export LiveReport with selected compounds to sdf as admin and non-admin user and verify exported sdf contents.

    :param ld_api_client: fixture that returns ldclient object
    """
    compounds_to_be_exported = ['V055682', 'V055691']
    expected_data = {
        'ID': ['V055682', 'V055691'],
        'All IDs': ['V055682', 'V055691'],
        'Lot Scientist': ['LiveDesign\ndemo', 'LiveDesign\ndemo'],
        'PK_PO_RAT (AUC) [uM]': ['20\n10', '100'],
        'PK_PO_RAT (Absorption) [uM]': ['100\n50', '7000'],
        'DRC TEST ASSAY (IC50%) [uM]': ['0.075', '1'],
        # NOTE(badlato): We need to make verify_sdf_contents smarter if we want to verify what
        # row each value is on, rather than just the order of the values
        'Test RPE Formula': ['200'],
        'Test RPE MPO': ['1'],
        'CorpID String (CorpID String)': [
            'This is a long string for corporate ID: V055682', 'This is a long string for corporate ID: V055691'
        ]
    }
    expected_columns = [
        'ID', 'All IDs', 'Lot Scientist', 'PK_PO_RAT (AUC) [uM]', 'PK_PO_RAT (Absorption) [uM]',
        'DRC TEST ASSAY (IC50%) [uM]', 'Test RPE Formula', 'Test RPE MPO', 'CorpID String (CorpID String)'
    ]

    # Export livereport with selected compounds to sdf format
    exported_live_report = export_live_report(ld_api_client,
                                              live_report_id,
                                              export_type='sdf',
                                              entity_ids=compounds_to_be_exported)
    # verify exported file contents
    verify_sdf_contents(expected_columns, expected_data, exported_live_report)


@pytest.mark.parametrize("ld_api_client", [('demo', 'demo'), ('userB', 'userB')], indirect=True)
def test_export_live_report_selected_columns_selected_compounds(ld_api_client):
    """
    Test export live report with selected columns and selected compounds to sdf as admin and non-admin user and verify exported sdf contents.

    :param ld_api_client: fixture that returns ldclient object
    """
    compounds_to_be_exported = ['V055682', 'V055691']
    columns_to_be_exported = ['1226', '1227', '1228', '606', '3186', '3937', '16']

    expected_data = {
        'ID': ['V055682', 'V055691'],
        'All IDs': ['V055682', 'V055691'],
        'PK_PO_RAT (AUC) [uM]': ['20\n10', '100'],
        'PK_PO_RAT (Absorption) [uM]': ['100\n50', '7000'],
        'DRC TEST ASSAY (IC50%) [uM]': ['0.075', '1'],
        'Test RPE Formula': ['200'],
        'CorpID String (CorpID String)': [
            'This is a long string for corporate ID: V055682', 'This is a long string for corporate ID: V055691'
        ]
    }
    expected_columns = [
        'ID', 'All IDs', 'PK_PO_RAT (AUC) [uM]', 'DRC TEST ASSAY (IC50%) [uM]', 'Test RPE Formula',
        'CorpID String (CorpID String)'
    ]

    # export live report with selected compounds and selected columns to sdf format
    exported_live_report = export_live_report(ld_api_client,
                                              live_report_id,
                                              column_ids=columns_to_be_exported,
                                              entity_ids=compounds_to_be_exported,
                                              export_type='sdf')
    # verify exported file contents
    verify_sdf_contents(expected_columns, expected_data, exported_live_report)


@pytest.mark.parametrize("ld_api_client", [('demo', 'demo'), ('userB', 'userB')], indirect=True)
def test_export_live_report_with_selected_hidden_columns(ld_api_client):
    """
    Export LiveReport with selected columns to sdf as admin and non-admin user and verify exported sdf contents.

    :param ld_api_client: fixture that returns ldclient object
    """
    expected_data = {
        'ID': ['V055682', 'V055683', 'V055685', 'V055691'],
        'Lot Date Registered': [
            '2016-08-04 16:03:11\n2015-11-16 11:53:32', '2016-08-04 15:35:47\n2015-11-16 11:53:32',
            '2016-08-04 15:32:05\n2015-11-16 11:53:39', '2016-08-04 15:32:13\n2015-11-16 11:53:39'
        ]
    }
    expected_columns = ['ID', 'Lot Date Registered']
    column_ids_to_export = ['1226', HIDDEN_COLUMN_IN_LR_2048]

    # Export livereport with selected columns to sdf format.
    exported_live_report = export_live_report(ld_api_client,
                                              live_report_id,
                                              column_ids=column_ids_to_export,
                                              export_type='sdf')
    # Verify exported file contents
    verify_sdf_contents(expected_columns, expected_data, exported_live_report)
