from ldclient.models import LiveReport

from helpers.api.verification.live_report import verify_visible_row_count, \
    verify_live_report_columns
from library.api.extended_ldclient.client import ExtendedLDClient
from library.api.extended_ldclient.requests import ReactionEnumerationRequest
from library.api.extended_ldclient.responses import ReactionEnumerationPreview, EnumerationResponse

BASE_NUMBER_OF_LIVE_REPORT_COLUMNS = 8


def get_products_from_reaction_enumeration_preview(ld_api_client: ExtendedLDClient,
                                                   enumeration_request: ReactionEnumerationRequest,
                                                   expected_products_count, *args, **kwargs):
    """
    Tests the endpoint used when generation Reaction enumeration preview in the UI

    For parameter descriptions, see test_reaction_enumeration

    :return: number of products
    """
    response: ReactionEnumerationPreview = ld_api_client.reaction_enumeration_preview(enumeration_request)
    assert len(response.products) == expected_products_count, response.products


def get_products_from_reaction_enumeration_submit(ld_api_client: ExtendedLDClient, new_live_report: LiveReport,
                                                  enumeration_request: ReactionEnumerationRequest,
                                                  expected_products_count, *args, **kwargs):
    """
    Tests the endpoints used when actually submitting a Reaction enumeration and importing the products into a
    LiveReport

    For parameter descriptions, see test_reaction_enumeration

    :return: number of products
    """
    enumeration_request.enumeration_data.live_report_id = new_live_report.id
    response: EnumerationResponse = ld_api_client.reaction_enumeration_sync(enumeration_request)
    assert response.live_report_id == new_live_report.id, f"Expected LiveReport ID {new_live_report.id} but got {response.live_report_id}"
    verify_visible_row_count(ldclient=ld_api_client,
                             lr_id=new_live_report.id,
                             expected_visible_row_count=expected_products_count,
                             should_execute_live_report=False)

    expected_column_count = BASE_NUMBER_OF_LIVE_REPORT_COLUMNS + 2 * len(
        enumeration_request.enumeration_data.reactants) + sum(
            len(column_list) for column_list in enumeration_request.enumeration_data.reactant_columns.values())
    verify_live_report_columns(ldclient=ld_api_client,
                               lr_id=new_live_report.id,
                               expected_column_count=expected_column_count)
