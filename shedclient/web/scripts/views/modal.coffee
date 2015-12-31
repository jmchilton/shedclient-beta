Backbone = require 'backbone'
$ = require 'jquery'

class ModalView extends Backbone.View
  id: 'modal'
  className: 'modal'
  events: {
  	'hidden': 'teardown'
  }

  initialize: (options)->
    @content = options.content
    _.bindAll @
    @render()
    self = @
    @$el.find("#ok-button").on "click", () -> options.callback(self)

  show: ->
    @$el.modal 'show'

  teardown: ->
    @$el.modal 'hide'
    @remove()

  render: ->
    @renderView()
    this

  renderView: ->
    @$el.html @content
    @$el.modal {show:false}

  formData: () ->
    @$el.find('form').serializeArray().reduce (obj, item) ->
      obj[item.name] = item.value;
      return obj;
    , {}

module.exports = ModalView
