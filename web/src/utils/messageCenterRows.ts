// 文件说明：统一生成消息中心列表数据，供页面列表和顶部消息角标共用。
import { getChatConversationList } from '@/api/chat'
import { getComplaintList } from '@/api/complaint'
import { getFeeList } from '@/api/fee'
import { getRepairList } from '@/api/repair'

export type MessageRow = {
    id: string
    type: string
    title: string
    content: string
    status: string
    created_at: string
    path: string
}

export const MESSAGE_FEEDBACK_STORAGE_KEYS = [
    'parkingPurchaseFeedback',
    'repairEvaluationFeedback',
    'serviceRatingFeedback',
]

export const MESSAGE_CENTER_REFRESH_EVENT = 'property-management-message-center-refresh'

export const MESSAGE_FEEDBACK_EVENTS = [
    'property-management-parking-feedback',
    'property-management-repair-evaluation-feedback',
    'property-management-service-rating-feedback',
    MESSAGE_CENTER_REFRESH_EVENT,
]

const adminRoles = ['admin', 'super_admin', 'property_admin']
const repairRoles = ['repair_staff', 'repairer', 'repair']

const extractList = (data: any) => {
    // 接口返回既可能是数组，也可能是分页 results；消息中心统一收敛成列表。
    if (Array.isArray(data)) {
        return data
    }

    if (Array.isArray(data?.results)) {
        return data.results
    }

    return []
}

// 角色可见性分块：消息中心只聚合当前角色能处理或应接收的业务消息。
const canSeeFee = (role: string) => {
    return ['owner', 'finance', 'finance_staff', 'admin', 'super_admin'].includes(role)
}

const canSeeRepair = (role: string) => {
    return [
        'owner',
        'repair_staff',
        'repairer',
        'repair',
        'property_admin',
        'admin',
        'super_admin',
    ].includes(role)
}

const canSeeComplaint = (role: string) => {
    return [
        'owner',
        'property_admin',
        'admin',
        'super_admin',
    ].includes(role)
}

const chatTargetPath = () => {
    // 所有站内会话统一回到消息中心，避免从铃铛入口进入旧客服页面。
    return '/message/center'
}

const feeTypeTextMap: Record<string, string> = {
    property: '物业费',
    water: '水费',
    electric: '电费',
    parking: '车位费',
    other: '其他费用',
}

const feeTypeText = (item: any) => {
    return item.fee_type_text || item.fee_type_display || feeTypeTextMap[item.fee_type] || '账单'
}

const feeStatusText = (status: string) => {
    return status === 'paid' ? '已缴费' : status === 'overdue' ? '已逾期' : '未缴费'
}

const repairStatusText = (status: string) => {
    if (status === 'finished') {
        return '已完成'
    }

    if (status === 'processing') {
        return '维修中'
    }

    if (status === 'accepted') {
        return '已接单'
    }

    return status === 'assigned' ? '待接单' : '待派单'
}

const complaintStatusText = (status: string) => {
    if (status === 'done') {
        return '已完成'
    }

    if (status === 'closed') {
        return '已关闭'
    }

    return status === 'processing' ? '处理中' : '待处理'
}

const readFeedbackItems = (storageKey: string) => {
    if (typeof window === 'undefined') {
        return []
    }

    try {
        const raw = window.localStorage.getItem(storageKey)
        const parsed = raw ? JSON.parse(raw) : null

        if (!parsed) {
            return []
        }

        return Array.isArray(parsed) ? parsed : [parsed]
    } catch {
        return []
    }
}

export const appendMessageFeedback = (storageKey: string, feedback: any) => {
    if (typeof window === 'undefined') {
        return
    }

    // 本地反馈只作为跨标签即时提醒，最多保留近期 50 条，避免长期使用后消息中心被旧缓存撑大。
    const history = readFeedbackItems(storageKey)
        .filter((item: any) => item.id !== feedback.id)
        .slice(0, 49)

    window.localStorage.setItem(storageKey, JSON.stringify([feedback, ...history]))
}

const roleMatchesTarget = (role: string, targetRole?: string) => {
    // 管理员能看到全部本地反馈；普通角色只看目标角色与自身别名匹配的反馈。
    if (adminRoles.includes(role)) {
        return true
    }

    if (!targetRole) {
        return false
    }

    const roleAliases: Record<string, string[]> = {
        finance_staff: ['finance_staff', 'finance'],
        finance: ['finance_staff', 'finance'],
        repair_staff: repairRoles,
        repairer: repairRoles,
        repair: repairRoles,
        property_admin: adminRoles,
        admin: adminRoles,
        super_admin: adminRoles,
    }

    return (roleAliases[targetRole] || [targetRole]).includes(role)
}

