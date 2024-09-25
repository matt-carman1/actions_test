import json
import pprint

import locust
import locustload.livedesign.paths as paths
from locustload import dbprofile
from locustload.suites.abstract_taskset import AbstractTaskSet
from locustload.util import ldlocust


@locust.task
class AdvancedTaskSet(AbstractTaskSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.live_report_id = None

    @locust.task
    def task1_create(self):
        self.timed_create_live_report("[section] 1 - Create LiveReport", has_parent=False)

    @locust.task
    def task2_list(self):
        self.timed_list_live_reports_and_projects("[section] 2 - List LiveReports and Projects", False)

    @locust.task
    def task3_import(self):
        with self.timed("[section] 3 - Add compounds", False):
            self.timed_add_compounds_via_import_csv("User Add Compounds via Import Csv")
            self.user.wait()

            self.timed_add_compounds_via_substructure_search("User Add Compounds via Substructure Search")
            self.user.wait()

            self.timed_add_compounds_via_similarity_search("User Add Compounds via Similarity Search")
            self.user.wait()

    @locust.task
    def task4_copy_livereport(self):
        self.timed_copy_livereport("[section] 4 - Copy LiveReport", False)

    @locust.task
    def task5_quick_properties_columns(self):
        with self.timed("[section] 5 - Quick Properties Columns", False):
            self.timed_add_addable_columns(
                "User Add Quick Properties Column Shortcut",
                self.live_report_id,
                dbprofile.get().advanced.quick_properties_column_ids,
            )
            self.timed_wait_until_cells_contain_values("User Add Quick Properties Column Data",
                                                       dbprofile.get().advanced.quick_properties_column_ids, 1)

    @locust.task
    def task6_plot(self):
        self.timed_create_plot("[section] 6 - Plot", False)

    @locust.task
    def task7_3d_column(self):
        with self.timed("[section] 7 - 3D Column", False):
            self.timed_add_compounds(
                "User Add Compound with 3D Data",
                self.live_report_id,
                dbprofile.get().advanced.compound_id_for_three_d_column,
                dbprofile.get().advanced.compound_id_search_num + 1,
            )
            self.timed_add_addable_columns("User Add 3D Column Shortcut", self.live_report_id,
                                           [dbprofile.get().advanced.three_d_column_id])
            self.timed_wait_until_cells_contain_values("User Add 3D Column Data",
                                                       [dbprofile.get().advanced.three_d_column_id], 1)

    @locust.task
    def task8_3d_data_structure_search(self):
        with self.timed("[section] 8 - 3D Data Structure Search", False):
            self.timed_3d_structure_search("3D Data Structure Search")

    @locust.task
    def task9_cleanup(self):
        with self.timed("[section] 9 - Cleanup", False):
            if self.live_report_id is not None:
                self.timed_delete_live_report("Request Delete LiveReport", self.live_report_id)

    @locust.task
    def task_finalize(self):
        # Stop Locust user at the end
        ldlocust.stop_user()
