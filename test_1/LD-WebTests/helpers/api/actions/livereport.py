from ldclient.client import LDClient
from ldclient.models import LiveReport
from requests import RequestException
import csv


def create_new_live_report(ld_client, title, project_id="4"):
    """
    Creates a new live report with a given title and project id in a specifc LD client.

    :param ld_client: live design client to create the new live report
    :param title: title of the live report being created
    :param project_id: project id where the live report is created, defaulted to "0" or "Global"
    :return: live report that was created
    """
    live_report = LiveReport(
        title=title,
        description="some",
        update_policy="by_cachebuilder",
        default_rationale="Default rationale description",
        owner="demo",
        template=False,
        shared_editable=True,
        active=True,
        project_id=project_id,
    )
    return ld_client.create_live_report(live_report)


def delete_live_report(ld_client: LDClient, live_report_id):
    """
    Deletes a live report with a given live report id in a specific LD client.

    :param ld_client: live design client where the live report should be deleted
    :param live_report_id: live report id of the live report to be deleted
    :return: does not return
    """
    ld_client.delete_live_report(live_report_id)


# TODO: Discuss it's usage. Nitin: I am not sure why are we wrapping a ldclient method in a separate helper. I would
# appreciate if some could explain the objective/goal behind doing this.
def export_live_report(ld_client, live_report_id, export_type="csv", column_ids=None, entity_ids=None):
    """
    Exports given columns and entities in a live report for a specific LD client to a provided format.

    :param ld_client: live design client whose live report should be exported
    :param live_report_id: the live report id of the live report to be exported
    :param export_type: the type of file to be created upon export: sdf, csv(default), xls, pptx, pdf
    :param column_ids: list of column ids whose columns should be exported
    :param entity_ids: list of entity ids to be exported
    :return: bytes, The exported Live Report
    """
    first_export = ld_client.export_live_report(
        live_report_id,
        export_type=export_type,
        projection=column_ids,
        corporate_ids_list=entity_ids,
    )
    return ld_client.export_live_report(
        live_report_id,
        export_type=export_type,
        projection=column_ids,
        corporate_ids_list=entity_ids,
    )


def refresh_live_report(ld_client: LDClient, live_report: LiveReport):
    """
    Refreshes the given live report in a LD client.

    :param ld_client: live design client whose live report should be refreshed
    :param live_report: live report to be refreshed
    :return: does not return
    """
    ld_client.invalidate_live_reports_by_live_report_ids([live_report.id])
    ld_client.execute_live_report(live_report.id)


def get_live_report_as_csv(ld_client: LDClient, live_report: LiveReport):
    """
    Gets a specific live report in a csv format

    :param ld_client: live design client whose live report should be converted to csv
    :param live_report: live report to be returned in csv format
    :return: csv dictionary of the live report
    """
    raw_csv = ld_client.export_live_report(live_report.id, 'csv')
    return csv.DictReader(raw_csv.decode('utf-8').splitlines())


def load_sdf_in_lr(ld_client,
                   live_report_id,
                   file_path,
                   compounds_only=False,
                   project='Global',
                   compound_source=None,
                   published=False):
    """
    Loads compounds into LiveDesign via sdf synchronously

    :param ld_client: LDClient, ldclient object
    :param live_report_id: str, live report to add compounds to
    :param file_path: str, the path of the sd file
    :param compound_source: str, set to pri for importing virtuals, anything else for reals (ex: non-pri)
    :return: list_of_compound_objects: 	A list of objects representing compounds from the original project table -
    as dicts
    """

    list_of_compound_objects = ld_client.load_sdf(live_report_id,
                                                  filename=file_path,
                                                  compounds_only=compounds_only,
                                                  project_name=project,
                                                  compound_source=compound_source,
                                                  published=published)

    return list_of_compound_objects


def live_report_details(ld_client, live_report_id):
    """
    Returns a LiveReport object with details
    Examples are title, description, update_policy, template, default_rationale, assay_view, id, alias, project_id,
    owner, is_private, addable_columns, last_saved_date, report_level, sorted_columns, hidden_rows, scaffolds,
    experiment_column_id, type etc.

    :param ld_client: LDClient, ldclient object
    :param live_report_id: str, ID of the livereport.
    :return: list, all rows in a LiveReport
    """
    live_report_object = ld_client.live_report(live_report_id=live_report_id)
    return live_report_object


def execute_live_report(ld_client, lr_id):
    """
    Executes the livereport by using execute_live_report function under ldclient.client and returns the response.

    :param ld_client: ldclient
    :param lr_id: str, ID of livereport
    :return: JSON and RequestException, response JSON if successfully executed or RequestException if unsuccessful
    """
    try:
        response = ld_client.execute_live_report(lr_id)
    except RequestException as e:
        response = e
    # passing error/Success response in the response
    return response


def update_live_report(ld_client, live_report_id, live_report):
    """
    Updates Live Report using update_live_report ldclient function.

    :param ld_client: ldclient
    :param live_report_id: ldclient.models.LiveReport to create in LD
    :param live_report: LiveReport object
    :return: ldclient.models.LiveReport
    """

    return ld_client.update_live_report(live_report_id, live_report)


def convert_live_report_into_template(ld_client, live_report):
    """
    Converts the given LiveReport into template

    :param ld_client: ldclient object
    :param live_report: LiveReport object
    :return: updated LiveReport object if successfully executed or RequestException
    """
    live_report.template = True
    try:
        response = ld_client.update_live_report(live_report.id, live_report)
    except RequestException as e:
        response = e
    # passing error/Success response in the response
    return response
