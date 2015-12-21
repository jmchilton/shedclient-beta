import os

from .test_utils import (
    MockShedTestCase,
    get_repo_path,
)

from six.moves.urllib.parse import urljoin

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
        download_url = urljoin(
            base_shed_url,
            "api",
            "galaxy",
            "v1",
            "galaxy_tools",
            "cat",
            "versions",
            "0.1",
            "download",
        )
        result = install_from_url.delay(shed_context.to_dict(), dict(
            target_directory=self.temp_directory,
            url=download_url,
        ))
        result.wait(10)
        assert os.path.exists(os.path.join(self.temp_directory, "download.tar.gz"))
