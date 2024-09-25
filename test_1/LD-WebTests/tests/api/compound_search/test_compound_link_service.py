from helpers.api.actions.livereport import load_sdf_in_lr
from helpers.api.actions.compound import search_compound_links, unlink_compounds, link_compounds, \
    delete_all_compound_links_for_compound
from helpers.extraction import paths

test_type = 'api'


def test_compound_link_service(ld_api_client, new_live_report):
    """
    Test compound link service APIs:
    1. Compounds linking.
    2. Search for compounds link.
    3. Search for compounds unlinking.

    :param ld_api_client: Fixture that returns ldclient object for "demo:demo"
    :param new_live_report: Fixture that creates a new livereport.
    """
    data_path = paths.get_resource_path("api/")
    lr_id = new_live_report.id

    # Registering a file with 1 real compound
    compounds_real = load_sdf_in_lr(ld_api_client,
                                    lr_id,
                                    file_path='{0}/stereo_real_linking.sdf'.format(data_path),
                                    compound_source="non_pri")
    # Verification that the real compound is imported
    assert len(compounds_real) == 1, "There was an error while importing reals. " \
                                     "Expected {} real compound but got {} compounds in return".format(1,
                                                                                                       len(compounds_real))

    real_id = compounds_real[0]['corporate_id']

    # Registering a file with 1 virtual compound
    compounds_virtual = load_sdf_in_lr(ld_api_client,
                                       lr_id,
                                       file_path='{0}/stereo_virtual_linking.sdf'.format(data_path),
                                       compound_source="pri")

    # Verification that the virtual compound is imported
    assert len(compounds_virtual) == 1, "There was an error while importing virtuals. " \
                                        "Expected {} virtual compound but got {} compounds in return".format(1,
                                                                                                             len(compounds_virtual))
    virtual_id = compounds_virtual[0]['corporate_id']

    # Create compound link
    link_obsv = link_compounds(ld_api_client, real_entity_id=real_id, virtual_entity_id=virtual_id)

    # Link should have created now.
    assert link_obsv.id is not None, \
        "Link does not exist. {} should be linked to {} with id {}".format(real_id, virtual_id, link_obsv.id)
    assert link_obsv.real_entity_id == real_id, "There was an error while linking."
    assert link_obsv.virtual_entity_id == virtual_id, "There was an error while linking."

    # Search should return valid link.
    search_link_obsv = search_compound_links(ld_api_client, [real_id])

    assert link_obsv.as_dict() == search_link_obsv[0].as_dict(), \
        "Created link and searched links are not similar"

    assert len(search_link_obsv) == 1, \
        "No link exists between real {} and virtual compound ID {}. The Observation ID returned is {}".format(
            real_id, virtual_id, link_obsv.id)

    # Remove compounds link.
    unlink_obsv = unlink_compounds(ld_api_client, link_obsv.id)
    assert unlink_obsv is None, \
        "Link still exist. {} should not be linked to {}".format(real_id, virtual_id)

    # Search should return no link.
    deleted_link_obsv = search_compound_links(ld_api_client, [real_id])
    assert deleted_link_obsv == [], \
        "There was an error while searching for links. Expected {} links but got {} links".format(0, len(link_obsv))
