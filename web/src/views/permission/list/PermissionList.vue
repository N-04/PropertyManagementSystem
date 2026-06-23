<!-- 文件说明：实现 src/views/permission/list/PermissionList.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
// =====================================================
// 导入 vue
// =====================================================

import { ref, onMounted } from 'vue'

// =====================================================
// 导入权限 API
// =====================================================

import { getPermissionList } from '@/api/permission'
import { useClientPagination } from '@/composables/useClientPagination'
import { useKeywordFilter } from '@/composables/useKeywordFilter'
import DataPagination from '@/components/common/DataPagination.vue'

// =====================================================
// 权限表格数据
// =====================================================

const tableData = ref<any[]>([])
const keyword = ref('')
const filteredTableData = useKeywordFilter(tableData, keyword, ['name', 'code'])
const {
    page,
    pageSize,
    total,
    pagedData: pagedTableData,
    resetPage,
} = useClientPagination(filteredTableData)

// =====================================================
// 获取权限列表
// =====================================================

const getList = async () => {
    // 调用接口
    const res = await getPermissionList()

    // 保存数据
    tableData.value = res.data.data
    resetPage()
}

const columns = [
    {
        title: 'ID',
        dataIndex: 'id',
    },
    {
        title: '权限名称',
        dataIndex: 'name',
    },
    {
        title: '权限编码',
        dataIndex: 'code',
    },
]

const handleFilter = () => {
    // 权限列表按名称和编码做本地模糊搜索。
    resetPage()
}

const resetFilter = () => {
    keyword.value = ''
    resetPage()
}

// =====================================================
// 页面加载完成执行
// =====================================================

onMounted(() => {
    // 获取权限列表
    getList()
})
</script>

<template>
    <!-- ================================================= -->
    <!-- 页面容器 -->
    <!-- ================================================= -->

    <div class="page-container">
        <!-- ================================================= -->
        <!-- 卡片 -->
        <!-- ================================================= -->

        <el-card>
            <!-- 标题 -->
            <template #header>
                <span>权限列表</span>
            </template>

            <div class="list-toolbar">
                <el-input
                    v-model="keyword"
                    clearable
                    placeholder="权限名称/编码"
                    style="width: 260px"
                    @keyup.enter="handleFilter"
                    @clear="handleFilter"
                />
                <el-button type="primary" @click="handleFilter">筛选</el-button>
                <el-button @click="resetFilter">重置</el-button>
            </div>

            <!-- ================================================= -->
            <!-- 表格 -->
            <!-- ================================================= -->

            <el-table :data="pagedTableData" row-key="id">
                <el-table-column prop="id" label="ID" width="100" />

                <!-- 权限名称 -->
                <el-table-column prop="name" label="权限名称" />

                <!-- 权限编码 -->
                <el-table-column prop="code" label="权限编码" />
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
    </div>
</template>

<style scoped>
/* ===================================================== */
/* 页面容器 */
/* ===================================================== */

.page-container {
    padding: 20px;
}

.list-toolbar {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
}
</style>
