Backbone = require 'backbone'
Routes = require 'scripts/routes.coffee'


class ToolManagementRouter extends Backbone.Router

  initialize: ->
    @routesHit = 0
    # keep count of number of routes handled by the application
    inc = () => @routesHit++
    Backbone.history.on 'route', inc, @
    @bind 'route', @trackPageview

  routes: {
    '' : 'main'
    'panel' : 'panel'
    'dependencies' : 'dependencies'
    'shed' : 'shed'
  }

  back: ->
    if @routesHit > 0
      window.history.back()
    else 
      @navigate '#', { trigger:true, replace:true }

  trackPageview: ->
    url = Backbone.history.getFragment();
    if !/^\//.test(url) && url != ""
      url = "/" + url

    # TODO: implement

  main: -> @appView().showMain()
  panel: -> @appView().showPanel()
  dependencies: -> @appView().showDependencies()
  shed: -> @appView().showShed()

  appView: -> window.appView

module.exports = ToolManagementRouter
