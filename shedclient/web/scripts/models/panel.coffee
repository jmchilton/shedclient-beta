Backbone = require 'backbone'


class ToolPanelModel extends Backbone.Model
  urlRoot: -> Galaxy.root + "shed_tool_conf"
  id: ""

  update: (items) ->
    @attributes.items = items
    @save(@attributes, {type: 'PUT'})

module.exports = ToolPanelModel
