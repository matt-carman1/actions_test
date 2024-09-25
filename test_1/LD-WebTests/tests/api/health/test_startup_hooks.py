import pytest
from library.api.extended_ldclient.client import ExtendedLDClient
from library.api.extended_ldclient.enums import StartupHookStatus


def test_startup_hooks(ld_api_client: ExtendedLDClient):
    """
    Test whether any startup hook fails.
    """

    start_hooks_status = ld_api_client.get_startup_hooks_status()
    failed_hooks = []

    for entry in start_hooks_status:
        if start_hooks_status[entry] == StartupHookStatus.FAILED:
            failed_hooks.append(entry)

    assert len(failed_hooks) == 0, f"Failing hooks: {failed_hooks}"
