import os

from .test_utils import shedclient_context


def test_installs():

    with shedclient_context() as context:
        installs_directory = context.installs_directory
        installable_directory_v0 = installs_directory.installable_directory(
            "galaxy_vizualization",
            "graphviz",
            "0",
        )
        assert not os.path.exists(installable_directory_v0.path)
        install_dir = installable_directory_v0.generate_install_directory()
        with open(os.path.join(install_dir, "content.xml"), "w") as f:
            f.write("<tool></tool>")
        assert not os.path.exists(installable_directory_v0.source_path)
        installable_directory_v0.install(install_dir)
        assert os.path.exists(installable_directory_v0.source_path)

        installable_directory_v1 = installs_directory.installable_directory(
            "galaxy_vizualization",
            "graphviz",
            "1",
        )

        versions = installs_directory.get_installables_version_strings(
            "galaxy_vizualization",
            "graphviz",
        )
        assert len(versions) == 1
        assert "0" in versions

        installable_directory_v1.generate_install_directory()

        versions = installs_directory.get_installables_version_strings(
            "galaxy_vizualization",
            "graphviz",
        )
        assert len(versions) == 2
        assert "0" in versions
        assert "1" in versions

        assert installable_directory_v0.installed
        assert not installable_directory_v1.installed
