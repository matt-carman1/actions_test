from helpers.extraction import paths


def get_attachment_id(ld_api_client, filename, attachment_type, project_id_list=[4]):
    """
    extract attachment id using ldclient method get_or_create_attachment

    :param ld_api_client: fixture which creates api client
    :param filename: name of attachment file
    :param attachment_type: type of attachment ('THREE_D', 'ATTACHMENT' or 'IMAGE')
    :param project_id_list: default list of project ids
    :return: the content of the persisted AttachmentMetadata, as a dict.
    """
    data_path = paths.get_resource_path("api/")
    return ld_api_client.get_or_create_attachment('{}/{}'.format(data_path, filename),
                                                  attachment_type,
                                                  project_ids=project_id_list)
