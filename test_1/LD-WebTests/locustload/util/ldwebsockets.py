"""
Module that facilitates subscribing to LiveReports using websockets.
"""
import asyncio
import json
import threading
import time
from contextlib import contextmanager

import requests
import websockets


@contextmanager
def subscribe_to_live_report(live_report_id: str):
    """
    Context manager for subscribing to LiveReport using websockets. Usage:

        with subscribe_to_live_report("123"):
            # perform LR operations

    The websockets connection is maintained in a separate thread and cleanly closed when
    the context ends.
    """
    thread = _LiveReportSubscriptionThread(live_report_id=live_report_id)
    thread.start()
    try:
        yield
    finally:
        thread.stop()
        # NOTE(fennell): the stop command is asynchronous. In order to ensure the connection is
        # closed when the context ends, we wait for the thread to fully finish.
        thread.join()


class _LiveReportSubscriptionThread(threading.Thread):
    """
    Thread object for creating a new thread that subscribes to a LiveReport using WebSockets.

    Do not use this object directly! Instead, use the context manager above to ensure that
    all necessary cleanup takes place.

    All of the thread's activity takes place on an asyncio event loop. The main reason for this
    is that the websockets library only has an asyncio API. However, we use the async API to our
    advantage. The initial connection is set up essentially synchronously - during setup, there
    are no other tasks on the event loop. During the main polling phase, there are two tasks on
    the event loop: one that polls the websockets connection, and one that polls the thread's
    internal stop event. When the stop event is triggered, the connection is closed and the
    thread exits.

    Note the stop method here is asynchronous. After calling it, call the join method to
    ensure all cleanup takes place before any following steps.
    """

    def __init__(self, *args, live_report_id, **kwargs):
        super().__init__(*args, **kwargs)
        self._live_report_id = live_report_id
        self._stop_event = threading.Event()

    def run(self):
        asyncio.run(
            self._create_and_persist_websockets_connection(live_report_id=self._live_report_id,
                                                           project_ids=["0", "1", "2", "3"]))

    def stop(self):
        self._stop_event.set()

    def is_stopped(self):
        return self._stop_event.is_set()

    async def _create_and_persist_websockets_connection(self, live_report_id, project_ids):
        """
        Create a LR subscription connection and persist until until thread is ordered to stop.
        """
        response = requests.post(
            "http://localhost/livedesign/api/auth/login",
            data={
                "username": "demo",
                "password": "demo"
            },
        )
        cookie = response.headers["Set-Cookie"]
        print("Logged in")
        async with websockets.connect(
                "ws://localhost/livedesign/api/websocket",
                extra_headers={
                    "Origin": "http://localhost",
                    "Cookie": cookie
                },
        ) as websocket:
            print("WebSockets connection established")
            await websocket.send(_build_live_report_subscription_message(live_report_id, project_ids))
            print("LiveReport subscription active")
            await self._read_websockets_connection_until_stopped(websocket)
            print("Closing WebSockets connection")
        print("WebSockets connection closed")

    async def _read_websockets_connection_until_stopped(self, websocket_connection):
        """
        Repeatedly read from the websockets connection until the thread is ordered to stop.
        """
        while True:
            # NOTE(fennell): the following asyncio command returns when either of the two functions
            # finishes. This command allows us to wait for incoming websockets messages, but
            # also interrupt early when a thread stop command has been issued.
            finished, unfinished_tasks = await asyncio.wait(
                [websocket_connection.recv(), self._wait_until_stopped()],
                return_when=asyncio.FIRST_COMPLETED,
            )
            if self.is_stopped():
                for unfinished_task in unfinished_tasks:
                    unfinished_task.cancel()
                return

    async def _wait_until_stopped(self):
        """
        Asynchronously check if the thread has been ordered to stop, and return when it has been.
        """
        while True:
            if self.is_stopped():
                return
            await asyncio.sleep(0.1)


def _build_live_report_subscription_message(live_report_id: str, project_ids: list) -> str:
    """
    Build the websocket message that when sent to the BE results in the LR being subscribed to.

    The JSON was scraped from network activity in the UI.
    """
    return json.dumps({
        "live_report_subscriptions": {
            "ACTIVE_USERS": [live_report_id],
            "AUDIT_LOG": [live_report_id],
            "COLUMN_ALIAS": [live_report_id],
            "COLUMN_DESCRIPTOR": [live_report_id],
            "COMMENT": [live_report_id],
            "FORMULA": [live_report_id],
            "FREEFORM_COLUMN": [live_report_id],
            "LAYOUT": [live_report_id],
            "LIVE_REPORT": [live_report_id],
            "PLOT": [live_report_id],
            "RATIONALE": [live_report_id],
            "QUERY": [live_report_id],
            "SUBSCRIPTION": [live_report_id],
        },
        "project_subscriptions": {
            "ATTACHMENT": project_ids,
            "COLUMN_ALIAS": project_ids,
            "FREEFORM_COLUMN": project_ids,
            "FORMULA": project_ids,
            "LAYOUT": project_ids,
            "LIVE_REPORT_METADATA": project_ids,
            "MPO": project_ids,
            "PREDICTOR": project_ids,
            "PREDICTOR_TRAINING_RUN": project_ids,
            "REACTION": project_ids,
            "SCAFFOLD": project_ids,
            "TAG": project_ids,
        },
        "live_report_result_subscriptions": [{
            "live_report_id":
                live_report_id,
            "report_level":
                "parent",
            "view_details": [
                {
                    "type": "page",
                    "row_return_type": "FROZEN_ONLY",
                    "projections": [],
                },
                {
                    "type": "page",
                    "row_return_type": "ALL",
                    "projections": [],
                    "start": 0,
                    "size": 250,
                },
                {
                    "type": "page",
                    "row_return_type": "ALL",
                    "projections": []
                },
            ],
        }],
    })
