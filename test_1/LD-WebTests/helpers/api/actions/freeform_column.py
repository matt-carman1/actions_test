from requests import RequestException

from helpers.api.actions.column import add_freeform_values
from helpers.api.actions.row import create_observation


def create_freeform_column_using_ffc_object(client, ffc_obj):
    """
    create freeform columns with provided freeform column object.

    :param client: LDClient, ldclient
    :param ffc_obj: ldclient.models.FreeformColumn, freeform column object to create in LD
    :return: ldclient.models.LiveReport and RequestException, FreeformColumn if successfully created or
                                                                RequestException if unsuccessful
    """
    try:
        response = client.create_freeform_column(ffc_obj)
    except RequestException as e:
        response = e
    # passing error/Success response in the response
    return response


def bulk_edit_ffc_values(ld_client, lr_id, ffc_column_id, compound_ids, ffc_value):
    """
    Function to bulk add/edit FFC values

    :param ld_client: LDClient
    :param lr_id: str, LiveReport id
    :param ffc_column_id: str, FreeForm Column id
    :param compound_ids: list, List of compound id's
    :param ffc_value: str, value for ffc column
    """
    text_ffc_observation_list = create_bulk_ffc_observations(lr_id, ffc_column_id, compound_ids, value=ffc_value)
    add_freeform_values(ld_client, text_ffc_observation_list)


def create_bulk_ffc_observations(lr_id, ffc_column_id, compound_ids, value):
    """
    Function to create bulk ffc observations

    :param lr_id: str, LiveReport id
    :param ffc_column_id: str, FreeForm Column id
    :param compound_ids: list, List of compound ids
    :param value: value for ffc column
    """
    ffc_observations_list = []
    # Traverse through given list of compounds and create an observation for each of them
    for compound_id in compound_ids:
        text_type_ffc_observation = create_observation(project_id='4',
                                                       entity_id=compound_id,
                                                       live_report_id=lr_id,
                                                       addable_column_id=ffc_column_id,
                                                       value=value)
        ffc_observations_list.append(text_type_ffc_observation)
    return ffc_observations_list


def bulk_delete_ffc_values(ld_client, lr_id, ffc_column_id, compound_ids):
    """
    Function to bulk delete FFC values

    :param ld_client: LDClient
    :param lr_id: str, LiveReport id
    :param ffc_column_id: str, FreeForm Column id
    :param compound_ids: list, List of compound ids
    """
    ffc_observation_list = create_bulk_ffc_observations(lr_id, ffc_column_id, compound_ids, value="")
    add_freeform_values(ld_client, ffc_observation_list)
