<!-- 文件说明：实现 src/views/log/login/list/LoginLogList.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
// Vue生命周期
import { onMounted, ref } from 'vue'

// 登录日志接口
import { getLoginLogList } from '@/api/log'
import { useClientPagination } from '@/composables/useClientPagination'
import { useKeywordFilter } from '@/composables/useKeywordFilter'
import DataPagination from '@/components/common/DataPagination.vue'

// 表格数据
const tableData = ref<any[]>([])
const keyword = ref('')
const filteredTableData = useKeywordFilter(tableData, keyword, ['username', 'ip', 'created_at'])
const {
    page,
    pageSize,
    total,
    pagedData: pagedTableData,
    resetPage,
} = useClientPagination(filteredTableData)

/**
 * 加载登录日志数据
 */
const loadData = async () => {
    // 调用接口
    const res = await getLoginLogList()

    // 赋值表格数据
    tableData.value = res.data.data
    resetPage()
}

/**
 * 导出Excel
 */
const exportExcel = () => {
    window.open('http://127.0.0.1:8000/api/log/login/export/')
}

const handleFilter = () => {
    // 登录日志按页面可见字段做本地模糊搜索。
    resetPage()
}

const resetFilter = () => {
    keyword.value = ''
    resetPage()
}

// 页面加载完成执行
onMounted(() => {
    loadData()
})
</script>

<template>
    <!-- 卡片容器 -->
    <el-card>
        <!-- 卡片标题 -->
        <template #header>
            <div class="card-header">
                <span>登录日志列表</span>
                <el-button type="success" @click="exportExcel"> 导出Excel </el-button>
            </div>
        </template>

        <div class="list-toolbar">
            <el-input
                v-model="keyword"
                clearable
                placeholder="用户名/IP/登录时间"
                style="width: 280px"
                @keyup.enter="handleFilter"
                @clear="handleFilter"
            />
            <el-button type="primary" @click="handleFilter">筛选</el-button>
            <el-button @click="resetFilter">重置</el-button>
        </div>

        <!-- 数据表格 -->
        <el-table :data="pagedTableData" border style="width: 100%">
            <!-- ID -->
            <el-table-column prop="id" label="ID" width="80" />

            <!-- 用户名 -->
            <el-table-column prop="username" label="用户名" />

            <!-- IP地址 -->
            <el-table-column prop="ip" label="IP地址" />

            <!-- 登录时间 -->
            <el-table-column prop="created_at" label="登录时间" />
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
