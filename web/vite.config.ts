// 文件说明：Vite 构建和开发服务器配置。
import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
    plugins: [vue()],
    build: {
        chunkSizeWarningLimit: 1000,
        rollupOptions: {
            output: {
                manualChunks(id) {
                    // 构建拆包分块：把体积稳定的第三方库拆出业务页面，降低首屏主包和工作台包体积。
                    if (!id.includes('node_modules')) {
                        return undefined
                    }

                    if (id.includes('echarts')) {
                        return 'vendor-echarts'
                    }

                    if (id.includes('element-plus') || id.includes('@element-plus')) {
                        return 'vendor-element-plus'
                    }

                    if (id.includes('/vue') || id.includes('vue-router') || id.includes('pinia')) {
                        return 'vendor-vue'
                    }

                    return 'vendor'
                },
            },
        },
    },
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url)),
        },
    },
})
