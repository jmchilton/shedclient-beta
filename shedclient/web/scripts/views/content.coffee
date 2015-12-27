Backbone = require 'backbone'
Routes = require 'scripts/routes.coffee'


class ContentView extends Backbone.View
  tagName: 'div'

  initialize: ->
    @$el.html @template({routes: Routes})


module.exports = ContentView
