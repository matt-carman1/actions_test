def verify_threed_structure(expected_structure, actual_structure):
    """
    Verifies the properties of 3D structure as returned by get_threed_structure() ldclient method

    :param expected_structure: dict, the expected structure to verify with
    :param actual_structure: dict, the actual returned structure to verify
    """
    # order of the elements in the list 'structure_attachments' returned by get_threed_structure() is non-deterministic
    # so sorting the list before comparison
    sorted_expected_struc = sorted(expected_structure['structure_attachments'],
                                   key=lambda i: i['structure_transformation'])
    sorted_actual_struc = sorted(actual_structure['structure_attachments'], key=lambda i: i['structure_transformation'])
    for exp_key, act_key in zip(expected_structure, actual_structure):
        if exp_key == 'structure_attachments':
            assert sorted_expected_struc == sorted_actual_struc, \
                "Expected {} but got {}".format(sorted_expected_struc, sorted_actual_struc)
        else:
            assert expected_structure[exp_key] == actual_structure[act_key], \
                "Expected {} but got {}".format(expected_structure[exp_key], actual_structure[act_key])
