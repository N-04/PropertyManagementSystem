// 文件说明：根据社区物业管理系统大纲提供本地菜单树。
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

export const fallbackMenus: AppMenuItem[] = [
    item('rbac', 'RBAC权限管理模块', undefined, [
        item('rbac-user', '用户管理', '/user/list'),
        item('rbac-role', '角色管理', '/role/list'),
        item('rbac-permission', '权限管理', '/permission/list'),
        item('rbac-menu', '菜单管理', '/menu/list'),
        item('rbac-api', '接口权限', '/permission/list'),
    ]),
    item('admin', '管理员模块', undefined, [
        item('admin-super', '超级管理员', undefined, [
            item('admin-super-config', '系统配置'),
            item('admin-super-permission', '权限分配', '/role/list'),
            item('admin-super-manager', '管理员管理', '/user/list'),
            item('admin-super-backup', '数据备份'),
            item('admin-super-audit-log', '日志审计', '/log/list'),
            item('admin-super-monitor', '系统监控', '/dashboard'),
        ]),
        item('admin-property', '物业管理员', undefined, [
            item('admin-property-user', '用户管理', undefined, [
                item('admin-property-owner', '业主管理', '/owner/list'),
                item('admin-property-repairer', '维修员管理', '/user/list'),
                item('admin-property-service', '客服人员管理', '/user/list'),
                item('admin-property-finance', '财务人员管理', '/user/list'),
                item('admin-property-realname', '实名认证审核', '/user/list'),
            ]),
            item('admin-property-community', '小区管理', undefined, [
                item('admin-property-community-info', '小区信息', '/community/list'),
                item('admin-property-building', '楼栋管理', '/building/list'),
                item('admin-property-unit', '单元管理', '/unit/list'),
                item('admin-property-house', '房屋管理', '/house/list'),
                item('admin-property-house-bind', '房产绑定', '/owner/list'),
            ]),
            item('admin-property-parking', '车位管理', undefined, [
                item('admin-property-parking-info', '车位信息', '/parking/list'),
                item('admin-property-parking-bind', '车位绑定', '/parking/list'),
                item('admin-property-parking-status', '车位状态', '/parking/list'),
                item('admin-property-parking-temp', '临时停车', '/parking/list'),
            ]),
            item('admin-property-work-order', '工单管理', undefined, [
                item('admin-property-repair-order', '报修工单', '/repair/list'),
                item('admin-property-dispatch', '派单管理', '/repair/list'),
                item('admin-property-order-status', '工单状态', '/repair/list'),
                item('admin-property-order-rate', '工单评价', '/repair/list'),
                item('admin-property-order-stat', '工单统计', '/dashboard'),
            ]),
            item('admin-property-notice', '公告管理', undefined, [
                item('admin-property-community-notice', '小区公告', '/notice/list'),
                item('admin-property-activity', '活动通知', '/notice/list'),
                item('admin-property-push', '消息推送', '/notice/list'),
            ]),
            item('admin-property-complaint', '投诉管理', undefined, [
                item('admin-property-complaint-handle', '投诉处理', '/complaint/list'),
                item('admin-property-feedback', '建议反馈', '/complaint/list'),
                item('admin-property-return-visit', '回访记录', '/complaint/list'),
            ]),
            item('admin-property-stat', '数据统计', undefined, [
                item('admin-property-user-stat', '用户统计', '/dashboard'),
                item('admin-property-fee-stat', '收费统计', '/dashboard'),
                item('admin-property-repair-stat', '工单统计', '/dashboard'),
                item('admin-property-chart', '可视化报表（优先显示在首页）', '/dashboard'),
            ]),
        ]),
    ]),
    item('finance', '财务人员模块', undefined, [
        item('finance-fee', '物业费管理', '/fee/list'),
        item('finance-water', '水费管理', '/fee/list'),
        item('finance-electric', '电费管理', '/fee/list'),
        item('finance-parking', '停车费管理', '/fee/list'),
        item('finance-pay', '在线支付', '/fee/list'),
        item('finance-record', '缴费记录', '/fee/list'),
        item('finance-arrears', '欠费提醒', '/fee/list'),
        item('finance-report', '财务报表', '/dashboard'),
        item('finance-income', '收入统计', '/dashboard'),
    ]),
    item('repairer', '维修员模块', undefined, [
        item('repairer-home', '首页', '/dashboard'),
        item('repairer-work-order', '工单管理', '/repair/list', [
            item('repairer-pending', '待接单工单', '/repair/list'),
            item('repairer-accepted', '已接单工单', '/repair/list'),
            item('repairer-fixing', '维修中工单', '/repair/list'),
            item('repairer-finished', '完成工单', '/repair/list'),
            item('repairer-history', '工单历史', '/repair/list'),
        ]),
        item('repairer-upload-image', '上传维修图片', '/repair/list'),
        item('repairer-upload-result', '上传维修结果', '/repair/list'),
        item('repairer-profile', '个人中心', '/profile'),
    ]),
    item('owner', '业主模块', undefined, [
        item('owner-home', '首页', '/dashboard', [
            item('owner-home-notice', '公告通知', '/notice/list'),
            item('owner-home-activity', '小区活动', '/notice/list'),
            item('owner-home-fee', '代缴费用', '/fee/list'),
            item('owner-home-message', '消息提醒', '/message/center'),
        ]),
        item('owner-profile', '个人中心', '/profile', [
            item('owner-realname', '实名认证', '/profile'),
            item('owner-phone', '手机号修改', '/profile'),
            item('owner-id-card-mask', '身份证脱敏显示', '/profile'),
            item('owner-password', '修改密码', '/profile'),
            item('owner-avatar', '头像上传', '/profile'),
        ]),
        item('owner-house', '房产信息', '/house/list', [
            item('owner-house-my', '我的房屋', '/house/list'),
            item('owner-house-auth', '房产认证', '/owner/list'),
            item('owner-house-family', '家庭成员', '/owner/list'),
            item('owner-house-detail', '房屋详情', '/house/list'),
        ]),
        item('owner-parking', '车位信息', '/parking/list', [
            item('owner-parking-my', '我的车位', '/parking/list'),
            item('owner-parking-record', '停车记录', '/parking/list'),
            item('owner-parking-pay', '停车缴费', '/fee/list'),
        ]),
        item('owner-pay-center', '缴费中心', '/fee/list', [
            item('owner-pay-property', '物业费缴纳', '/fee/list'),
            item('owner-pay-water', '水费缴纳', '/fee/list'),
            item('owner-pay-electric', '电费缴纳', '/fee/list'),
            item('owner-pay-parking', '停车费缴纳', '/fee/list'),
            item('owner-pay-online', '在线支付', '/fee/list'),
            item('owner-pay-record', '缴费记录', '/fee/list'),
        ]),
        item('owner-repair', '在线报修', '/repair/list', [
            item('owner-repair-submit', '提交报修', '/repair/create'),
            item('owner-repair-upload', '上传图片', '/repair/create'),
            item('owner-repair-progress', '工单进度', '/repair/list'),
            item('owner-repair-rate', '维修评价', '/repair/list'),
            item('owner-repair-history', '历史报修', '/repair/list'),
        ]),
        item('owner-complaint', '在线投诉', undefined, [
            item('owner-complaint-submit', '提交投诉', '/complaint/create'),
            item('owner-complaint-progress', '投诉进度', '/complaint/list'),
            item('owner-complaint-result', '结果反馈', '/complaint/list'),
            item('owner-complaint-history', '历史投诉', '/complaint/list'),
        ]),
        item('owner-message', '消息中心', '/message/center', [
            item('owner-message-system', '系统通知', '/message/center'),
            item('owner-message-fee', '缴费提醒', '/message/center'),
            item('owner-message-work-order', '工单通知', '/message/center'),
            item('owner-message-activity', '活动通知', '/message/center'),
        ]),
    ]),
    item('contact-service', '联系客服', '/contact/service'),
    item('message', '消息通知模块', undefined, [
        item('message-sms', '短信通知'),
        item('message-notice', '系统公告', '/notice/list'),
        item('message-work-order', '工单通知', '/repair/list'),
        item('message-fee', '缴费提醒', '/fee/list'),
        item('message-websocket', 'WebSocket实时通知'),
        item('message-mail', '站内信通知', '/message/center'),
    ]),
    item('file', '文件管理模块', undefined, [
        item('file-image', '图片上传', '/upload/test'),
        item('file-id-card', '身份证上传', '/upload/test'),
        item('file-repair-image', '工单图片上传', '/upload/test'),
        item('file-oss', 'OSS对象存储', '/upload/test'),
        item('file-security', '文件安全校验', '/upload/test'),
    ]),
    item('security', '系统安全模块', undefined, [
        item('security-jwt', 'JWT认证'),
        item('security-redis', 'Redis缓存'),
        item('security-limit', '接口限流'),
        item('security-sql', 'SQL注入防护'),
        item('security-xss', 'XSS防护'),
        item('security-csrf', 'CSRF防护'),
        item('security-mask', '敏感数据脱敏'),
        item('security-audit-log', '操作审计日志', '/log/list'),
        item('security-exception', '异常监控', '/dashboard'),
    ]),
]
