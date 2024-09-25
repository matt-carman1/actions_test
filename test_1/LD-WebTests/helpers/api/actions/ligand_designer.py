from ldclient.models import ColumnarLigandDesignerConfiguration
from ldclient.enums import DockingPrecision


def create_explicit_ligand_designer_config(ld_api_client,
                                           name,
                                           ref_ligand,
                                           grid_file,
                                           project_ids,
                                           dock_prec=DockingPrecision.SP):
    """
    create explicit ligand designer configuration with provided name and project_id.

    :param ld_api_client: fixture which creates api client
    :param name: name of configuration
    :param project_ids: list of project ids
    :param dock_prec: Docking precision can be either HTVS or SP (default)
    :return: ldclient.models.ColumnarLigandDesignerConfiguration
    """
    test_config_obj = ColumnarLigandDesignerConfiguration(name=name,
                                                          description='test create explicit config via ldclient',
                                                          grid_file_attachment_id=grid_file["id"],
                                                          reference_ligand_attachment_ids=[ref_ligand["id"]],
                                                          project_ids=project_ids,
                                                          docking_precision=dock_prec)
    return ld_api_client.create_explicit_columnar_ligand_designer_configuration(test_config_obj)
