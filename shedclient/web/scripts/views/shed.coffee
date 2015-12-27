ContentView = require 'scripts/views/content.coffee'
template = require 'templates/shed.jade'

class ShedView extends ContentView
  template: template

module.exports = ShedView
