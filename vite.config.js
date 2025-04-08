import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';

export default defineConfig({
  plugins: [vue()],
  build: {
    outDir: 'staticfiles/dist',
    assetsDir: 'assets',
    rollupOptions: {
      input: {
        'vue-music-list': path.resolve(__dirname, 'staticfiles/js/vue-music-list.js'),
      },
      output: {
        entryFileNames: 'js/[name].js',
        chunkFileNames: 'js/[name]-[hash].js',
        assetFileNames: (assetInfo) => {
          const info = assetInfo.name.split('.');
          const ext = info[info.length - 1];
          if (/\.(css)$/.test(assetInfo.name)) {
            return `css/[name].[ext]`;
          }
          return `assets/[name].[ext]`;
        }
      }
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'staticfiles/js')
    }
  },
  // 开发服务器配置
  server: {
    port: 3000,
    open: '/static/dev.html'
  }
}); 