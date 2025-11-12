// webpack.config.js
const path = require('path');

module.exports = {
  // 1. Where Webpack starts looking for code
  entry: './mainApp.tsx',

  // 2. The final compiled and bundled output file
  output: {
    path: path.resolve(__dirname, 'dist'), // Puts the output in a 'dist' folder
    filename: 'bundle.js',
  },

  // 3. How to process files (using ts-loader for .tsx)
  module: {
    rules: [
      {
        test: /\.tsx?$/, // Apply this rule to .ts and .tsx files
        use: 'ts-loader',
        exclude: /node_modules/,
      },
    ],
  },

  // 4. Resolve file extensions so you don't need to type '.tsx'
  resolve: {
    extensions: ['.tsx', '.ts', '.js'],
  },

  // Set mode to development for easier debugging
  mode: 'development',
};
