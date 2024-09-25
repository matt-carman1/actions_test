from ldclient.client import LDClient
from ldclient.models import LiveReport, FreeformColumn, ModelReturn, Model, ModelRecursive, ModelCommand, \
    ModelTemplateVar
from library.api.wait import wait_until_condition_met
from library.api.exceptions import LiveDesignAPIException


def create_freeform_column(ld_client: LDClient, live_report: LiveReport, name='An FFC'):
    """
    Creates a freeform column of a specified name in a specific live report and LD client.

    :param ld_client: live design client where the freeform column should be created
    :param live_report: live report where the freeform column should be created
    :param name: name to call freeform column, defaulted to "An FFC"
    :return: freeform column that was created
    """
    freeform_column = ld_client.create_freeform_column(
        FreeformColumn(name=name,
                       type=FreeformColumn.COLUMN_TEXT,
                       description='Pytest Freeform Column',
                       project_id=live_report.project_id,
                       live_report_id=str(live_report.id),
                       published=True,
                       picklist=False))
    ld_client.add_columns(str(live_report.id), [freeform_column.id])

    def freeform_column_added():
        live_report_data = ld_client.live_report_results_metadata(str(live_report.id))
        actual_column_ids = set(live_report_data["columns"].keys())
        assert str(freeform_column.id) in actual_column_ids

    wait_until_condition_met(freeform_column_added)
    return freeform_column


def create_assay_column(ld_client: LDClient, live_report: LiveReport, assay_name, assay_type_name):
    """
    Creates an assay column of a specified name and type name in a specific live report and LD client.

    :param ld_client: live design client where the assay column should be created
    :param live_report: live report where the assay column should be created
    :param assay_name: name to call the assay column
    :param assay_type_name: the type name of the assay column
    :return: assay column that was created
    """
    assay_column = ld_client.get_or_create_assay(assay_name=assay_name,
                                                 assay_type_name=assay_type_name,
                                                 column_type="ASSAY",
                                                 project_ids=["0"])
    add_columns_to_live_report(ld_client, live_report.id, [assay_column['addable_column_id']])
    return assay_column


def create_model_column(ld_client: LDClient, live_report: LiveReport):
    """
    Creates a model column in a specific live report and LD client.

    :param ld_client: live design client where the model column should be created
    :param live_report: live report where the assay column should be created
    :return: new model column that was created
    """
    # Create the protocol
    pre_command = ModelCommand(command='cp ${python file:FILE-INPUT} input.py', driver_id=1)
    command = ModelCommand(command='$SCHRODINGER/run input.py --input ${SDF-FILE} > '
                           '${temp filename:TEXT-INPUT}',
                           driver_id=1)
    post_command = ModelCommand(command='cat ${temp filename:TEXT-INPUT}', driver_id=1)
    protocol_def = Model(name='Protocol pytest',
                         commands=[pre_command, command, post_command],
                         description='run a python file that requires the schrodinger python library',
                         archived=False,
                         published=False,
                         folder="Computational Models/User Defined/demo",
                         user="demo",
                         project_ids=['4'],
                         template_vars=[],
                         returns=[],
                         batch_size=ModelRecursive(tag='DEFAULT', value=100),
                         command_type=ModelRecursive(tag='READ_ONLY', value='NORMAL'),
                         command_queue=ModelRecursive(tag='READ_ONLY', value='sync'))

    protocol = ld_client.create_protocol(protocol_def)

    # Define a model version
    attachment = ld_client.get_or_create_attachment('resources/pytest_model.py', 'ATTACHMENT', ['4'])
    template_vars = [
        ModelTemplateVar(name='temp filename', type='STRING', data='out.csv', tag='READ_ONLY'),
        ModelTemplateVar(name='python file', type='FILE', data=attachment['id'], tag='READ_ONLY')
    ]
    returns = [
        ModelReturn(key="Result",
                    type="STRING",
                    units="mol/L",
                    precision=1,
                    tag='DEFAULT',
                    display_name="Model pytest result")
    ]

    model_def = Model(name="Pytest Model",
                      description="A fake model for API pytests",
                      folder="Computational Models/User Defined/demo",
                      archived=False,
                      published=True,
                      user='demo',
                      returns=returns,
                      parent=protocol.id,
                      template_vars=template_vars,
                      project_ids=['4'],
                      batch_size=ModelRecursive(tag='DEFAULT', value=20),
                      command_type=ModelRecursive(tag='DEFAULT', value='NORMAL'),
                      command_queue=ModelRecursive(tag='DEFAULT', value='FAST'))

    new_model = ld_client.create_model(model_def)
    add_columns_to_live_report(ld_client, live_report.id, [new_model.returns[0].addable_column_id])
    return new_model


