Backbone = require 'backbone'
template = require 'templates/modal.jade'


class ModalView extends Backbone.View
  tagName: 'div'

  initialize: ->
    @$el.html template()


module.exports = ModalView
