import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Use backend:8000 in Docker, localhost:8000 for local dev
const backendUrl = process.env.VITE_API_URL || 'http://localhost:8000';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: backendUrl,
        changeOrigin: true,
      },
      '/health': {
        target: backendUrl,
        changeOrigin: true,
      },
    },
  },
});
