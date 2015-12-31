'use strict';

var webpack = require('webpack'),
    path = require( 'path' ),
    scriptsBase = path.join( __dirname, 'scripts' );

// webpack.config.js
module.exports = {
  entry: {
    main   : 'main.coffee',
  },
  output  : {
    path        : 'static/packed/',
    filename    : '[name].js',
    publicPath  : 'static/packed/'
  },
  resolve: {
    // Absolute path that contains modules
    root: __dirname,

    // Directory names to be searched for modules
    modulesDirectories: ['js', 'views', 'node_modules'],

    // Replace modules with other modules or paths for compatibility or convenience
    alias: {
      'underscore': 'lodash'
    }

  },

  module: {
    loaders: [
      {test: /bootstrap\/js\//, loader: 'imports?jQuery=jquery'},
      {test: /\.jade$/, loader: 'jade'},
      {test: /\.less$/, loader: 'style!css!less'},
      {test: /\.css$/, loader: 'style!css'},
      {test: /\.coffee$/, loader: 'coffee'},
      {test: /\.svg(\?v=\d+\.\d+\.\d+)?$/, loader: 'url?limit=8192&mimetype=image/svg+xml'},
      {test: /\.woff2(\?v=\d+\.\d+\.\d+)?$/, loader: 'url?limit=8192&mimetype=application/font-woff2'},
      {test: /\.woff(\?v=\d+\.\d+\.\d+)?$/, loader: 'url?limit=8192&mimetype=application/font-woff'},
      {test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/, loader: 'url?limit=8192&mimetype=application/octet-stream'},
      {test: /\.eot(\?v=\d+\.\d+\.\d+)?$/, loader: 'file'}
    ]
  },


};
