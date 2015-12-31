ContentView = require 'scripts/views/content.coffee'
PanelModel = require 'scripts/models/panel.coffee'
template = require 'templates/panel.jade'
require 'imports?jQuery=jquery!jstree/dist/jstree.js'
require 'imports?jQuery=jquery!jstreegrid/jstreegrid.js'
$ = require 'jquery'
_ = require 'underscore'


class PanelView extends ContentView
  template: template
  model: new PanelModel()

  $createLabelButton: -> @$el.find("#create-label-button")
  $createSectionButton: -> @$el.find("#create-section-button")
  $saveButton: -> @$el.find("#save-button")

  initialize: ->
    super.initialize
    _.bindAll @
    @model.on "change", @updateContents
    @$createLabelButton().on "click", @alert
    @$createSectionButton().on "click", @alert

  alert: ->
    alert("Alerting")

  updateContents: ->
    @$el.find("#panel_contents").val @model.attributes.contents
    $("#panel_tree").jstree {
      plugins: ['dnd', 'grid', 'wholerow'],
      core: {data: @modelToTree(), check_callback: @checkCallback},
      grid: {
        columns: [
          {width: "50%", header: "Tool Path"},
          {width: "5%", header: "Active", value: "active"},
        ],
      }
    }

  checkCallback: (operation, node, nodeParent, nodePosition, more) ->
    operation == 'rename_node' ? true : false

  modelToTree: () ->
    children = (@itemToTreeNode(item) for item in @model.attributes.contents.items)
    # {"text": "Shed Managed Tools", "children": children}
    children

  itemToTreeNode: (item) ->
    children = null
    opened = true
    if item.type == "tool"
      icon = "wrench"
      text = item.file
    else if item.type == "group"
      icon = "wrench"
      opened = false
      text = item.id
    else if item.type == "section"
      icon = "folder"
      text = item.name
      children = (@itemToTreeNode(childItem) for childItem in item.items)
    else if item.type == "label"
      icon = "pencil-square"
      text = item.text
    item = {
      text: text
      icon: "fa fa-" + icon
      data: {active: "true"},
      opened: opened
    }
    if children != null
      item["children"] = children
    item

  render: ->
    @model.fetch()


module.exports = PanelView
