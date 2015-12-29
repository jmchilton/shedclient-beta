Backbone = require 'backbone'
Routes = require 'scripts/routes.coffee'


class ContentView extends Backbone.View
  tagName: 'div'

  initialize: ->
    console.log "View"
    console.log @$el
    @$el.html @template({routes: Routes})


module.exports = ContentView
