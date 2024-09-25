import pytest
from ldclient.models import FreeformColumn

from helpers.api.actions.freeform_column import create_freeform_column_using_ffc_object
from library import utils

test_type = 'api'


@pytest.fixture(scope='function')
def freeform_column_via_api(request, ld_api_client, new_live_report):
    """
    Fixture to create freeform columns

    Defaults may be overridden by adding module variables named

    'ffc_name', 'ffc_type', 'ffc_description', 'ffc_project_id',  'ffc_live_report_id', 'is_published',
    'is_picklist', 'ffc_values', 'ffc_value_type', 'is_multiple_values_allowed'.

    For Example:
        ffc_name = 'FFC name'
        ffc_type = 'type'
        ffc_description = 'description'
        ffc_project_id = '4'
        ffc_live_report_id = '1'
        is_published = True
        is_picklist = True
        ffc_values = ['va1']
        ffc_value_type = FreeformColumn.VALUE_STRING
        is_multiple_values_allowed = True
    :param request: request object with test metadata (from pytest fixture)
    :param ld_api_client: LDClient, fixture which returns ldclient object
    :param new_live_report: LiveReport, fixture which returns livereport
    :return: (FreeformColumn, FreeformColumn), Response from create_freeform_column method, Actual ffc object
    """
    ffc_name = getattr(request.module, 'ffc_name', utils.make_unique_name('test_ffc'))
    ffc_type = getattr(request.module, 'ffc_type', FreeformColumn.COLUMN_TEXT)
    ffc_description = getattr(request.module, 'ffc_description', 'Description value')
    ffc_project_id = getattr(request.module, 'ffc_project_id', '4')
    ffc_live_report_id = getattr(request.module, 'ffc_live_report_id', new_live_report.id)
    is_published = getattr(request.module, 'is_published', False)
    is_picklist = getattr(request.module, 'is_picklist', False)
    ffc_values = getattr(request.module, 'ffc_values', [])
    ffc_value_type = getattr(request.module, 'ffc_value_type', FreeformColumn.VALUE_STRING)
    is_multiple_values_allowed = getattr(request.module, 'is_multiple_values_allowed', False)

    ffc_object = FreeformColumn(name=ffc_name,
                                type=ffc_type,
                                description=ffc_description,
                                project_id=ffc_project_id,
                                live_report_id=ffc_live_report_id,
                                published=is_published,
                                picklist=is_picklist,
                                values=ffc_values,
                                value_type=ffc_value_type,
                                multiple_values_allowed=is_multiple_values_allowed)

    return create_freeform_column_using_ffc_object(ld_api_client, ffc_object), ffc_object
