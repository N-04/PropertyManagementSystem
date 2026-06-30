// 文件说明：后端菜单异常时使用的本地兜底菜单，保持与当前后台 UI 分组一致。
export type AppMenuItem = {
    id: string | number
    title: string
    path?: string
    hidden?: boolean
    menu_type?: number
    children?: AppMenuItem[]
}

const item = (
    id: string,
    title: string,
    path?: string,
    children: AppMenuItem[] = [],
    hidden = false
): AppMenuItem => {
    // 本地菜单节点保持和后端菜单相同字段，布局层可以无差别渲染。
    return {
        id,
        title,
        path,
        hidden,
        menu_type: 1,
        children,
    }
}

export const appMenuTitle = '社区物业管理系统'

// 兜底菜单分块：后端菜单接口失败时，仍按角色展示最小可用业务入口。
export const fallbackMenus: AppMenuItem[] = [
    item('admin', '管理员', undefined, [
        item('admin-dashboard', '运营工作台', '/dashboard'),
        item('admin-users', '用户管理', undefined, [
            item('admin-user-list', '账号管理', '/user/list'),
            item('admin-owner-list', '业主管理', '/owner/list'),
            item('admin-role-list', '角色配置', '/role/list'),
        ]),
        item('admin-community', '小区资源', undefined, [
            item('admin-community-list', '小区信息', '/community/list'),
            item('admin-building-list', '楼栋管理', '/building/list'),
            item('admin-unit-list', '单元管理', '/unit/list'),
            item('admin-house-list', '房屋管理', '/house/list'),
        ]),
        item('admin-visitor', '访客通行', undefined, [
            item('admin-visitor-list', '访客列表', '/visitor/list'),
            item('admin-visitor-create', '访客登记', '/visitor/create'),
        ]),
        item('admin-parking', '车位管理', undefined, [
            item('admin-owner-parking', '业主车位', '/parking/list?parking_view=owner'),
            item('admin-visitor-parking', '访客临停', '/parking/list?parking_view=visitor'),
            item('admin-car-list', '车辆管理', '/car/list'),
        ]),
        item('admin-repair', '工单中心', undefined, [
            item('admin-repair-list', '报修工单', '/repair/list'),
            item('admin-repair-finished', '完成验收', '/repair/list?status=finished'),
        ]),
        item('admin-fee', '收费管理', undefined, [
            item('admin-fee-list', '费用账单', '/fee/list'),
            item('admin-fee-record', '缴费记录', '/fee/list?status=paid'),
            item('admin-fee-overdue', '欠费提醒', '/fee/list?status=unpaid'),
        ]),
        item('admin-notice-list', '公告通知', '/notice/list'),
        item('admin-complaint', '投诉建议', undefined, [
            item('admin-complaint-list', '投诉建议', '/complaint/list'),
        ]),
        item('admin-setting', '系统设置', undefined, [
            item('admin-operation-log', '操作日志', '/log/list'),
            item('admin-login-log', '登录日志', '/log/login/list'),
        ]),
    ]),
    item('finance', '财务人员', undefined, [
        item('finance-dashboard', '财务工作台', '/dashboard'),
        item('finance-fee', '费用管理', undefined, [
            item('finance-fee-list', '账单管理', '/fee/list'),
        ]),
        item('finance-record', '缴费记录', undefined, [
            item('finance-paid-record', '收款记录', '/fee/list?status=paid'),
        ]),
        item('finance-profile', '个人中心', undefined, [
            item('finance-profile-page', '个人资料', '/profile'),
            item('finance-profile-password', '修改密码', '/profile/password'),
        ]),
    ]),
    item('repairer', '维修员', undefined, [
        item('repair-dashboard', '维修工作台', '/dashboard'),
        item('repair-history', '工单历史', '/repair/list'),
        item('repair-profile', '个人中心', '/profile'),
    ]),
    item('owner', '业主', undefined, [
        item('owner-dashboard', '业主首页', '/dashboard'),
        item('owner-profile', '个人中心', undefined, [
            item('owner-profile-page', '个人资料', '/profile'),
            item('owner-profile-password', '修改密码', '/profile/password'),
        ]),
        item('owner-house', '房产信息', undefined, [
            item('owner-house-list', '我的房屋', '/house/list'),
        ]),
        item('owner-parking', '车位信息', undefined, [
            item('owner-parking-owner', '我的车位', '/parking/list?parking_view=owner'),
            item('owner-parking-purchase', '购买车位', '/parking/list?parking_view=owner&parking_mode=available'),
        ]),
        item('owner-pay', '缴费中心', undefined, [
            item('owner-fee-list', '在线缴费', '/fee/list'),
            item('owner-fee-record', '缴费记录', '/fee/list?status=paid'),
        ]),
        item('owner-repair', '在线报修', undefined, [
            item('owner-repair-create', '提交报修', '/repair/create'),
            item('owner-repair-list', '报修进度', '/repair/list'),
        ]),
        item('owner-complaint', '在线投诉', undefined, [
            item('owner-complaint-create', '提交投诉', '/complaint/create'),
            item('owner-complaint-list', '投诉进度', '/complaint/list'),
        ]),
        item('owner-notice-list', '公告活动', '/notice/list'),
    ]),
]
