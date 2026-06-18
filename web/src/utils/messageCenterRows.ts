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

const extractList = (data: any) => {
    if (Array.isArray(data)) {
        return data
    }

    if (Array.isArray(data?.results)) {
        return data.results
    }

    return []
}

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
        'customer_service',
        'service',
        'admin',
        'super_admin',
    ].includes(role)
}

const chatTargetPath = (role: string) => {
    return ['customer_service', 'service'].includes(role) ? '/service/chat' : '/message/center'
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

export const loadMessageCenterRows = async (role: string) => {
    const rows: MessageRow[] = []

    try {
        const res = await getChatConversationList()
        const conversations = extractList(res.data.data)

        conversations.forEach((item: any) => {
            rows.push({
                id: `chat-${item.id}`,
                type: `${item.created_by_real_name || item.created_by_name || '发起人'} → ${item.target_role_text || '处理角色'}`,
                title: item.title || `会话 #${item.id}`,
                content: item.last_message || '暂无最新消息',
                status: item.status_text || '沟通中',
                created_at: item.updated_at || item.created_at || '',
                path: chatTargetPath(role),
            })
        })
    } catch (error) {
        // 站内会话加载失败不影响账单、工单等业务消息。
    }

    if (canSeeFee(role)) {
        try {
            const res = await getFeeList()
            const fees = extractList(res.data.data)

            fees.filter(
                (item: any) => item.status === 'unpaid' || item.status === 'overdue'
            ).forEach((item: any) => {
                rows.push({
                    id: `fee-${item.id}`,
                    type: '财务人员 → 业主',
                    title: `${item.owner_name || '业主'} ${feeTypeText(item)}待处理`,
                    content: item.remark || `应缴 ${item.amount || 0} 元，截止时间：${item.deadline || '-'}`,
                    status: feeStatusText(item.status),
                    created_at: item.created_at || item.deadline || '',
                    path: '/fee/list',
                })
            })
        } catch (error) {
            // 单类消息加载失败不影响其他消息。
        }
    }

    if (canSeeRepair(role)) {
        try {
            const res = await getRepairList({})
            const repairs = extractList(res.data.data)

            repairs
                .filter((item: any) => item.status !== 'finished')
                .forEach((item: any) => {
                    rows.push({
                        id: `repair-${item.id}`,
                        type: '维修员 → 业主',
                        title: item.title || `报修工单 #${item.id}`,
                        content: item.content || '',
                        status: repairStatusText(item.status),
                        created_at: item.created_at || '',
                        path: '/repair/list',
                    })
                })
        } catch (error) {
            // 单类消息加载失败不影响其他消息。
        }
    }

    if (canSeeComplaint(role)) {
        try {
            const res = await getComplaintList({})
            const complaints = extractList(res.data.data)

            complaints.forEach((item: any) => {
                rows.push({
                    id: `complaint-${item.id}`,
                    type: '客服人员 → 业主',
                    title: item.title || `投诉建议 #${item.id}`,
                    content: item.handle_result || item.return_visit || item.content || '',
                    status: complaintStatusText(item.status),
                    created_at: item.updated_at || item.created_at || '',
                    path: '/complaint/list',
                })
            })
        } catch (error) {
            // 单类消息加载失败不影响其他消息。
        }
    }

    return rows.sort((a, b) => `${b.created_at}`.localeCompare(`${a.created_at}`))
}
