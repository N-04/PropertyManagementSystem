<!-- 文件说明：实现 src/views/log/list/OperationLogList.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getOperationLogList } from '@/api/log'
import { useClientPagination } from '@/composables/useClientPagination'
import { useKeywordFilter } from '@/composables/useKeywordFilter'
import DataPagination from '@/components/common/DataPagination.vue'

const tableData = ref<any[]>([])
const keyword = ref('')
const filteredTableData = useKeywordFilter(tableData, keyword, ['username', 'module', 'action', 'created_at'])
const {
    page,
    pageSize,
    total,
    pagedData: pagedTableData,
    resetPage,
} = useClientPagination(filteredTableData)

const loadData = async () => {
    const res = await getOperationLogList()

    tableData.value = res.data.data
    resetPage()
}

/**
 * 导出Excel
 */
const exportExcel = () => {
    window.open('http://127.0.0.1:8000/api/log/operation/export/')
}

const handleFilter = () => {
    // 日志列表按页面可见字段做本地模糊搜索。
    resetPage()
}

const resetFilter = () => {
    keyword.value = ''
    resetPage()
}

onMounted(() => {
    loadData()
})
</script>

<template>
    <el-card>
        <template #header>
            <div class="card-header">
                <span>操作日志列表</span>
                <el-button type="primary" @click="exportExcel"> 导出Excel </el-button>
            </div>
        </template>

        <div class="list-toolbar">
            <el-input
                v-model="keyword"
                clearable
                placeholder="用户名/模块/操作内容"
                style="width: 280px"
                @keyup.enter="handleFilter"
                @clear="handleFilter"
            />
            <el-button type="primary" @click="handleFilter">筛选</el-button>
            <el-button @click="resetFilter">重置</el-button>
        </div>

        <el-table :data="pagedTableData" border>
            <el-table-column type="index" label="序号" width="80" />

            <el-table-column prop="username" label="用户名" />

            <el-table-column prop="module" label="模块" />

            <el-table-column prop="action" label="操作内容" />

            <el-table-column prop="created_at" label="操作时间" width="180" />
        </el-table>

        <DataPagination
            v-model:current-page="page"
            v-model:page-size="pageSize"
            :page-sizes="[5, 10, 20, 50]"
            :total="total"
            background
            layout="total, sizes, prev, pager, next, jumper"
        />
    </el-card>
</template>

<style scoped>
.card-header,
.list-toolbar {
    display: flex;
    align-items: center;
    gap: 10px;
}

.card-header {
    justify-content: space-between;
}

.list-toolbar {
    margin-bottom: 12px;
}
</style>
