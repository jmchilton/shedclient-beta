Backbone = require 'backbone'
NavigationView = require 'scripts/views/navigation.coffee'
$ = require 'jquery'

MainView = require 'scripts/views/main.coffee'
ShedView = require 'scripts/views/shed.coffee'
DependenciesView = require 'scripts/views/dependencies.coffee'
PanelView = require 'scripts/views/panel.coffee'

template = require 'templates/app.jade'


class AppView extends Backbone.View
  el: 'body'

  initialize: -> 
    @$el.html template()
    @navigationView = new NavigationView()
    @mainView = new MainView()
    @contentViews = {
      'main': @mainView
      'shed': null
      'dependencies': null
      'panel': null
    }
    @currentView = null
    @currentViewName = null
    @showContent 'main'

  showMain: ->
    @showContent 'main', MainView

  showShed: ->
    @showContent 'shed', ShedView

  showDependencies: ->
    @showContent 'dependencies', DependenciesView

  showPanel: ->
    @showContent 'panel', PanelView

  showContent: (viewName, viewClass) ->
    targetView = @contentViews[viewName]
    if targetView == null
      targetView = new viewClass()
      @contentViews[viewName] = targetView
      @$content().append targetView.$el
    if @currentView != null and @currentView != targetView
      @currentView.$el.hide()
    @currentView = targetView
    @currentView.render()
    @currentView.$el.show()

  $content: -> $(@$el.find("#content"))

module.exports = AppView
