import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig(({ mode }) => {
  const isDev = mode === 'development';

  return {
    plugins: [react()],
    ...(isDev
      ? {
          // ✅ 개발 환경 설정
          server: {
            host: '0.0.0.0',
            port: 5173,
            hmr: {
              clientPort: 24678,
            },
          },
        }
      : {
          // ✅ 운영 환경 설정
          build: {
            outDir: 'dist',
            emptyOutDir: true,
            sourcemap: false,
            rollupOptions: {
              input: path.resolve(__dirname, 'index.html'),
            },
          },
        }),
  };
});
