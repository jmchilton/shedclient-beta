ContentView = require 'scripts/views/content.coffee'
template = require 'templates/main.jade'

class MainView extends ContentView
  template: template

module.exports = MainView

