'use strict';

var webpack = require('webpack'),
    path = require( 'path' ),
    scriptsBase = path.join( __dirname, 'scripts' ),
    libsBase = path.join( scriptsBase, 'libs' );



// webpack.config.js
module.exports = {
  entry: {
    main   : 'main.js',
  },
  output  : {
	path        : './',
	filename    : '[name].bundled.js'
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
      { test: /\.less$/, loader: 'style!css!less' },
      { test: /\.css$/, loader: 'style!css' },
      { test: /\.coffee$/, loader: 'coffee' },
      { test: /\.js$/, loader: 'babel' }
    ]
  },


};
