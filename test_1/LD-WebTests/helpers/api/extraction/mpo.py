def get_mpo_names_from_project(ldclient, project_ids=None):
    """
    Get list of mpo names present in the project

    :param ldclient: LDClient, ldclient object
    :param project_ids: list, list of project ids

    :return:list, list of mpo names
    """
    mpo_objs = ldclient.list_mpos(project_ids=project_ids)
    return [mpo.name for mpo in mpo_objs]
