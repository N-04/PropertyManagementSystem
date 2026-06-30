// 文件说明：维护前端全局状态和跨页面共享数据。
import { defineStore } from 'pinia'

import { getUserMenus } from '@/api/menu'

export const useMenuStore = defineStore('menu', {
    // 菜单状态分块：后端返回的角色菜单作为布局和路由兜底判断的单一来源。
    state: () => ({
        menus: [] as any[],
    }),

    actions: {
        async loadMenus() {
            const res = await getUserMenus()

            // 接口层保持原始树结构，具体可见性过滤交给布局和菜单组件处理。
            this.menus = res.data.data
        },
    },
})
