import helpers.api as api
import ldclient
import locust
from locustload import dbprofile
from locustload.suites.abstract_taskset import AbstractTaskSet
from locustload.util import ldlocust


@locust.task
class WarmupTaskSet(AbstractTaskSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.live_report_id = None

    @locust.task
    def task_create(self):
        self.live_report_id = self.timed_create_new_live_report("Request Create Live Report")

        self.timed_add_compounds(
            "User Add Compounds via *",
            self.live_report_id,
            dbprofile.get().common.compound_id_search_query,
            dbprofile.get().common.compound_id_search_num,
        )

    @locust.task
    def task_add_scaffolds(self):
        self.timed_add_scaffold("User Add Scaffold")

    @locust.task
    def task_substructure_search(self):
        with self.timed("Substructure Search"):
            self.locust_ld_client.compound_search(
                dbprofile.get().advanced.molecule_for_search_warmup,
                search_type='SUBSTRUCTURE',
                max_results=1,
                search_threshold=0.7,
                project_id=dbprofile.get().common.project_id,
            )

    @locust.task
    def task_similarity_search(self):
        with self.timed("Similarity Search"):
            self.locust_ld_client.compound_search(
                dbprofile.get().advanced.molecule_for_search_warmup,
                search_type='SIMILARITY',
                max_results=1,
                search_threshold=0.5,
                project_id=dbprofile.get().common.project_id,
            )

    @locust.task
    def task_import_3d_data(self):
        self.timed_import_3D_data("Import 3D data", False)

    @locust.task
    def add_and_remove_compounds_via_import_csv(self):
        self.timed_add_compounds_via_import_csv("User Add Compounds via Import Csv", True)

    def timed_list_live_reports_metadata(self, action_name, has_parent):
        with self.timed(action_name, has_parent):
            live_reports_metadata = self.locust_ld_client.live_reports_metadata([dbprofile.get().common.project_id])
            return live_reports_metadata

    @locust.task
    def task_cleanup(self):
        if self.live_report_id is not None:
            self.timed_delete_live_report("Request Delete LiveReport", self.live_report_id)

    @locust.task
    def task_create_coincident_lr_by_title(self):
        live_reports_metadata = self.timed_list_live_reports_metadata("Get LiveReport Metadata", True)
        for metadata in live_reports_metadata:
            if metadata.title == dbprofile.get().coincident.coincident_live_report_title:
                self.locust_ld_client.delete_live_report(metadata.id)

        coincident_live_report_id = self.timed_create_live_report(
            "Create Coincident LiveReport",
            has_parent=True,
            lr_title=dbprofile.get().coincident.coincident_live_report_title)

        freeform_columns = self.locust_ld_client.freeform_columns(project_id=dbprofile.get().common.project_id)
        freeform_columns_name = [
            freeform_column.name
            for freeform_column in freeform_columns
            if freeform_column.live_report_id == coincident_live_report_id
        ]
        for coincident_ffc in dbprofile.get().coincident.coincident_freeform_columns_name:
            if coincident_ffc not in freeform_columns_name:
                freeform_column = ldclient.client.FreeformColumn(coincident_ffc,
                                                                 "For the load test",
                                                                 published=True,
                                                                 type=ldclient.client.FreeformColumn.COLUMN_NUMBER,
                                                                 live_report_id=coincident_live_report_id)
                freeform_column = self.locust_ld_client.create_freeform_column(freeform_column.as_dict())
                api.actions.column.add_columns_to_live_report(self.locust_ld_client, coincident_live_report_id,
                                                              [freeform_column.id])

    @locust.task
    def task_finalize(self):
        # Stop Locust user at the end
        ldlocust.stop_user()
