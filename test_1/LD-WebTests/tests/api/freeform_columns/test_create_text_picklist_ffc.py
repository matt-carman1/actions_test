import pytest
from ldclient.models import FreeformColumn, FreeformColumnPicklistValue

from helpers.api.actions.freeform_column import create_freeform_column_using_ffc_object
from helpers.api.verification.freeform_columns import verify_create_ffc_response
from library import utils

# LiveReport ID
lr_id = '883'

# Published text type picklist FFC
published_ffc_picklist = FreeformColumn(
    name=utils.make_unique_name('published_text_picklist_ffc'),
    type=FreeformColumn.COLUMN_TEXT,
    description='Published Text Picklist FFC',
    project_id='4',
    live_report_id=lr_id,
    published=True,
    picklist=True,
    values=[FreeformColumnPicklistValue(value='text1'),
            FreeformColumnPicklistValue(value='text2')])

# Published text type picklist FFC with multiple values
published_ffc_multivalues = FreeformColumn(
    name=utils.make_unique_name('published_text_multivalues_picklist_ffc'),
    type=FreeformColumn.COLUMN_TEXT,
    description='Published Text Multivalues Picklist FFC',
    project_id='4',
    live_report_id=lr_id,
    published=True,
    picklist=True,
    values=[FreeformColumnPicklistValue(value='text1'),
            FreeformColumnPicklistValue(value='text2')],
    multiple_values_allowed=True)

# Unpublished text type picklist FFC
unpublished_ffc_picklist = FreeformColumn(
    name=utils.make_unique_name('unpublished_text_picklist_ffc'),
    type=FreeformColumn.COLUMN_TEXT,
    description='Unpublished Text Picklist FFC',
    project_id='4',
    live_report_id=lr_id,
    published=False,
    picklist=True,
    values=[FreeformColumnPicklistValue(value='1'),
            FreeformColumnPicklistValue(value='2')])

# Unpublished text type picklist FFC with multiple values
unpublished_ffc_multivalues = FreeformColumn(
    name=utils.make_unique_name('unpublished_text_multivalues_picklist_ffc'),
    type=FreeformColumn.COLUMN_TEXT,
    description='Unpublished Text Multivalues Picklist FFC',
    project_id='4',
    live_report_id=lr_id,
    published=False,
    picklist=True,
    values=[FreeformColumnPicklistValue(value='12-12-2012'),
            FreeformColumnPicklistValue(value='12-12-2013')],
    multiple_values_allowed=True)


@pytest.mark.parametrize('ffc_object, status_code, error_message', [(published_ffc_picklist, None, None),
                                                                    (published_ffc_multivalues, None, None),
                                                                    (unpublished_ffc_picklist, None, None),
                                                                    (unpublished_ffc_multivalues, None, None)])
def test_picklist_text_ffc(ld_api_client, ffc_object, status_code, error_message):
    """
    Test to create text type picklist FFC w/ and w/o multiple values and verify the response

    1. Create published text type picklist FFC w/ multiple text values
    2. Create published text type picklist FFC w/o multiple text values
    3. Create unpublished text type picklist FFC w/ multiple text values
    4. Create unpublished text type picklist FFC w/o multiple text values

    :param ld_api_client: Fixture to create ld_api_client object
    :param ffc_object: FreeformColumn, FFC object with different FFC properties
    :param status_code: str, None for successful FFC creation; Status code for unsuccessful FFC creation
    :param error_message: str, None for successful FFC creation; Error message for unsuccessful FFC creation
    :return:
    """
    ffc_create_response = create_freeform_column_using_ffc_object(ld_api_client, ffc_object)
    verify_create_ffc_response(ld_api_client, ffc_object, ffc_create_response, status_code, error_message)
