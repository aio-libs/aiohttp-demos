import path from 'path';


const STATIC_FOLDER = path.join(__dirname, '..', '/graph/static');


const config = {
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: ['babel-loader']
      }, {
        test: /\.(css)$/,
        use: [
          { loader: "style-loader" },
          { loader: "css-loader" }
        ]
      }
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx']
  },
  output: {
    path: STATIC_FOLDER,
    publicPath: '/',
    filename: 'bundle.js'
  }
};

export default config;
