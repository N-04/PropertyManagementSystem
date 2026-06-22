<!-- 文件说明：展示角色与角色之间的站内消息、缴费协同、工单协同和投诉反馈。 -->
<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ChatLineRound, Refresh, Search, View } from '@element-plus/icons-vue'
import { useClientPagination } from '@/composables/useClientPagination'
import { useKeywordFilter } from '@/composables/useKeywordFilter'
import DataPagination from '@/components/common/DataPagination.vue'
import { AUTH_STATE_CHANGED_EVENT, getStoredRole } from '@/utils/authState'
import {
    loadMessageCenterRows,
    MESSAGE_FEEDBACK_EVENTS,
    MESSAGE_FEEDBACK_STORAGE_KEYS,
    type MessageRow,
} from '@/utils/messageCenterRows'

const router = useRouter()
const role = ref(getStoredRole())
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

const latestMessageTime = computed(() => tableData.value[0]?.created_at || '-')

const pendingCount = computed(() => {
    return tableData.value.filter((item) => !['已解决', '已完成', '已关闭', '已评价'].includes(item.status)).length
})

const relationCount = computed(() => messageTypeOptions.value.length)

const statusTone = (status: string) => {
    if (['已解决', '已完成', '已关闭', '已评价'].includes(status)) {
        return 'success'
    }

    if (['未缴费', '已逾期', '待跟进', '待处理'].includes(status)) {
        return 'danger'
    }

    return 'primary'
}

