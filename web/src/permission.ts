// 文件说明：前端路由权限控制入口。
import router from './router'
import { getStoredToken } from '@/utils/authState'

router.beforeEach((to, from) => {
    const token = getStoredToken()
    const whiteList = ['/login', '/register']

    if (whiteList.includes(to.path)) {
        return true
    }

    if (!token) {
        return '/login'
    }

    return true
})
