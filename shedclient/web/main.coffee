require 'main.less'
require 'bootstrap-webpack!./bootstrap.config.js'
$ = require 'jquery'

AppView = require 'scripts/views/app.coffee'
Router = require 'scripts/router.coffee'



$ ->
  window.appView = new AppView()

  # Initialize routing and start Backbone.history()
  new Router()
  Backbone.history.start()
