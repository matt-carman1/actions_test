"""
This is a collection of utils that extend Locust's capabilities for use in LiveDesign testing.

Many of these features rely on Locust easter eggs that are not guaranteed to exist in future
versions of Locust!
"""
import contextlib
import csv
import time

import ldclient
from ldclient.__experimental.experimental_client import ExperimentalLDClient
import locust
from locust import exception as locust_exception

from locustload import dbprofile
from locustload.livedesign import paths


class LocustLDClient(ExperimentalLDClient):
    """
    LD Client object that routes HTTP requests through the Locust session.
    """

    class _LocustSessionApiClient(ldclient.client.SessionApiClient):

        def __init__(self, locust_session, host, username=None, password=None, model_encoder=None, verify_ssl=None):
            super(ldclient.client.SessionApiClient, self).__init__()
            self.host = host
            self.setup_verification(verify_ssl, self.host + "/auth" + "/non_existent_endpoint")
            self.model_encoder = model_encoder

            # Login
            self.session = locust_session
            self.token = None
            retries_left = 30
            while retries_left > 0:
                try:
                    self.session_id = self.login(username, password)
                    break
                except Exception as e:
                    print(e)
                    print("Failed to login to LiveDesign. Retrying...")
                    retries_left -= 1
                    time.sleep(30)
            if retries_left == 0:
                exit(1)
            self.refresh_token = None
            self.access_token = None

            self._verify_version()

    def __init__(self, *args, **kwargs):
        # We don't call super here because that will instantiate a second SessionApiClient
        # which will log into LiveDesign.
        self.client = self._LocustSessionApiClient(*args, **kwargs)
        self.ignore_deprecation_failure_for_version = None
        self.disable_string_identifier_conversion = False
        self.compatibility_mode = (8, 10)


class User(locust.HttpUser):
    """
    Locust user adapted for the LiveDesign way of testing.

    This User automatically instantiates a LD Client session. It also results in Locust exiting
    out when the user ends, if this is the last user.
    """

    abstract = True  # So that Locust doesn't run tests with this empty class
    locust_ld_client: LocustLDClient = None
    stop_on_last_user = 1

    def on_start(self):
        self.locust_ld_client = LocustLDClient(
            locust_session=self.client,
            host=self.environment.host + paths.BASE,
            username=dbprofile.get().common.username,
            password=dbprofile.get().common.password,
            model_encoder=ldclient.models.ModelEncoder,
        )
        if hasattr(self.environment.parsed_options, "load_profile"):
            self.stop_on_last_user = self.environment.parsed_options.load_profile == "variable"

    def on_stop(self):
        runner = self.environment.runner
        if runner.user_count <= 1 and self.stop_on_last_user == 1:
            print("This is the last user to stop; quitting")
            self.environment.runner.quit()


class LocustLDClientProviderMixin:
    """
    Mixin for locust.TaskSet and locust.SequentialTaskSet so that tasks can access the user's
    LD Client session using self.locust_ld_client.
    """

    @property
    def locust_ld_client(self) -> LocustLDClient:
        return self.user.locust_ld_client


@contextlib.contextmanager
def time_async_operation(response_generator):
    """
    Context manager that enables timing an asynchronous LiveDesign action.

    This context manager can be used when you access a URL directly using the Locust client (rather
    than LD Client). You pass the request to the context manager with the catch_response argument
    as True. The request's total time will be set to be the time for the original HTTP request
    plus the time for the logic in the context to run.

    Usage:

        with time_async_operation(
            locust_client.get(url, name="Action name", catch_response=True)
        ) as response:
            # Perform other steps in the async operation, like polling to see when the operation
            # completes.
            if not success:
                response.failure("Didn't work!")

    """
    start_time = time.time()
    with response_generator as response:
        yield response
        response.request_meta["response_time"] = (time.time() - start_time) * 1000


class RawDataLogger:
    """
    Class that enables writing all Locust raw data to a CSV file.

    The class listens to Locust events (request and quitting), stores all Locust requests,
    and writes them in a CSV file when Locust process exits. One instance of this logger
    is created in locustfile.py.
    """

    _TIMESTAMP = "timestamp"
    _NAME = "name"
    _HTTP_METHOD = "http_method"
    _RESPONSE_TIME = "response_time"
    _SUCCESS = "success"
    _LOCUST_USER_ID = 'locust_user_id'
    _START = 'start'
    _END = 'end'
    _ALL_FIELDS = [_TIMESTAMP, _NAME, _HTTP_METHOD, _RESPONSE_TIME, _SUCCESS, _LOCUST_USER_ID, _START, _END]

    def __init__(self):
        self._data = []
        # NOTE(fennell): all listener functions have **kwargs captures to aid with forward
        # compatibility with future versions of Locust, which may pass additional arguments
        # to the handler.
        locust.events.request.add_listener(self._request_handler)
        locust.events.quitting.add_listener(self._write)

    def _success_handler(self, **kwargs):
        self._add_data_entry(success=True, **kwargs)

    def _error_handler(self, **kwargs):
        self._add_data_entry(success=False, **kwargs)

    def _request_handler(self, request_type, name, response_time, exception, context, **kwargs):
        success = exception is None
        timed_action_info = context['action'] if 'action' in context else {'locust_user_id': '', 'start': '', 'end': ''}
        locust_user_id = timed_action_info['locust_user_id']
        start = timed_action_info['start']
        end = timed_action_info['end']
        self._add_data_entry(request_type, name, response_time, success, locust_user_id, start, end)

    def _add_data_entry(self, request_type, name, response_time, success, locust_user_id, start, end):
        self._data.append({
            self._TIMESTAMP: time.time(),
            self._NAME: name,
            self._HTTP_METHOD: request_type,
            self._RESPONSE_TIME: response_time,
            self._SUCCESS: success,
            self._LOCUST_USER_ID: locust_user_id,
            self._START: start,
            self._END: end,
        })

    def _write(self, environment, **kwargs):
        if environment.parsed_options.csv_prefix is not None:
            output_file_path = environment.parsed_options.csv_prefix + "_all_data.csv"
            with open(output_file_path, "w") as f:
                csv_writer = csv.DictWriter(f, self._ALL_FIELDS)
                csv_writer.writeheader()
                for data in self._data:
                    csv_writer.writerow(data)


def stop_user():
    """
    Stop the current Locust user.

    This uses the locust.exceptions.StopUser easter egg feature.
    """
    raise locust_exception.StopUser()
