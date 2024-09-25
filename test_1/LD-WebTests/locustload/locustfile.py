# NOTE(nikolaev): To ensure that commands like time.sleep() are greenlet-(i.e. cooperative thread)-friendly,
# we need to monkey-patch the standard library.
#
# For that, either
#   import locust
# or
#   import gevent.monkey; gevent.monkey.patch_all()
# should be included at the very beginning of the main script.
#
# For more info see:
# 1) http://blog.pythonisito.com/2012/08/gevent-monkey-patch.html
# 2) https://github.com/pglass/how-do-i-locust

import locust

from locustload.util.ldlocust import RawDataLogger

from locustload.default_user import DefaultUser

from locustload.suites.basic import BasicTaskSet
from locustload.suites.basic_advanced_search import BasicAdvancedSearchTaskSet
from locustload.suites.advanced import AdvancedTaskSet
from locustload.suites.coincident import CoincidentTaskSet
from locustload.suites.service_response import ServiceResponseTaskSet
from locustload.suites.execution import ExecutionTaskSet
from locustload.suites.warmup import WarmupTaskSet
from locustload.suites.subtasksets.create_taskset import create_taskset
from locustload.suites.cleanup import CleanupTaskSet

raw_data_logger = RawDataLogger()


class BasicUser(DefaultUser):
    tasks = [BasicTaskSet]


class BasicAdvancedSearchUser(DefaultUser):
    tasks = [BasicAdvancedSearchTaskSet]


class AdvancedUser(DefaultUser):
    tasks = [AdvancedTaskSet]


class ServiceResponseUser(DefaultUser):
    tasks = [ServiceResponseTaskSet]


class ExecutionUser(DefaultUser):
    tasks = [ExecutionTaskSet]


class WarmupUser(DefaultUser):
    tasks = [WarmupTaskSet]


class CoincidentUser(DefaultUser):
    tasks = [CoincidentTaskSet]


class CleanupUser(DefaultUser):
    tasks = [CleanupTaskSet]