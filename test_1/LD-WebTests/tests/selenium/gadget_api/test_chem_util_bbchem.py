# coding: utf-8

import pytest

from helpers.change.actions_pane import open_tools_pane
from helpers.change.gadgets import open_gadget
from helpers.extraction import paths
from helpers.selection.gadgets import GADGET_DUMMY_ABOUT
from helpers.verification import svg
from library import iframe

LD_PROPERTIES = {
    "CUSTOM_TOOLS":
        """
    [
        {
            "categoryName": "Dummy Category",
            "gadgets": [
                {
                    "name": "Dummy About Gadget",
                    "location": "../../api/about"
                }
            ]
        }
    ]
"""
}


@pytest.mark.serial
@pytest.mark.usefixtures("customized_server_config")
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_convert_molfile_to_smiles(selenium):
    open_tools_pane(selenium)
    gadget_id = open_gadget(selenium, GADGET_DUMMY_ABOUT)

    # Get  mol string
    with open(paths.get_resource_path('benzene.mol'), 'r') as file:
        molfile = file.read()
    script = f"""
    var callback = arguments[arguments.length - 1];

    window.bb.util.chem.convert(`{molfile}`, window.bb.enums.MoleculeFormat.SDF, window.bb.enums.MoleculeFormat.SMILES)
    .then((representation) => callback(representation));
    """

    @iframe.within_iframe('#' + gadget_id)
    def execute_script(_driver, _script):
        result = _driver.execute_async_script(_script)
        assert len(result) > 0

    execute_script(selenium, script)


@pytest.mark.serial
@pytest.mark.usefixtures("customized_server_config")
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_convert_molfile_to_smarts(selenium):
    open_tools_pane(selenium)
    gadget_id = open_gadget(selenium, GADGET_DUMMY_ABOUT)

    # Get  mol string
    with open(paths.get_resource_path('benzene.mol'), 'r') as file:
        molfile = file.read()
    script = f"""
    var callback = arguments[arguments.length - 1];

    window.bb.util.chem.convert(`{molfile}`, window.bb.enums.MoleculeFormat.SDF, window.bb.enums.MoleculeFormat.SMARTS)
    .then((representation) => callback(representation));
    """

    @iframe.within_iframe('#' + gadget_id)
    def execute_script(_driver, _script):
        result = _driver.execute_async_script(_script)
        assert len(result) > 0

    execute_script(selenium, script)


@pytest.mark.app_defect(reason="SS-38472")
@pytest.mark.serial
@pytest.mark.usefixtures("customized_server_config")
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_convert_smiles_to_molfile(selenium):
    open_tools_pane(selenium)
    gadget_id = open_gadget(selenium, GADGET_DUMMY_ABOUT)

    # Get  mol string
    with open(paths.get_resource_path('benzene_rdkit.sdf'), 'r') as file:
        molfile = file.read()
    script = """
    var callback = arguments[arguments.length - 1];

    window.bb.util.chem.convert('C1=CC=CC=C1', window.bb.enums.MoleculeFormat.SMILES, window.bb.enums.MoleculeFormat.SDF)
    .then((representation) => callback(representation));
    """

    @iframe.within_iframe('#' + gadget_id)
    def execute_script(_driver, _script):
        result = _driver.execute_async_script(_script)
        # NOTE(novak): skipping first two lines of molefiles to avoid the (variable) timestamp in the second line
        assert len(result) > 0

    execute_script(selenium, script)


@pytest.mark.serial
@pytest.mark.usefixtures("customized_server_config")
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_render_svg_image_from_smiles(selenium):
    open_tools_pane(selenium)
    gadget_id = open_gadget(selenium, GADGET_DUMMY_ABOUT)

    script = """
    var callback = arguments[arguments.length - 1];

    window.bb.util.chem.generateImage('C1=CC=CC=C1', window.bb.enums.MoleculeFormat.SMILES, window.bb.enums.ImageFormat.SVG)
    .then((representation) => callback(representation));
    """

    @iframe.within_iframe('#' + gadget_id)
    def execute_script(_driver, _script):
        result = _driver.execute_async_script(_script)
        svg.verify_valid_svg(result)

    execute_script(selenium, script)
