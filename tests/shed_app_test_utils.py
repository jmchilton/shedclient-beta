from collections import namedtuple
import contextlib
import shutil
import socket
from time import time as now
from tempfile import mkdtemp
import threading
from requests import post

from werkzeug.serving import run_simple

from .shed_app import (
    app,
    InMemoryShedDataModel,
)
from galaxy.util.sockets import unused_port


DEFAULT_OP_TIMEOUT = 2


def mock_model(directory):
    return InMemoryShedDataModel(
        directory
    ).add_category(
        "c1", "Text Manipulation"
    ).add_category(
        "c2", "Sequence Analysis"
    ).add_category(
        "c3", "Tool Dependency Packages"
    )


def setup_mock_shed():
    port = unused_port()
    directory = mkdtemp()
    model = mock_model(directory)

    def run():
        app.debug = True
        app.config["model"] = model
        run_simple(
            'localhost',
            port,
            app,
            use_reloader=False,
            use_debugger=True
        )

    t = threading.Thread(target=run)
    t.start()
    wait_net_service("localhost", port, DEFAULT_OP_TIMEOUT)
    return MockShed("http://localhost:%d" % port, directory, t, model)


# code.activestate.com/recipes/576655-wait-for-network-service-to-appear
def wait_net_service(server, port, timeout=None):
    """ Wait for network service to appear
        @param timeout: in seconds, if None or 0 wait forever
        @return: True of False, if timeout is None may return only True or
                 throw unhandled network exception
    """
    s = socket.socket()
    # Following line prevents this method from interfering with process
    # it is waiting for on localhost.
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if timeout:
        end = now() + timeout

    while True:
        try:
            if timeout:
                next_timeout = end - now()
                if next_timeout < 0:
                    return False
                else:
                    s.settimeout(next_timeout)

            s.connect((server, port))

        except socket.timeout:
            # this exception occurs only if timeout is set
            if timeout:
                return False

        except socket.error:
            pass
        else:
            s.close()
            return True


@contextlib.contextmanager
def mock_shed():
    mock_shed_obj = None
    try:
        mock_shed_obj = setup_mock_shed()
        yield mock_shed_obj
    finally:
        if mock_shed_obj is not None:
            mock_shed_obj.shutdown()


def _shutdown(self):
    post("%s/shutdown" % self.url)
    self.thread.join(DEFAULT_OP_TIMEOUT)
    shutil.rmtree(self.directory)

MockShed = namedtuple("MockShed", ["url", "directory", "thread", "model"])
MockShed.shutdown = _shutdown

__all__ = ["setup_mock_shed", "mock_shed"]
