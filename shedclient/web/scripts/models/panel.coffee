Backbone = require 'backbone'


class ToolPanelModel extends Backbone.Model
  urlRoot: -> Galaxy.root + "shed_tool_conf"


module.exports = ToolPanelModel
