import os

from .test_utils import (
    MockShedTestCase,
    get_repo_path,
)

from shedclient import context
from shedclient.model.tasks import (
    install_from_url,
)


class ToolInstallTestCase(MockShedTestCase):

    def test_install(self):
        repo_path = get_repo_path("cat0")
        self.mock_shed.model.add_installable(
            "galaxy_tool",
            "cat",
            "0.1",
            repo_path,
        )
        shed_context = context.ShedClientContext(
            install_directory=self.temp_directory,
        )
        base_shed_url = self.mock_shed.url
        download_url = "/".join([
            base_shed_url,
            "api",
            "galaxy",
            "v1",
            "galaxy_tools",
            "cat",
            "versions",
            "0.1",
            "download",
        ])
        result = install_from_url.delay(shed_context.to_dict(), dict(
            target_directory=self.temp_directory,
            installable_type="galaxy_tool",
            id="cat",
            version="0.1",
            url=download_url,
        ))
        result.wait(10)
        install_directory = shed_context.install_directory
        installable_directory = install_directory.installable_directory("galaxy_tool", "cat", "0.1")
        assert os.path.exists(installable_directory.path)
        assert os.path.exists(installable_directory.source_path)
        print(os.listdir(installable_directory.source_path))
        assert os.path.exists(os.path.join(installable_directory.source_path, "cat.xml"))
