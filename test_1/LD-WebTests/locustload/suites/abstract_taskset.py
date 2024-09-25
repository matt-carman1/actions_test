import datetime
import os
import pprint
import random
import tempfile
import time
import uuid

import helpers.api as api
import helpers.api.actions.compound
import helpers.api.actions.livereport
import ldclient
import locust
from ldclient.__experimental.experimental_models import Plot
from ldclient.__experimental.experimental_models import QueryObservationCondition
from ldclient.__experimental.experimental_models import QueryRangedObservationCondition
from ldclient.__experimental.experimental_models import Scaffold
from ldclient.__experimental.experimental_models import ScatterPlot
from ldclient.__experimental.experimental_models import StructureSearchRequest
from locustload import dbprofile
from locustload.util import ldlocust
from locustload.util import timed
from locustload.util.timed import PropagateError
from locustload.util.timed import TimedAction


class AbstractTaskSet(locust.SequentialTaskSet, ldlocust.LocustLDClientProviderMixin):
    """
    This is a parent TaskSet class that defines common helper methods for LiveDesign Locust load tests
    """

    def wait_until_condition(self,
                             condition_function,
                             retries=dbprofile.get().common.default_retries,
                             interval=dbprofile.get().common.default_wait_interval,
                             **kwargs):
        """
        Repeatedly call condition_function() until either the condition is met (which happens when the call
        does not raise an AssertionError) or the number of retries reaches the specified limit.

        Caught exceptions (from locustload.utils.timed.exception_list) don't stop the polling process.

        Raises AssertionError on timeout to indicate that the polling process failed.

        :param retries: number of retries
        :param interval: delay in milliseconds
        keyword args:
        start_time (float): time when the function execution started or lr refreshed
        :return: the returned value of the first not failed condition_function() call
        """
        failures = 0
        count_retries = 0
        latest_assertion_exception = None
        latest_non_assertion_exception = None
        for i in range(retries):
            try:
                if i > 0:
                    time.sleep(interval * 0.001)
                    count_retries += 1
                v = condition_function(**kwargs)
                return v
            except AssertionError as e:  # condition_function() is not satisfied
                latest_assertion_exception = e
                pass
            except timed.exception_list as e:  # condition_function() raised a known exception: record and skip
                latest_non_assertion_exception = e
                failures += 1
                pass

            # This loop breaks on any unknown (and therefore uncaught) exception

        # NOTE(nikolaev): This is the total sleep time, not the actual duration. Since Locust aggregates
        # request failures by name, keeping consistent duration helps to group failures together.
        total_duration = (count_retries * interval) * 0.001

        if failures > 0:
            assert False, \
                "Timeout ({} seconds) (failed {}/{} retries with non-assertion exceptions, the latest: {})".format(
                    total_duration, failures, retries, repr(latest_non_assertion_exception))
        else:
            assert False, \
                "Timeout ({} seconds, waiting for assertion: {})".format(
                    total_duration, repr(latest_assertion_exception))

    def get_live_report_results(self, live_report_id, projections=[], row_keys=[], report_level="PARENT"):
        view_details = [{
            "type": "row_key",
            "row_return_type": "ALL",
            "projections": projections,
            "row_keys": row_keys,
        }]
        return self.locust_ld_client.live_report_results(live_report_id=live_report_id,
                                                         view_details=view_details,
                                                         report_level=report_level)

    def get_cells(self, live_report_id, addable_column_id, row_keys):
        results = self.get_live_report_results(live_report_id, projections=[addable_column_id], row_keys=row_keys)
        row_keys_to_statuses_and_values = {}
        for row_key in row_keys:
            cell = results[row_key][addable_column_id]
            row_keys_to_statuses_and_values[row_key] = cell
        return row_keys_to_statuses_and_values

    def wait_for_cell_values(self,
                             live_report_id,
                             addable_column_id,
                             row_key_to_expected_value,
                             accept_statuses=[],
                             **kwargs):
        """
        Wait until for each of the specified LiveReport cells either:
        - their value content matches their expected value,
        - or the cell status matches one of the provided accept_statuses (e.g. can be used to accept cells
        with 'failed' status)

        :param live_report_id: LiveReport ID
        :param addable_column_id: addable column ID
        :param row_key_to_expected_value: Dictionary of row_key -> expected value.
        :param accept_statuses: list of cell statuses

        Any additional keyword arguments are passed unchanged as parameters to self.wait_until_condition() call,
        so one can set the delay interval and the number of retries.
        """

        def condition():
            row_keys = list(row_key_to_expected_value.keys())
            requested_cells = self.get_cells(live_report_id, addable_column_id, row_keys)
            for row_key, expected_value in row_key_to_expected_value.items():
                actual_cell = requested_cells[row_key]
                actual_statuses = actual_cell.get("statuses", [])
                actual_values = actual_cell.get("values", [])
                print("LR {}. Wait for cell ({},{}). Actual state: {}. Expected values: {}.".format(
                    live_report_id, row_key, addable_column_id, actual_cell, [expected_value]))
                expected_values_found = len(actual_values) == 1 and str(actual_values[0]) == str(expected_value)
                accepted_status_found = any([status.get('code') in accept_statuses for status in actual_statuses])
                assert (expected_values_found or accepted_status_found), \
                    "LR {}. Cell ({},{}) has status {} and contains: {}. Expected single value: {}".format(
                        live_report_id, addable_column_id, row_key, repr(actual_statuses), repr(actual_values),
                        expected_value)

        self.wait_until_condition(condition, **kwargs)

    def wait_for_cell_values_change(self, live_report_id, addable_column_id, row_key_to_old_values,
                                    row_key_to_expected_values, **kwargs):
        """
        Wait until for each of the specified LiveReport cells either:
        - their value content matches their expected value or,
        - their value content changed,

        :param live_report_id: LiveReport ID
        :param addable_column_id: addable column ID
        :param row_key_to_old_values: Dictionary of row_key -> old value.
        :param row_key_to_expected_value: Dictionary of row_key -> expected value.

        Any additional keyword arguments are passed unchanged as parameters to self.wait_until_condition() call,
        so one can set the delay interval and the number of retries.
        """

        # Waiting time to refresh LR (in the middle of the full waiting time, measured in ms)
        wait_to_refresh = 0.5 * (dbprofile.get().common.default_retries *
                                 dbprofile.get().common.default_wait_interval) * 0.001

        def condition(start_time):
            current_time = time.time()
            if current_time - start_time > wait_to_refresh:
                print('Refreshing LR results on an interval of {}'.format(current_time - start_time))
                start_time = current_time  # reset the waiting clock
                self.locust_ld_client.refresh_live_report_results([str(self.live_report_id)])

            row_keys = list(row_key_to_old_values.keys())
            requested_cells = self.get_cells(live_report_id, addable_column_id, row_keys)
            for row_key, old_value in row_key_to_old_values.items():
                actual_value = requested_cells[row_key].get("values", [])
                new_value_found = (actual_value != old_value) or (len(actual_value) == 1 and (str(
                    actual_value[0]) == str(row_key_to_expected_values[row_key])))
                print(
                    "LR {}. Wait for cell ({},{}). Actual state: {}. Expected values: {} or  old values should be changed {} != {}."
                    .format(live_report_id,
                            row_key, addable_column_id, actual_value, [row_key_to_expected_values[row_key]],
                            repr(old_value), [row_key_to_expected_values[row_key]]))
                assert (new_value_found), \
                    "LR {}. Cell ({},{}) contains: {}. Old value: {}".format(
                        live_report_id, addable_column_id, row_key, repr(actual_value), repr(old_value))

        self.wait_until_condition(condition, start_time=time.time())

    def wait_for_async_task(self, task_id: int, **kwargs):
        """
        Waits until the async task with task_id is finished.

        Any additional keyword arguments are passed unchanged as parameters to self.wait_until_condition() call,
        so one can set the delay interval and the number of retries.
        """

        def condition():
            results = self.locust_ld_client.async_tasks(task_ids=[task_id],
                                                        status_types=["finished", "running_stage2", "failed"])
            assert (results != []), "Async task {} has not been processed yet"
            status = results[0]["status"]
            assert (status == "finished"), "Async task {} status is {}".format(task_id, status)

        self.wait_until_condition(condition, **kwargs)

    def find_column_descriptor_by_column_id(self, live_report_id, column_id):
        descriptors = self.locust_ld_client.column_descriptors(live_report_id)
        for descriptor in descriptors:
            if descriptor.addable_column_id == column_id:
                return descriptor
        assert False, ("Descriptor for column '{}' is not found".format(column_id))

    def find_live_report_ids_by_title(self, action_name, title, has_parent=False):
        # Note(mushtaqu) : Run warmup user first So that A LR with the given title should present
        live_reports_metadata = self.timed_list_live_reports_metadata("User Search LiveReports Metadata", True)
        result = [
            live_report_metadata.id
            for live_report_metadata in live_reports_metadata
            if live_report_metadata.title == title
        ]
        return result if len(result) != 0 else None

    def timed(self, action_name, has_parent=True):
        """
        Create a context manager for timing actions. Usage:

        with self.timed("NAME"):
            <ACTION TO TIME>

        :param action_name: name of the recorded action, used as the request name when Locust records the event
        :param has_parent: When this argument is True, this times action re-raises caught exceptions so
        the parent action can record its success/failure status correctly.
        :return: TimedAction context manager
        """
        return TimedAction(self.user, action_name, has_parent)

    def timed_get_results_metadata(self, live_report_id, action_name="[poll/results-metadata]", has_parent=True):
        with self.timed(action_name, has_parent):

            def get_results_metadata():
                results_metadata = self.locust_ld_client.live_report_results_metadata(live_report_id)
                assert results_metadata  # Could be None or empty bytes
                return results_metadata

            result = self.wait_until_condition(get_results_metadata)
            assert (result is not None)
            return result

    def timed_create_new_live_report(self,
                                     action_name,
                                     has_parent=True,
                                     project_id=dbprofile.get().common.project_id,
                                     lr_title="Locust Test ({})".format(datetime.datetime.now().strftime("%H:%M:%S"))):
        with self.timed(action_name, has_parent):
            live_report = api.actions.livereport.create_new_live_report(
                self.locust_ld_client,
                lr_title,
                project_id=project_id,
            )
            return live_report.id

    def timed_create_live_report(self, action_name, has_parent=True, **kwargs):
        with self.timed(action_name, has_parent):
            self.live_report_id = self.timed_create_new_live_report("Request Create LiveReport", has_parent, **kwargs)
            self.user.wait()

            self.timed_add_addable_columns("User Add Columns Shortcut", self.live_report_id,
                                           dbprofile.get().common.add_column_ids)
            self.user.wait()

            self.timed_add_compounds(
                "User Add Compounds via *",
                self.live_report_id,
                dbprofile.get().common.compound_id_search_query,
                dbprofile.get().common.compound_id_search_num,
            )
            return self.live_report_id

    def timed_add_addable_columns(self, action_name, live_report_id, column_ids, has_parent=True):
        with self.timed(action_name, has_parent) as add_columns_action:
            with self.timed(add_columns_action + " - Request"):
                self.locust_ld_client.add_columns(live_report_id, column_ids)
            with self.timed(add_columns_action + " - Wait"):

                def columns_are_added():
                    results_metadata = self.timed_get_results_metadata(live_report_id)
                    actual_column_ids = set(results_metadata["columns"].keys())
                    assert all(str(column_id) in actual_column_ids for column_id in column_ids)

                self.wait_until_condition(columns_are_added)

    def timed_add_compounds(self,
                            action_name,
                            live_report_id,
                            search_query,
                            expected_number,
                            has_parent=True,
                            error_tolerance=0.1):
        with self.timed(action_name, has_parent) as add_compounds_action:
            with self.timed(add_compounds_action + " - Request"):
                database_names = [database.name for database in self.locust_ld_client.databases()]
                self.locust_ld_client.compound_search_by_id_async(search_query, database_names,
                                                                  dbprofile.get().common.project_id, live_report_id)

            with self.timed(add_compounds_action + " - Wait"):

                def rows_are_added():
                    results_metadata = self.timed_get_results_metadata(live_report_id)
                    total_rows = results_metadata["stats"]["total_rows"]
                    min_expected = expected_number * (1.0 - error_tolerance)
                    max_expected = expected_number * (1.0 + error_tolerance)
                    is_in_expected_range = min_expected < total_rows < max_expected
                    assert is_in_expected_range, ("Incorrect number of compounds in LR. "
                                                  "Actual: {}. Allowed range: [{:.0f},{:.0f}]").format(
                                                      total_rows, min_expected, max_expected)

                self.wait_until_condition(rows_are_added,
                                          interval=2 * dbprofile.get().common.default_wait_interval,
                                          retries=2 * dbprofile.get().common.default_retries)

    def timed_3d_structure_search(self,
                                  action_name,
                                  experiment_addable_column_id=None,
                                  column_ids=None,
                                  row_keys=None,
                                  has_parent=True):
        with self.timed(action_name, has_parent):
            threed_structure_search_group_result_len = self.locust_ld_client.structure_groups_size_by_threed_structure_search(
                StructureSearchRequest(live_report_id=str(self.live_report_id),
                                       report_level="parent",
                                       experiment_addable_column_id=experiment_addable_column_id,
                                       column_ids=column_ids,
                                       row_keys=row_keys))
            assert threed_structure_search_group_result_len > 0, f"Expected 3d structure search group result > 0 and found {threed_structure_search_group_result_len}"

    def timed_delete_live_report(self, action_name, live_report_id, has_parent=True):
        with self.timed(action_name, has_parent):
            self.locust_ld_client.delete_live_report(live_report_id)

    def timed_get_random_row(self, action_name, live_report_id):
        with self.timed(action_name):
            results_metadata = self.timed_get_results_metadata(live_report_id)
            row_infos = results_metadata["row_infos"]
            assert len(row_infos) > 0, "No rows found"
            return random.choice(row_infos)

    def timed_verify_number_of_filtered_rows(self, action_name, live_report_id, expected_number_of_filtered_rows):
        """
        Timed action that verifies the number of filtered rows in a LiveReport
        """
        with self.timed(action_name):
            results_metadata = self.timed_get_results_metadata(live_report_id)
            filtered_rows = results_metadata["stats"]["filtered_rows"]
            assert (filtered_rows == expected_number_of_filtered_rows), ("Unexpected number of filtered rows in LR. "
                                                                         "Actual: {}. Expected: {}").format(
                                                                             filtered_rows,
                                                                             expected_number_of_filtered_rows)

    def timed_add_text_filter(self, action_name, live_report_id, addable_column_id, entity_id):
        with self.timed(action_name):
            with self.timed(action_name + " - Request"):

                column_filter = ldclient.models.TextColumnFilter(
                    filter_type="text",
                    enabled=True,
                    inverted=False,
                    addable_column_id=addable_column_id,
                    value=entity_id,
                    delimiter=",",
                    case_sensitive=False,
                    text_match_type="exactly",
                )

                self.locust_ld_client.set_column_filter(live_report_id, column_filter)

            with self.timed(action_name + " - Wait"):

                def rows_are_filtered():
                    results_metadata = self.timed_get_results_metadata(live_report_id)
                    filtered_rows = results_metadata["stats"]["filtered_rows"]
                    total_rows = results_metadata["stats"]["total_rows"]
                    assert (filtered_rows == total_rows - 1)

                self.wait_until_condition(rows_are_filtered)

    def timed_remove_filter(self, action_name, live_report_id, addable_column_id):
        with self.timed(action_name):
            results_metadata_initial = self.timed_get_results_metadata(live_report_id)
            filtered_rows_initial = results_metadata_initial["stats"]["filtered_rows"]
            with self.timed(action_name + " - Request"):
                self.locust_ld_client.remove_column_filter(live_report_id, addable_column_id)
            with self.timed(action_name + " - Wait"):

                def rows_are_not_filtered():
                    results_metadata = self.timed_get_results_metadata(live_report_id)
                    filtered_rows = results_metadata["stats"]["filtered_rows"]
                    assert (filtered_rows < filtered_rows_initial)

                self.wait_until_condition(rows_are_not_filtered)

    def timed_add_scaffold(self, action_name, has_parent=True):
        with self.timed(action_name, has_parent):
            with self.timed("Request Create Scaffold"):
                scaffold = self.locust_ld_client.create_scaffold(
                    Scaffold(structure=dbprofile.get().basic.scaffold, project_ids=[dbprofile.get().common.project_id]))
                scaffold_id = scaffold.id
            with self.timed("Request Get LiveReport"):
                lr = self.locust_ld_client.live_report(self.live_report_id)

            new_scaffold_name = dbprofile.get().basic.new_scaffold_name

            with self.timed("User Add Scaffold to LiveReport - Request"):
                lr.scaffolds = [{"id": scaffold_id, "name": new_scaffold_name}]
                self.locust_ld_client.update_live_report(self.live_report_id, lr)

            with self.timed("User Add Scaffold to LiveReport - Wait"):
                with self.timed("User Add Scaffold to LiveReport - Wait for Columns"):
                    scaffold_name_column_id = dbprofile.get().basic.scaffold_name_column

                    def scaffold_name_column_descriptor_added():
                        return self.find_column_descriptor_by_column_id(self.live_report_id, scaffold_name_column_id)

                    self.wait_until_condition(scaffold_name_column_descriptor_added)

                    def scaffold_name_column_appeared():
                        results_metadata = self.timed_get_results_metadata(self.live_report_id)
                        assert (scaffold_name_column_id in results_metadata["columns"])

                    self.wait_until_condition(scaffold_name_column_appeared)

                with self.timed("User Add Scaffold to LiveReport - Wait for Results"):

                    def scaffold_analysis_computed():
                        results = self.get_live_report_results(live_report_id=self.live_report_id,
                                                               projections=[scaffold_name_column_id])

                        # We wait until:
                        #   1) there is no "incomplete" statuses and
                        #   2) at least one row matches the newly added scaffold
                        number_of_matched_scaffolds = 0
                        for row_key in results:
                            cell = results[row_key][scaffold_name_column_id]
                            if "statuses" in cell:
                                assert (cell['statuses'][0]['code'] != 'incomplete')
                            if "values" in cell:
                                if cell["values"][0] == new_scaffold_name:
                                    number_of_matched_scaffolds += 1
                        assert (number_of_matched_scaffolds > 0)

                    self.wait_until_condition(scaffold_analysis_computed,
                                              interval=2 * dbprofile.get().common.default_wait_interval,
                                              retries=2 * dbprofile.get().common.default_retries)

    def timed_wait_until_cells_contain_values(self, action_name, column_ids, minimum_number_of_cells_with_values,
                                              **kwargs):
        """
            Waits until a subset of the LiveReport (given by a list of column_ids):
            1) has no cells with "incomplete" statuses and
            2) the number of cells that contain values is equal or exceeds the provided threshold
            (minimum_number_of_cells_with_values)
        """
        with self.timed(action_name):

            def condition():
                results = self.get_live_report_results(self.live_report_id, projections=column_ids)

                number_of_cells_with_values = 0
                for row_key in results:
                    for column_id in column_ids:
                        cell = results[row_key][column_id]
                        if "statuses" in cell:
                            assert (cell['statuses'][0]['code'] != 'incomplete'), "Cell with incomplete status found"
                        if "values" in cell:
                            non_empty_values = [
                                v for v in cell['values'] if (v is not None) and (v != '') and (v != [])
                            ]
                            if len(non_empty_values) > 0:
                                number_of_cells_with_values += 1
                assert(number_of_cells_with_values >= minimum_number_of_cells_with_values),\
                    "Found {} cells with values, which is less than {}".format(
                        number_of_cells_with_values,
                        minimum_number_of_cells_with_values
                    )

            self.wait_until_condition(condition, **kwargs)

    def timed_change_report_level(self, action_name, live_report_id, new_level, has_parent=True):
        with self.timed(action_name, has_parent):
            with self.timed("Request Get LiveReport", has_parent):
                lr = self.locust_ld_client.live_report(live_report_id)
            lr.report_level = new_level
            with self.timed(action_name + " - Request", has_parent):
                self.locust_ld_client.update_live_report(live_report_id, lr)

    def timed_switch_aggregation_mode(self, action_name, report_level="PARENT_BATCH", has_parent=True):
        with self.timed(action_name, has_parent):
            # Before changing aggregation mode:
            original_number_display_id_eq_entity_id = 0
            with self.timed("User Get LiveReport Results"):
                results_metadata = self.timed_get_results_metadata(self.live_report_id)
                row_infos = results_metadata["row_infos"]
                for row_info in row_infos:
                    if row_info["display_id"] == row_info["entity_id"]:
                        original_number_display_id_eq_entity_id += 1

            # Change it
            self.timed_change_report_level("Switch Aggregation Mode", self.live_report_id, report_level)

            # After changing aggregation mode:
            # We determine that the aggregation mode changed by counting the number of rows in which
            # their display_id != entity_id.
            with self.timed("Switch Aggregation Mode - Wait"):

                def mode_changed():
                    results_metadata = self.timed_get_results_metadata(self.live_report_id)
                    row_infos = results_metadata["row_infos"]
                    new_report_level = results_metadata["report_level"]
                    new_number_display_id_eq_entity_id = 0
                    for row_info in row_infos:
                        if row_info["display_id"] == row_info["entity_id"]:
                            new_number_display_id_eq_entity_id += 1
                    assert ((new_report_level.lower() == report_level.lower()) and
                            (original_number_display_id_eq_entity_id != new_number_display_id_eq_entity_id))

                self.wait_until_condition(mode_changed)

    def timed_sketch_compound(self, action_name, has_parent=True):
        with self.timed(action_name, has_parent):
            with self.timed("Sketch Compound - Request"):
                sketched_entity_id = self.locust_ld_client.create_compound(dbprofile.get().basic.compound_structure,
                                                                           "0", "demo")

            with self.timed("Request Add Row"):
                api.actions.row.add_rows_to_live_report(self.locust_ld_client, self.live_report_id,
                                                        [sketched_entity_id])

    def helper_row_order_changed(self, row_infos_1, row_infos_2):

        def row_keys(row_infos):
            return [row_info["row_key"] for row_info in row_infos]

        return row_keys(row_infos_1) != row_keys(row_infos_2)

    def helper_do_sorting(self, lr, column_id, ascending):
        with self.timed("User Execute LiveReport"):
            initial_results = self.locust_ld_client.execute_live_report(self.live_report_id)
            initial_row_infos = initial_results["row_infos"]

        lr.sorted_columns = [{
            "addable_column_id": column_id,
            "ascending": ascending,
        }]

        sort_order = "Ascending" if ascending else "Descending"

        with self.timed("Request Sort {}".format(sort_order)):
            self.locust_ld_client.update_live_report(self.live_report_id, lr)

        with self.timed("ZZ Wait Sort {}".format(sort_order)):

            def rows_order_changed():
                with self.timed("User Execute LiveReport"):
                    final_results = self.locust_ld_client.execute_live_report(self.live_report_id)
                    final_row_infos = final_results["row_infos"]
                assert self.helper_row_order_changed(initial_row_infos, final_row_infos)

            self.wait_until_condition(rows_order_changed)

    def timed_sort_columns(self, action_name, has_parent=True):
        with self.timed(action_name, has_parent):
            column_id = dbprofile.get().basic.column_id_for_subtask_sort

            with self.timed("Request Get LiveReport"):
                lr = self.locust_ld_client.live_report(self.live_report_id)

            self.helper_do_sorting(lr, column_id, True)
            self.helper_do_sorting(lr, column_id, False)

    def timed_reorder_columns(self, action_name, has_parent=True):
        with self.timed(action_name, has_parent):
            with self.timed("Request Get Column Groups"):
                column_groups = self.locust_ld_client.get_column_groups_by_live_report_id(self.live_report_id)
            # Move "Compound Structure" and "ID" columns to the end of the list and then reverse the list:
            first = column_groups[0]
            second = column_groups[1]
            del column_groups[1]
            del column_groups[0]
            column_groups.append(second)
            column_groups.append(first)
            column_groups.reverse()
            with self.timed("Request Reorder Columns (WE DONT WAIT)"):
                self.locust_ld_client.update_column_groups(self.live_report_id, column_groups)

            expected_column_groups = column_groups

            with self.timed("ZZ Verify Column Reordered"):
                actual_column_groups = self.locust_ld_client.get_column_groups_by_live_report_id(self.live_report_id)
                assert (len(expected_column_groups) == len(actual_column_groups)), \
                    "Unexpected number of columns after reordering. Expected: {}. Found: {}.".format(
                        len(expected_column_groups), len(actual_column_groups)
                    )
                for expected, actual in zip(expected_column_groups, actual_column_groups):
                    assert (expected.columns_order == actual.columns_order), \
                        "Unexpected order of columns after reordering. Expected {}. Found: {}.".format(
                            repr(expected), repr(actual)
                        )

    def timed_retrieve_all_rows(self, action_name="User Retrieve All Rows", has_parent=True):
        with self.timed(action_name, has_parent):
            return self.locust_ld_client.live_report_rows(self.live_report_id)

    def timed_add_and_remove_filters(self, action_name, has_parent=True):
        with self.timed(action_name, has_parent):
            filter_column_id = dbprofile.get().basic.column_id_for_subtask_filter
            entity_ids = self.timed_retrieve_all_rows()

            with self.timed("Loop to Filter") as loop_action:
                total_iterations = 20
                failed_iterations = 0
                for _ in range(total_iterations):
                    try:
                        with self.timed("User Filter On All IDs"):
                            entity_id = self.timed_get_random_row("Request Pick Random Row",
                                                                  self.live_report_id)["entity_id"]
                            self.timed_add_text_filter("User Add Filter", self.live_report_id, filter_column_id,
                                                       entity_id)
                            self.timed_verify_number_of_filtered_rows("ZZ Verify Compounds Filtered",
                                                                      self.live_report_id,
                                                                      len(entity_ids) - 1)
                            self.timed_remove_filter("User Remove Filter", self.live_report_id, filter_column_id)
                            self.timed_verify_number_of_filtered_rows("ZZ Verify Compounds Unfiltered",
                                                                      self.live_report_id, 0)
                    except PropagateError:
                        # Stay in the loop, don't bubble up the error, but keep count
                        failed_iterations += 1
                    finally:
                        self.user.wait()

                assert (failed_iterations <= 0), \
                    "Failed {}/{} iterations of the loop".format(failed_iterations, total_iterations)

    def timed_remove_and_add_rows(self, action_name, has_parent=True):
        with self.timed(action_name, has_parent):
            entity_ids = self.timed_retrieve_all_rows()

            with self.timed("Loop to Remove and Add Row"):
                sorted_entity_ids = sorted(entity_ids)
                total_iterations = 10
                failed_iterations = 0
                for i in range(total_iterations):
                    index = i * 3
                    entity_id = sorted_entity_ids[index]
                    try:
                        with self.timed("User Remove and Add Row"):
                            with self.timed("User Remove Row"):
                                api.actions.row.remove_rows_from_live_report(self.locust_ld_client, self.live_report_id,
                                                                             [entity_id])
                            with self.timed("User Add Row"):
                                api.actions.row.add_rows_to_live_report(self.locust_ld_client, self.live_report_id,
                                                                        [entity_id])

                    except PropagateError:
                        failed_iterations += 1
                    finally:
                        self.user.wait()

                assert (failed_iterations <= 0), \
                    "Failed {}/{} iterations of the loop".format(failed_iterations, total_iterations)

    def timed_get_column_descriptors(self, action_name="Request Column Descriptors", has_parent=True):
        with self.timed(action_name, has_parent):
            return self.locust_ld_client.column_descriptors(self.live_report_id)

    def helper_generate_new_unique_column_name(self):
        live_report_column_descriptors = self.timed_get_column_descriptors()
        live_report_column_names = [
            column_descriptor.display_name for column_descriptor in live_report_column_descriptors
        ]

        while True:
            column_name = "Load test FFC {}".format(uuid.uuid4())
            if column_name not in live_report_column_names:
                return column_name

    def timed_get_freeform_columns(self, action_name, has_parent):
        with self.timed(action_name, has_parent):
            return self.locust_ld_client.freeform_columns(project_id=dbprofile.get().common.project_id)

    def timed_add_freeform_column(self, action_name, has_parent=False):
        with self.timed(action_name, has_parent):
            freeform_column = ldclient.client.FreeformColumn(self.helper_generate_new_unique_column_name(),
                                                             "For the load test",
                                                             type=ldclient.client.FreeformColumn.COLUMN_NUMBER,
                                                             live_report_id=self.live_report_id)
            freeform_column = self.locust_ld_client.create_freeform_column(freeform_column.as_dict())
            api.actions.column.add_columns_to_live_report(self.locust_ld_client, self.live_report_id,
                                                          [freeform_column.id])
            self.timed_wait_until_cells_contain_values(action_name + " - Get Column Results", [freeform_column.id], 0)
            return freeform_column.id

    def timed_edit_freeform_column_cell(self,
                                        action_name,
                                        entity_id,
                                        ffc_value,
                                        freeform_column_id,
                                        wait_for_any_change=False):
        with self.timed(action_name) as add_ffc_value_action:
            if wait_for_any_change:
                with self.timed(add_ffc_value_action + " - Get old values"):
                    cell = self.get_cells(self.live_report_id, freeform_column_id, [entity_id])
                    row_key_to_old_values = {entity_id: cell[entity_id].get('values', [])}
            with self.timed(add_ffc_value_action + " - Request"):
                observation = ldclient.client.Observation(
                    project_id=dbprofile.get().common.project_id,
                    entity_id=entity_id,
                    addable_column_id=freeform_column_id,
                    value=str(ffc_value),
                    live_report_id=self.live_report_id,
                )
                # NOTE(nikolaev): This method is using sync /observation/batch/ endpoint
                self.locust_ld_client.add_freeform_column_values([observation.as_dict()])

            with self.timed(add_ffc_value_action + " - Wait"):
                if wait_for_any_change:
                    self.wait_for_cell_values_change(self.live_report_id, freeform_column_id, row_key_to_old_values,
                                                     {entity_id: str(ffc_value)})
                else:
                    self.wait_for_cell_values(self.live_report_id, freeform_column_id, {entity_id: str(ffc_value)})

    def timed_create_and_edit_ffc(self, action_name, has_parent=True):
        with self.timed(action_name, has_parent):
            freeform_column_id = self.timed_add_freeform_column("User Create FFC")
            self.user.wait()

            entity_ids = self.timed_retrieve_all_rows()
            sorted_entity_ids = sorted(entity_ids)
            entered_ffc_values = {}

            with self.timed("Loop to Edit FFC"):
                total_iterations = 10
                failed_iterations = 0
                for i in range(total_iterations):
                    index = i * 5
                    entity_id = sorted_entity_ids[index]
                    ffc_value = i
                    try:
                        self.timed_edit_freeform_column_cell("User Edit FFC Cell", entity_id, ffc_value,
                                                             freeform_column_id)
                        # Cell value was successfully updated, save the entity_id
                        entered_ffc_values[entity_id] = ffc_value
                    except PropagateError:
                        failed_iterations += 1
                    finally:
                        self.user.wait()

                assert (failed_iterations <= 0), \
                    "Failed {}/{} iterations of the loop".format(failed_iterations, total_iterations)
        return (freeform_column_id, entered_ffc_values)

    def timed_add_model(self, action_name, freeform_column_id, entered_ffc_values):
        with self.timed(action_name) as add_model_action:
            with self.timed("Request Create Attachment"):
                attachment_metadata = self.locust_ld_client.get_or_create_attachment(
                    "resources/add_three_skip_script.py",
                    "ATTACHMENT", [dbprofile.get().common.project_id],
                    remote_file_name="add_three_skip_script.py")
                attachment_id = attachment_metadata["id"]

            with self.timed("Request Create Protocol"):
                # Create the protocol
                command = ldclient.models.ModelCommand(
                    command='$SCHRODINGER/run ${script:FILE-INPUT} --input ${SDF-FILE} --col ${column:COLUMN-INPUT}',
                    driver_id=1)
                protocol = ldclient.models.Model(name='Locust load test: A protocol to run add three model',
                                                 commands=[command],
                                                 description='Used for Locust load test',
                                                 archived=False,
                                                 published=False,
                                                 folder="Computational Models/User Defined/",
                                                 user=dbprofile.get().common.username,
                                                 project_ids=[dbprofile.get().common.project_id],
                                                 template_vars=[
                                                     ldclient.models.ModelTemplateVar("ABSTRACT", "FILE", "script"),
                                                     ldclient.models.ModelTemplateVar(
                                                         "ABSTRACT", "SDF_FILE", "SDF-FILE"),
                                                     ldclient.models.ModelTemplateVar("ABSTRACT", "COLUMN", "column"),
                                                 ],
                                                 returns=[
                                                     ldclient.models.ModelReturn("Result",
                                                                                 "REAL",
                                                                                 "",
                                                                                 "Result",
                                                                                 tag='DEFAULT',
                                                                                 precision=1,
                                                                                 addable_column_id=None,
                                                                                 id=None)
                                                 ],
                                                 batch_size=ldclient.models.ModelRecursive(tag='DEFAULT', value=100),
                                                 command_type=ldclient.models.ModelRecursive(tag='READ_ONLY',
                                                                                             value='NORMAL'),
                                                 command_queue=ldclient.models.ModelRecursive(tag='READ_ONLY',
                                                                                              value='sync'))

                created_protocol = self.locust_ld_client.create_protocol(protocol)

            with self.timed("Request Create Model"):
                model = ldclient.models.Model(name='Locust load test: Add three model',
                                              commands=[],
                                              parent=created_protocol.id,
                                              description='Adds three to an input column',
                                              archived=False,
                                              published=False,
                                              folder="Computational Models/User Defined/",
                                              user=dbprofile.get().common.username,
                                              project_ids=[dbprofile.get().common.project_id],
                                              template_vars=[
                                                  ldclient.models.ModelTemplateVar("READ_ONLY",
                                                                                   "FILE",
                                                                                   "script",
                                                                                   data=attachment_id),
                                                  ldclient.models.ModelTemplateVar("PASS", "SDF_FILE", "SDF-FILE"),
                                                  ldclient.models.ModelTemplateVar("READ_ONLY",
                                                                                   "COLUMN",
                                                                                   "column",
                                                                                   data=freeform_column_id),
                                              ],
                                              returns=[
                                                  ldclient.models.ModelReturn("Result",
                                                                              "REAL",
                                                                              "",
                                                                              "Result",
                                                                              tag='DEFAULT',
                                                                              precision=1,
                                                                              addable_column_id=None,
                                                                              id=None)
                                              ],
                                              batch_size=ldclient.models.ModelRecursive(tag='READ_ONLY', value=100),
                                              command_type=ldclient.models.ModelRecursive(tag='READ_ONLY',
                                                                                          value='NORMAL'),
                                              command_queue=ldclient.models.ModelRecursive(tag='READ_ONLY',
                                                                                           value='sync'))

                created_model = self.locust_ld_client.create_model(model)

                model_column_id = created_model.returns[0].addable_column_id

            with self.timed("User Add Model to LR - Request and Wait"):
                api.actions.column.add_columns_to_live_report(self.locust_ld_client, self.live_report_id,
                                                              [model_column_id])

            try:
                with self.timed("Wait on Model Calculate"):
                    expected_values = {}
                    for entity_id, value in entered_ffc_values.items():
                        expected_values[entity_id] = str(float(value + 3))
                    self.wait_for_cell_values(self.live_report_id,
                                              model_column_id,
                                              expected_values,
                                              accept_statuses=["failed"],
                                              interval=2 * dbprofile.get().common.default_wait_interval,
                                              retries=4 * dbprofile.get().common.default_retries)
            except PropagateError:
                pass

            return (created_model, created_protocol)

    def timed_model(self, action_name, freeform_column_id, entered_ffc_values, has_parent=True):
        with self.timed(action_name, has_parent):
            created_model, created_protocol = self.timed_add_model("User Add Dependent Model", freeform_column_id,
                                                                   entered_ffc_values)
            self.user.wait()

            model_column_id = created_model.returns[0].addable_column_id

            entity_ids = self.timed_retrieve_all_rows()
            sorted_entity_ids = sorted(entity_ids)

            with self.timed("Loop to Edit FFC to Trigger Model Events"):
                total_iterations = 10
                failed_iterations = 0
                for i in range(total_iterations):
                    index = i * 2
                    entity_id = sorted_entity_ids[index]
                    ffc_value = 1000 + i
                    try:
                        self.timed_edit_freeform_column_cell("User Edit FFC Cell to Trigger Model Events", entity_id,
                                                             ffc_value, freeform_column_id)
                        with self.timed("User Edit FFC Cell To Trigger Model Events cell value check"):
                            expected_values = {entity_id: str(float(ffc_value + 3))}
                            self.wait_for_cell_values(self.live_report_id,
                                                      model_column_id,
                                                      expected_values,
                                                      accept_statuses=[],
                                                      interval=2 * dbprofile.get().common.default_wait_interval)

                    except PropagateError:
                        failed_iterations += 1
                    finally:
                        self.user.wait()

                assert (failed_iterations <= 0), \
                    "Failed {}/{} iterations of the loop".format(failed_iterations, total_iterations)

            with self.timed("User Remove Model from LR"):
                api.actions.column.remove_columns_from_live_report(self.locust_ld_client, self.live_report_id,
                                                                   [model_column_id])

            self.timed_model_cleanup("User Archive Model and Protocol", created_model, created_protocol)

    def timed_model_cleanup(self, action_name, created_model, created_protocol, has_parent=True):
        with self.timed(action_name, has_parent):
            if (created_model is not None) and (created_model.id is not None):
                created_model.archived = True
                with self.timed("Request Archive Model"):
                    self.locust_ld_client.update_model(created_model.id, created_model)

            if (created_protocol is not None) and (created_protocol.id is not None):
                created_protocol.archived = True
                with self.timed("Request Archive Protocol"):
                    self.locust_ld_client.update_protocol(created_protocol.id, created_protocol)

    def timed_advanced_search(self, action_name, query_name, has_parent, query_condition, expected_number):
        with self.timed(action_name, has_parent) as root_action:
            with self.timed("ZZ Request Get Query"):
                query = self.locust_ld_client.get_advanced_search_query(self.live_report_id)
                pprint.pprint(query.as_dict())
            self.user.wait()

            with self.timed("Update {} Query".format(query_name)):
                pprint.pprint(query_condition.as_dict())
                query.conditions = [query_condition]
                query.expression = "1"
                self.locust_ld_client.update_advanced_search_query(self.live_report_id, query)
            self.user.wait()

            with self.timed("Run {} Query".format(query_name)):
                result = self.locust_ld_client.execute_advanced_search_query(self.live_report_id)
                actual_number = len(result)
                min_expected = expected_number * 0.9
                max_expected = expected_number * 1.1
                is_in_range = min_expected <= actual_number <= max_expected
                assert (is_in_range), ("Unexpected number of compounds. Actual: {}, Expected range: [{},{}]".format(
                    actual_number, min_expected, max_expected))
            self.user.wait()

    def timed_advanced_search_numeric_range(self, action_name, has_parent):
        numeric_column = dbprofile.get().basic_adv_search.numeric_range_column
        value_lo = dbprofile.get().basic_adv_search.numeric_range_value_low
        value_hi = dbprofile.get().basic_adv_search.numeric_range_value_high
        self.timed_advanced_search(
            action_name, "Numeric Range Value", has_parent,
            QueryRangedObservationCondition(str(numeric_column), value=(value_lo, value_hi), id="1"),
            dbprofile.get().basic_adv_search.expected_numeric_range_result)

    def timed_advanced_search_numeric_defined(self, action_name, has_parent):
        numeric_column = dbprofile.get().basic_adv_search.numeric_defined_column
        self.timed_advanced_search(action_name, "Numeric Defined Value", has_parent,
                                   QueryObservationCondition(str(numeric_column), value=["(defined)"], id="1"),
                                   dbprofile.get().basic_adv_search.expected_numeric_defined_result)

    def timed_advanced_search_text_exact(self, action_name, has_parent):
        text_column = dbprofile.get().basic_adv_search.text_exact_column
        exact_value = dbprofile.get().basic_adv_search.text_exact_value
        self.timed_advanced_search(action_name, "Text Exact Value", has_parent,
                                   QueryObservationCondition(str(text_column), value=[exact_value], id="1"),
                                   dbprofile.get().basic_adv_search.expected_text_exact_result)

    def timed_advanced_search_text_defined(self, action_name, has_parent):
        text_column = dbprofile.get().basic_adv_search.text_defined_column
        self.timed_advanced_search(action_name, "Text Defined Value", has_parent,
                                   QueryObservationCondition(str(text_column), value=["(defined)"], id="1"),
                                   dbprofile.get().basic_adv_search.expected_text_defined_result)

    def timed_list_live_reports_and_projects(self, action_name, has_parent):
        with self.timed(action_name, has_parent):
            with self.timed("Request Post Project Search"):
                self.locust_ld_client.live_reports([dbprofile.get().common.project_id])

            with self.timed("Request Get All Projects"):
                self.locust_ld_client.projects()

    def timed_add_compounds_via_import_csv(self, action_name, has_parent=True):
        with self.timed(action_name, has_parent):
            filename = dbprofile.get().advanced.filename_csv_import
            file_content = (filename, open(filename, 'rb'), '')
            task_id = self.locust_ld_client.load_csv_async(self.live_report_id, filename, file_content)

            assert (task_id is not None), "Async task is not created"

            with self.timed(action_name + " - Wait Async Task"):
                self.wait_for_async_task(task_id,
                                         interval=4 * dbprofile.get().common.default_wait_interval,
                                         retries=6 * dbprofile.get().common.default_retries)

    def timed_wait_for_new_rows(self, action_name, **kwargs):
        with self.timed(action_name):
            initial_rows_count = self.timed_get_results_metadata(self.live_report_id)["stats"]["total_rows"]

            def condition():
                updated_rows_count = self.timed_get_results_metadata(self.live_report_id)["stats"]["total_rows"]
                assert (updated_rows_count > initial_rows_count), "Row count has not changed"

            self.wait_until_condition(condition, **kwargs)

    def timed_add_compounds_via_substructure_search(self, action_name, has_parent=True):
        with self.timed(action_name, has_parent):
            with self.timed("User Add Compounds via Substructure Search - Request Search"):
                corporate_ids = self.locust_ld_client.compound_search(
                    dbprofile.get().advanced.molecule_for_substructure_search,
                    search_type='SUBSTRUCTURE',
                    max_results=20,
                    search_threshold=0.7,
                    project_id=dbprofile.get().common.project_id,
                )
            with self.timed("User Add Compounds via Substructure Search - Request To Add"):
                self.locust_ld_client.add_rows(self.live_report_id, corporate_ids)

            self.timed_wait_for_new_rows("User Add Compounds via Substructure Search - Wait",
                                         interval=2 * dbprofile.get().common.default_wait_interval,
                                         retries=2 * dbprofile.get().common.default_retries)

    def timed_add_compounds_via_similarity_search(self, action_name, has_parent=True):
        with self.timed(action_name, has_parent):
            with self.timed("User Add Compounds via Similarity Search - Request Search"):
                corporate_ids = self.locust_ld_client.compound_search(
                    dbprofile.get().advanced.molecule_for_similarity_search,
                    search_type='SIMILARITY',
                    max_results=20,
                    search_threshold=0.5,
                    project_id=dbprofile.get().common.project_id,
                )
            with self.timed("User Add Compounds via Similarity Search - Request To Add"):
                self.locust_ld_client.add_rows(self.live_report_id, corporate_ids)

            self.timed_wait_for_new_rows("User Add Compounds via Similarity Search - Wait",
                                         interval=2 * dbprofile.get().common.default_wait_interval,
                                         retries=2 * dbprofile.get().common.default_retries)

    def timed_copy_livereport(self, action_name, has_parent):
        with self.timed(action_name, has_parent):
            self.locust_ld_client.copy_live_report(self.live_report_id)

    def timed_create_plot(self, action_name, has_parent):
        plot = {
            "live_report_id": str(self.live_report_id),
            "name": "Scatter",
            "plot_mode": "scatter",
            "plot_type": "viz",
            "scatter_details": {
                "axis_range": {},
                "x_axis_column_id": None,
                "y_axis_column_id": None,
                "color_by_axis_column_id": None,
                "size_by_axis_column_id": None,
                "shape_by_axis_column_id": None,
                "shape_by_type": "value",
                "size_by_type": "UNIFORM"
            },
            "gadget_type": "plot"
        }

        with self.timed(action_name, has_parent):
            with self.timed("Request Create Scatter Plot"):
                plot = Plot(live_report_id=str(self.live_report_id),
                            plot_mode="scatter",
                            plot_type="viz",
                            name="Scatter",
                            scatter_details=ScatterPlot())

                plot = self.locust_ld_client.create_plot(plot)

            with self.timed("Request Plot Choose X-Axis Column"):
                plot.scatter_details.x_axis_column_id = "1274"
                plot = self.locust_ld_client.update_plot(plot)

            with self.timed("Request Plot Choose Y-Axis Column"):
                plot.scatter_details.y_axis_column_id = "1274"
                plot = self.locust_ld_client.update_plot(plot)

            with self.timed("Request Plot Choose Color By Column"):
                plot.scatter_details.color_by_axis_column_id = "1274"
                plot = self.locust_ld_client.update_plot(plot)

            with self.timed("Request Plot Choose Size By Column"):
                plot.scatter_details.size_by_axis_column_id = "1274"
                plot.scatter_details.size_by_type = "COLUMN"
                plot = self.locust_ld_client.update_plot(plot)

    def timed_list_live_reports_metadata(self, action_name, has_parent):
        with self.timed(action_name, has_parent):
            live_reports_metadata = self.locust_ld_client.live_reports_metadata([dbprofile.get().common.project_id])
        return live_reports_metadata

    def timed_import_3D_data(self, action_name, has_parent=True):
        entity_ids = sorted(self.locust_ld_client.live_report_rows(self.live_report_id))[0:10]

        minimal_sdf_molecule_template = ('Locust-molecule-{index}-for-{compound_id}\n'
                                         '  Mrv0541 02101517582D\n'
                                         '\n'
                                         '  0  0  0  0  0  0            999 V2000\n'
                                         'M  END\n'
                                         '\n'
                                         '> <s_ld_export_compound_id>\n'
                                         '{index}\n'
                                         '\n'
                                         '> <Corporate_id>\n'
                                         '{compound_id}\n'
                                         '\n'
                                         '$$$$\n')

        mapping_line_template = "{index}\tUNUSED\t{column_name}\t{ligand_file}\t{target_file}\n"

        # Create Mapping file
        mapping_file = tempfile.NamedTemporaryFile(mode="w+t", prefix="locust", suffix=".tsv", delete=False)
        mapping_file.write(
            "s_ld_export_compound_id	entity_id\tmodel_name\tligand_zip_file_path\ttarget_zip_file_path\n")
        column_name = dbprofile.get().advanced.three_d_column_name
        for index in range(len(entity_ids)):
            mapping_file.write(
                mapping_line_template.format(index=index,
                                             column_name=column_name,
                                             ligand_file="ligand.mae",
                                             target_file=""))
        mapping_file.close()

        # Create SDF file
        sdf_file = tempfile.NamedTemporaryFile(mode="w+t", prefix='locust', suffix=".sdf", delete=False)
        for index in range(len(entity_ids)):
            entity_id = entity_ids[index]
            sdf_file.write(minimal_sdf_molecule_template.format(index=index, compound_id=entity_id))
        sdf_file.close()

        print("Mapping file:", mapping_file.name)
        print("SDF file:", sdf_file.name)

        # Import 3D data
        with self.timed(action_name, has_parent):
            task_id = self.locust_ld_client.load_assay_and_pose_data(
                sdf_file_name=sdf_file.name,
                sdf_file_sha1=None,
                mapping_file_name=mapping_file.name,
                mapping_file_sha1=None,
                three_d_file_name=dbprofile.get().advanced.filename_3d_import,
                three_d_file_sha1=None,
                project='Global',
                live_report_name=None,
                corporate_id_column='Corporate_id',
                published=True,
                properties=[],
                export_type='MAESTRO_SDF',
                live_report_id=str(self.live_report_id))
            url = self.locust_ld_client.wait_and_get_result_url(task_id)
            task_response_dict = self.locust_ld_client.get_task_result(url)
            pprint.pprint(task_response_dict)

        os.remove(mapping_file.name)
        os.remove(sdf_file.name)

    def timed_remove_all_rows(self, action_name, has_parent=True):
        with self.timed(action_name, has_parent):
            entity_ids = self.timed_retrieve_all_rows()
            api.actions.row.remove_rows_from_live_report(self.locust_ld_client, self.live_report_id, entity_ids)
