import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    allowedHosts: [
      ".ngrok.io",
      "srni-backend.ngrok.io"
    ],
    proxy: {
      "/api": {
        target: "http://rni_backend:8000",
        changeOrigin: true,
        secure: false,
      },
    },
  },
});
