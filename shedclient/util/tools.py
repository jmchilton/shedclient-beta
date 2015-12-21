from galaxy.tools import loader_directory
from galaxy.tools.parser import factory

import logging
log = logging.getLogger(__name__)


def verify_tool_directory(tool_directory, enable_beta_formats):
    possible_tool = find_single_tool(tool_directory, enable_beta_formats)
    try:
        factory.get_tool_source(
            possible_tool,
            enable_beta_formats=enable_beta_formats,
        )
    except Exception:
        message = "Failed to parse potential tool source."
        log.warn(message)
        raise Exception(message)
    # TODO: lint for "ERROR"s
    # TODO: allow tool and account level config of stronger linting
    # requirements.


def find_single_tool(tool_directory, enable_beta_formats):
    possible_tools = loader_directory.find_possible_tools_from_path(
        tool_directory,
        recursive=True,
        enable_beta_formats=enable_beta_formats
    )
    if len(possible_tools) > 1:
        raise Exception("Found more than one potential tool.")
    if len(possible_tools) == 0:
        raise Exception("Found no potential tools in archive.")
    return possible_tools[0]
