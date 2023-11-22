import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  // Move all paths to under app/*
  base: '/static/',
  build: {
    outDir: '../vite-build',
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      'vue': "vue/dist/vue.esm-bundler.js",
    },
  },
})
