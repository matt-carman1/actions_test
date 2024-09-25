from helpers.api.verification.live_report import verify_live_report_columns
from helpers.extraction import paths
from ldclient.models import FreeformColumn
from helpers.api.actions.row import create_observation
from helpers.api.actions.column import add_freeform_values
from helpers.api.extraction.grid import get_cell_values_for_rows_and_columns
from library.api.wait import wait_until_condition_met
import pytest

live_report_to_duplicate = {'livereport_name': 'FFC - All types, published and unpublished', 'livereport_id': '1299'}
test_type = 'api'


@pytest.mark.app_defect(reason="SS-43352: flaky on Jenkins due to ordering of date fields")
def test_add_freeform_column_values(ld_api_client, duplicate_live_report):
    """
    Test to add values into cells of different type of FFC and verifying them.

    :param ld_api_client: ldclient, LDClient object
    :param duplicate_live_report: livereport, Duplicate an existing LiveReport
    """
    lr_id = duplicate_live_report.id
    # Following lines were added to get the addable column id for the unpublished columns on the duplicate LR
    lr_column_desc = ld_api_client.column_descriptors(live_report_id=lr_id)
    livereport_column_details = {}
    for col_desc in lr_column_desc:
        livereport_column_details[col_desc.display_name] = col_desc.addable_column_id

    # Unpublished AnyValue Text FFC
    text_type_ffc_name = 'Text - unpublished'
    text_type_ffc_id = livereport_column_details[text_type_ffc_name]
    observation_text_type_ffc = create_ffc_observation(lr_id=lr_id,
                                                       column_id=text_type_ffc_id,
                                                       ffc_value='Freeform value #01')

    # Unpublished Picklist Number FFC
    number_type_ffc_name = 'Number  - unpublished'
    number_type_ffc_id = livereport_column_details[number_type_ffc_name]
    picklist_number_type_ffc = FreeformColumn(id=number_type_ffc_id,
                                              name='Number  - unpublished',
                                              description='Modified by API',
                                              type='NUMBER',
                                              live_report_id=lr_id,
                                              project_id='4',
                                              picklist=True,
                                              values=['1', '-0.5', '2.4'])
    ld_api_client.update_freeform_column(freeform_column_id=number_type_ffc_id,
                                         freeform_column=picklist_number_type_ffc)
    observation_number_type_ffc = create_ffc_observation(lr_id=lr_id, column_id=number_type_ffc_id, ffc_value='-0.5')

    # Unpublished Boolean FFC
    bool_type_ffc_name = 'Boolean  - unpublished'
    bool_type_ffc_id = livereport_column_details[bool_type_ffc_name]
    observation_bool_type_ffc = create_ffc_observation(lr_id=lr_id, column_id=bool_type_ffc_id, ffc_value='true')

    # Unpublished Multi-select picklist FFC
    date_type_ffc_name = 'Date  - unpublished'
    date_type_ffc_id = livereport_column_details[date_type_ffc_name]
    picklist_date_type_ffc = FreeformColumn(id=date_type_ffc_id,
                                            name='Date  - unpublished',
                                            description='Modified by API',
                                            type='DATE',
                                            live_report_id=lr_id,
                                            project_id='4',
                                            picklist=True,
                                            values=['2021-01-02', '2021-03-04', '2021-05-06'],
                                            multiple_values_allowed=True)
    ld_api_client.update_freeform_column(freeform_column_id=date_type_ffc_id, freeform_column=picklist_date_type_ffc)
    observation_first_date_type_ffc = create_ffc_observation(lr_id=lr_id,
                                                             column_id=date_type_ffc_id,
                                                             ffc_value='2021-01-02')
    observation_second_date_type_ffc = create_ffc_observation(lr_id=lr_id,
                                                              column_id=date_type_ffc_id,
                                                              ffc_value='2021-05-06')

    # Unpublished File/Image FFC
    file_type_ffc_name = 'File - unpublished'
    file_type_ffc_id = livereport_column_details[file_type_ffc_name]
    data_path = paths.get_resource_path("api/")
    attachment = ld_api_client.get_or_create_attachment('{0}/snowman.jpg'.format(data_path), 'IMAGE', ['4'])
    observation_file_type_ffc = create_ffc_observation(lr_id=lr_id,
                                                       column_id=file_type_ffc_id,
                                                       ffc_value=attachment['id'])

    expected_cell_values = ['Freeform value #01', '-0.5', 'true', ['2021-01-02', '2021-05-06'], attachment['id']]

    add_freeform_values(ld_api_client,
                        observations=[
                            observation_text_type_ffc, observation_number_type_ffc, observation_bool_type_ffc,
                            observation_first_date_type_ffc, observation_second_date_type_ffc, observation_file_type_ffc
                        ])

    def verify_values():
        actual_cell_values = get_cell_values_for_rows_and_columns(
            ld_api_client,
            livereport_id=duplicate_live_report.id,
            column_ids=[text_type_ffc_id, number_type_ffc_id, bool_type_ffc_id, date_type_ffc_id, file_type_ffc_id],
            row_ids=['CRA-031137'])
        assert actual_cell_values['CRA-031137'] == expected_cell_values, \
            'Expected cell values {} but got {}'.format(expected_cell_values, actual_cell_values['CRA-031137'])

    wait_until_condition_met(verify_values, retries=3)


def create_ffc_observation(lr_id, column_id, ffc_value):
    """
    Function to create observations for FFC cells specific to this test.

    :param lr_id: str, LiveReport ID
    :param column_id: str, Addable column ID
    :param ffc_value: str, FFC value to add into the cell
    :return: Observation, Observation object
    """
    return create_observation(project_id='4',
                              entity_id='CRA-031137',
                              live_report_id=lr_id,
                              addable_column_id=column_id,
                              value=ffc_value)
