import { createRouter, createWebHistory } from 'vue-router'
import { isCustomerServiceRole } from '@/api/menu'

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

    // 客服即时通讯工作台：登录后独立展示，不使用后台侧边栏。
    {
        path: '/service/chat',
        component: () => import('@/views/message/CustomerServiceChat.vue'),
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
                path: 'permission/list',
                component: () => import('@/views/permission/list/PermissionList.vue'),
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
                path: 'message/center',
                component: () => import('@/views/message/MessageCenter.vue'),
            },
            {
                path: 'contact/service',
                component: () => import('@/views/contact/ContactService.vue'),
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

// 路由拦截，未登录不允许进入后台。
router.beforeEach((to) => {
    const token = localStorage.getItem('token')
    const role = localStorage.getItem('role') || ''

    const publicPaths = ['/login', '/register', '/forgot-password']

    if (publicPaths.includes(to.path)) {
        return true
    }

    if (!token) {
        return '/login'
    }

    if (isCustomerServiceRole(role) && to.path !== '/service/chat') {
        return '/service/chat'
    }

    return true
})

export default router
