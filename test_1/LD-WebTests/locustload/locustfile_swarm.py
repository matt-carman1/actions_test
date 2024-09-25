import math
import random

import helpers.api as api
import helpers.api.actions.column
import helpers.api.actions.row
import locust
from locustload import dbprofile
from locustload.default_user import DefaultUser
from locustload.suites.abstract_taskset import AbstractTaskSet
from locustload.suites.subtasksets.create_taskset import create_taskset
from locustload.util import ldlocust
from locustload.util.ldlocust import RawDataLogger
from locustload.util.timed import PropagateError

raw_data_logger = RawDataLogger()

default_repetitions = 10

# Denotes the load shape: default_load or variable_load
# Command line arg: --load_profile
# NOTE(kansal): Don't use default_load with single taskset users without specifying --max_run_time
# since we run them in a loop indefinitely
load_profile = None

# Denotes the max number of users running concurrently
# Command line arg: --max_user_count
max_user_count = None

# Denotes the max number of users that can run concurrently
# Command line arg: --custom_spawn_rate
custom_spawn_rate = None

# Denotes max run time for the test
# Command line arg: --max_run_time
max_run_time = None

# Denotes the time at which concurrent number of users should reach max_user_count
# Used when load_profile = variable_load
# Command line arg: --peak_run_time
peak_run_time = None


@locust.events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--load_profile", type=str, env_var="LOCUST_LOAD_PROFILE", default="constant")
    parser.add_argument("--max_user_count", type=int, env_var="LOCUST_MAX_USER_COUNT", default=1)
    parser.add_argument("--custom_spawn_rate", type=int, env_var="LOCUST_CUSTOM_SPAWN_RATE", default=1)
    parser.add_argument("--max_run_time", type=int, env_var="LOCUST_MAX_RUN_TIME", default=None)
    parser.add_argument("--peak_run_time", type=int, env_var="LOCUST_PEAK_RUN_TIME", default=None)


@locust.events.init.add_listener
def set_options(environment, **kwargs):
    global load_profile
    load_profile = environment.parsed_options.load_profile
    global max_user_count
    max_user_count = environment.parsed_options.max_user_count
    global custom_spawn_rate
    custom_spawn_rate = environment.parsed_options.custom_spawn_rate
    global max_run_time
    max_run_time = environment.parsed_options.max_run_time
    global peak_run_time
    peak_run_time = environment.parsed_options.peak_run_time


def sketch_compound(self):
    self.timed_sketch_compound("[section] 2 - Sketch Compound", False)


def switch_aggregation_mode(self):
    self.timed_switch_aggregation_mode("[section] 2 - Switch Aggregation Mode", "PARENT_BATCH", False)
    self.timed_switch_aggregation_mode("[section] 2 - Switch Aggregation Mode", "PARENT", False)


def reorder_columns(self):
    self.timed_reorder_columns("[section] 2 - Reorder Columns", False)


def sort_columns(self):
    self.timed_sort_columns("[section] 2 - Sort Columns", False)


def add_scaffold(self):
    self.timed_add_scaffold("[section] 2 - Add Scaffold", False)


def add_and_remove_filters(self):
    self.timed_add_and_remove_filters("[section] 2 - Filters", False)


def remove_and_add_rows(self):
    self.timed_remove_and_add_rows("[section] 2 - Remove and Add Rows", False)


def create_and_edit_ffc(self):
    self.timed_create_and_edit_ffc("[section] 2 - FFC", False)


def add_model(self):
    freeform_column_id, entered_ffc_values = self.timed_create_and_edit_ffc("[section] 2 - FFC", False)
    self.timed_model("[section] 3 - Model", freeform_column_id, entered_ffc_values, False)


def numeric_range_value_search(self):
    self.timed_advanced_search_numeric_range("[section] 2 - Numeric Range Value Advanced Search", False)


def numeric_defined_value_search(self):
    self.timed_advanced_search_numeric_defined("[section] 2 - Numeric Defined Value Advanced Search", False)


def text_exact_value_search(self):
    self.timed_advanced_search_text_exact("[section] 2 - Text Exact Value Advanced Search", False)


def text_defined_value_search(self):
    self.timed_advanced_search_text_defined("[section] 2 - Text Defined Value Advanced Search", False)


def list_live_reports_and_projects(self):
    self.timed_list_live_reports_and_projects("[section] 2 - List LiveReports and Projects", False)


def add_and_remove_compounds_via_import_csv(self):
    with self.timed("[section] 2 - Add and Remove Compounds via Import Csv", False):
        self.timed_remove_all_rows("User Remove All Rows")
        self.timed_add_compounds_via_import_csv("User Add Compounds via Import Csv", True)


def add_and_remove_compounds_via_substructure_search(self):
    with self.timed("[section] 2 - Add and Remove Compounds via Substructure Search", False):
        self.timed_remove_all_rows("User Remove All Rows")
        self.timed_add_compounds_via_substructure_search("User Add Compounds via Substructure Search", True)


def add_and_remove_compounds_via_similarity_search(self):
    with self.timed("[section] 2 - Add and Remove Compounds via Similarity Search", False):
        self.timed_remove_all_rows("User Remove All Rows")
        self.timed_add_compounds_via_similarity_search("User Add Compounds via Similarity Search", True)


def create_plot(self):
    self.timed_create_plot("[section] 2 - Plot", False)


