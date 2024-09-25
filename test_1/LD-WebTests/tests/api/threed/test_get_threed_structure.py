from helpers.api.verification.compound_structures import verify_threed_structure


def test_get_threed_structure(ld_api_client):
    """
    This test checks ldclient method get_threed_structure()

    :param ld_api_client: ldclient object
    """
    # Get a ligand structure of MAE format
    observed_ligand_mae = ld_api_client.get_threed_structure('56100').as_dict()
    # Expected structure
    expected_threed_info_ligand_mae = {
        'structure_attachments': [{
            'id': '4803ba44be9e316b1f4be646f1ae9a8268e36483',
            'structure_transformation': 'file_upload',
            'attachment_alternate_id': '60fd210b-8cb9-4e06-b243-fcbedced48da'
        }],
        'entity_id': 'CMPD-2',
        'name': None,
        'file_format': 'mae',
        'id': '56100',
        'favorite': False,
        'structure_type': 'ligand',
    }
    # Compare the expected structure to the actual structure
    verify_threed_structure(expected_threed_info_ligand_mae, observed_ligand_mae)

    # Get a ligand structure of PSE format
    observed_ligand_pse = ld_api_client.get_threed_structure('38991').as_dict()
    # Expected structure
    expected_threed_info_ligand_pse = {
        'structure_attachments': [{
            'id': '4ff45a93d0783699c3aba0e1b7c621c98c732fa1',
            'structure_transformation': 'file_upload',
            'attachment_alternate_id': '7'
        }],
        'entity_id': 'CRA-035498',
        'name': None,
        'file_format': 'pse',
        'id': '38991',
        'favorite': False,
        'structure_type': 'ligand'
    }
    # Compare the expected structure to the actual structure
    verify_threed_structure(expected_threed_info_ligand_pse, observed_ligand_pse)

    # Get a protein structure of PSE format
    observed_protein_pse = ld_api_client.get_threed_structure('39138').as_dict()
    # Expected structure
    expected_threed_info_protein_pse = {
        'structure_attachments': [{
            'id': '38d918e217c947883c433d2a676ec32565f5f3c9',
            'structure_transformation': 'file_upload',
            'attachment_alternate_id': '55'
        }, {
            'id': 'a1478317eff1b3ea93730d0bbeedc32c41b3609c',
            'structure_transformation': 'truncated',
            'attachment_alternate_id': 'e159a31f-6109-4bb5-adaf-a4856b382cb0'
        }],
        'entity_id': None,
        'name': None,
        'file_format': 'pse',
        'id': '39138',
        'favorite': False,
        'structure_type': 'protein'
    }
    # Compare the expected structure to the actual structure
    verify_threed_structure(expected_threed_info_protein_pse, observed_protein_pse)
