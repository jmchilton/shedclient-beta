ContentView = require 'scripts/views/content.coffee'
PanelModel = require 'scripts/models/panel.coffee'
ModalView = require 'scripts/views/modal.coffee'
template = require 'templates/panel.jade'
newSectionModalTemplate = require 'templates/new_section_modal.jade'
newLabelModalTemplate = require 'templates/new_label_modal.jade'
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
  $treeEl: -> @$el.find("#panel_tree")
  tree: -> @$treeEl().jstree(true)

  initialize: ->
    super.initialize
    _.bindAll @
    @model.on "change", @updateContents
    @$saveButton().on "click", @save
    @$createLabelButton().on "click", @showNewLabelModal
    @$createSectionButton().on "click", @showNewSectionModal

  save: ->
    items = (@nodeToItem(node) for node in @tree().get_json("#"))
    @model.update(items)

  showNewSectionModal: ->
    modal = new ModalView
      content: newSectionModalTemplate()
      callback: @newSection
    modal.show()

  showNewLabelModal: ->
    modal = new ModalView
      content: newLabelModalTemplate()
      callback: @newLabel
    modal.show()

  newSection: (modalView) ->
    data = modalView.formData()
    node = @itemToNode {type: "section", name: data.name, id: data.id, items: [] }
    @addNode node
    modalView.teardown()

  newLabel: (modalView) ->
    data = modalView.formData()
    node = @itemToNode {type: "label", text: data.text }
    @addNode node
    modalView.teardown()

  addNode: (node) ->
    @tree().create_node null, node

  error: (e) ->
    console.log e

  handleSelectionChanged: ->
    # TODO: updated button visibility...

  changed: (e, data) ->
    if data.action in ['select_node', 'deselect_node']
      @handleSelectionChanged()

  updateContents: ->
    @$el.find("#panel_contents").val @model.attributes.contents
    @$treeEl().on('changed.jstree', @changed).jstree
      plugins: ['dnd', 'grid', 'wholerow']
      core:
        data: @modelToTree()
        check_callback: @checkCallback
        error: @error
      grid:
        columns: [
          {width: '50%', header: 'Tool Path'},
          {width: '5%', header: 'Active', value: 'active_html'},
        ]
      dnd:
        check_while_dragging: true

  checkCallback: (operation, node, nodeParent, nodePosition, more) ->
    nodeType = node.data.type
    allowed = false
    if operation == 'create_node'
      # Coming from buttons, they will do checking
      allowed = true
    else if operation == 'move_node'
      if nodeParent.id == '#'
        allowed = true
      else
        if nodeParent.data.type != 'section'
          allowed = false
        else if nodeType == 'section'
          allowed = false
        else
          allowed = true
    else if 'rename_node'
      allowed = nodeType in ['label', 'section']
    allowed

  modelToTree: () ->
    children = (@itemToNode(item) for item in (@model.attributes.contents.items or []))
    # {"text": "Shed Managed Tools", "children": children}
    children

  itemToNode: (item) ->
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
      children = (@itemToNode(childItem) for childItem in (item.items or []))
    else if item.type == "label"
      icon = "bookmark-o fa-rotate-90"
      text = item.text

    data = _.defaults(_.omit(item, 'items'), {active: true})
    if not data['active']
      data['active_html'] = '<i class="fa fa-times"></i>&nbsp;'
    else
      data['active_html'] = '<i class="fa fa-check"></i>&nbsp;'
    item =
      text: text
      icon: 'fa fa-' + icon
      data: data,
      opened: opened
    if children != null
      item['children'] = children
    item

  nodeToItem: (node) ->
    item = _.omit _.clone(node.data), 'active_html'
    if item.type in ['section']
      item['items'] = (@nodeToItem(childNode) for childNode in (node.children))
    item

  render: ->
    @model.fetch()


module.exports = PanelView
