from ldclient.client import LDClient
from ldclient.models import Observation
from library.api.wait import wait_until_condition_met


def add_rows_to_live_report(ld_client: LDClient, live_report_id, corporate_ids):
    """
    Adds rows with specified corporate ids to a specific live report and LD client.

    :param ld_client: live design client where the row(s) should be added
    :param live_report_id: live report where the row(s) should be added
    :param corporate_ids: list of corporate ids whose rows should be added
    :return: list of compounds (additional rows) in the live report
    """
    response = ld_client.add_rows(live_report_id, corporate_ids)

    def rows_added_to_live_report():
        live_report_data = ld_client.live_report_results_metadata(live_report_id)
        row_keys = [row_info["entity_id"] for row_info in live_report_data["row_infos"]]
        row_keys.extend([row_info.get("virtual_entity_id", None) for row_info in live_report_data["row_infos"]])
        assert all(corporate_id in row_keys for corporate_id in corporate_ids)

    wait_until_condition_met(rows_added_to_live_report)
    return response


def remove_rows_from_live_report(ld_client: LDClient, live_report_id, corporate_ids):
    """
    Removes rows with specified corporate ids in specific a live report and LD client.

    :param ld_client: live design client where the row(s) should be removed
    :param live_report_id: live report where the row(s) should be removed
    :param corporate_ids: list of corporate ids whose rows should be removed
    :return: list of compounds (additional rows) in the live report
    """
    response = ld_client.remove_rows(live_report_id, corporate_ids)

    def rows_removed_from_live_report():
        live_report_data = ld_client.live_report_results_metadata(live_report_id)
        row_keys = [row_info["entity_id"] for row_info in live_report_data["row_infos"]]
        assert all(corporate_id not in row_keys for corporate_id in corporate_ids)

    wait_until_condition_met(rows_removed_from_live_report)
    return response


def get_live_report_rows(ld_client: LDClient, live_report_id):
    """
    Retrieves the rows in a single live report

    :param ld_client: live design client being affected
    :param live_report_id: live report id whose rows should be returned
    :return: rows in a single live report
    """
    return ld_client.live_report_rows(live_report_id)


def create_observation(project_id,
                       entity_id,
                       addable_column_id,
                       value,
                       live_report_id=None,
                       units=None,
                       lot_number=None,
                       salt_id=None,
                       protocol=None,
                       date=None,
                       notebook=None,
                       notebook_page=None,
                       concentration=None,
                       concentration_units=None,
                       operator=None,
                       batch=None,
                       attachment_urls=None,
                       published=None,
                       obs_id=None):
    """
    Helper function to create observation on an entity.
    For example, this could be an experimental value or a freeform column value paired with its corresponding entity ID.

    :param project_id: str, Numeric ID of the project that the observation is in.
    :param entity_id: str, ID of the entity that the observation is on.
    :param addable_column_id: str, ID of the addable column that the observation belongs to.
    :param value: str, Value of the observation.
    :param live_report_id: str, Numeric ID of the Live Report that the observation is in.
    :param units: str, Units.
    :param lot_number: str, Lot number.
    :param salt_id: str, Salt ID.
    :param protocol: str, ID of the protocol.
    :param date: str, Date of the observation.
    :param notebook: str,Notebook.
    :param notebook_page: str,Notebook page.
    :param concentration: float,Concentration.
    :param concentration_units: str, Concentration units.
    :param operator: str, Operator.
    :param batch: str, Batch.
    :param attachment_urls: list of dict, List of attachment URLs.
    :param published: bool, True if observation is published, False otherwise.
    :param obs_id: str, ID of the observation.

    :return: Observation, observation on an entity
    """
    return Observation(project_id=project_id,
                       entity_id=entity_id,
                       addable_column_id=addable_column_id,
                       value=value,
                       live_report_id=live_report_id,
                       units=units,
                       lot_number=lot_number,
                       salt_id=salt_id,
                       protocol=protocol,
                       date=date,
                       notebook=notebook,
                       notebook_page=notebook_page,
                       concentration=concentration,
                       concentration_units=concentration_units,
                       operator=operator,
                       batch=batch,
                       attachment_urls=attachment_urls,
                       published=published,
                       id=obs_id)
