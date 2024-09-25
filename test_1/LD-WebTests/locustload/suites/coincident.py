import locust

import random

from locustload import dbprofile
from locustload.util import ldlocust
from locustload.suites.abstract_taskset import AbstractTaskSet
from locustload.util.timed import PropagateError


@locust.task
class CoincidentTaskSet(AbstractTaskSet):

    wait_time = locust.constant(4)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.live_report_id = None
        self.freeform_column_ids = []

    @locust.task
    def task1_set_coincident_lr_id_by_title(self):
        self.live_report_id = self.find_live_report_ids_by_title(
            "Get Coincident LiveReport ID By Title",
            dbprofile.get().coincident.coincident_live_report_title)[0]
        assert self.live_report_id != None, "Coincident Live Id should not be none. Run Warmup User First"

    @locust.task
    def task2_get_coincident_ffc(self):
        with self.timed("Get Coincident FFCs", False):
            # Note(mushtaqu):- Run warmup user first. All four ffcs will be created in warmup user, If any of the ffcs not present then it means error
            freeform_columns = self.timed_get_freeform_columns("Get all Freeform Columns", True)
            for coincident_ffc in dbprofile.get().coincident.coincident_freeform_columns_name:
                self.freeform_column_ids.append([
                    freeform_column.id
                    for freeform_column in freeform_columns
                    if freeform_column.name == coincident_ffc and freeform_column.live_report_id == self.live_report_id
                ][0])

    def timed_edit_freeform_column_cell_wrapper(self, action_name, has_parent, freeform_column_id):
        with self.timed(action_name, has_parent):
            entity_ids = self.timed_retrieve_all_rows()
            sorted_entity_ids = sorted(entity_ids)
            entered_ffc_values = {}

            with self.timed("Loop to Edit Coincident FFC", True):
                total_iterations = 10
                failed_iterations = 0
                for i in range(total_iterations):
                    # Alternating between random and deterministic rows to edit FFC's value. It will make some edits with expected collision and some edits with no collision.
                    # Index of rows to be edited ----> [0, rnd, 5, rnd, 10, rnd, ...]
                    index = i * 5
                    if i & 1:
                        # picking random row to edit ffc value
                        index = random.randrange(len(sorted_entity_ids))
                    entity_id = sorted_entity_ids[index]
                    ffc_value = random.randint(0, 1000000)
                    try:
                        self.timed_edit_freeform_column_cell("User Edit FFC Cell", entity_id, ffc_value,
                                                             freeform_column_id, True)
                        # Cell value was successfully updated, save the entity_id
                        entered_ffc_values[entity_id] = ffc_value
                    except PropagateError:
                        failed_iterations += 1
                    finally:
                        self.user.wait()

                assert (failed_iterations <= 0), \
                    "Failed {}/{} iterations of the loop".format(failed_iterations, total_iterations)

    @locust.task
    def task3_edit_ffc(self):
        with self.timed("User Edit All Coincident FFCs", False):
            for ffc_id in self.freeform_column_ids:
                self.entered_ffc_values = self.timed_edit_freeform_column_cell_wrapper(
                    "User Edit Coincident FFC", True, ffc_id)

    @locust.task
    def task_finalize(self):
        # Stop Locust user at the end
        ldlocust.stop_user()
