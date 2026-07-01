<!-- 文件说明：实现 src/views/community/list/CommunityList.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getCommunityList } from '@/api/community'
import { useClientPagination } from '@/composables/useClientPagination'
import { useKeywordFilter } from '@/composables/useKeywordFilter'
import { useRealtimeRefresh } from '@/composables/useRealtimeRefresh'
import DataPagination from '@/components/common/DataPagination.vue'
import { extractListRows } from '@/utils/listResponse'

const tableData = ref<any[]>([])
const keyword = ref('')
const filteredTableData = useKeywordFilter(tableData, keyword, ['name', 'address'])
const {
    page,
    pageSize,
    total,
    pagedData: pagedTableData,
    resetPage,
} = useClientPagination(filteredTableData)

const getList = async () => {
    const res = await getCommunityList({ page_size: 100 })

    tableData.value = extractListRows(res.data.data)
}

const handleFilter = () => {
    // 模糊搜索条件变化后回到第一页，避免停在空页。
    resetPage()
}

const resetFilter = () => {
    keyword.value = ''
    resetPage()
}

onMounted(() => {
    getList()
})

useRealtimeRefresh(getList, {
    scope: 'community',
    immediate: false,
    intervalMs: 30000,
})
</script>

<template>
    <el-card>
        <template #header>
            <span>小区列表</span>
        </template>

        <div class="list-toolbar">
            <el-input
                v-model="keyword"
                clearable
                placeholder="小区名称/地址"
                style="width: 260px"
                @keyup.enter="handleFilter"
                @clear="handleFilter"
            />
            <el-button type="primary" @click="handleFilter">筛选</el-button>
            <el-button @click="resetFilter">重置</el-button>
        </div>

        <el-table :data="pagedTableData" border>
            <el-table-column prop="id" label="ID" width="80" />

            <el-table-column prop="name" label="小区名称" />

            <el-table-column prop="address" label="地址" />

            <el-table-column prop="created_at" label="创建时间" />
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
.list-toolbar {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
}
</style>
