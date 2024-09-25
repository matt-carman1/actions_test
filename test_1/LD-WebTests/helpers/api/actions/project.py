def get_folders_in_project(ld_client, *project_id):
    """
    Get folder name list for mentioned project(s)

    :param ld_client: LDClient, ldclient object
    :param project_id: str, id(s) of the project

    :return: list, list of folder names
    """
    folders = ld_client.list_folders(list(project_id))
    # getting folder name from Folder object
    return [folder.name for folder in folders]


def create_folder(ld_client, folder_name, project_id):
    """
    Create folder in mentioned project

    :param ld_client: LDClient, ldclient object
    :param folder_name: str, name of the folder
    :param project_id: str, id of the project

    :return: Folder, Folder object
    """
    return ld_client.create_folder(folder_name, project_id)
