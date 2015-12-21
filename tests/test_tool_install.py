import os

from .test_utils import (
    MockShedTestCase,
    get_repo_path,
)

from shedclient.model.tasks import (
    install,
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
        result = install.delay(dict(
            target_directory=self.temp_directory,
            url="http://google.com",
        ))
        result.wait(10)
        assert os.path.exists(os.path.join(self.temp_directory, "download.tar.gz"))
