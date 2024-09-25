from helpers.extraction import paths
import hashlib


def test_get_attachment(ld_api_client):
    """
    Test get_attachment function doesn't fail after adding URL encoding of parameter in 9.0.1
    :param ld_api_client: fixture that returns ldclient object.
    """
    alternate_id = 'bcf83de0-1a1e-4009-8b86-7158705c1fdd#6905'
    expected_md5sum_hash = '034f142c8aa91652db1338adfc4da9b5'
    file_path = paths.get_resource_path("get_attachment_file_data")
    md5_hash = hashlib.md5()

    attachment_data = ld_api_client.get_attachment(alternate_id)

    with open(file_path, mode='wb') as local_file_to_write:
        local_file_to_write.write(attachment_data)

    with open(file_path, mode='rb') as local_file_to_read:
        # For large files which can't be fit as a whole in the memory we'll read chunks of 4096 bytes sequentially
        # and feed them to the md5 method
        for chunk in iter(lambda: local_file_to_read.read(4096), b""):
            md5_hash.update(chunk)
        md5_hash = md5_hash.hexdigest()

    assert len(attachment_data) != 0
    assert md5_hash == expected_md5sum_hash
