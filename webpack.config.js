var path = require("path")
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')

module.exports = {
  context: __dirname,

  entry: './static/js/app', // entry point of our app. assets/js/app.js should require other js modules and dependencies it needs

  output: {
    path: path.resolve('./static/bundles/'),
    filename: "[name]-[hash].js",
  },

  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
  ],

  module: {
    rules: [
      { test: /\.js?$/, exclude: /node_modules/, loader: 'babel-loader'}, // to transform ES7+ into JS
      // todo: css-loader
    ],
  },

  resolve: {
    modules: ['node_modules'],
    extensions: ['.js']
  },
}
