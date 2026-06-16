// 文件说明：封装 src/api/menu.ts 对应后端接口请求，供页面组件调用。菜单过滤，根据登录角色显示菜单
import request from '@/utils/request'
import type { AppMenuItem } from '@/menu/fallbackMenus'

export function getUserMenus() {
    return request.get('/user/menus/')
}

export function getMenuList() {
    return request.get('/menu/list/')
}

export function getMenuTree() {
    return request.get('/menu/tree/')
}

const adminMenuIds = ['auth', 'rbac', 'admin', 'finance', 'repairer', 'owner', 'contact-service', 'message', 'file', 'security']
const adminMenuRule: RoleMenuRule = {
    allow: adminMenuIds,
}

type RoleMenuRule = {
    allow: string[]
    deny?: string[]
}

const roleMenuMap: Record<string, RoleMenuRule> = {
    admin: adminMenuRule,

    super_admin: {
        allow: adminMenuIds,
    },

    property_admin: {
        allow: ['rbac-user', 'rbac-role', 'rbac-permission', 'admin', 'contact-service'],
        deny: ['admin-super'],
    },

    finance_staff: {
        allow: ['finance', 'message', 'contact-service'],
    },

    finance: {
        allow: ['finance', 'message', 'contact-service'],
    },

    customer_service: {
        allow: ['message'],
    },

    service: {
        allow: ['message'],
    },

    repair_staff: {
        allow: ['repairer', 'message', 'contact-service'],
    },

    repair: {
        allow: ['repairer', 'message', 'contact-service'],
    },

    owner: {
        allow: ['owner', 'contact-service'],
    },
}

const isMatchedMenuId = (id: string, ruleIds: string[]) => {
    return ruleIds.some((ruleId) => id === ruleId || id.startsWith(`${ruleId}-`))
}

const filterMenuChildrenByRule = (menus: AppMenuItem[], rule: RoleMenuRule): AppMenuItem[] => {
    return menus
        .filter((menu) => {
            const id = String(menu.id)

            if (rule.deny && isMatchedMenuId(id, rule.deny)) {
                return false
            }

            return isMatchedMenuId(id, rule.allow)
        })
        .map((menu) => ({
            ...menu,
            children: filterMenuChildrenByRule(menu.children || [], rule),
        }))
}

export function filterMenusByRole(menus: AppMenuItem[], role: string): AppMenuItem[] {
    if (!role) {
        return menus
    }

    const rule = roleMenuMap[role] ?? adminMenuRule

    return filterMenuChildrenByRule(menus, rule)
}

const hiddenMenuIds = [
    'rbac-menu',
    'rbac-api',
    'admin-super-monitor',
    'file-oss',
    'file-security',
]

const adminRoles = ['admin', 'super_admin', 'property_admin']
const repairRoles = ['repair_staff', 'repairer', 'repair']
const financeRoles = ['finance_staff', 'finance']
const customerServiceRoles = ['customer_service', 'service']

const leafMenu = (id: string, title: string, path: string, children: AppMenuItem[] = []): AppMenuItem => {
    return {
        id,
        title,
        path,
        menu_type: 1,
        children,
    }
}

const cloneMenu = (menu: AppMenuItem): AppMenuItem => {
    return {
        ...menu,
        children: (menu.children || []).map(cloneMenu),
    }
}

const findMenuById = (menus: AppMenuItem[], id: string): AppMenuItem | undefined => {
    for (const menu of menus) {
        if (String(menu.id) === id) {
            return menu
        }

        const child = findMenuById(menu.children || [], id)

        if (child) {
            return child
        }
    }

    return undefined
}

const removeHiddenMenus = (menus: AppMenuItem[]): AppMenuItem[] => {
    return menus
        .filter((menu) => !hiddenMenuIds.includes(String(menu.id)))
        .map((menu) => ({
            ...menu,
            children: removeHiddenMenus(menu.children || []),
        }))
}

const getMenu = (menus: AppMenuItem[], id: string) => {
    const menu = findMenuById(menus, id)
    return menu ? cloneMenu(menu) : undefined
}

const messageMenu = () => {
    return leafMenu('role-message-center', '消息通知', '/message/center')
}

const noticePublishMenu = () => {
    // 财务和维修只发布相关公告，不进入消息中心接收公告。
    return leafMenu('role-notice-publish', '消息通知', '/notice/list')
}

const contactServiceMenu = () => {
    // 联系客服作为独立侧边栏模块，非客服角色可以从这里发起会话。
    return leafMenu('role-contact-service', '联系客服', '/contact/service')
}

const adminDisplayMenus = (menus: AppMenuItem[], role: string): AppMenuItem[] => {
    const scopedMenus = filterMenusByRole(removeHiddenMenus(menus), role)
    const adminModule = getMenu(scopedMenus, 'admin') || leafMenu('role-admin-module', '管理员模块', '/dashboard')

    adminModule.id = 'role-admin-module'
    adminModule.title = '管理员模块'

    return [
        leafMenu('role-user-list', '用户列表', '/user/list'),
        leafMenu('role-role-list', '角色列表', '/role/list'),
        leafMenu('role-repair-list', '报修列表', '/repair/list'),
        leafMenu('role-permission-list', '权限管理', '/permission/list'),
        adminModule,
        contactServiceMenu(),
    ]
}

export function isCustomerServiceRole(role: string) {
    return customerServiceRoles.includes(role)
}

export function buildDisplayMenusByRole(menus: AppMenuItem[], role: string): AppMenuItem[] {
    const cleanedMenus = removeHiddenMenus(menus)

    if (customerServiceRoles.includes(role)) {
        return []
    }

    if (adminRoles.includes(role)) {
        return adminDisplayMenus(cleanedMenus, role)
    }

    if (repairRoles.includes(role)) {
        return [
            leafMenu('role-repair-list', '报修列表', '/repair/list'),
            noticePublishMenu(),
            contactServiceMenu(),
        ]
    }

    if (financeRoles.includes(role)) {
        const financeMenu = getMenu(filterMenusByRole(cleanedMenus, role), 'finance')
            || leafMenu('role-finance', '财务人员模块', '/fee/list')

        financeMenu.title = '财务人员模块'

        return [
            financeMenu,
            noticePublishMenu(),
            contactServiceMenu(),
        ]
    }

    if (role === 'owner') {
        const ownerMenu = getMenu(filterMenusByRole(cleanedMenus, role), 'owner')
            || leafMenu('role-owner', '业主模块', '/dashboard')

        ownerMenu.title = '业主模块'

        return [ownerMenu, contactServiceMenu()]
    }

    return filterMenusByRole(cleanedMenus, role)
}
