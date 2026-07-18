import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = fileURLToPath(new URL('.', import.meta.url));

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
      // two entries: index.html is the classic report view (the landing page);
      // app.html is the interactive React explorer.
      input: {
        main: resolve(here, 'index.html'),
        app: resolve(here, 'app.html'),
      },
      output: {
        manualChunks: {
          echarts: ['echarts/core', 'echarts/charts', 'echarts/components', 'echarts/features', 'echarts/renderers'],
          react: ['react', 'react-dom'],
        },
      },
    },
  },
});
