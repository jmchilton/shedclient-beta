import json
import os

SOURCE_DIRECTORY_NAME = "source"
INSTALL_RECORD_FILE_NAME = "shed_install.json"


class InstallDirectory(object):

    def __init__(self, shed_client_context):
        self.shed_client_context = shed_client_context

    def installable_directory(self, installable_type, id, version):
        return InstallableDirectory(self, installable_type, id, version)


class InstallableDirectory(object):

    def __init__(self, install_directory, installable_type, id, version):
        self.shed_client_context = install_directory.shed_client_context
        self.installable_type = installable_type
        self.id = id
        self.version = version

    @property
    def source_path(self):
        return os.path.join(self.path, SOURCE_DIRECTORY_NAME)

    @property
    def path(self):
        return os.path.join(
            self.shed_client_context.install_directory_path,
            self.installable_type + "s",
            self.id,
            self.version,
        )

    @property
    def install_record_path(self):
        return os.path.join(self.path, INSTALL_RECORD_FILE_NAME)

    @property
    def install_record(self):
        with open(self.install_record_path, "w") as f:
            json.load(f)

    def register_install_record(self, as_dict):
        with open(self.install_record_path, "w") as f:
            json.dump(f, as_dict)
