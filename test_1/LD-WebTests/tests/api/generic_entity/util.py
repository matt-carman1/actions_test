import uuid


def build_unique_id():
    return 'ID-' + uuid.uuid4().hex
