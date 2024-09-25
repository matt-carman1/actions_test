from io import BytesIO

import pytest
from PIL import Image
from ldclient.enums import CompoundFormat
from requests import HTTPError

from helpers.api.verification.general import verify_error_response


def test_get_compound_image(ld_api_client):
    """
    Test for getting compound image using entity id.
    1. Get image, verify format and default image size
    2. Get image with specific height, width and verify the result image height and width.
    3. Get compound image with invalid entity_id
    4. Get Compound image for entity id which is present in DB and not in LR

    :param ld_api_client: LDClient, a fixture that returns LDClient object
    """
    # ----- Get image, verify format and default image size ----- #
    compound = ld_api_client.get_compound(entity_id='CRA-032662', format=CompoundFormat.PNG, live_report_id='2699')
    # verify default image size
    img = Image.open(BytesIO(compound))
    assert (200, 100) == img.size, "Default size for image is:{}, But got:{}".format((200, 100), img.size)
    # verify the image format
    assert 'PNG' == img.format, "Expected image size is:{}, but got:{}".format('PNG', img.format)

    # ----- Get image with specific height, width and verify the result image height and width. ----- #
    # Get compound image
    compound = ld_api_client.get_compound(entity_id='CRA-032662',
                                          format=CompoundFormat.PNG,
                                          height=900,
                                          width=1200,
                                          live_report_id='2699',
                                          bgcolor="FFFF00")

    # verify image size
    actual_img = Image.open(BytesIO(compound))
    assert (1200, 900) == actual_img.size, "Image size not matched, Expected size is: {}, Actual Size is:{}".format(
        (1200, 900), actual_img.size)

    # ----- Get Compound image with invalid entity_id ----- #
    with pytest.raises(HTTPError) as error_response:
        ld_api_client.get_compound(entity_id='Invalid', format=CompoundFormat.PNG)
    verify_error_response(error_response.value,
                          expected_status_code='400',
                          expected_error_message='Unable to retrieve entity id for specified id Invalid')

    # ----- Get Compound image for entity id which is present in DB and not in LR ----- #
    compound = ld_api_client.get_compound(entity_id='V055824', format=CompoundFormat.PNG, live_report_id='2699')
    # verify image size
    img = Image.open(BytesIO(compound))
    assert (200, 100) == img.size, "Default size for image is:{}, But got:{}".format((200, 100), img.size)
