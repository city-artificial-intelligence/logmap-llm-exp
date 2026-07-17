import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// base: './' keeps asset URLs relative so the built site works from any sub-path
// (e.g. GitHub Pages, a file server, or a nested route).
export default defineConfig({
  base: './',
  plugins: [react()],
  build: {
    outDir: 'dist',
    sourcemap: false,
    chunkSizeWarningLimit: 1200,
    rollupOptions: {
      output: {
        manualChunks: {
          echarts: ['echarts/core', 'echarts/charts', 'echarts/components', 'echarts/features', 'echarts/renderers'],
          react: ['react', 'react-dom'],
        },
      },
    },
  },
});
