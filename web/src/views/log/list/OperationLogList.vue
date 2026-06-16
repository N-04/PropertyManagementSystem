<!-- 文件说明：实现 src/views/log/list/OperationLogList.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getOperationLogList } from '@/api/log'
import { useClientPagination } from '@/composables/useClientPagination'
import DataPagination from '@/components/common/DataPagination.vue'

const tableData = ref<any[]>([])
const {
    page,
    pageSize,
    total,
    pagedData: pagedTableData,
    resetPage,
} = useClientPagination(tableData)

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

onMounted(() => {
    loadData()
})
</script>

<template>
    <el-card>
        <template #header>
            <span>操作日志列表</span>
            <el-button type="success" @click="exportExcel"> 导出Excel </el-button>
        </template>

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
