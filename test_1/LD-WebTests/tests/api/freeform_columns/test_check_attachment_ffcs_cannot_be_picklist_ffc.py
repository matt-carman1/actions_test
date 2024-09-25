from ldclient.models import FreeformColumn

from helpers.api.verification.freeform_columns import verify_create_ffc_response

test_type = 'api'

# Params for freeform_column_via_api fixture
ffc_type = FreeformColumn.COLUMN_ATTACHMENT
is_picklist = True


def test_check_attachment_ffcs_cannot_be_picklist_ffc(ld_api_client, freeform_column_via_api):
    """
    Test Attachment type ffc cannot have constrained values (picklist).

    :param ld_api_client: LDClient
    """
    actual_response, ffc_object = freeform_column_via_api
    # verify picklist ffc's cannot support attachment type
    verify_create_ffc_response(ld_api_client, ffc_object, actual_response, '400',
                               'Picklist columns cannot be Attachment-type')