const feedbackRows = (role: string): MessageRow[] => {
    // 本地反馈分块：跨标签即时消息先落 localStorage，再在消息中心合并展示。
    const rows: MessageRow[] = []

    if (adminRoles.includes(role)) {
        readFeedbackItems('parkingPurchaseFeedback').forEach((item: any, index) => {
            rows.push({
                id: `parking-feedback-${item.id || index}`,
                type: '业主 → 物业管理员',
                title: '车位购买反馈',
                content: item.message || `车位 ${item.parking_no || ''} 已完成购买/绑定`,
                status: '待跟进',
                created_at: item.created_at || '',
                path: '/parking/list?parking_view=owner',
            })
        })
    }

    if (adminRoles.includes(role) || repairRoles.includes(role)) {
        readFeedbackItems('repairEvaluationFeedback').forEach((item: any, index) => {
            rows.push({
                id: `repair-evaluation-feedback-${item.id || index}`,
                type: '业主 → 维修员',
                title: item.title ? `工单评价：${item.title}` : '工单评价反馈',
                content: item.message || `用户已提交 ${item.score || '-'} 分维修评价`,
                status: '已评价',
                created_at: item.created_at || '',
                path: '/repair/list',
            })
        })
    }

    readFeedbackItems('serviceRatingFeedback')
        .filter((item: any) => roleMatchesTarget(role, item.target_role))
        .forEach((item: any, index) => {
            rows.push({
                id: `service-rating-feedback-${item.id || index}`,
                type: `业主 → ${item.target_role_text || '相关人员'}`,
                title: item.title ? `服务评分：${item.title}` : '服务评分反馈',
                content: item.message || `用户已提交 ${item.score || '-'} 分服务评分`,
                status: '已评价',
                created_at: item.created_at || '',
                path: '/message/center',
            })
        })

    return rows
}

const sortMessageRows = (rows: MessageRow[]) => {
    return rows.sort((a, b) => `${b.created_at}`.localeCompare(`${a.created_at}`))
}

export const getImmediateMessageRows = (role: string) => {
    return sortMessageRows(feedbackRows(role))
}

export const loadMessageCenterRows = async (role: string) => {
    // 接口消息分块：站内会话始终加载，其余账单/工单/投诉按角色权限追加。
    const tasks: Promise<MessageRow[]>[] = [
        (async () => {
            try {
                const res = await getChatConversationList()
                const conversations = extractList(res.data.data)

                return conversations.map((item: any) => ({
                    id: `chat-${item.id}`,
                    type: `${item.created_by_real_name || item.created_by_name || '发起人'} → ${item.target_role_text || '处理角色'}`,
                    title: item.title || `会话 #${item.id}`,
                    content: item.last_message || '暂无最新消息',
                    status: item.status_text || '沟通中',
                    created_at: item.updated_at || item.created_at || '',
                    path: chatTargetPath(),
                }))
            } catch {
                // 站内会话加载失败不影响账单、工单等业务消息。
                return []
            }
        })(),
    ]

    if (canSeeFee(role)) {
        tasks.push((async () => {
            try {
                const res = await getFeeList()
                const fees = extractList(res.data.data)

                return fees
                    // 消息中心只提示待处理账单，已缴费订单留在缴费记录里展示。
                    .filter((item: any) => item.status === 'unpaid' || item.status === 'overdue')
                    .map((item: any) => ({
                        id: `fee-${item.id}`,
                        type: '财务人员 → 业主',
                        title: `${item.owner_name || '业主'} ${feeTypeText(item)}待处理`,
                        content: item.remark || `应缴 ${item.amount || 0} 元，截止时间：${item.deadline || '-'}`,
                        status: feeStatusText(item.status),
                        created_at: item.created_at || item.deadline || '',
                        path: '/fee/list',
                    }))
            } catch {
                // 单类消息加载失败不影响其他消息。
                return []
            }
        })())
    }

    if (canSeeRepair(role)) {
        tasks.push((async () => {
            try {
                const res = await getRepairList({})
                const repairs = extractList(res.data.data)

                return repairs
                    // 完成工单不再占用消息提醒，避免用户把历史记录误认为待办。
                    .filter((item: any) => item.status !== 'finished')
                    .map((item: any) => ({
                        id: `repair-${item.id}`,
                        type: '维修员 → 业主',
                        title: item.title || `报修工单 #${item.id}`,
                        content: item.content || '',
                        status: repairStatusText(item.status),
                        created_at: item.created_at || '',
                        path: '/repair/list',
                    }))
            } catch {
                // 单类消息加载失败不影响其他消息。
                return []
            }
        })())
    }

    if (canSeeComplaint(role)) {
        tasks.push((async () => {
            try {
                const res = await getComplaintList({})
                const complaints = extractList(res.data.data)

                return complaints.map((item: any) => ({
                    id: `complaint-${item.id}`,
                    type: '物业管理员 → 业主',
                    title: item.title || `投诉建议 #${item.id}`,
                    content: item.handle_result || item.return_visit || item.content || '',
                    status: complaintStatusText(item.status),
                    created_at: item.updated_at || item.created_at || '',
                    path: '/complaint/list',
                }))
            } catch {
                // 单类消息加载失败不影响其他消息。
                return []
            }
        })())
    }

    // 刷新进入页面时，各类消息互不依赖，使用并行请求避免顶部角标和消息中心被慢接口拖住。
    const results = await Promise.all(tasks)

    return sortMessageRows([
        ...getImmediateMessageRows(role),
        ...results.flat(),
    ])
}