def add_3D_column(self):
    with self.timed("[section] 2 - 3D Column", False):
        self.timed_add_compounds(
            "User Add Compound with 3D Data",
            self.live_report_id,
            dbprofile.get().advanced.compound_id_for_three_d_column,
            dbprofile.get().common.compound_id_search_num + 1,
        )
        for _ in range(default_repetitions):
            self.timed_add_addable_columns("User Add 3D Column Shortcut", self.live_report_id,
                                           [dbprofile.get().advanced.three_d_column_id])
            self.timed_wait_until_cells_contain_values("User Add 3D Column Data",
                                                       [dbprofile.get().advanced.three_d_column_id], 1)
            with self.timed("User Remove 3D Column"):
                api.actions.column.remove_columns_from_live_report(self.locust_ld_client, self.live_report_id,
                                                                   [dbprofile.get().advanced.three_d_column_id])


def threed_structure_search(self):
    self.timed_3d_structure_search("[section] 2 - 3d_structure_search", self.live_report_id)


class CopyLRTaskSet(AbstractTaskSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @locust.task
    def copy_random_live_reports(self):
        with self.timed("[section] 2 - Copy Random Live Reports", False):
            live_reports = self.locust_ld_client.live_reports([dbprofile.get().common.project_id])
            failed_iterations = 0
            with self.timed("Loop", True):
                for _ in range(default_repetitions):
                    try:
                        index = random.randint(0, len(live_reports) - 1)
                        live_report_id = live_reports[index].id

                        with self.timed("Request Copy Live Report"):
                            copied_live_report = self.locust_ld_client.copy_live_report(live_report_id)

                        self.timed_delete_live_report("Request Delete LiveReport", copied_live_report.id)
                    except PropagateError:
                        failed_iterations += 1
                    finally:
                        self.user.wait()

            assert(failed_iterations <= 0), \
                "Failed {}/{} iterations of the loop".format(failed_iterations, default_repetitions)

    @locust.task
    def task_finalize(self):
        ldlocust.stop_user()


AddAndRemoveFiltersTaskset = create_taskset(add_and_remove_filters, default_repetitions)
AddCompoundsViaImportCSVTaskset = create_taskset(add_and_remove_compounds_via_import_csv, default_repetitions)
AddCompoundsViaSimilaritySearchTaskset = create_taskset(add_and_remove_compounds_via_similarity_search,
                                                        default_repetitions)
AddCompoundsViaSubstructureSearchTaskset = create_taskset(add_and_remove_compounds_via_substructure_search,
                                                          default_repetitions)
AddModelTaskset = create_taskset(add_model, default_repetitions)
AddScaffoldTaskset = create_taskset(add_scaffold, default_repetitions)
CreateAndEditFFCTaskset = create_taskset(create_and_edit_ffc, math.ceil(default_repetitions / 10))
CreatePlotTaskset = create_taskset(create_plot, default_repetitions)
ListLiveReportsAndProjectsTaskset = create_taskset(list_live_reports_and_projects, default_repetitions)
NumericDefinedValueSearchTaskset = create_taskset(numeric_defined_value_search, default_repetitions)
NumericRangeValueSearchTaskset = create_taskset(numeric_range_value_search, default_repetitions)
RemoveAndAddRowsTaskset = create_taskset(remove_and_add_rows, math.ceil(default_repetitions / 10))
ReorderColumnsTaskset = create_taskset(reorder_columns, default_repetitions)
SketchCompoundTaskset = create_taskset(sketch_compound, default_repetitions)
SortColumnsTaskset = create_taskset(sort_columns, default_repetitions)
SwitchAggregationModeTaskset = create_taskset(switch_aggregation_mode, default_repetitions)
TextDefinedValueSearchTaskset = create_taskset(text_defined_value_search, default_repetitions)
TextExactValueSearchTaskset = create_taskset(text_exact_value_search, default_repetitions)
Add3DColumnTaskset = create_taskset(add_3D_column)
ThreeDStructureSearch = create_taskset(threed_structure_search)


class SwarmUser(DefaultUser):
    tasks = [
        SketchCompoundTaskset,
        SwitchAggregationModeTaskset,
        ReorderColumnsTaskset,
        SortColumnsTaskset,
        AddScaffoldTaskset,
        AddAndRemoveFiltersTaskset,
        RemoveAndAddRowsTaskset,
        CreateAndEditFFCTaskset,
        AddModelTaskset,
        NumericRangeValueSearchTaskset,
        NumericDefinedValueSearchTaskset,
        TextExactValueSearchTaskset,
        TextDefinedValueSearchTaskset,
        ListLiveReportsAndProjectsTaskset,
        AddCompoundsViaImportCSVTaskset,
        AddCompoundsViaSubstructureSearchTaskset,
        AddCompoundsViaSimilaritySearchTaskset,
        CreatePlotTaskset,
        Add3DColumnTaskset,
        ThreeDStructureSearch,
    ]


class CustomLoadShape(locust.LoadTestShape):

    def is_within_time_limit(self):
        if max_run_time == None or max_run_time > self.get_run_time():
            return True
        return False

    def constant_load(self):
        return (max_user_count, custom_spawn_rate)

    def variable_load(self):
        run_time = self.get_run_time()
        break_time = max(0, max_run_time - 2 * peak_run_time)
        if run_time > peak_run_time and run_time < (peak_run_time + break_time):
            return (0, 1)
        spawn_rate = max_user_count / peak_run_time
        return (max_user_count, spawn_rate)

    def tick(self):
        if self.is_within_time_limit():
            if load_profile == "constant":
                return self.constant_load()
            elif load_profile == "variable":
                return self.variable_load()

        return None
