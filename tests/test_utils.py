
""" Provide abstractions over click testing of the
TEST_DIR = os.path.dirname(__file__)
TEST_DATA_DIR = os.path.join(TEST_DIR, "data")
TEST_REPOS_DIR = os.path.join(TEST_DATA_DIR, "repos")
"""
from __future__ import print_function
import os
from multiprocessing import Process
from tempfile import mkdtemp
import shutil
from sys import version_info

from galaxy.tools.deps.commands import which
from shedclient.model.tasks import (
    app,
    APP_PATH,
)

from .shed_app_test_utils import (
    setup_mock_shed,
)


if version_info < (2, 7):
    from unittest2 import TestCase, skip
    PRE_PYTHON_27 = True
else:
    from unittest import TestCase, skip
    PRE_PYTHON_27 = False
if version_info[0] == 2 and version_info[1] >= 7:
    PYTHON_27 = True
else:
    PYTHON_27 = False

TEST_DIR = os.path.dirname(__file__)
TEST_DATA_DIR = os.path.join(TEST_DIR, "data")
TEST_REPOS_DIR = os.path.join(TEST_DATA_DIR, "repos")


def get_repo_path(name):
    return os.path.join(TEST_REPOS_DIR, name)


class TempDirectoryTestCase(TestCase):

    def setUp(self):  # noqa
        self.temp_directory = mkdtemp()

    def tearDown(self):  # noqa
        shutil.rmtree(self.temp_directory)


class TempDirectoryContext(object):
    def __init__(self):
        self.temp_directory = mkdtemp()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        shutil.rmtree(self.temp_directory)


def worker(*argv):
    return app.worker_main(list(argv))


class MockShedTestCase(TempDirectoryTestCase):

    def setUp(self):  # noqa
        super(MockShedTestCase, self).setUp()
        self.spawn_worker()
        self.mock_shed = setup_mock_shed()

    def tearDown(self):  # noqa
        super(MockShedTestCase, self).tearDown()
        exception = None
        try:
            self.join_worker()
        except Exception as e:
            exception = e
        try:
            self.mock_shed.shutdown()
        except Exception as e:
            exception = e
        if exception:
            raise exception

    @property
    def broker(self):
        return 'sqla+sqlite:///%s/broker.sqlite' % (self.temp_directory)

    @property
    def result(self):
        return 'db+sqlite:///%s/results.sqlite' % (self.temp_directory)

    def spawn_worker(self):
        app.conf.update(
            BROKER_URL=self.broker,
            CELERY_RESULT_BACKEND=self.result
        )
        app.finalize()

        argv = ["--app=%s" % APP_PATH]

        p = Process(target=worker, args=argv)
        p.start()
        self.worker = p

    def join_worker(self):
        p = self.worker
        p.terminate()
        p.join()


def skip_unless_environ(var):
    if var in os.environ:
        return lambda func: func
    template = "Environment variable %s not found, dependent test skipped."
    return skip(template % var)


def skip_if_environ(var):
    if var not in os.environ:
        return lambda func: func
    template = "Environment variable %s set, dependent test skipped."
    return skip(template % var)


def skip_unless_module(module):
    available = True
    try:
        __import__(module)
    except ImportError:
        available = False
    if available:
        return lambda func: func
    template = "Module %s could not be loaded, dependent test skipped."
    return skip(template % module)


def skip_unless_executable(executable):
    if which(executable):
        return lambda func: func
    return skip("PATH doesn't contain executable %s" % executable)


def skip_unless_python_2_7():
    if PYTHON_27:
        return lambda func: func
    return skip("Python 2.7 required for test.")