const loadMessages = async () => {
    loading.value = true

    try {
        tableData.value = await loadMessageCenterRows(role.value)
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

const handleMessageFeedbackChanged = () => {
    loadMessages()
}

const handleAuthStateChanged = () => {
    const nextRole = getStoredRole()

    if (nextRole !== role.value) {
        // 复制标签或切换账号后，消息中心必须跟随当前角色重新统计和展示。
        role.value = nextRole
        keyword.value = ''
        typeFilter.value = ''
    }

    loadMessages()
}

const handleMessageFeedbackStorage = (event: StorageEvent) => {
    if (MESSAGE_FEEDBACK_STORAGE_KEYS.includes(event.key || '')) {
        loadMessages()
    }
}

onMounted(() => {
    window.addEventListener(AUTH_STATE_CHANGED_EVENT, handleAuthStateChanged)
    window.addEventListener('storage', handleMessageFeedbackStorage)
    MESSAGE_FEEDBACK_EVENTS.forEach((eventName) => {
        window.addEventListener(eventName, handleMessageFeedbackChanged)
    })
    loadMessages()
})

onBeforeUnmount(() => {
    window.removeEventListener(AUTH_STATE_CHANGED_EVENT, handleAuthStateChanged)
    window.removeEventListener('storage', handleMessageFeedbackStorage)
    MESSAGE_FEEDBACK_EVENTS.forEach((eventName) => {
        window.removeEventListener(eventName, handleMessageFeedbackChanged)
    })
})
</script>

<template>
    <div class="message-page">
        <header class="page-heading">
            <div>
                <h1>消息中心</h1>
                <p>展示当前角色相关的缴费、工单、投诉和服务协同消息。</p>
            </div>
            <button type="button" class="refresh-button" :disabled="loading" @click="loadMessages">
                <el-icon><Refresh /></el-icon>
                {{ loading ? '刷新中' : '刷新' }}
            </button>
        </header>

        <section class="summary-grid">
            <article class="summary-card active">
                <span>消息总数</span>
                <strong>{{ tableData.length }}</strong>
                <small>顶部红点同步此统计</small>
            </article>
            <article class="summary-card">
                <span>待处理</span>
                <strong>{{ pendingCount }}</strong>
                <small>缴费、工单、投诉待跟进</small>
            </article>
            <article class="summary-card">
                <span>角色关系</span>
                <strong>{{ relationCount }}</strong>
                <small>跨角色协同来源</small>
            </article>
            <article class="summary-card">
                <span>最近更新</span>
                <strong class="time-value">{{ latestMessageTime }}</strong>
                <small>按消息时间倒序展示</small>
            </article>
        </section>

        <section class="panel message-panel">
            <div class="filter-bar">
                <label class="filter-field search-field">
                    <span>搜索</span>
                    <el-input
                        v-model="keyword"
                        clearable
                        placeholder="角色关系 / 标题 / 内容 / 状态"
                        @keyup.enter="handleFilter"
                        @clear="handleFilter"
                    >
                        <template #prefix>
                            <el-icon><Search /></el-icon>
                        </template>
                    </el-input>
                </label>

                <label class="filter-field">
                    <span>角色关系</span>
                    <el-select v-model="typeFilter" clearable placeholder="全部关系">
                        <el-option
                            v-for="item in messageTypeOptions"
                            :key="item"
                            :label="item"
                            :value="item"
                        />
                    </el-select>
                </label>

                <div class="filter-actions">
                    <button type="button" class="primary-button" @click="handleFilter">筛选</button>
                    <button type="button" class="ghost-button" @click="resetFilter">重置</button>
                </div>
            </div>

            <el-table
                v-loading="loading"
                :data="pagedTableData"
                class="message-table"
                border
            >
                <el-table-column prop="type" label="角色关系" min-width="170" />
                <el-table-column prop="title" label="标题" min-width="190" show-overflow-tooltip />
                <el-table-column prop="content" label="最近内容" min-width="280" show-overflow-tooltip />
                <el-table-column label="状态" width="118">
                    <template #default="scope">
                        <span class="status-pill" :class="statusTone(scope.row.status)">
                            {{ scope.row.status }}
                        </span>
                    </template>
                </el-table-column>
                <el-table-column prop="created_at" label="时间" min-width="170" />
                <el-table-column label="操作" width="104" fixed="right">
                    <template #default="scope">
                        <button type="button" class="table-action" @click="openMessage(scope.row)">
                            <el-icon><View /></el-icon>
                            查看
                        </button>
                    </template>
                </el-table-column>
                <template #empty>
                    <div class="empty-state">
                        <el-icon><ChatLineRound /></el-icon>
                        <span>暂无角色协同消息</span>
                    </div>
                </template>
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
        </section>
    </div>
</template>

<style scoped>
.message-page {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.page-heading {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 20px;
}

.page-heading h1 {
    margin: 0;
    color: var(--text-heading);
    font-size: 24px;
    font-weight: 700;
    line-height: 32px;
}

.page-heading p {
    margin: 4px 0 0;
    color: var(--text-muted);
    font-size: 14px;
    line-height: 22px;
}

.summary-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 14px;
}

.summary-card {
    min-height: 110px;
    padding: 18px 20px;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    background: var(--surface-card);
}

.summary-card.active {
    border-color: var(--brand-primary);
    background: var(--brand-primary-subtle);
}

.summary-card span,
.summary-card small {
    display: block;
}

.summary-card span {
    color: var(--text-subtle);
    font-size: 14px;
    font-weight: 600;
    line-height: 22px;
}

.summary-card strong {
    display: block;
    margin-top: 10px;
    color: var(--brand-primary);
    font-size: 28px;
    font-weight: 700;
    line-height: 36px;
}

.summary-card .time-value {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    color: var(--text-heading);
    font-size: 18px;
    line-height: 28px;
}

.summary-card small {
    margin-top: 4px;
    color: var(--text-muted);
    font-size: 13px;
    line-height: 20px;
}

.panel {
    border: 1px solid var(--border-color);
    border-radius: 8px;
    background: var(--surface-card);
    box-shadow: 0 12px 30px rgba(15, 23, 42, 0.04);
}

.message-panel {
    padding: 20px;
}

.filter-bar {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
    margin-bottom: 18px;
}

.filter-field {
    display: inline-flex;
    align-items: center;
    gap: 10px;
}

.filter-field span {
    flex: 0 0 auto;
    color: var(--text-subtle);
    font-size: 14px;
    font-weight: 600;
    line-height: 22px;
}

.search-field {
    flex: 1 1 420px;
    min-width: 320px;
}

.search-field :deep(.el-input) {
    width: 100%;
}

.filter-field :deep(.el-input__wrapper),
.filter-field :deep(.el-select__wrapper) {
    min-height: 42px;
    border-radius: 6px;
    box-shadow: 0 0 0 1px var(--border-color) inset;
}

.filter-field :deep(.el-select) {
    width: 220px;
}

.filter-actions {
    display: inline-flex;
    align-items: center;
    gap: 10px;
}

.refresh-button,
.primary-button,
.ghost-button,
.table-action {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    line-height: 20px;
}

.refresh-button,
.ghost-button {
    min-height: 42px;
    padding: 0 18px;
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    background: #fff;
}

.refresh-button:hover,
.ghost-button:hover {
    color: var(--brand-primary);
    border-color: rgba(15, 118, 110, 0.4);
    background: var(--brand-primary-subtle);
}

.refresh-button:disabled {
    cursor: not-allowed;
    opacity: 0.7;
}

.primary-button {
    min-height: 42px;
    padding: 0 22px;
    border: 0;
    color: #fff;
    background: var(--brand-primary);
}

.primary-button:hover {
    background: var(--brand-primary-hover);
}

.message-table {
    width: 100%;
    font-size: 14px;
}

.message-table :deep(.el-table__header th) {
    height: 54px;
    color: var(--text-subtle);
    background: var(--surface-muted);
    font-size: 13px;
    font-weight: 600;
    line-height: 20px;
}

.message-table :deep(.el-table__row td) {
    padding: 16px 0;
    color: var(--text-primary);
    font-size: 14px;
    line-height: 22px;
}

.status-pill {
    display: inline-flex;
    min-width: 64px;
    min-height: 26px;
    align-items: center;
    justify-content: center;
    padding: 0 10px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    line-height: 18px;
}

.status-pill.primary {
    color: #1677ff;
    background: #eaf2ff;
}

.status-pill.success {
    color: #0f766e;
    background: #dff5f1;
}

.status-pill.danger {
    color: #ef4444;
    background: #fee2e2;
}

.table-action {
    min-height: 32px;
    padding: 0 12px;
    border: 1px solid rgba(15, 118, 110, 0.35);
    color: var(--brand-primary);
    background: #fff;
}

.table-action:hover {
    border-color: var(--brand-primary);
    background: var(--brand-primary-subtle);
}

.empty-state {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    padding: 32px 0;
    color: var(--text-muted);
}

.empty-state .el-icon {
    color: var(--brand-primary);
    font-size: 28px;
}

.pagination-wrapper {
    display: flex;
    justify-content: center;
    margin-top: 18px;
}

@media (max-width: 1280px) {
    .summary-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

</style>
