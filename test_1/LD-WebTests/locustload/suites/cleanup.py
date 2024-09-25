import locust

from locustload import dbprofile
from locustload.util import ldlocust
from locustload.suites.abstract_taskset import AbstractTaskSet


@locust.task
class CleanupTaskSet(AbstractTaskSet):

    wait_time = locust.constant(4)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @locust.task
    def task1_delete_coincident_lr_id_by_title(self):
        coincident_live_report_ids = self.find_live_report_ids_by_title(
            "Get Coincident LiveReport ID By Title",
            dbprofile.get().coincident.coincident_live_report_title)
        for coincident_live_report_id in coincident_live_report_ids:
            self.locust_ld_client.delete_live_report(coincident_live_report_id)

    @locust.task
    def task_finalize(self):
        # Stop Locust user at the end
        ldlocust.stop_user()
