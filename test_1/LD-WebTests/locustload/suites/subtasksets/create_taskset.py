import locust
from locust.user.task import TaskSet

from locustload.util import ldlocust
from locustload.suites.abstract_taskset import AbstractTaskSet
from locustload.util.timed import PropagateError


def create_taskset(task_method, repetitions=1):
    """
    Method for creating new tasksets

    :param task_method: function/task to be executed after creation of live report
    :param repetitions: number of times to repeat the task_method
    :return: returns a class that can be used as a taskset
    """

    class GenericTaskSet(AbstractTaskSet):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.live_report_id = None

        @locust.task
        def task1_create(self):
            self.timed_create_live_report("[section] 1 - Create LiveReport", has_parent=False)

        @locust.task
        def task2(self):
            failed_iterations = 0
            with self.timed("Loop") as loop_action:
                for _ in range(repetitions):
                    try:
                        task_method(self)
                    except PropagateError:
                        failed_iterations += 1
                    finally:
                        self.user.wait()

            assert(failed_iterations <= 0), \
                "Failed {}/{} iterations of the loop".format(failed_iterations, repetitions)

        @locust.task
        def task3_cleanup(self):
            with self.timed("[section] 3 - Cleanup", False):
                if self.live_report_id is not None:
                    self.timed_delete_live_report("Delete LiveReport Request", self.live_report_id)

        @locust.task
        def task_finalize(self):
            self.interrupt()

    return GenericTaskSet
