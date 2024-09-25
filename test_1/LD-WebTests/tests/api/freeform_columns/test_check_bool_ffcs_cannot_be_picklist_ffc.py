from ldclient.models import FreeformColumn
from helpers.api.verification.freeform_columns import verify_create_ffc_response

test_type = 'api'

# Params for freeform_column_via_api fixture
ffc_type = FreeformColumn.COLUMN_BOOLEAN
is_picklist = True


def test_check_bool_ffcs_cannot_be_picklist_ffc(ld_api_client, freeform_column_via_api):
    """
    Test Boolean type ffc cannot have constrained values (picklist).

    :param ld_api_client: LDClient
    """
    # verify picklist ffc's cannot support boolean type
    actual_respone, ffc_object = freeform_column_via_api
    verify_create_ffc_response(ld_api_client, ffc_object, actual_respone, '400',
                               'Picklist columns cannot be Boolean-type')
