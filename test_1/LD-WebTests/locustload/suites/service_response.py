import locust

from locustload import dbprofile
from locustload.util import ldlocust
from locustload.livedesign import paths
from locustload.suites.abstract_taskset import AbstractTaskSet


@locust.task
class ServiceResponseTaskSet(AbstractTaskSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.live_report_id = None

    @locust.task
    def task_main(self):
        with self.timed("[section] Service Response", False):

            self.live_report_id = self.timed_create_new_live_report(
                "Create Live Report",
                project_id=dbprofile.get().service_response.project_id,
            )
            with self.timed("ZZ Wait On Live Report To Execute"):
                self.locust_ld_client.execute_live_report(self.live_report_id)
            self.user.wait()

            with self.timed("Request Get All Freeform Columns"):
                self.locust_ld_client.freeform_columns()
            self.user.wait()

            with self.timed("Request Get All Mpos"):
                self.locust_ld_client.list_mpos()
            self.user.wait()

            with self.timed("Request Post Models Search"):
                self.locust_ld_client.get_models_by_project_id(
                    project_ids=[dbprofile.get().service_response.project_id])
            self.user.wait()

            with self.timed("Request Get Live Report Queries"):
                response = self.client.get(paths.LIVE_REPORTS_QUERIES.format(live_report_id=self.live_report_id))
                response.raise_for_status()
            self.user.wait()

            with self.timed("Request Post Live Report Results"):
                payload = {
                    "live_report_id":
                        self.live_report_id,
                    "report_level":
                        "PARENT",
                    "view_details": [{
                        "type": "page",
                        "row_return_type": "FROZEN_ONLY",
                        "projections": [],
                    }, {
                        "type": "page",
                        "row_return_type": "ALL",
                        "projections": [],
                        "start": 0
                    }]
                }
                response = self.client.post(paths.LIVE_REPORTS_RESULTS, json=payload)
                response.raise_for_status()
            self.user.wait()

            with self.timed("Request Post Live Report Search"):
                self.locust_ld_client.live_reports(project_ids=[dbprofile.get().service_response.project_id])
            self.user.wait()

            with self.timed("Request Post Live Report Metadata Search"):
                self.locust_ld_client.live_reports_metadata(project_ids=[dbprofile.get().service_response.project_id])
            self.user.wait()

            with self.timed("Request Post Observation Search"):
                payload = {'live_report_id_search_query': {'live_report_id': self.live_report_id}}
                response = self.client.post(paths.OBSERVATION_SEARCH, json=payload)
                response.raise_for_status()
            self.user.wait()

            with self.timed("Request Post Rationales Search"):
                payload = {'live_report_id_search_query': {'live_report_id': self.live_report_id}}
                response = self.client.post(paths.RATIONALES_SEARCH, json=payload)
                response.raise_for_status()
            self.user.wait()

            with self.timed("Request Post Column Descriptors Search"):
                self.locust_ld_client.column_descriptors(self.live_report_id)
            self.user.wait()

            with self.timed("Request Post Active Users Search"):
                payload = {'live_report_id_search_query': {'live_report_id': self.live_report_id}}
                response = self.client.post(paths.ACTIVE_USERS_SEARCH, json=payload)
                response.raise_for_status()
            self.user.wait()

            with self.timed("Request Post Plot Search"):
                payload = {"search_by_live_report": {"query": self.live_report_id}, "search_type": "live_report"}
                response = self.client.post(paths.PLOT_SEARCH, json=payload)
                response.raise_for_status()
            self.user.wait()

            with self.timed("Request Properties"):
                enable_column_tree_microservice = False
                configured_properties = self.locust_ld_client.property_search(
                    property_keys=['ENABLE_COLUMN_TREE_MICROSERVICE'])
                for property in configured_properties.results:
                    if property.key == 'ENABLE_COLUMN_TREE_MICROSERVICE':
                        enable_column_tree_microservice = (property.value.upper() == 'TRUE')
                        break
            self.user.wait()

            with self.timed("Request Post Column Folder Search"):
                payload = {
                    "addable_column_type": [
                        "assay", "substructure", "model", "database", "id", "compound", "database", "rationale",
                        "scaffold", "scaffold", "enumeration", "r_group", "freeform"
                    ],
                    "exclude_clustering_models": True,
                    "exclude_add_all": True,
                    "exclude_create": True,
                    "display_column_type": [
                        "project_favorites", "computed_property", "computational_model", "experimental_assay",
                        "database", "freeform"
                    ],
                    "value_type": ["integer", "float", "string", "date", "datetime", "variable", "boolean"],
                    "parent_id": None
                }
                params = {"project_id": "0"}
                response = self.client.post(
                    paths.COLUMN_FOLDER_SEARCH.format('/v2' if enable_column_tree_microservice else ''),
                    json=payload,
                    params=params)
                response.raise_for_status()
            self.user.wait()

            with self.timed("Request Post Column Alias Search"):
                self.locust_ld_client.column_aliases(dbprofile.get().service_response.project_id)
            self.user.wait()

    @locust.task
    def task_cleanup(self):
        if self.live_report_id is not None:
            self.timed_delete_live_report("Delete LiveReport", self.live_report_id)

    @locust.task
    def task_finalize(self):
        # Stop Locust user at the end
        ldlocust.stop_user()
