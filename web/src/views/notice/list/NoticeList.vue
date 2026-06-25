<!-- 文件说明：实现 src/views/notice/list/NoticeList.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { getNoticeList, deleteNotice } from '@/api/notice'
import { useRouter } from 'vue-router'
import { useClientPagination } from '@/composables/useClientPagination'
import { useKeywordFilter } from '@/composables/useKeywordFilter'
import { useRealtimeRefresh } from '@/composables/useRealtimeRefresh'
import DataPagination from '@/components/common/DataPagination.vue'
import { getStoredRole } from '@/utils/authState'
// =====================================================
// 响应式数据
// =====================================================

const router = useRouter()
const role = getStoredRole()
const canPublishNotice = computed(() => {
    // 管理员、财务和维修角色只负责发布公告；业主只能接收查看。
    return [
        'admin',
        'super_admin',
        'property_admin',
        'finance_staff',
        'finance',
        'repair_staff',
        'repairer',
        'repair',
    ].includes(role)
})
// =====================================================
// 公告列表数据
// =====================================================
const tableData = ref<any[]>([])
const keyword = ref('')
const filteredTableData = useKeywordFilter(tableData, keyword, [
    'title',
    'content',
    'notice_type_display',
    'status_display',
])
const {
    page,
    pageSize,
    total,
    pagedData: pagedTableData,
    resetPage,
} = useClientPagination(filteredTableData)
const getList = async (shouldResetPage = true) => {
    const res = await getNoticeList()

    tableData.value = res.data.data

    if (shouldResetPage) {
        resetPage()
    }
}

const handleFilter = () => {
    // 公告列表本地模糊搜索后回到第一页。
    resetPage()
}

const resetFilter = () => {
    keyword.value = ''
    resetPage()
}

// =====================================================
// 编辑公告
// =====================================================
const handleEdit = (row: any) => {
    // 页面跳转
    router.push(`/notice/edit/${row.id}`)
}

// =====================================================
// 删除公告
// =====================================================

const handleDelete = async (row: any) => {
    await deleteNotice(row.id)

    await getList()
}

onMounted(() => {
    getList()
})

useRealtimeRefresh(() => getList(false), {
    scope: 'notices',
    immediate: false,
    intervalMs: 30000,
})
</script>

<template>
    <el-card>
        <template #header>
            <div class="notice-header">
                <span>公开公告</span>
                <el-button
                    v-if="canPublishNotice"
                    type="primary"
                    @click="router.push('/notice/create')"
                >
                    发布公告
                </el-button>
            </div>
        </template>
        <div class="list-toolbar">
            <el-input
                v-model="keyword"
                clearable
                placeholder="公开公告标题/内容/类型/状态"
                style="width: 300px"
                @keyup.enter="handleFilter"
                @clear="handleFilter"
            />
            <el-button type="primary" @click="handleFilter">筛选</el-button>
            <el-button @click="resetFilter">重置</el-button>
        </div>

        <el-table :data="pagedTableData" style="width: 100%" border>
            <el-table-column prop="id" label="ID" width="80" />

            <el-table-column prop="title" label="公告标题" />

            <el-table-column prop="content" label="公告内容" />

            <el-table-column prop="notice_type_display" label="公告类型" width="110" />

            <el-table-column prop="created_at" label="创建时间" />

            <el-table-column prop="status_display" label="状态" />

            <el-table-column v-if="canPublishNotice" label="操作">
                <template #default="{ row }">
                    <el-button type="primary" @click="handleEdit(row)">编辑</el-button>
                    <el-button type="danger" @click="handleDelete(row)">删除</el-button>
                </template>
            </el-table-column>
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
.notice-header {
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
</style>
