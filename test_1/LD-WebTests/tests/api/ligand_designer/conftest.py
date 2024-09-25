import pytest

from helpers.api.actions.ligand_designer import create_explicit_ligand_designer_config
from helpers.api.extraction.ligand_designer_attachment_id import get_attachment_id
from library.utils import make_unique_name


@pytest.fixture(scope='function')
def create_explicit_lig_designer_config_via_api(request, ld_api_client):
    """
    Creates an explicit ligand designer configuration and archives configuration at the end

    :param request: request object with test metadata (from pytest fixture)
    :param ld_api_client: LDClient, ldclient object

    :return: The newly created columnar ligand designer configuration

    Example: ColumnarLigandDesignerConfiguration(id=350, name=Explicit Config1, description=test, addable_column_id=114700,
    folder=Computational Models/Ligand Designer, grid_file_attachment_id=4eb48505-f965-45b9-ae85-8adff4f982b9,
    protein_attachment_id=be13ac43-38a3-4640-91c5-f7acba185082,
    reference_ligand_attachment_ids=['b087e775-a704-4071-a2bc-b26c74780c92'], overlays=[], project_ids=['0'],
    docking_precision=SP, user=None, created_at=1631626779873, updated_at=1662072548144)
    """
    ref_grid_file = getattr(request.module, 'test_reference_grid_file', 'thrombin_grid.zip')
    grid_file_obj = get_attachment_id(ld_api_client, filename=ref_grid_file, attachment_type='ATTACHMENT')

    ref_ligand_file = getattr(request.module, 'test_reference_ligand_file', 'thrombin_reference_modified.mae')
    ref_ligand_obj = get_attachment_id(ld_api_client, filename=ref_ligand_file, attachment_type='THREE_D')

    explicit_test_config = create_explicit_ligand_designer_config(ld_api_client,
                                                                  name=make_unique_name("Test Docking"),
                                                                  ref_ligand=ref_ligand_obj,
                                                                  grid_file=grid_file_obj,
                                                                  project_ids=['4'])

    def finalizer():
        ld_api_client.delete_columnar_ligand_designer_configuration(explicit_test_config.id)

    request.addfinalizer(finalizer)

    return explicit_test_config
