import pytest
import time
from helpers.api.actions import livereport
from helpers.api.actions.compound import create_virtual_compound, delete_all_compound_links_for_compound, \
    create_real_compound


@pytest.fixture(scope="function")
def live_report(request, ld_client, use_module_isolated_project):
    project_id = ld_client.get_project_id_by_name(use_module_isolated_project)
    live_report = livereport.create_new_live_report(ld_client=ld_client, title="Compound Link", project_id=project_id)

    def finalizer():
        livereport.delete_live_report(ld_client, live_report.id)

    request.addfinalizer(finalizer)

    return live_report


@pytest.fixture(scope="function")
def real_compound_seed(worker_id):
    return "R" + worker_id + time.time().hex()


@pytest.fixture(scope="function")
def virtual_compound_seed(worker_id):
    return "V" + worker_id + time.time().hex()


@pytest.fixture(scope="function")
def real_compound(request, real_compound_seed, new_live_report, ld_client):
    response = create_real_compound(ld_client, new_live_report, real_compound_seed)

    def finalizer():
        delete_all_compound_links_for_compound(ld_client, real_compound_seed)

    request.addfinalizer(finalizer)

    return response


@pytest.fixture(scope="function")
def virtual_compound(virtual_compound_seed, new_live_report, ld_client):
    response = create_virtual_compound(ld_client, new_live_report.project_id, new_live_report.id, virtual_compound_seed)
    return response
