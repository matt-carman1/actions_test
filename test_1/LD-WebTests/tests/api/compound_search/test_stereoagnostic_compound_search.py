from helpers.api.actions.livereport import load_sdf_in_lr
from helpers.api.actions.compound import compound_search
from helpers.extraction import paths

test_type = 'api'


def test_stereoagnostic_compound_search(ld_api_client, new_live_report):
    """
    Test exact compound search w/ and w/o ignoring stereo information.
    1. Create a new livereport.
    2. Register reals and virtuals that are stereo-isomers of each other.
    3. Verify that the registration is as expected.
    4. Run a search ignoring stereo-specificity - Verify all compounds show up.
    5. Run a search respecting stereo-specificity - Verify only required compound show up.

    :param ld_api_client: Fixture that returns ldclient object for "demo:demo"
    """
    # Input data required throughout the test
    data_path = paths.get_resource_path("api/")
    molecule = 'CN[C@H]1CCNC[C@H]1OC'

    # Finding ID of the new livereport
    lr_id = new_live_report.id

    # Registering a file with real compounds
    compounds_real = load_sdf_in_lr(ld_api_client,
                                    lr_id,
                                    file_path='{0}/stereo_reals.sdf'.format(data_path),
                                    compound_source="non_pri")
    # Verification that all four compounds with reals are imported
    assert len(compounds_real) == 4, \
        "There was an error while importing reals. Expected {} but got {}".format(4, len(compounds_real))

    # Registering a file with virtual compounds
    compounds_virtual = load_sdf_in_lr(ld_api_client,
                                       lr_id,
                                       file_path='{0}/stereo_virtuals.sdf'.format(data_path),
                                       compound_source="pri")

    # Verification that both compounds are imported
    assert len(compounds_virtual) == 2, \
        "There was an error while importing virtuals. Expected {} but got {}".format(2, len(compounds_virtual))

    # Storing virtual ids from their respective corp_ids
    virtual_ids = [compound['corporate_id'] for compound in compounds_virtual]

    # Search molecule ignoring its stereo information- negative validation.
    matching_ids_stereo_false = compound_search(ld_api_client,
                                                mol_smiles=molecule,
                                                search_type='EXACT',
                                                ignore_stereospecific=True)
    expected_id_list = ['SCHRO55827', virtual_ids[0], virtual_ids[1], 'SCHRO55825', 'SCHRO55826', 'SCHRO55824']

    # Verification that all ids in the list show up as expected
    assert set(expected_id_list) == set(matching_ids_stereo_false), \
        "There was an error while performing the search . Expected {} but got {}".format(expected_id_list,
                                                                                         matching_ids_stereo_false)

    # Search molecule considering its stereo information- positive validation
    matching_ids_stereo_true = compound_search(ld_api_client,
                                               mol_smiles=molecule,
                                               search_type='EXACT',
                                               ignore_stereospecific=False)

    # Verification that only the required id in the list show up.
    assert [virtual_ids[1]] == matching_ids_stereo_true, \
        "There was an error while performing the search. Expected {} but got {}".format(virtual_ids[1],
                                                                                        matching_ids_stereo_true)
