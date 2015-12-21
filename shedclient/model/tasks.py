from __future__ import print_function

import os
import tempfile

from celery import Celery
from kombu import Queue

from galaxy.tools.deps import commands

from shedclient.util import archives
from shedclient.util import tools
from shedclient import context


APP_PATH = "%s.app" % __name__
APP_NAME = "shedclient"


CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = (
    Queue('default', routing_key='task.#'),
    Queue('toolpanel', routing_key='task.#'),
)
CELERY_DEFAULT_EXCHANGE = 'tasks'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_DEFAULT_ROUTING_KEY = 'task.default'

CELERY_ROUTES = {
    'shedclient.install_from_url': {'queue': 'default'},
    'shedclient.modify_toolpanel': {'queue': 'toolpanel'},
}

app = Celery(APP_NAME)
app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ROUTES=CELERY_ROUTES,
    CELERY_DEFAULT_QUEUE=CELERY_DEFAULT_QUEUE,
    CELERY_QUEUES=CELERY_QUEUES,
    CELERY_DEFAULT_EXCHANGE=CELERY_DEFAULT_EXCHANGE,
    CELERY_DEFAULT_EXCHANGE_TYPE=CELERY_DEFAULT_EXCHANGE_TYPE,
    CELERY_DEFAULT_ROUTING_KEY=CELERY_DEFAULT_ROUTING_KEY,
)


@app.task()
def install_from_url(shed_client_context, install_request):
    shed_client_context = context.ensure(shed_client_context)
    url = install_request["url"]
    installable_type = install_request["installable_type"]
    installable_id = install_request["id"]
    installable_version = install_request["version"]
    installable_directory = shed_client_context.install_directory.installable_directory(
        installable_type,
        installable_id,
        installable_version
    )
    target_directory = installable_directory.source_path
    if os.path.exists(installable_directory.source_path):
        raise Exception("Installable already exists.")
    download_and_extract_archive(url, target_directory)
    verify_download(installable_type, target_directory)


def verify_download(installable_type, target_directory):
    if installable_type == "galaxy_tool":
        tools.verify_tool_directory(target_directory, enable_beta_formats=False)
    elif installable_type == "cwl_tool":
        tools.verify_tool_directory(target_directory, enable_beta_formats=True)
    else:
        raise Exception("Installable type [%s] not yet implemented." % installable_type)


def download_and_extract_archive(url, target_directory):
    temp_file = download_installable_archive(url)
    try:
        extract(temp_file, target_directory)
    finally:
        os.remove(temp_file)


def extract(temp_file, target_directory):
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    archives.extract_file_safely(temp_file, target_directory)


def download_installable_archive(url):
    """ Download a tar ball from the shed. Caller is responsible for
    deleting the resulting tarball.
    """
    temp_file = tempfile.NamedTemporaryFile(delete=False).name
    # TODO: Just do this in Python, ensure a reasonable maximum size.
    try:
        download_command = commands.download_command(url)
        full_command = "%s > '%s'" % (" ".join(download_command), temp_file)
        if commands.shell(full_command):
            raise Exception("Failed to download shed tarball [%s]." % url)
    except Exception:
        if os.path.exists(temp_file):
            os.remove(temp_file)
        raise
    return temp_file


__all__ = [
    'install_from_url',
    'app'
]
