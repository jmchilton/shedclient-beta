""" A minimal Toolbox implementation and Tool definition for managing
tools, dependencies, and the dynamic tool conf.
"""

import logging
import os
import sys

from galaxy.tools.parser import get_tool_source
from galaxy.tools.toolbox import BaseGalaxyToolBox
from galaxy.tools.toolbox import managed_conf

from galaxy.util.dictifiable import Dictifiable
from galaxy.util.bunch import Bunch
from galaxy.util.properties import load_app_properties

log = logging.getLogger(__name__)


MANAGED_TOOL_CONF_FILENAME = "shed_tools.json"


def resolve_path(path):
    if path:
        return os.path.abspath(path)
    else:
        return None


class ShedClientApp(object):

    def __init__(self, config_file=None):
        configure_logging()
        properties = load_app_properties(ini_file=config_file)
        self.name = "shedclient"

        tool_dependency_dir = resolve_path(properties.get("tool_dependency_dir", None))
        managed_shed_conf = resolve_path(properties.get("managed_shed_conf", None))
        if not managed_shed_conf:
            managed_shed_conf = os.path.join(tool_dependency_dir or '.', MANAGED_TOOL_CONF_FILENAME)
        self.config = Bunch(
            tool_dependency_dir=tool_dependency_dir,
            use_tool_dependencies=tool_dependency_dir is not None,
            dependency_resolvers_config_file=resolve_path(properties.get("dependency_resolvers_config_file", None)),
            managed_shed_conf=managed_shed_conf,
            tool_path=resolve_path(properties.get("tool_path", "tools"))
        )
        self.reload_toolbox()

    def reload_toolbox(self):
        self.toolbox = ShedClientManagedToolBox(self)


class ShedClientTool(Dictifiable, object):
    dict_collection_visible_keys = ( 'id', 'name', 'version', 'description', 'labels' )

    def __init__(self, config_file, tool_source, app, **kwds):
        self.config_file = config_file
        self.tool_dir = os.path.dirname(config_file)
        self.app = app
        self.parse(tool_source)

        # TODO: remove toolbox logic that just assumes these toolshed
        # properties are available.
        self.guid = None
        self.tool_shed = None

    def parse(self, tool_source):
        self.id = tool_source.parse_id()
        self.name = tool_source.parse_name()
        # TODO: validating tool parser...
        if not self.name:
            raise Exception("Missing tool 'name'")
        self.version = tool_source.parse_version()
        if not self.version:
            # For backward compatibility, some tools may not have versions yet.
            self.version = "1.0.0"
        # Is this a 'hidden' tool (hidden in tool menu)
        self.hidden = tool_source.parse_hidden()
        # Short description of the tool
        self.description = tool_source.parse_description()
        # Requirements (dependencies)
        requirements, containers = tool_source.parse_requirements_and_containers()
        self.requirements = requirements
        self.containers = containers


class ShedClientManagedToolBox(BaseGalaxyToolBox):

    def __init__(self, app):
        config_filename = app.config.managed_shed_conf
        tool_path = app.config.managed_shed_conf
        super(ShedClientManagedToolBox, self).__init__(
            config_filenames=[config_filename],
            tool_root_dir=tool_path,
            app=app,
        )
        self.managed_tool_conf = managed_conf.ManagedConf(config_filename)
        self.managed_tool_conf_view = managed_conf.ManagedConfView(self.managed_tool_conf)

    def create_tool(self, config_file, **kwds):
        tool_source = get_tool_source(config_file, True)
        tool = ShedClientTool( config_file, tool_source, self.app, **kwds )
        return tool


def configure_logging():
    """
    Allow some basic logging configuration to be read from ini file.
    """
    # Get root logger
    root = logging.getLogger()
    format = "%(name)s %(levelname)s %(asctime)s %(message)s"
    level = logging._levelNames["DEBUG"]
    destination = "stdout"
    log.info("Logging at '%s' level to '%s'" % (level, destination))
    # Set level
    root.setLevel(level)
    # Remove old handlers
    for h in root.handlers[:]:
        root.removeHandler(h)
    # Create handler
    if destination == "stdout":
        handler = logging.StreamHandler(sys.stdout)
    else:
        handler = logging.FileHandler(destination)
    # Create formatter
    formatter = logging.Formatter(format)
    # Hook everything up
    handler.setFormatter(formatter)
    root.addHandler(handler)
