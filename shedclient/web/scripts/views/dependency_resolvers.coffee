ContentView = require 'scripts/views/content.coffee'
template = require 'templates/dependency_resolvers.jade'

class DependencyResolversView extends ContentView
  template: template

module.exports = DependencyResolversView
