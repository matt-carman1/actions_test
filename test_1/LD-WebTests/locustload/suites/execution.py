import locust

import random

import ldclient

from locustload import dbprofile
from locustload.util import ldlocust
from locustload.suites.abstract_taskset import AbstractTaskSet
from locustload.livedesign import paths

import pprint

import helpers.api as api
import helpers.api.actions.row
import helpers.api.actions.column

from locustload.util.timed import TimedAction, PropagateError


@locust.task
class ExecutionTaskSet(AbstractTaskSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.live_report_id = None
        self.freeform_column_id = None
        self.entered_ffc_values = None

    @locust.task
    def task1_create(self):
        self.timed_create_live_report("[section] 1 - Create LiveReport", False)

    @locust.task
    def task2_add_extra_compounds(self):
        with self.timed("[section] 2 - Add extra compounds", False):
            expected_number = dbprofile.get().common.compound_id_search_num
            for (query, number) in dbprofile.get().execution.extra_compound_queries:
                expected_number += number
                self.timed_add_compounds("User Add Extra Compounds via *",
                                         self.live_report_id,
                                         query,
                                         expected_number,
                                         error_tolerance=0.01)
                self.user.wait()

    @locust.task
    def task3_add_extra_columns(self):
        self.timed_add_addable_columns("[section] 3 - Add extra columns",
                                       self.live_report_id,
                                       dbprofile.get().execution.extra_column_ids,
                                       has_parent=False)

    @locust.task
    def task4_filters(self):
        self.timed_add_and_remove_filters("[section] 4 - Filters", False)

    @locust.task
    def task5_ffc(self):
        self.freeform_column_id, self.entered_ffc_values = self.timed_create_and_edit_ffc("[section] 5 - FFC", False)

    @locust.task
    def task6_remove_and_add_rows(self):
        self.timed_remove_and_add_rows("[section] 6 - Remove and Add Rows", False)

    @locust.task
    def task7_other(self):
        with self.timed("[section] 7 - Other", False):
            self.timed_reorder_columns("User Reorder Columns")
            self.user.wait()

            self.timed_sort_columns("User Sort Column")
            self.user.wait()

            self.timed_sketch_compound("User Sketch Compound")
            self.user.wait()

            self.timed_switch_aggregation_mode("User Switch Aggregation Mode")

    @locust.task
    def task8_cleanup(self):
        with self.timed("[section] 8 - Cleanup", False):
            if self.live_report_id is not None:
                self.timed_delete_live_report("Request Delete LiveReport", self.live_report_id)

    @locust.task
    def task_finalize(self):
        # Stop Locust user at the end
        ldlocust.stop_user()
