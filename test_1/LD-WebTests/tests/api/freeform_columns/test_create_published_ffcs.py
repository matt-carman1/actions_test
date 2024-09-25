import pytest
from library import utils

from ldclient.models import FreeformColumn

from helpers.api.actions.freeform_column import create_freeform_column_using_ffc_object
from helpers.api.verification.freeform_columns import verify_create_ffc_response

# Variables
project_id = '4'
lr_id = '883'

# Published Text Type FFC Object
text_ffc_object = FreeformColumn(name=utils.make_unique_name('published_text_ffc'),
                                 description='Published Text FFC - API Test',
                                 type=FreeformColumn.COLUMN_TEXT,
                                 published=True,
                                 project_id=project_id,
                                 live_report_id=lr_id)

# Published Number Type FFC Object
num_ffc_object = FreeformColumn(name=utils.make_unique_name('published_number_ffc'),
                                description='Published Number FFC - API Test',
                                type=FreeformColumn.COLUMN_NUMBER,
                                published=True,
                                project_id=project_id,
                                live_report_id=lr_id)

# Published Date Type FFC Object
date_ffc_object = FreeformColumn(name=utils.make_unique_name('published_date_ffc'),
                                 description='Published Date FFC - API Test',
                                 type=FreeformColumn.COLUMN_DATE,
                                 published=True,
                                 project_id=project_id,
                                 live_report_id=lr_id)

# Published Boolean Type FFC Object
boolean_ffc_object = FreeformColumn(name=utils.make_unique_name('published_boolean_ffc'),
                                    description='Published Boolean FFC - API Test',
                                    type=FreeformColumn.COLUMN_BOOLEAN,
                                    published=True,
                                    project_id=project_id,
                                    live_report_id=lr_id)

# Published Attachment Type FFC Object
attachment_ffc_object = FreeformColumn(name=utils.make_unique_name('published_attachment_ffc'),
                                       description='Published Attachment FFC - API Test',
                                       type=FreeformColumn.COLUMN_ATTACHMENT,
                                       published=True,
                                       project_id=project_id,
                                       live_report_id=lr_id)


@pytest.mark.smoke
@pytest.mark.parametrize("ffc_object",
                         [text_ffc_object, num_ffc_object, date_ffc_object, boolean_ffc_object, attachment_ffc_object])
def test_create_published_ffcs(ld_api_client, ffc_object):
    """
    Test for create published FFCs with all possible data types (positive scenarios).

    :param ld_api_client: Fixture which creates API Client
    :param ffc_object: FFC model object
    """
    created_ffc = create_freeform_column_using_ffc_object(ld_api_client, ffc_object)
    verify_create_ffc_response(ld_api_client, ffc_object, created_ffc)
