import json
import os
import shutil
import time

SOURCE_DIRECTORY_NAME = "source"
SOURCE_INSTALL_DIRECTORY_PATTERN = "source-install-%s"
INSTALL_RECORD_FILE_NAME = "shed_install.json"


class InstallsDirectory(object):

    def __init__(self, shed_client_context):
        self.shed_client_context = shed_client_context

    def installable_directory(self, installable_type, id, version):
        return InstallableDirectory(self, installable_type, id, version)

    def get_installables_version_strings(self, installable_type, id):
        installables_directory = os.path.join(
            self.shed_client_context.install_directory_path,
            installable_type + "s",
            id,
        )
        return os.listdir(installables_directory)

    def installable_path(self, installable_type, id, version):
        return os.path.join(
            self.shed_client_context.install_directory_path,
            installable_type + "s",
            id,
            version
        )


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

    def generate_install_directory(self):
        timestamp = str(time.time()).replace(".", '')
        install_dir_name = SOURCE_INSTALL_DIRECTORY_PATTERN % timestamp
        install_directory = os.path.join(self.path, install_dir_name)
        os.makedirs(install_directory)
        return install_directory

    def install(self, install_path):
        shutil.move(install_path, self.source_path)

    @property
    def installed(self):
        return os.path.exists(self.source_path)

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
