import pytest

from ldclient.models import FreeformColumn
from helpers.api.actions.freeform_column import create_freeform_column_using_ffc_object
from helpers.api.verification.freeform_columns import verify_create_ffc_response
from library import utils

# LiveReport alias
lr_id = '883'


class TestCreateDateFFC:
    # Positive test data
    # Published date type picklist ffc.
    published_ffc_picklist = FreeformColumn(name=utils.make_unique_name('unique_date_ffc'),
                                            type=FreeformColumn.COLUMN_DATE,
                                            description='Published date ffc',
                                            project_id='4',
                                            live_report_id=lr_id,
                                            published=True,
                                            picklist=True,
                                            values=['2021-03-12', '2021-03-10'])

    # Published date type picklist ffc with multiple values
    published_ffc_multivalues = FreeformColumn(name=utils.make_unique_name('unique_date_multivalues_ffc'),
                                               type=FreeformColumn.COLUMN_DATE,
                                               description='Published date ffc',
                                               project_id='4',
                                               live_report_id=lr_id,
                                               published=True,
                                               picklist=True,
                                               values=['2021-03-12', '2021-03-10'],
                                               multiple_values_allowed=True,
                                               value_type=FreeformColumn.VALUE_STRING)

    # Unpublished date type picklist ffc
    unpublished_ffc_picklist = FreeformColumn(name=utils.make_unique_name('unpublished_ffc_picklist'),
                                              type=FreeformColumn.COLUMN_DATE,
                                              description='Unpublished date ffc',
                                              project_id='4',
                                              live_report_id=lr_id,
                                              published=False,
                                              picklist=True,
                                              values=['2021-03-12', '2021-03-10'])

    # Unpublished date type picklist with multiple values
    unpublished_ffc_multivalues = FreeformColumn(name=utils.make_unique_name('unpublished_ffc_multivalues'),
                                                 type=FreeformColumn.COLUMN_DATE,
                                                 description='Unpublished date ffc',
                                                 project_id='4',
                                                 live_report_id=lr_id,
                                                 published=False,
                                                 picklist=True,
                                                 values=['2021-03-12', '2021-03-10'],
                                                 multiple_values_allowed=True,
                                                 value_type=FreeformColumn.VALUE_STRING)

    # Negative validation
    # Invalid published date type ffc
    published_ffc_invalid = FreeformColumn(name=utils.make_unique_name('published_ffc_invalid'),
                                           type=FreeformColumn.COLUMN_DATE,
                                           description='Published date ffc',
                                           project_id='4',
                                           live_report_id=lr_id,
                                           published=True,
                                           picklist=True,
                                           values=['10'])

    # Invalid unpublished date type ffc
    unpublished_ffc_invalid = FreeformColumn(name=utils.make_unique_name('unpublished_ffc_invalid'),
                                             type=FreeformColumn.COLUMN_DATE,
                                             description='Unpublished date ffc',
                                             project_id='4',
                                             live_report_id=lr_id,
                                             published=False,
                                             picklist=True,
                                             values=['12-03-2021'])

    @pytest.mark.parametrize("ffc_object, status_code, error_message", [
        (published_ffc_picklist, None, None), (published_ffc_multivalues, None, None),
        (unpublished_ffc_picklist, None, None), (unpublished_ffc_multivalues, None, None),
        pytest.param(published_ffc_invalid, '400', "Invalid value", marks=pytest.mark.app_defect(reason='SS-33532')),
        pytest.param(unpublished_ffc_invalid, '400', "Invalid value", marks=pytest.mark.app_defect(reason='SS-33532'))
    ])
    def test_picklist_date_ffc(self, ld_api_client, ffc_object, status_code, error_message):
        """
        Test for create date picklist FFC. (both published and unpublished)

        a. Create date published picklist ffc.
        b. Create date published picklist ffc with multiple values.
        c. Create date unpublished picklist ffc.
        d. Create date unpublished picklist ffc with multiple values.
        e. Create invalid published date type ffc.
        f. Create invalid unpublished date type ffc.

        :param ld_api_client: LDClient, ldclient
        :param ffc_object: FreeformColumn, freeform column object which has all details of ffc
        :param status_code: str, status code for cases which will not create ffc, None for cases which will crease ffc
        :param error_message: str, error message for case which doesn't create ffc, None for cases which will create ffc
        """
        created_ffc = create_freeform_column_using_ffc_object(ld_api_client, ffc_object)
        verify_create_ffc_response(ld_api_client, ffc_object, created_ffc, status_code, error_message)
