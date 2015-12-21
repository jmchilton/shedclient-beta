from __future__ import print_function

import os

from celery import Celery

from galaxy.tools.deps import commands

APP_PATH = "%s.app" % __name__
APP_NAME = "shedclient"

app = Celery(APP_NAME)
app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
)


@app.task()
def install(install_request):
    target_directory = install_request["target_directory"]
    url = install_request["url"]
    download_command = commands.download_command(url)
    target = os.path.join(target_directory, "download.tar.gz")
    full_command = "%s > '%s'" % (" ".join(download_command), target)
    commands.shell(full_command)


__all__ = [
    'install',
    'app'
]
