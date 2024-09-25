from ldclient.client import LDClient
from ldclient.models import LiveReport

from helpers.api import actions
import os

ASSAY_NAME = "Pytest Assay"
COLUMN_NAME_SMILES = "Compound Structure"
COLUMN_NAME_ID = "Corporate ID"
CSV_HEADER_SMILES = COLUMN_NAME_SMILES + "," + ASSAY_NAME + "\n"
CSV_HEADER_ID = COLUMN_NAME_ID + "," + ASSAY_NAME + "\n"
CSV_ROW = "{},{}\n"


def create_smiles_string(seed):
    """
    Creates a smiles string from a specific seed.

    :param seed: assumed to be in the format RXXXX or VXXXX, where R/V denotes real/virtual and XXXX is any string
    :return: smiles string that is (probably) unique to each R/V + string combination.
    """
    length = int.from_bytes(seed.encode(), 'little') % 1000  # convert string seed to (probably) unique integer
    return "S" * length  # an arbitrarily long chain of sulfurs as a SMILES string


def create_compound_csv_file_by_smiles(seed):
    """
    Creates a csv file in the resources file with the same name as the seed with smiles headers and data.

    :param seed: assumed to be in the format RXXXX or VXXXX, where R/V denotes real/virtual and XXXX is any string
    :return: file name that was created
    """
    smiles = create_smiles_string(seed)
    filename = "resources/" + seed + ".csv"
    with open(filename, "w") as f:
        f.write(CSV_HEADER_SMILES)
        f.write(CSV_ROW.format(smiles, int.from_bytes(seed.encode(), 'little') % 1000))
        f.close()
    return filename


def create_compound_csv_file_by_id(seed):
    """
    Creates a csv file in the resources file with the same name as the seed with id headers and data
    :param seed: assumed to be in the format RXXXX or VXXXX, where R/V denotes real/virtual and XXXX is any string
    :return: file name that was created
    """
    filename = "resources/" + seed + ".csv"
    with open(filename, "w") as f:
        f.write(CSV_HEADER_ID)
        f.write(CSV_ROW.format(seed, int.from_bytes(seed.encode(), 'little') % 1000))
        f.close()
    return filename


def link_compounds(ld_client: LDClient, real_entity_id, virtual_entity_id):
    """
    Links compounds in a specified LD client.

    :param ld_client: live design client to link compounds
    :param real_entity_id: real entity id to link compounds
    :param virtual_entity_id: virtual entity id to link compounds
    :return: does not return
    """
    return ld_client.create_compound_link(real_entity_id, virtual_entity_id)


def unlink_compounds(ld_client: LDClient, compound_link_id):
    """
    Unlinks compounds in a specified LD client.

    :param ld_client: live design client to link compounds.
    :param compound_link_id: the compound link id that should be unlinked.
    :return: does not return
    """
    return ld_client.delete_compound_link(compound_link_id)


def search_compound_links(ld_client: LDClient, real_entity_ids):
    """
    Searches for compound links by real entity ids.

    :param ld_client: live design client to search for compound links.
    :param real_entity_ids: list of real entity ids to search for compound links
    :return: list of compound links that were found
    """
    return ld_client.get_compound_links_by_real_entity_ids(real_entity_ids)


def delete_all_compound_links_for_compound(ld_client, real_compound_id):
    """
    Deletes all compound links for specified real compound ids.

    :param ld_client: live design client where compound links should be deleted
    :param real_compound_id: list of real compound ids whose compound links should be deleted
    :return: does not return
    """
    compound_links = actions.compound.search_compound_links(ld_client, [real_compound_id])
    for link in compound_links:
        actions.compound.unlink_compounds(ld_client, link.id)


def create_real_compound(ld_client: LDClient, live_report: LiveReport, seed):
    """
    Creates a real compound with a given seed in a specific live report and LD client.

    :param ld_client: live design client to create a real compound
    :param live_report: live report to create a real compound
    :param seed: assumed to be in the format RXXXX or VXXXX, where R/V denotes real/virtual and XXXX is any string
    :return: seed provided
    """
    # NOTE(badlato): We can only register virtuals when importing by csv. To work around this,
    #   we are going to:
    #   1. import csv
    #   2. export to sdf
    #   3. remove the virtual from the LiveReport
    #   4. register as a real through sdf import
    #   5. add the real to the LiveReport through csv - with the assay data

    filename = create_compound_csv_file_by_smiles(seed)
    project_name = get_project_name_by_id(ld_client, live_report.project_id)
    csv_virtuals = register_compounds_from_csv(ld_client,
                                               project_name=project_name,
                                               lr_id=live_report.id,
                                               column_identifier=COLUMN_NAME_SMILES,
                                               file_name=filename)

    os.remove(filename)
    actions.row.add_rows_to_live_report(ld_client, live_report.id, csv_virtuals)
    sdf_contents_str = ld_client.export_live_report(live_report_id=str(live_report.id),
                                                    export_type='sdf',
                                                    corporate_ids_list=csv_virtuals).decode('utf-8')

    # setting the title of the sdf
    sdf_contents_str = sdf_contents_str.replace(csv_virtuals[0], seed)
    if sdf_contents_str and len(sdf_contents_str.split('\n', 1)[0].strip()) == 0:
        sdf_contents_str = seed + sdf_contents_str

    sdf_contents = sdf_contents_str.encode('utf-8')
    actions.row.remove_rows_from_live_report(ld_client, live_report.id, csv_virtuals)
    ld_client.register_compounds_sdf(project_name=project_name,
                                     file_contents=sdf_contents,
                                     file_name=filename,
                                     published=False,
                                     import_assay_data=False,
                                     use_corporate_id=True,
                                     compound_source="non_pri")
    real_filename = create_compound_csv_file_by_id(seed)
    register_compounds_from_csv(ld_client,
                                project_name,
                                live_report.id,
                                real_filename,
                                column_identifier=COLUMN_NAME_ID,
                                import_assay_data=True,
                                published=False)
    os.remove(filename)
    return seed


