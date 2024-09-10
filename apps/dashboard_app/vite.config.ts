import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Info from 'unplugin-info/vite'

// https://vitejs.dev/config/
export default defineConfig({
  base: '/dashboard',
  plugins: [
    vue(),
    Info()
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:6384',
        changeOrigin: true,
        secure: false,
      }
    }
  }
})
