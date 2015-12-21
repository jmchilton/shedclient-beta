""" Test app to emulate planemo-relevant portions of the
the ToolShed API... for now :).
"""
import os
import json
import tarfile
import uuid

from flask import (
    Flask,
    request,
    send_file,
)

app = Flask(__name__)


@app.route('/api/galaxy/v1/<installable_type>s/<id>/versions/<version>/download', methods=['GET'])
def download(installable_type, id, version):
    model = app.config["model"]
    repo_path = model.get_installable_path(
        installable_type, id, version
    )
    repo_tar_download_path = os.path.join(model.new_temp_dir(), "download.tar.gz")
    tar = tarfile.open(repo_tar_download_path, "w:gz")
    print repo_path
    print installable_type
    try:
        tar.add(
            repo_path,
            arcname=".",
            recursive=True,
        )
    finally:
        tar.close()
    assert os.path.exists(repo_tar_download_path)
    return send_file(repo_tar_download_path)


@app.route('/shutdown', methods=['POST'])
def shutdown():
    # Used to shutdown test server.
    _shutdown_server()
    return ''


def _request_post_message():
    return json.loads(request.data.decode("utf-8"))


class InMemoryShedDataModel(object):

    def __init__(self, directory):
        self.directory = directory
        self._repositories = {
            'galaxy_tool': {},
            'galaxy_viz': {},
        }
        self._repositories_msg = {}
        self._categories = []

    def new_temp_dir(self):
        temp_dir = os.path.join(self.directory, str(uuid.uuid4()))
        os.makedirs(temp_dir)
        return temp_dir

    def add_category(self, id, name):
        self._categories.append({"id": id, "name": name})
        return self

    def get_installable_path(self, installable_type, id, version):
        installable = self._repositories[installable_type][id][version]
        return installable["directory"]

    def add_installable(self, type, id, version, directory=None, metadata={}):
        type_dict = self._repositories[type]
        if id not in type_dict:
            type_dict[id] = {}
        id_dict = type_dict[id]
        assert "version" not in id_dict
        id_dict[version] = dict(
            metadata=metadata.copy(),
            directory=directory,
        )
        return self

    def get_categories(self):
        return self._categories

    def repository_path(self, id):
        return os.path.join(self.directory, id)

    def repository_path_for_update(self, id, message):
        if id not in self._repositories_msg:
            self._repositories_msg[id] = []
        self._repositories_msg[id].append(message)
        return self.repository_path(id)


def _shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
