import pytest
from ldclient.models import LiveReport

from helpers.api.verification.live_report import verify_visible_row_count
from library.api.extended_ldclient.enums import OrderType
from library.api.extended_ldclient.requests import RGroupEnumerationData, RGroupEnumerationRequest, RGroup
from library.api.extended_ldclient.responses import EnumerationResponse
from library.api.extended_ldclient.client import ExtendedLDClient
from resources.structures.structures_test_rgroup_max_enumeration_results_ff import RGROUP_CXSMILES, SCAFFOLD_MOL

test_type = 'api'

LD_PROPERTIES = {'MAX_ENUMERATION_RESULTS': 3}


@pytest.mark.usefixtures('customized_server_config')
@pytest.mark.parametrize('expected_products_count,max_compounds', [(3, 3), (3, 4), (2, 2)])
def test_rgroup_max_enumeration_results_ff(ld_api_client: ExtendedLDClient, new_live_report, expected_products_count,
                                           max_compounds):
    """
    Test to verify the MAX_ENUMERATION_RESULTS feature flag for R-Group enumeration

    :param ld_api_client: Extended ldclient
    :param new_live_report: fixture to create new live report
    :param expected_products_count: int, total expected number of products after enumeration
    :param max_compounds: int, total number of enumeration results user can request from enumeration UI
    """
    # R group  input structures
    r_groups = {
        1: [
            RGroup(structure=RGROUP_CXSMILES[0]),
            RGroup(structure=RGROUP_CXSMILES[1]),
            RGroup(structure=RGROUP_CXSMILES[2]),
            RGroup(structure=RGROUP_CXSMILES[3])
        ]
    }

    enumeration_data = RGroupEnumerationData(live_report_id=new_live_report.id,
                                             r_groups=r_groups,
                                             max_compounds=max_compounds,
                                             result_order=OrderType.SEQUENTIAL)
    request = RGroupEnumerationRequest(scaffold_representation=SCAFFOLD_MOL, enumeration_data=enumeration_data)
    response = ld_api_client.rgroup_enumeration_sync(request)
    assert response.live_report_id == new_live_report.id
    verify_visible_row_count(ldclient=ld_api_client,
                             lr_id=new_live_report.id,
                             expected_visible_row_count=expected_products_count,
                             should_execute_live_report=False)
