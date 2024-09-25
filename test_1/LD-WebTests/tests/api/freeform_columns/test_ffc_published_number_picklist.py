import pytest

from ldclient.models import FreeformColumn
from helpers.api.actions.freeform_column import create_freeform_column_using_ffc_object
from helpers.api.verification.freeform_columns import verify_create_ffc_response
from library import utils

# LiveReport alias
lr_id = '883'


class TestCreateFFC:
    # ----- Test Data ----- #
    # Positive test data
    published_ffc_without_values = FreeformColumn(name=utils.make_unique_name('published_ffc_without_values'),
                                                  type=FreeformColumn.COLUMN_NUMBER,
                                                  description='Unpublished ffc',
                                                  project_id='0',
                                                  live_report_id=lr_id,
                                                  published=True,
                                                  picklist=True)
    published_ffc_with_values = FreeformColumn(name=utils.make_unique_name('published_ffc_with_values'),
                                               type=FreeformColumn.COLUMN_NUMBER,
                                               description='Unpublished ffc',
                                               project_id='0',
                                               live_report_id=lr_id,
                                               published=True,
                                               picklist=True,
                                               values=['2', '3'])
    published_ffc_multivalued = FreeformColumn(name=utils.make_unique_name('published_ffc_multivalued'),
                                               type=FreeformColumn.COLUMN_NUMBER,
                                               description='Unpublished ffc',
                                               project_id='0',
                                               live_report_id=lr_id,
                                               published=True,
                                               picklist=True,
                                               values=['1', '2', '3'],
                                               multiple_values_allowed=True,
                                               value_type=FreeformColumn.VALUE_STRING)
    published_ffc_multivalued_without_values = FreeformColumn(
        name=utils.make_unique_name('published_ffc_multivalued_without_values'),
        type=FreeformColumn.COLUMN_NUMBER,
        description='Unpublished ffc',
        project_id='0',
        live_report_id=lr_id,
        published=True,
        picklist=True,
        multiple_values_allowed=True,
        value_type=FreeformColumn.VALUE_STRING)
    ffc_with_invalid_project = FreeformColumn(name=utils.make_unique_name('ffc_with_invalid_project'),
                                              description='test',
                                              project_id='-1',
                                              live_report_id=lr_id,
                                              published=True)

    # Negative test data
    ffc_with_only_name_parameter = FreeformColumn(name=utils.make_unique_name("ffc_with_only_name_parameter"),
                                                  description='',
                                                  published=True)
    ffc_with_invalid_project_str = FreeformColumn(name=utils.make_unique_name('ffc_with_invalid_project_str'),
                                                  description='asaasd',
                                                  project_id='NA',
                                                  live_report_id=lr_id)
    ffc_with_invalid_lr = FreeformColumn(name=utils.make_unique_name('ffc_with_invalid_lr'),
                                         description='asaasd',
                                         live_report_id='-1')
    ffc_with_invalid_lr_str = FreeformColumn(name=utils.make_unique_name('ffc_with_invalid_lr_str'),
                                             description='asaasd',
                                             live_report_id='NA')
    ffc_not_picklist_and_values = FreeformColumn(utils.make_unique_name('ffc_not_picklist_and_values'),
                                                 type=FreeformColumn.COLUMN_NUMBER,
                                                 description='Unpublished ffc',
                                                 project_id='0',
                                                 live_report_id=lr_id,
                                                 published=True,
                                                 picklist=False,
                                                 values=['1', '2', '3'],
                                                 multiple_values_allowed=True,
                                                 value_type=FreeformColumn.VALUE_STRING)
    ffc_not_picklist_but_multivalued = FreeformColumn(utils.make_unique_name('ffc_not_picklist_but_multivalued'),
                                                      type=FreeformColumn.COLUMN_NUMBER,
                                                      description='Unpublished ffc',
                                                      project_id='4',
                                                      live_report_id=lr_id,
                                                      published=True,
                                                      picklist=False,
                                                      multiple_values_allowed=True,
                                                      value_type=FreeformColumn.VALUE_STRING)

    published_ffc_invalid = FreeformColumn(name=utils.make_unique_name('unpublished_ffc_invalid'),
                                           type=FreeformColumn.COLUMN_NUMBER,
                                           description='Published date ffc',
                                           project_id='4',
                                           live_report_id=lr_id,
                                           published=True,
                                           picklist=True,
                                           values=['test'])

    @pytest.mark.parametrize("ffc_object, status_code, error_message",
                             [(ffc_not_picklist_and_values, '400', "A non-picklist column cannot have picklist values"),
                              (ffc_with_only_name_parameter, '400', "Live Report ID 0 is invalid"),
                              (ffc_with_invalid_project_str, '400',
                               r'The input was valid JSON but there was a missing field or incorrect value: Cannot '
                               r'deserialize value of type `long` from String \"NA\": not a valid `long` value\n at ['
                               r'Source: (org.apache.cxf.transport.http.AbstractHTTPDestination$1);'),
                              (ffc_with_invalid_lr_str, '400',
                               r'The input was valid JSON but there was a missing field or incorrect value: Cannot '
                               r'deserialize value of type `long` from String \"NA\": not a valid `long` value\n at ['
                               r'Source: (org.apache.cxf.transport.http.AbstractHTTPDestination$1);'),
                              (ffc_with_invalid_lr, '400', "Live Report ID -1 is invalid"),
                              (ffc_not_picklist_but_multivalued, None, None),
                              (published_ffc_without_values, None, None), (published_ffc_with_values, None, None),
                              (published_ffc_multivalued, None, None),
                              (published_ffc_multivalued_without_values, None, None),
                              (ffc_with_invalid_project, None, None),
                              (published_ffc_invalid, '400', "Observation value test is not a number")])
    def test_ffc_published_number_picklist(self, ld_api_client, ffc_object, status_code, error_message):
        """
        Test for create number picklist FFC.

        :param ld_api_client: LDClient, ldclient
        :param ffc_object: FreeformColumn, freeform column object which has all details of ffc
        :param status_code: str, status code for cases which will not create ffc, None for cases which will crease ffc
        :param error_message: str, error message for case which doesn't create ffc, None for cases which will create ffc
        """
        created_ffc = create_freeform_column_using_ffc_object(ld_api_client, ffc_object)
        verify_create_ffc_response(ld_api_client, ffc_object, created_ffc, status_code, error_message)
