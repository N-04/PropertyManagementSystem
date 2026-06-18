<!-- 文件说明：展示角色与角色之间的站内消息、缴费协同、工单协同和投诉反馈。 -->
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useClientPagination } from '@/composables/useClientPagination'
import { useKeywordFilter } from '@/composables/useKeywordFilter'
import DataPagination from '@/components/common/DataPagination.vue'
import { getStoredRole } from '@/utils/authState'
import { loadMessageCenterRows, type MessageRow } from '@/utils/messageCenterRows'

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

const loadMessages = async () => {
    loading.value = true

    try {
        tableData.value = await loadMessageCenterRows(role)
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
