// 文件说明：维护前端全局状态和跨页面共享数据。
import { defineStore } from 'pinia'

import { getUserMenus } from '@/api/menu'

export const useMenuStore = defineStore('menu', {
    state: () => ({
        menus: [] as any[],
    }),

    actions: {
        async loadMenus() {
            const res = await getUserMenus()

            this.menus = res.data.data
        },
    },
})
