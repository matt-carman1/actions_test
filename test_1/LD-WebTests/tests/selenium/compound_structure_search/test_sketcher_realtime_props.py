"""
To test Realtime Properties panel above Compound Sketcher in Add Compounds panel.
"""

import pytest

from helpers.change.actions_pane import open_add_compounds_panel, close_add_compounds_panel, open_add_data_panel
from helpers.change.columns_action import add_column_by_name
from helpers.change.sketcher import import_structure_into_sketcher, clear_structure_from_sketcher
from helpers.verification.element import verify_is_visible
from helpers.selection.add_compound_panel import REALTIME_EMPTY_MESSAGE, REALTIME_PROPERTY_
from library import dom


@pytest.mark.require_webgl
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_sketcher_realtime_props(selenium):
    """
    Adds a compound to sketcher in a LiveReport with few quick properties. Checks that correct values appear in the
    realtime pane above the sketcher. Checks that values change when a new compound is added to the sketcher.

    :param selenium: Selenium Webdriver
    """

    # compounds to be added to sketcher
    nabumetone_molv = '\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 17 18 0 0 1\nM  V30 BEGIN ATOM\nM  V30 1 C 5.692000 0.151143 0.000000 0\nM  V30 2 O 4.454286 -0.562286 0.000000 0\nM  V30 3 C 3.217714 0.153143 0.000000 0\nM  V30 4 C 3.218857 1.581714 0.000000 0\nM  V30 5 C 1.982286 2.296857 0.000000 0\nM  V30 6 C 0.744571 1.583714 0.000000 0\nM  V30 7 C -0.492000 2.298857 0.000000 0\nM  V30 8 C -1.729714 1.585714 0.000000 0\nM  V30 9 C -2.966286 2.300857 0.000000 0\nM  V30 10 C -4.204000 1.587429 0.000000 0\nM  V30 11 C -5.440571 2.302857 0.000000 0\nM  V30 12 C -6.678286 1.589429 0.000000 0\nM  V30 13 O -5.439429 3.731429 0.000000 0\nM  V30 14 C -1.730857 0.156857 0.000000 0\nM  V30 15 C -0.494286 -0.558286 0.000000 0\nM  V30 16 C 0.743429 0.154857 0.000000 0\nM  V30 17 C 1.980000 -0.560000 0.000000 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 2 1 2 3\nM  V30 3 2 3 4\nM  V30 4 1 4 5\nM  V30 5 2 5 6\nM  V30 6 1 6 7\nM  V30 7 2 7 8\nM  V30 8 1 8 9\nM  V30 9 1 9 10\nM  V30 10 1 10 11\nM  V30 11 1 11 12\nM  V30 12 2 11 13\nM  V30 13 1 8 14\nM  V30 14 2 14 15\nM  V30 15 1 15 16\nM  V30 16 1 6 16\nM  V30 17 2 16 17\nM  V30 18 1 3 17\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n$$$$'
    amlexanox_analog_molv = '\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 22 24 0 0 1\nM  V30 BEGIN ATOM\nM  V30 1 C -5.176857 1.212000 0.000000 0\nM  V30 2 C -3.939143 1.925429 0.000000 0\nM  V30 3 O -3.938000 3.354000 0.000000 0\nM  V30 4 C -2.702571 1.210286 0.000000 0\nM  V30 5 C -2.703714 -0.218286 0.000000 0\nM  V30 6 C -1.467143 -0.933714 0.000000 0\nM  V30 7 C -0.229429 -0.220286 0.000000 0\nM  V30 8 O 1.007143 -0.935714 0.000000 0\nM  V30 9 C 2.244857 -0.222286 0.000000 0\nM  V30 10 N 3.481429 -0.937714 0.000000 0\nM  V30 11 C 4.719143 -0.224286 0.000000 0\nM  V30 12 N 5.955714 -0.939714 0.000000 0\nM  V30 13 C 4.720286 1.204286 0.000000 0\nM  V30 14 C 3.483714 1.919429 0.000000 0\nM  V30 15 C 2.246000 1.206286 0.000000 0\nM  V30 16 C 1.009429 1.921429 0.000000 0\nM  V30 17 O 1.010571 3.350000 0.000000 0\nM  V30 18 C -0.228286 1.208286 0.000000 0\nM  V30 19 C -1.464857 1.923429 0.000000 0\nM  V30 20 C 5.958000 1.917429 0.000000 0\nM  V30 21 O 7.194571 1.202286 0.000000 0\nM  V30 22 O 5.959143 3.346000 0.000000 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 2 1 2 3\nM  V30 3 1 2 4\nM  V30 4 2 4 5\nM  V30 5 1 5 6\nM  V30 6 2 6 7\nM  V30 7 1 7 8\nM  V30 8 1 8 9\nM  V30 9 2 9 10\nM  V30 10 1 10 11\nM  V30 11 1 11 12\nM  V30 12 2 11 13\nM  V30 13 1 13 14\nM  V30 14 2 14 15\nM  V30 15 1 9 15\nM  V30 16 1 15 16\nM  V30 17 2 16 17\nM  V30 18 1 16 18\nM  V30 19 1 7 18\nM  V30 20 2 18 19\nM  V30 21 1 4 19\nM  V30 22 1 13 20\nM  V30 23 1 20 21\nM  V30 24 2 20 22\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n$$$$'
    # realtime property columns
    alogp_column_name = 'AlogP'
    hbd_column_name = 'HBD'
    psa_column_name = 'PSA'

    # Adding Realtime Property columns to the LiveReport
    open_add_data_panel(selenium)
    add_column_by_name(selenium, alogp_column_name)
    add_column_by_name(selenium, hbd_column_name)
    add_column_by_name(selenium, psa_column_name)

    # Opening the Compounds Panel and adding a compound to the sketcher
    open_add_compounds_panel(selenium)
    import_structure_into_sketcher(selenium, nabumetone_molv)

    # Verifying values in Realtime Properties pane
    verify_realtime_prop(selenium, alogp_column_name, '2.8')
    verify_realtime_prop(selenium, hbd_column_name, '0.0')
    verify_realtime_prop(selenium, psa_column_name, '26.3')

    # Now sketching a different compound and verifying values
    import_structure_into_sketcher(selenium, amlexanox_analog_molv)
    verify_realtime_prop(selenium, alogp_column_name, '1.7')
    verify_realtime_prop(selenium, hbd_column_name, '2.0')
    verify_realtime_prop(selenium, psa_column_name, '126.7')

    # Checking message in the realtime pane for empty sketcher
    clear_structure_from_sketcher(selenium)

    # (agupta) disabling this verification, it should be re-enabled after SS-36555.
    # verify_is_visible(selenium,
    #                   REALTIME_EMPTY_MESSAGE,
    #                   selector_text='To preview properties as you sketch, add some '
    #                   'Property columns to your Live Report.')
    close_add_compounds_panel(selenium)


def verify_realtime_prop(driver, name, expected_value):
    prop = dom.get_element(driver, REALTIME_PROPERTY_.format(name))
    verify_is_visible(prop, 'label', selector_text=name)
    verify_is_visible(prop, 'div', selector_text=expected_value, custom_timeout=30)
