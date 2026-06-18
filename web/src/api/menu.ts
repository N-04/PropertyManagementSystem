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

const adminMenuIds = ['admin', 'finance', 'repairer', 'owner', 'message', 'file', 'security']
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
        allow: ['admin'],
        deny: ['admin-super'],
    },

    finance_staff: {
        allow: ['finance', 'message'],
    },

    finance: {
        allow: ['finance', 'message'],
    },

    customer_service: {
        allow: ['message'],
    },

    service: {
        allow: ['message'],
    },

    repair_staff: {
        allow: ['repairer', 'message'],
    },

    repair: {
        allow: ['repairer', 'message'],
    },

    owner: {
        allow: ['owner'],
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
    const rule = roleMenuMap[role]

    if (!rule) {
        return []
    }

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

const groupMenu = (id: string, title: string, children: AppMenuItem[] = []): AppMenuItem => {
    return {
        id,
        title,
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

const adminDisplayMenus = (): AppMenuItem[] => {
    // 管理员后台使用面向实际工作的 UI 分组，不再按 XMind 节点逐条平铺。
    return [
        leafMenu('admin-dashboard', '运营工作台', '/dashboard'),
        groupMenu('admin-users', '用户管理', [
            leafMenu('admin-user-list', '账号管理', '/user/list'),
            leafMenu('admin-owner-list', '业主管理', '/owner/list'),
            leafMenu('admin-role-list', '角色配置', '/role/list'),
        ]),
        groupMenu('admin-community', '小区资源', [
            leafMenu('admin-community-list', '小区信息', '/community/list'),
            leafMenu('admin-building-list', '楼栋管理', '/building/list'),
            leafMenu('admin-unit-list', '单元管理', '/unit/list'),
            leafMenu('admin-house-list', '房屋管理', '/house/list'),
        ]),
        groupMenu('admin-visitor', '访客通行', [
            leafMenu('admin-visitor-list', '访客列表', '/visitor/list'),
            leafMenu('admin-visitor-create', '访客登记', '/visitor/create'),
        ]),
        groupMenu('admin-parking', '车位管理', [
            leafMenu('admin-owner-parking', '业主车位', '/parking/list?parking_view=owner'),
            leafMenu('admin-visitor-parking', '访客临停', '/parking/list?parking_view=visitor'),
            leafMenu('admin-car-list', '车辆管理', '/car/list'),
        ]),
        groupMenu('admin-repair', '工单中心', [
            leafMenu('admin-repair-list', '报修工单', '/repair/list'),
            leafMenu('admin-repair-dispatch', '派单处理', '/repair/list?status=assigned'),
            leafMenu('admin-repair-finished', '完成验收', '/repair/list?status=finished'),
        ]),
        groupMenu('admin-fee', '收费管理', [
            leafMenu('admin-fee-list', '费用账单', '/fee/list'),
            leafMenu('admin-fee-record', '缴费记录', '/fee/list?status=paid'),
            leafMenu('admin-fee-overdue', '欠费提醒', '/fee/list?status=unpaid'),
        ]),
        leafMenu('admin-notice-list', '公告通知', '/notice/list'),
        groupMenu('admin-complaint', '投诉建议', [
            leafMenu('admin-complaint-list', '投诉建议', '/complaint/list'),
        ]),
        groupMenu('admin-setting', '系统设置', [
            leafMenu('admin-operation-log', '操作日志', '/log/list'),
            leafMenu('admin-login-log', '登录日志', '/log/login/list'),
        ]),
    ]
}

const financeDisplayMenus = (): AppMenuItem[] => [
    leafMenu('finance-dashboard', '财务工作台', '/dashboard'),
    groupMenu('finance-fee', '费用管理', [
        leafMenu('finance-fee-list', '账单管理', '/fee/list'),
        leafMenu('finance-fee-unpaid', '待缴账单', '/fee/list?status=unpaid'),
    ]),
    groupMenu('finance-record', '缴费记录', [
        leafMenu('finance-paid-record', '收款记录', '/fee/list?status=paid'),
    ]),
    groupMenu('finance-overdue', '欠费提醒', [
        leafMenu('finance-overdue-list', '欠费列表', '/fee/list?status=unpaid'),
    ]),
    groupMenu('finance-report', '财务报表', [
        leafMenu('finance-dashboard-report', '收入统计', '/dashboard'),
    ]),
    groupMenu('finance-profile', '个人中心', [
        leafMenu('finance-profile-page', '个人资料', '/profile'),
        leafMenu('finance-profile-password', '修改密码', '/profile/password'),
    ]),
]

const repairDisplayMenus = (): AppMenuItem[] => [
    leafMenu('repair-dashboard', '维修工作台', '/dashboard'),
    groupMenu('repair-pending', '待接工单', [
        leafMenu('repairer-pending', '待接单', '/repair/list'),
    ]),
    groupMenu('repair-processing', '维修中', [
        leafMenu('repairer-accepted', '已接单', '/repair/list'),
        leafMenu('repairer-fixing', '维修中', '/repair/list'),
    ]),
    groupMenu('repair-finished', '完成工单', [
        leafMenu('repairer-finished', '完成工单', '/repair/list'),
    ]),
    groupMenu('repair-history', '工单历史', [
        leafMenu('repairer-history', '历史记录', '/repair/list'),
    ]),
    groupMenu('repair-profile', '个人中心', [
        leafMenu('repair-profile-page', '个人资料', '/profile'),
        leafMenu('repair-profile-password', '修改密码', '/profile/password'),
    ]),
]

const ownerDisplayMenus = (): AppMenuItem[] => [
    leafMenu('owner-dashboard', '业主首页', '/dashboard'),
    groupMenu('owner-profile', '个人中心', [
        leafMenu('owner-profile-page', '个人资料', '/profile'),
        leafMenu('owner-profile-password', '修改密码', '/profile/password'),
    ]),
    groupMenu('owner-house', '房产信息', [
        leafMenu('owner-house-list', '我的房屋', '/house/list'),
    ]),
    groupMenu('owner-parking', '车位信息', [
        leafMenu('owner-parking-owner', '我的车位', '/parking/list?parking_view=owner'),
        leafMenu('owner-parking-purchase', '购买车位', '/parking/list?parking_view=owner&parking_mode=available'),
    ]),
    groupMenu('owner-pay', '缴费中心', [
        leafMenu('owner-fee-list', '在线缴费', '/fee/list'),
        leafMenu('owner-fee-record', '缴费记录', '/fee/list?status=paid'),
    ]),
    groupMenu('owner-repair', '在线报修', [
        leafMenu('owner-repair-create', '提交报修', '/repair/create'),
        leafMenu('owner-repair-list', '报修进度', '/repair/list'),
    ]),
    groupMenu('owner-complaint', '在线投诉', [
        leafMenu('owner-complaint-create', '提交投诉', '/complaint/create'),
        leafMenu('owner-complaint-list', '投诉进度', '/complaint/list'),
    ]),
    leafMenu('owner-notice-list', '公告活动', '/notice/list'),
]

export function isCustomerServiceRole(role: string) {
    return customerServiceRoles.includes(role)
}

export function buildDisplayMenusByRole(menus: AppMenuItem[], role: string): AppMenuItem[] {
    const cleanedMenus = removeHiddenMenus(menus)

    if (customerServiceRoles.includes(role)) {
        return []
    }

    if (adminRoles.includes(role)) {
        return adminDisplayMenus()
    }

    if (repairRoles.includes(role)) {
        return repairDisplayMenus()
    }

    if (financeRoles.includes(role)) {
        return financeDisplayMenus()
    }

    if (role === 'owner') {
        return ownerDisplayMenus()
    }

    return filterMenusByRole(cleanedMenus, role)
}
