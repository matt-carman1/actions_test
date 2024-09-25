import pytest

from ldclient.models import LiveReport

from helpers.api.verification.live_report import verify_visible_row_count
from library.api.extended_ldclient.client import ExtendedLDClient
from library.api.extended_ldclient.enums import OrderType
from library.api.extended_ldclient.requests import RGroupEnumerationRequest, RGroupEnumerationData, \
    RGroup
from library.api.extended_ldclient.responses import EnumerationResponse, RGroupEnumerationPreview
from library.utils import is_k8s

test_type = 'api'
SCAFFOLD_MOL = '\n  Mrv1908 08032121502D          \n\n  0  0  0     0  0            999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 7 7 0 0 0\nM  V30 BEGIN ATOM\nM  V30 1 C -1.8959 1.9984 0 0\nM  V30 2 C -3.2295 1.2284 0 0\nM  V30 3 C -3.2295 -0.3118 0 0\nM  V30 4 C -1.8959 -1.0818 0 0\nM  V30 5 C -0.5622 -0.3118 0 0\nM  V30 6 C -0.5622 1.2284 0 0\nM  V30 7 R# -1.896 3.5384 0 0 RGROUPS=(1 1)\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 2 1 2\nM  V30 2 1 2 3\nM  V30 3 2 3 4\nM  V30 4 1 4 5\nM  V30 5 2 5 6\nM  V30 6 1 6 1\nM  V30 7 1 1 7\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n'
RGROUP_CXSMILES = '*C1CCCC1 |$_AP1;;;;;$|'
EXPECTED_PRODUCTS = ['c1ccc(C2CCCC2)cc1']


@pytest.mark.xfail(not is_k8s(), reason="SS-40265: RMQ issues in Old Jenkins")
def test_rgroup_enumeration_preview(ld_api_client: ExtendedLDClient):
    """
    Tests the endpoint used when generating an R-Group enumeration preview in the UI
    :param ld_api_client: ldclient
    """
    enumeration_data = RGroupEnumerationData(live_report_id=None,
                                             r_groups={1: [RGroup(structure=RGROUP_CXSMILES)]},
                                             max_compounds=10,
                                             result_order=OrderType.SEQUENTIAL)
    request = RGroupEnumerationRequest(scaffold_representation=SCAFFOLD_MOL, enumeration_data=enumeration_data)
    response: RGroupEnumerationPreview = ld_api_client.rgroup_enumeration_preview(request)
    assert response == RGroupEnumerationPreview(products=EXPECTED_PRODUCTS)


@pytest.mark.xfail(not is_k8s(), reason="SS-40265: RMQ issues in Old Jenkins")
def test_rgroup_enumeration(ld_api_client: ExtendedLDClient, new_live_report: LiveReport):
    """
    Tests the endpoints used when actually running an R-Group enumeration & registering the results into a LiveReport
    :param ld_api_client: ldclient
    :param new_live_report: the new LiveReport created for this test
    """
    enumeration_data = RGroupEnumerationData(live_report_id=new_live_report.id,
                                             r_groups={1: [RGroup(structure=RGROUP_CXSMILES)]},
                                             max_compounds=10,
                                             result_order=OrderType.SEQUENTIAL)
    request = RGroupEnumerationRequest(scaffold_representation=SCAFFOLD_MOL, enumeration_data=enumeration_data)
    response: EnumerationResponse = ld_api_client.rgroup_enumeration_sync(request)
    assert response.live_report_id == new_live_report.id
    verify_visible_row_count(ldclient=ld_api_client,
                             lr_id=new_live_report.id,
                             expected_visible_row_count=len(EXPECTED_PRODUCTS),
                             should_execute_live_report=False)
