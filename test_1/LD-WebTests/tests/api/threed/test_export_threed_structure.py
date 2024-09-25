import os

from helpers.extraction.paths import get_resource_path


def test_export_threed_structure(ld_api_client):
    """
    This test checks ldclient method export_threed_structure()

    It exports the structure to two binary files, matches the file content and
    verifies if the file size is within known limit

    :param ld_api_client: ldclient object
    """
    # Exports the 3D structure into 'resources' directory & writes to two different files to compare
    with open('resources/ligand1.mae', 'wb') as binary_file1, open('resources/ligand2.mae', 'wb') as binary_file2:
        binary_file1.write(ld_api_client.export_threed_structure('56100'))
        binary_file2.write(ld_api_client.export_threed_structure('56100'))

    # get the paths of the exported ligand files
    path_ligand1, path_ligand2 = get_resource_path('ligand1.mae'), get_resource_path('ligand2.mae')

    # Read both files and check if the contents are same
    with open(path_ligand1, 'rb') as binary_file1, open(path_ligand2, 'rb') as binary_file2:
        ligand_data1, ligand_data2 = binary_file1.read(), binary_file2.read()
        assert ligand_data1 == ligand_data2, "Exported ligand structures are different"

    # expected_ligand_size = 2292
    ligand_file_size = os.path.getsize(path_ligand1)

    # Checks if the file size is within certain limit (which varies in 2300 ~ 2500), taking buffer in each side
    assert 2000 < ligand_file_size < 3000, "Exported ligand file size is not within limit"

    # Exports the 3D structure into 'resources' directory & writes to two different files to compare
    with open('resources/protein1.pse', 'wb') as binary_file1, open('resources/protein2.pse', 'wb') as binary_file2:
        binary_file1.write(ld_api_client.export_threed_structure('38992'))
        binary_file2.write(ld_api_client.export_threed_structure('38992'))

    # get the paths of the exported protein files
    path_protein1, path_protein2 = get_resource_path('protein1.pse'), get_resource_path('protein2.pse')

    # Read both files and check if the contents are same
    with open(path_protein1, 'rb') as binary_file1, open(path_protein2, 'rb') as binary_file2:
        protein_data1, protein_data2 = binary_file1.read(), binary_file2.read()
        assert protein_data1 == protein_data2, "Exported protein structures are different"

    # expected_protein_size = 3012761
    protein_file_size = os.path.getsize(path_protein1)

    # Checks if the file size is within certain limit (which varies in 3000100 to 3050000), taking buffer in each side
    assert 3000000 < protein_file_size < 3100000, "Exported protein file size is not within limit"
