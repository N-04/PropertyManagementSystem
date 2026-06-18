<!-- 文件说明：展示角色与角色之间的站内消息、缴费协同、工单协同和投诉反馈。 -->
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { getChatConversationList } from '@/api/chat'
import { getComplaintList } from '@/api/complaint'
import { getFeeList } from '@/api/fee'
import { getRepairList } from '@/api/repair'
import { useClientPagination } from '@/composables/useClientPagination'
import { useKeywordFilter } from '@/composables/useKeywordFilter'
import DataPagination from '@/components/common/DataPagination.vue'
import { getStoredRole } from '@/utils/authState'

type MessageRow = {
    id: string
    type: string
    title: string
    content: string
    status: string
    created_at: string
    path: string
}

const router = useRouter()
const role = getStoredRole()
const loading = ref(false)
const tableData = ref<MessageRow[]>([])
const keyword = ref('')
const typeFilter = ref('')
const keywordFilteredData = useKeywordFilter(tableData, keyword, ['type', 'title', 'content', 'status'])
const filteredTableData = computed(() => {
    if (!typeFilter.value) {
        return keywordFilteredData.value
    }

    return keywordFilteredData.value.filter((item) => item.type === typeFilter.value)
})

const {
    page,
    pageSize,
    total,
    pagedData: pagedTableData,
    resetPage,
} = useClientPagination(filteredTableData)

const messageTypeOptions = computed(() => {
    return Array.from(new Set(tableData.value.map((item) => item.type).filter(Boolean)))
})

const canSeeFee = computed(() => {
    return ['owner', 'finance', 'finance_staff', 'admin', 'super_admin'].includes(role)
})

const canSeeRepair = computed(() => {
    return [
        'owner',
        'repair_staff',
        'repairer',
        'repair',
        'property_admin',
        'admin',
        'super_admin',
    ].includes(role)
})

const canSeeComplaint = computed(() => {
    return [
        'owner',
        'property_admin',
        'customer_service',
        'service',
        'admin',
        'super_admin',
    ].includes(role)
})

const extractList = (data: any) => {
    if (Array.isArray(data)) {
        return data
    }

    if (Array.isArray(data?.results)) {
        return data.results
    }

    return []
}

const chatTargetPath = () => {
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

const loadMessages = async () => {
    loading.value = true

    try {
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
                    path: chatTargetPath(),
                })
            })
        } catch (error) {
            // 站内会话加载失败不影响账单、工单等业务消息。
        }

        if (canSeeFee.value) {
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

        if (canSeeRepair.value) {
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

        if (canSeeComplaint.value) {
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

        tableData.value = rows.sort((a, b) => `${b.created_at}`.localeCompare(`${a.created_at}`))
        resetPage()
    } finally {
        loading.value = false
    }
}

const openMessage = (row: MessageRow) => {
    router.push(row.path)
}

const handleFilter = () => {
    // 消息中心按类型、标题、内容和状态做本地模糊搜索。
    resetPage()
}

const resetFilter = () => {
    keyword.value = ''
    typeFilter.value = ''
    resetPage()
}

onMounted(() => {
    loadMessages()
})
</script>

<template>
    <el-row :gutter="16">
        <el-col :span="24">
            <el-card>
                <template #header>
                    <div class="card-header">
                        <span>消息中心</span>
                        <el-button type="primary" link :loading="loading" @click="loadMessages">
                            刷新
                        </el-button>
                    </div>
                </template>

                <div class="list-toolbar">
                    <el-input
                        v-model="keyword"
                        clearable
                        placeholder="角色关系/标题/内容/状态"
                        style="width: 300px"
                        @keyup.enter="handleFilter"
                        @clear="handleFilter"
                    />
                    <el-select v-model="typeFilter" clearable placeholder="角色关系" style="width: 180px">
                        <el-option
                            v-for="item in messageTypeOptions"
                            :key="item"
                            :label="item"
                            :value="item"
                        />
                    </el-select>
                    <el-button type="primary" @click="handleFilter">筛选</el-button>
                    <el-button @click="resetFilter">重置</el-button>
                </div>

                <el-table v-loading="loading" :data="pagedTableData" border align="center">
                    <el-table-column prop="type" label="角色关系" width="170" />
                    <el-table-column
                        prop="title"
                        label="标题"
                        min-width="150"
                        show-overflow-tooltip
                    />
                    <el-table-column
                        prop="content"
                        label="最近内容"
                        min-width="220"
                        show-overflow-tooltip
                    />
                    <el-table-column prop="status" label="状态" width="100" />
                    <el-table-column prop="created_at" label="时间" width="170" />
                    <el-table-column label="操作" width="90">
                        <template #default="scope">
                            <el-button type="primary" size="small" @click="openMessage(scope.row)">
                                查看
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>

                <div class="pagination-wrapper">
                    <DataPagination
                        v-model:current-page="page"
                        v-model:page-size="pageSize"
                        :page-sizes="[5, 10, 20, 50]"
                        :total="total"
                        background
                        layout="total, sizes, prev, pager, next, jumper"
                    />
                </div>
            </el-card>
        </el-col>

    </el-row>
</template>

<style scoped>
.card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.list-toolbar {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
    margin-bottom: 16px;
}

.pagination-wrapper {
    display: flex;
    justify-content: center;
    margin-top: 16px;
}

</style>
