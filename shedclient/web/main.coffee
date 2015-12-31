
require 'bootstrap-webpack!./bootstrap.config.js'
# TODO: get this to work so we don't need a vendor folder.
# require '!style!css!jstree/dist/themes/default/style.css'
require 'font-awesome-webpack'
$ = require 'jquery'

AppView = require 'scripts/views/app.coffee'
Router = require 'scripts/router.coffee'



$ ->
  window.appView = new AppView()

  # Initialize routing and start Backbone.history()
  new Router()
  Backbone.history.start()
