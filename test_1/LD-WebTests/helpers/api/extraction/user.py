def get_users_list(ld_client, include_permissions=False):
    """
    Get list of users

    :param ld_client: LDClient, ldclient object
    :param include_permissions: bool, controls if response contains the user permissions

    :return: List of users (:class:`models.User` objects as dictionaries)
    """
    return ld_client.list_users(include_permissions=include_permissions)
