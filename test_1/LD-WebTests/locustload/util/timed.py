import time
import sys

from locust.exception import CatchResponseError
from requests.exceptions import RequestException, HTTPError
from json import JSONDecodeError
from ldclient.exceptions import SchrodingerException


class PropagateError(Exception):
    pass


class UnexpectedError(Exception):
    pass


exception_list = (AssertionError, RequestException, HTTPError, CatchResponseError, JSONDecodeError,
                  SchrodingerException, PropagateError, UnexpectedError, ValueError)

time_at_startup = time.time()  # seconds since epoch, not guaranteed to be monotonic
perf_counter_at_startup = time.perf_counter()  # precise monotonic clock, but its reference point is undefined


class TimedAction:
    """
    A context manager for timing arbitrary user-defined actions. The elapsed time of each action is reported as
    a Locust request of the type "action".

    A usage example:

        with TimedAction(locust_user, "My-Action", False) as my_action:
            with TimedAction(locust_user, my_action + ":Sleep-1", True):
                time.sleep(1)
            with TimedAction(locust_user, my_action + ":Sleep-2", True):
                time.sleep(2)

    This creates three nested timed actions:

    My-Action:                      (expected elapsed time 3s)
        |
        +- My-Action:Sleep-1        (expected elapsed time 1s)
        |
        +-My-Action:Sleep-2         (expected elapsed time 2s)

    The "as"-clause of the manager provides the name of the action (String), which can be useful when naming
    child actions (those that are nested within the parent timed action).

    Exceptions specified in the global variable exception_list (e.g. AssertionError) are caught by the context manager
    and re-raised as a PropagateError exception so the parent action status can be correctly reported as failed
    (to enable this error propagation, the child action should be created with the argument has_parent_action=True,
    which is the default value for this argument).

    Root actions (i.e. that have no parent, has_parent_action=False) don't propagate caught exceptions.

    Note that a Locust TaskSet can define a helper method (TODO: Make a custom TaskSet class that provides this method)

        def timed(self, name, has_parent=True):
            return TimedAction(self.user, name, has_parent)

    which removes redundancy when creating timed actions:

        with self.timed("My-Action", False) as my_action:
            with self.timed(my_action + ":Sleep-1"):
                time.sleep(1)
            with self.timed(my_action + ":Sleep-2"):
                time.sleep(2)
    """

    def __init__(self, locust_user, name, has_parent_action=True):
        self.locust_user = locust_user
        self.name = name
        self.has_parent_action = has_parent_action

    def __enter__(self):
        self.start_perf_counter = time.perf_counter()
        return self.name

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value is not None:
            print("(!) TIMED ACTION", self.name, "IS INTERRUPTED BY", repr(exc_value), file=sys.stderr)

        end_perf_counter = time.perf_counter()
        duration = end_perf_counter - self.start_perf_counter
        start_time_since_epoch = (time_at_startup - perf_counter_at_startup) + self.start_perf_counter
        end_time_since_epoch = (time_at_startup - perf_counter_at_startup) + end_perf_counter

        request_meta = {
            "request_type": "action",
            "name": self.name,
            "response_length": 0,
            "response": None,
            "context": {
                "action": {
                    "locust_user_id": id(self.locust_user),
                    "start": start_time_since_epoch,  # seconds
                    "end": end_time_since_epoch,  # seconds
                }
            },
            "exception": None,
            "response_time": duration * 1000  # milliseconds
        }

        # Wrap unexpected exceptions in UnexpectedError
        if (exc_value is not None) and (exc_type not in exception_list):
            # GreenletExit is raised by locust to stop the load test.
            # We should not wrap this exception in UnexpectedError and throw it as is.
            # This is a workaround as importing it from gevent and adding it to the exception list above didn't work.
            if (repr(exc_value) == 'GreenletExit()'):
                raise exc_type
            exc_value = UnexpectedError(repr(exc_value))

        request_meta["exception"] = exc_value

        self.locust_user.environment.events.request.fire(**request_meta)  # Make Locust record the request!

        # If exiting without an exception, no error propagation is necessary
        if exc_value is None:
            return True

        # If the current timed action has a parent, we bubble up the error to the parent.
        if self.has_parent_action:
            raise PropagateError(request_meta["exception"])
        else:
            return True  # Suppress handled exceptions if the timed action is a root
