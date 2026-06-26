import { createRouter, createWebHistory } from 'vue-router'
import { appMenuTitle } from '@/menu/fallbackMenus'
import {
    AUTH_STATE_CHANGED_EVENT,
    getStoredRole,
    getStoredToken,
} from '@/utils/authState'

const routes = [
    // 登录页：系统入口，不显示后台菜单
    {
        path: '/login',
        component: () => import('@/views/login/LoginPage.vue'),
        meta: {
            public: true,
        },
    },

    // 注册页：系统入口，不显示后台菜单
    {
        path: '/register',
        component: () => import('@/views/register/RegisterPage.vue'),
        meta: {
            public: true,
        },
    },

    // 找回密码：系统入口，不显示后台菜单
    {
        path: '/forgot-password',
        component: () => import('@/views/login/ForgotPassword.vue'),
        meta: {
            public: true,
        },
    },

    // 后台系统：登录后才显示菜单
    {
        path: '/',
        component: () => import('@/layout/LayoutPage.vue'),
        redirect: '/dashboard',
        children: [
            {
                path: 'dashboard',
                component: () => import('@/views/dashboard/DashboardPage.vue'),
            },
            {
                path: 'user/list',
                component: () => import('@/views/user/list/UserList.vue'),
            },
            {
                path: 'user/create',
                component: () => import('@/views/user/create/UserCreate.vue'),
            },
            {
                path: 'user/edit/:id',
                component: () => import('@/views/user/edit/UserEdit.vue'),
            },
            {
                path: 'role/list',
                component: () => import('@/views/role/list/RoleList.vue'),
            },
            {
                path: 'role/create',
                component: () => import('@/views/role/create/RoleCreate.vue'),
            },
            {
                path: 'role/edit/:id',
                component: () => import('@/views/role/edit/RoleEdit.vue'),
            },
            {
                path: 'menu/list',
                component: () => import('@/views/menu/MenuList.vue'),
            },
            {
                path: 'community/list',
                component: () => import('@/views/community/list/CommunityList.vue'),
            },
            {
                path: 'building/list',
                component: () => import('@/views/building/list/BuildingList.vue'),
            },
            {
                path: 'building/create',
                component: () => import('@/views/building/create/BuildingCreate.vue'),
            },
            {
                path: 'unit/list',
                component: () => import('@/views/unit/list/UnitList.vue'),
            },
            {
                path: 'house/list',
                component: () => import('@/views/house/list/HouseList.vue'),
            },
            {
                path: 'house/create',
                component: () => import('@/views/house/create/HouseCreate.vue'),
            },
            {
                path: 'owner/list',
                component: () => import('@/views/owner/list/OwnerList.vue'),
            },
            {
                path: 'owner/create',
                component: () => import('@/views/owner/create/OwnerCreate.vue'),
            },
            {
                path: 'owner/detail/:id',
                component: () => import('@/views/owner/detail/OwnerDetail.vue'),
            },
            {
                path: 'owner/edit/:id',
                component: () => import('@/views/owner/edit/OwnerEdit.vue'),
            },
            {
                path: 'parking/list',
                component: () => import('@/views/parking/list/ParkingList.vue'),
            },
            {
                path: 'parking/create',
                component: () => import('@/views/parking/create/ParkingCreate.vue'),
            },
            {
                path: 'parking/edit/:id',
                component: () => import('@/views/parking/edit/ParkingEdit.vue'),
            },
            {
                path: 'car/list',
                component: () => import('@/views/car/list/CarList.vue'),
            },
            {
                path: 'car/create',
                component: () => import('@/views/car/create/CarCreate.vue'),
            },
            {
                path: 'car/detail/:id',
                component: () => import('@/views/car/detail/CarDetail.vue'),
            },
            {
                path: 'car/edit/:id',
                component: () => import('@/views/car/edit/CarEdit.vue'),
            },
            {
                path: 'repair/list',
                component: () => import('@/views/repair/list/RepairList.vue'),
            },
            {
                path: 'repair/create',
                component: () => import('@/views/repair/create/RepairCreate.vue'),
            },
            {
                path: 'repair/detail/:id',
                component: () => import('@/views/repair/detail/RepairDetail.vue'),
            },
            {
                path: 'repair/edit/:id',
                component: () => import('@/views/repair/edit/RepairEdit.vue'),
            },
            {
                path: 'repair/assign/:id',
                component: () => import('@/views/repair/assign/RepairAssign.vue'),
            },
            {
                path: 'complaint/list',
                component: () => import('@/views/complaint/list/ComplaintList.vue'),
            },
            {
                path: 'complaint/create',
                component: () => import('@/views/complaint/create/ComplaintCreate.vue'),
            },
            {
                path: 'fee/list',
                component: () => import('@/views/fee/list/FeeList.vue'),
            },
            {
                path: 'fee/create',
                component: () => import('@/views/fee/create/FeeCreate.vue'),
            },
            {
                path: 'notice/list',
                component: () => import('@/views/notice/list/NoticeList.vue'),
            },
            {
                path: 'notice/create',
                component: () => import('@/views/notice/create/NoticeCreate.vue'),
            },
            {
                path: 'notice/edit/:id',
                component: () => import('@/views/notice/edit/NoticeEdit.vue'),
            },
            {
                path: 'visitor/list',
                component: () => import('@/views/visitor/list/VisitorList.vue'),
            },
            {
                path: 'visitor/create',
                component: () => import('@/views/visitor/create/VisitorCreate.vue'),
            },
            {
                path: 'visitor/detail/:id',
                component: () => import('@/views/visitor/detail/VisitorDetail.vue'),
            },
            {
                path: 'visitor/edit/:id',
                component: () => import('@/views/visitor/edit/VisitorEdit.vue'),
            },
            {
                path: 'visitor/approve/:id',
                component: () => import('@/views/visitor/approve/VisitorApprove.vue'),
            },
            {
                path: 'profile',
                component: () => import('@/views/profile/ProfilePage.vue'),
            },
            {
                path: 'profile/password',
                component: () => import('@/views/profile/ProfilePage.vue'),
            },
            {
                path: 'message/center',
                component: () => import('@/views/message/MessageCenter.vue'),
            },
            {
                path: 'upload',
                component: () => import('@/views/upload/Upload.vue'),
            },
            {
                path: 'upload/test',
                component: () => import('@/views/upload/UploadTest.vue'),
            },
            {
                path: 'log/list',
                component: () => import('@/views/log/list/OperationLogList.vue'),
            },
            {
                path: 'log/login/list',
                component: () => import('@/views/log/login/list/LoginLogList.vue'),
            },
        ],
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

const roleTitleMap: Record<string, string> = {
    admin: '管理员',
    super_admin: '超级管理员',
    property_admin: '物业管理员',
    finance_staff: '财务人员',
    finance: '财务人员',
    repair_staff: '维修员',
    repairer: '维修员',
    repair: '维修员',
    owner: '业主',
}

const routeTitleMap: Record<string, string> = {
    '/dashboard': '首页',
    '/user/list': '用户列表',
    '/user/create': '新增用户',
    '/role/list': '角色列表',
    '/role/create': '新增角色',
    '/community/list': '小区信息',
    '/building/list': '楼栋管理',
    '/unit/list': '单元管理',
    '/house/list': '房产信息',
    '/owner/list': '业主管理',
    '/parking/list': '车位管理',
    '/parking/create': '新增车位',
    '/car/list': '车辆管理',
    '/repair/list': '报修列表',
    '/repair/create': '提交报修',
    '/complaint/list': '投诉列表',
    '/complaint/create': '提交投诉',
    '/fee/list': '费用管理',
    '/fee/create': '新增账单',
    '/notice/list': '公告通知',
    '/notice/create': '发布公告',
    '/visitor/list': '访客管理',
    '/profile': '个人中心',
    '/profile/password': '修改密码',
    '/message/center': '消息中心',
    '/upload': '文件上传',
    '/upload/test': '文件上传',
    '/log/list': '操作审计日志',
    '/log/login/list': '登录日志',
}

const publicTitleMap: Record<string, string> = {
    '/login': '登录',
    '/register': '注册',
    '/forgot-password': '找回密码',
}

const normalizePath = (path: string) => {
    return path.replace(/\/\d+(?=\/|$)/g, '/:id')
}

const getModuleTitle = (path: string) => {
    const normalizedPath = normalizePath(path)

    if (routeTitleMap[path]) {
        return routeTitleMap[path]
    }

    if (normalizedPath.includes('/edit/:id')) {
        return '编辑信息'
    }

    if (normalizedPath.includes('/detail/:id')) {
        return '详情'
    }

    if (normalizedPath.includes('/assign/:id')) {
        return '派单管理'
    }

    if (normalizedPath.includes('/approve/:id')) {
        return '审核'
    }

    return '后台'
}

const updateBrowserTitle = (path: string) => {
    if (publicTitleMap[path]) {
        document.title = `${publicTitleMap[path]} - ${appMenuTitle}`
        return
    }

    const role = getStoredRole()
    const roleTitle = roleTitleMap[role] || '用户'
    const moduleTitle = getModuleTitle(path)

    // 浏览器标签展示当前角色和访问模块，方便多角色、多页面调试和使用。
    document.title = `${roleTitle} - ${moduleTitle}`
}

export const refreshBrowserTitle = () => {
    updateBrowserTitle(router.currentRoute.value.path)
}

if (typeof window !== 'undefined') {
    window.addEventListener(AUTH_STATE_CHANGED_EVENT, refreshBrowserTitle)
}

// 路由拦截，未登录不允许进入后台。
router.beforeEach((to) => {
    const token = getStoredToken()

    const publicPaths = ['/login', '/register', '/forgot-password']

    if (publicPaths.includes(to.path)) {
        return true
    }

    if (!token) {
        return '/login'
    }

    return true
})

router.afterEach((to) => {
    updateBrowserTitle(to.path)
})

export default router
