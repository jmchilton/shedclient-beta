ContentView = require 'scripts/views/content.coffee'
template = require 'templates/panel.jade'

class PanelView extends ContentView
  template: template

module.exports = PanelView