def create_virtual_compound(ld_client: LDClient, project_id, lr_id, seed):
    """
    Creates a virtual compound with a given seed in a specific live report and LD client.

    :param ld_client: live design client to create the virtual compound
    :param project_id: ID of the project
    :param lr_id: ID of the live report
    :param seed: assumed to be in the format RXXXX or VXXXX, where R/V denotes real/virtual and XXXX is any string
    :return: id of the virtual compound
    """
    filename = create_compound_csv_file_by_smiles(seed)
    project_name = get_project_name_by_id(ld_client, project_id)
    csv_virtuals = register_compounds_from_csv(ld_client,
                                               project_name,
                                               lr_id,
                                               filename,
                                               column_identifier=COLUMN_NAME_SMILES,
                                               import_assay_data=True,
                                               published=False)
    os.remove(filename)
    return csv_virtuals[0]


def get_project_name_by_id(ld_client: LDClient, project_id):
    """
    Gets the project name by a given project id in a specific LD client.

    :param ld_client: live design client to get the project name
    :param project_id: project id for the project name being returned
    :return: project name
    """
    matching_projects = [p for p in ld_client._projects_w_global() if p.id == project_id]
    return matching_projects[0].name if matching_projects else matching_projects


def register_compounds_from_csv(ld_client,
                                project_name,
                                lr_id,
                                file_name,
                                file_contents_input=None,
                                column_identifier="Compound Structure",
                                compound_identifier_type="CSV_SMILES",
                                import_assay_data=False,
                                published=False):
    """
    Registers compound into specified LR/project using register_compounds_via_csv method in ld client.

    :param ld_client: LDClient, LDClient
    :param project_name: str, name of the project
    :param lr_id: str, ID of the livereport
    :param file_name: str, Name of the csv file
    :param file_contents_input: str, file contents from the input
    :param column_identifier: str, Column Identifier
    :param import_assay_data: boolean, True if you want to import data, False otherwise
    :param published: boolean, True to publish data to other livereports, False otherwise
    """
    with open(file_name, 'rb') as file_contents:
        # getting file contents from testdata if passed, otherwise using file to get the contents
        file_contents = file_contents_input if file_contents_input else file_contents
        response = ld_client.register_compounds_via_csv(project_name,
                                                        file_contents,
                                                        column_identifier,
                                                        file_name,
                                                        live_report_id=lr_id,
                                                        import_assay_data=import_assay_data,
                                                        published=published,
                                                        compound_identifier_type=compound_identifier_type)
    return response


def create_compound_through_smiles(ld_client, file_name, project_name):
    """
    Create compound for the given csv

    :param ld_client: LDClient
    :param file_name: str, name of the file
    :param project_name: str, name of the project
    """
    with open(file_name, 'rb') as file_contents:
        compounds = ld_client.register_compounds_sdf(project_name, file_contents.read(), file_name)
        compound_ids = [compound['corporate_id'] for compound in compounds]
        file_contents.close()
    return compound_ids


def compound_search_by_id(ld_client, query, project_id, database_names=[]):
    """
    Compound search via ID

    :param ld_client: LDClient, ldclient object
    :param query: str, the query to be passed
    :param project_id: str, the project id to search the compounds
    :param database_names: list of str, the list of databases to search for
    :return:
    """

    list_of_corp_ids = ld_client.compound_search_by_id(query, database_names, project_id)

    return list_of_corp_ids


def compound_search(ld_client, mol_smiles, search_type=None, ignore_stereospecific=False):
    """
    Retrieves the corporate ids of the compounds that match the structure search

    :param ld_client: LDClient, ldclient object
    :param mol_smiles: str, SMILES of the compound to search
    :param search_type: str, type of search: EXACT, SIMILARITY or SUBSTRUCTURE
    :param ignore_stereospecific: bool, Determines whether or not ignore stereo information during search. This
    option is honored only for EXACT search type.
    :return: List of corporate ids
    """

    list_of_matching_corp_ids = ld_client.compound_search(molecule=mol_smiles,
                                                          search_type=search_type,
                                                          ignore_stereospecific=ignore_stereospecific)

    return list_of_matching_corp_ids


def load_compounds_from_csv(ld_client,
                            lr_id,
                            filename,
                            project_name,
                            is_published=False,
                            is_compounds_only=True,
                            is_columns_only=False,
                            column_identifier="Compound Structure",
                            compound_identifier_type="CSV_SMILES"):
    """
    Import compounds into LR using load_csv method

    :param ld_client: LDClient, ld client object
    :param lr_id: str, ID of livereport
    :param filename: str, name of the file to be imported
    :param project_name: str, project name
    :param is_published: bool, Whether to publish data, default value is False
    :param is_compounds_only: bool, whether to import compounds only, default value is True
    :param is_columns_only: bool, whether to import columns only, default value is False
    :param column_identifier: str, column identifier, default value is "Compound Structure"
    """
    response = ld_client.load_csv(live_report_id=lr_id,
                                  filename=filename,
                                  project_name=project_name,
                                  published=is_published,
                                  compounds_only=is_compounds_only,
                                  columns_only=is_columns_only,
                                  identifier=column_identifier,
                                  compound_identifier_type=compound_identifier_type)
    # getting compound ids from row
    corporate_ids = [row['corporate_id'] for row in response if row['corporate_id']]
    return corporate_ids
