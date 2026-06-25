import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// The frontend calls the backend at http://localhost:5000 directly (CORS is enabled
// on the backend). A dev proxy for /api is also provided in case you switch the
// frontend to relative URLs.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
    },
  },
});
