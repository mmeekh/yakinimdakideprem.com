/**
 * Webpack Configuration - Anlık Deprem
 * Optimized bundling for production
 */

const path = require('path');
const TerserPlugin = require('terser-webpack-plugin');

module.exports = {
  mode: 'production',
  entry: {
    main: './js/main.js',
    core: './js/core/App.js'
  },
  output: {
    path: path.resolve(__dirname, 'dist/js'),
    filename: '[name].bundle.min.js',
    clean: true
  },
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          compress: {
            drop_console: true,
            drop_debugger: true,
            pure_funcs: ['console.log', 'console.info', 'console.debug']
          },
          mangle: {
            reserved: ['EarthquakeApp', 'DataModule', 'MapModule', 'UIModule', 'StatsModule']
          }
        },
        extractComments: false
      })
    ],
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all'
        },
        core: {
          test: /[\\/]js[\\/]core[\\/]/,
          name: 'core',
          chunks: 'all'
        }
      }
    }
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
            plugins: [
              '@babel/plugin-proposal-class-properties',
              '@babel/plugin-transform-runtime'
            ]
          }
        }
      }
    ]
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'js'),
      '@core': path.resolve(__dirname, 'js/core'),
      '@components': path.resolve(__dirname, 'components')
    }
  },
  performance: {
    hints: 'warning',
    maxEntrypointSize: 250000,
    maxAssetSize: 250000
  }
};
