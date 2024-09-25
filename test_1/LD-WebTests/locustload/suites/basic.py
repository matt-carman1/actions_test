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
class BasicTaskSet(AbstractTaskSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.live_report_id = None
        self.freeform_column_id = None
        self.entered_ffc_values = None

    def helper_column_is_present(self, column_id):
        results = self.locust_ld_client.execute_live_report(self.live_report_id)
        row_infos = results["row_infos"]
        row_key = row_infos[0]["row_key"]  # take an arbitrary row key
        cells = results["rows"][row_key]["cells"]
        return column_id in cells

    def timed_remove_column(self, action_name):
        with self.timed(action_name):
            column_id = dbprofile.get().basic.column_id_for_subtask_remove_column

            assert (self.helper_column_is_present(column_id)), "Column {} is not found in LiveReport".format(column_id)

            with self.timed(action_name + " - Request"):
                self.locust_ld_client.remove_columns(self.live_report_id, [column_id])

            with self.timed(action_name + " - Wait"):

                def column_is_removed():
                    assert (not self.helper_column_is_present(column_id)), (
                        "Column {} is not removed from LiveReport".format(column_id))

                self.wait_until_condition(column_is_removed)

    @locust.task
    def task1_create(self):
        self.timed_create_live_report("[section] 1 - Create LiveReport", has_parent=False)

    @locust.task
    def task2_filters(self):
        self.timed_add_and_remove_filters("[section] 2 - Filters", False)

    @locust.task
    def task3_ffc(self):
        self.freeform_column_id, self.entered_ffc_values = self.timed_create_and_edit_ffc("[section] 3 - FFC", False)

    @locust.task
    def task4_model(self):
        self.timed_model("[section] 4 - Model", self.freeform_column_id, self.entered_ffc_values, False)

    @locust.task
    def task5_remove_and_add_rows(self):
        self.timed_remove_and_add_rows("[section] 5 - Remove and Add Rows", False)

    @locust.task
    def task6_other(self):
        with self.timed("[section] 6 - Other", False):
            self.timed_reorder_columns("User Reorder Columns")
            self.user.wait()

            self.timed_sort_columns("User Sort Column")
            self.user.wait()

            self.timed_remove_column("User Remove Column")
            self.user.wait()

            self.timed_sketch_compound("User Sketch Compound")
            self.user.wait()

            self.timed_add_scaffold("User Add Scaffold")
            self.user.wait()

            self.timed_switch_aggregation_mode("User Switch Aggregation Mode")

    @locust.task
    def task7_cleanup(self):
        with self.timed("[section] 7 - Cleanup", False):
            if self.live_report_id is not None:
                self.timed_delete_live_report("Request Delete LiveReport", self.live_report_id)

    @locust.task
    def task_finalize(self):
        # Stop Locust user at the end
        ldlocust.stop_user()
