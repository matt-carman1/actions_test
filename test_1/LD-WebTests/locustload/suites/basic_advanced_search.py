import locust

import random

import ldclient

from locustload import dbprofile
from locustload.util import ldlocust
from locustload.suites.abstract_taskset import AbstractTaskSet
from locustload.livedesign import paths

import pprint


@locust.task
class BasicAdvancedSearchTaskSet(AbstractTaskSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.live_report_id = None

    def timed_run_advanced_search_query(self, search_query_method, search_query_name, has_parent=True):
        with self.timed("Execute Advanced Search Query", has_parent):
            self.live_report_id = self.timed_create_new_live_report("Request Create LiveReport")
            self.user.wait()

            search_query_method(search_query_name, True)

            if self.live_report_id is not None:
                self.timed_delete_live_report("Delete LiveReport Request", self.live_report_id)

    @locust.task
    def task1_numeric_range_value(self):
        self.timed_run_advanced_search_query(self.timed_advanced_search_numeric_range,
                                             "Numeric Range Value Advanced Search", False)

    @locust.task
    def task2_numeric_defined_value(self):
        self.timed_run_advanced_search_query(self.timed_advanced_search_numeric_defined,
                                             "Numeric Defined Value Advanced Search", False)

    @locust.task
    def task3_text_exact_value(self):
        self.timed_run_advanced_search_query(self.timed_advanced_search_text_exact, "Text Exact Value Advanced Search",
                                             False)

    @locust.task
    def task4_text_defined_value(self):
        self.timed_run_advanced_search_query(self.timed_advanced_search_text_defined,
                                             "Text Defined Value Advanced Search", False)

    @locust.task
    def task_finalize(self):
        # Stop Locust user at the end
        ldlocust.stop_user()