def add_columns(ld_client: LDClient, live_report: LiveReport, column_names=[]):
    """
    Creates columns with specified names in a specific live report and LD client.

    :param ld_client: live design client where the column(s) should be added
    :param live_report: live report where the column(s) should be added
    :param column_names: list of column names to be created
    :return: list of columns that were created
    """
    columns = []
    if not isinstance(column_names, list):
        raise LiveDesignAPIException("Parameter column_names in add_columns(...) expects a list")
    for column_name in column_names:
        columns.append(create_freeform_column(ld_client, live_report, column_name))
    return columns


def add_columns_to_live_report(ld_client: LDClient, live_report_id, column_ids):
    """
    Adds columns with specified column ids to a specific live report and LD client.

    :param ld_client: live design client where the column(s) should be added
    :param live_report_id: live report where the column(s) should be added
    :param column_ids: list of column ids whose columns should be added
    :return: list of columns in the live report
    """
    response = ld_client.add_columns(live_report_id, column_ids)

    def columns_added_to_live_report():
        live_report_data = ld_client.live_report_results_metadata(live_report_id)
        # added asserting for live_report_data, as live_report_results_metadata is returning empty string when LR is
        # not properly loaded, This check is to wait until LR loads properly.
        assert live_report_data
        actual_column_ids = set(live_report_data["columns"].keys())
        assert all(str(column_id) in actual_column_ids for column_id in column_ids)

    wait_until_condition_met(columns_added_to_live_report)
    return response


def remove_columns_from_live_report(ld_client: LDClient, live_report_id, column_ids):
    """
    Removes columns with specified column ids in specific a live report and LD client.

    :param ld_client: live design client where the column(s) should be removed
    :param live_report_id: live report where the column(s) should be removed
    :param column_ids: list of column ids whose columns should be removed
    :return: list of columns in the live report
    """
    response = ld_client.remove_columns(live_report_id, column_ids)

    def columns_removed_from_live_report():
        live_report_data = ld_client.live_report_results_metadata(live_report_id)
        actual_column_ids = set(live_report_data["columns"].keys())
        assert all(str(column_id) not in actual_column_ids for column_id in column_ids)

    wait_until_condition_met(columns_removed_from_live_report)
    return response


def add_freeform_values(ld_client: LDClient, observations):
    """
    Adds freeform values from specified observations in a specific LD client.

    :param ld_client: live design client where the freeform value should be added
    :param observations: list of observations to be added
    :return: list of observations
    """
    ld_client.add_freeform_column_values(observations)


def get_column_values(ld_client: LDClient, live_report: LiveReport, freeform_column: FreeformColumn, entity_ids):
    """
    Gets column values from a specified freeform column and entity id with a specific live report and LD client.

    :param ld_client: live design client to return column values
    :param live_report: live report to return column values
    :param freeform_column: freeform column to return values
    :param entity_ids: specific entity id to return column values
    :return: column values
    """
    return ld_client.get_observations_by_entity_ids_and_column_ids([freeform_column.id], entity_ids,
                                                                   live_report.project_id, str(live_report.id))


def replace_column_async(ld_client: LDClient, old_column_id, new_column_id, project_ids=['0']):
    """
    Replaces a specified column with another column in determined projects with a specific LD client.

    :param ld_client: live design client where columns are being replaced
    :param old_column_id: the existing column id that will be replaced
    :param new_column_id: the new column id which will replace the old column
    :param project_ids: a list of project ids in str where the column replacement occurs, defaulted to "Global"
    :return: does not return
    """
    ld_client.replace_column_async(old_column_id, new_column_id, project_ids)


def replace_column_groups(ld_client, live_report_id, list_of_column_groups, ungroup_mode=None):
    """
    Replaces a specified column with another column in determined projects with a specific LD client.

    :param ld_client: LDClient, LiveDesign client object
    :param live_report_id: str, ID of the Live Report for which to update column groups
    :param list_of_column_groups: list of ColumnGroups,  Ordered list of the new column groups for the Live Report
    :param ungroup_mode: str, ungroup mode, defaults to None, available: KEEP, REMOVE
    :return: does not return
    """
    ld_client.update_column_groups(live_report_id=live_report_id,
                                   column_groups=list_of_column_groups,
                                   ungroup_mode=ungroup_mode)


def get_column_groups_by_live_report_id(ld_client, live_report_id):
    """
    Fetches the list of all ColumnGroups for a particular LiveReport ID

    :param ld_client: LDClient, live design client object
    :param live_report_id: str, ID of the Live Report to fetch ColumnGroups
    :return: An ordered list of column groups in the specified LiveReport
    """
    return ld_client.get_column_groups_by_live_report_id(live_report_id=live_report_id)
