Backbone = require 'backbone'
Routes = require 'scripts/routes.coffee'
template = require 'templates/navigation.jade'


class NavigationView extends Backbone.View
  el: 'nav'

  initialize: ->
    @$el.html template {routes: Routes}


#@listenTo App.vent, 'navigation:change', @highlightNavigation
#highlightNavigation: (nav) ->
#  @ui.menuItem.removeClass('active')
#  unless _.isEmpty(nav)
#    @$el.find("a[data-nav='#{nav}']").parent().addClass('active')

module.exports = NavigationView
