import defusedxml.ElementTree as ET


def verify_valid_svg(xml):
    """
    Verifies that xml string is valid xml and contains svg tag
    :param xml: string to test
    """
    assert len(xml) != 0
    tree = ET.fromstring(xml)
    assert tree.tag == '{http://www.w3.org/2000/svg}svg'
