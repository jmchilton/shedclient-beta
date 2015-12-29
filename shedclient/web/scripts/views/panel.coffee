ContentView = require 'scripts/views/content.coffee'
PanelModel = require 'scripts/models/panel.coffee'
template = require 'templates/panel.jade'

class PanelView extends ContentView
  template: template
  model: new PanelModel()

  initialize: ->
  	super.initialize
  	@model.bind "change", @update_contents

  update_contents: ->
    console.log "Foo"
    console.log @
    console.log @$
    console.log @$el
    @$el.find("#panel_contents").val @model.attributes.contents

  render: ->
  	@model.fetch()


module.exports = PanelView
