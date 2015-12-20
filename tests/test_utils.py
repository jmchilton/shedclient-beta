
""" Provide abstractions over click testing of the
app and unittest.
"""
from __future__ import print_function
import os
from tempfile import mkdtemp
import shutil
from sys import version_info

from galaxy.tools.deps.commands import which

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
