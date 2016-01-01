""" A minimal Toolbox implementation and Tool definition for managing
tools, dependencies, and the dynamic tool conf.
"""

import os

from galaxy.tools.parser import get_tool_source
from galaxy.tools.toolbox import BaseGalaxyToolBox
from galaxy.tools.toolbox import managed_conf

from galaxy.util.dictifiable import Dictifiable
from galaxy.util.bunch import Bunch

MANAGED_TOOL_CONF_FILENAME = "shed_tools.json"


class ShedClientApp(object):

    def __init__(self, managed_directory):
        self.name = "shedclient"
        self.config = Bunch(
            use_tool_dependencies=True,
            tool_dependency_dir=os.path.join(managed_directory, "dependencies"),
            dependency_resolvers_config_file=None,
        )
        self.managed_directory = managed_directory
        self.reload_toolbox()

    def reload_toolbox(self):
        self.toolbox = ShedClientManagedToolBox(
            self.managed_directory, self
        )


class ShedClientTool(Dictifiable, object):
    dict_collection_visible_keys = ( 'id', 'name', 'version', 'description', 'labels' )

    def __init__(self, config_file, tool_source, app, **kwds):
        self.config_file = config_file
        self.tool_dir = os.path.dirname(config_file)
        self.app = app
        self.parse(tool_source)

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

    def __init__(self, managed_directory, app):
        config_filename = os.path.join(managed_directory, MANAGED_TOOL_CONF_FILENAME)
        super(ShedClientManagedToolBox, self).__init__(
            config_filenames=[config_filename],
            tool_root_dir=managed_directory,
            app=app,
        )
        self.managed_tool_conf = managed_conf.ManagedConf(config_filename)
        self.managed_tool_conf_view = managed_conf.ManagedConfView(self.managed_tool_conf)

    def create_tool(self, config_file, **kwds):
        tool_source = get_tool_source(config_file, True)
        tool = ShedClientTool( config_file, tool_source, self.app, **kwds )
        return tool
