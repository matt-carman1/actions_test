from pathlib import Path


def get_resource_path(file_name):
    """
    Returns a string for the path to a specified file in the resources directory.

    :param file_name: file name
    :type file_name: str
    :return: A path to the file in the resources directory
    :rtype: string
    """
    data_folder = "resources"
    file_to_import = (Path.cwd() / data_folder / file_name).resolve()
    return str(file_to_import)
