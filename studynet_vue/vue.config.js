const { defineConfig } = require('@vue/cli-service')
module.exports = {
  devServer: {
    port: 8080,
    proxy: 'http://127.0.0.1:8080/',
  },
};