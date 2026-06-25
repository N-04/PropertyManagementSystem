<!-- 文件说明：实现 src/views/house/list/HouseList.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getHouseList } from '@/api/house'
import { useRealtimeRefresh } from '@/composables/useRealtimeRefresh'
import DataPagination from '@/components/common/DataPagination.vue'

const tableData = ref<any[]>([])
const keyword = ref('')
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

/**
 * 获取房屋列表
 */
const getList = async () => {
    const res = await getHouseList({
        keyword: keyword.value,
        page: page.value,
        page_size: pageSize.value,
    })
    const rows = res.data.data

    if (Array.isArray(rows)) {
        tableData.value = rows
        total.value = rows.length
        return
    }

    tableData.value = rows?.results || []
    total.value = rows?.total || 0
}

const handleFilter = () => {
    // 模糊搜索条件变化后回到第一页，并按后端真实总数重新分页。
    page.value = 1
    getList()
}

const resetFilter = () => {
    keyword.value = ''
    page.value = 1
    getList()
}

const statusTextMap: Record<string, string> = {
    occupied: '已入住',
    vacant: '空置',
    idle: '空置',
    rented: '已出租',
    renting: '出租',
    repairing: '装修中',
    sold: '已出售',
}

const getStatusText = (status: string) => {
    return statusTextMap[status] || status || '-'
}

const getStatusTagType = (status: string) => {
    if (['occupied', 'sold'].includes(status)) {
        return 'success'
    }

    if (['renting'].includes(status)) {
        return 'primary'
    }

    if (['vacant', 'idle'].includes(status)) {
        return 'info'
    }

    return 'warning'
}

onMounted(() => {
    getList()
})

useRealtimeRefresh(() => getList(), {
    scope: 'houses',
    immediate: false,
    intervalMs: 30000,
})
</script>

<template>
    <el-card class="house-list-card">
        <template #header>
            <div class="card-header">
                <span>房屋列表</span>
                <span class="card-subtitle">共 {{ total }} 套房屋</span>
            </div>
        </template>

        <div class="list-toolbar">
            <el-input
                v-model="keyword"
                class="filter-input"
                clearable
                placeholder="小区/楼栋/单元/房号"
                @keyup.enter="handleFilter"
                @clear="handleFilter"
            />
            <el-button type="primary" @click="handleFilter">筛选</el-button>
            <el-button @click="resetFilter">重置</el-button>
        </div>

        <el-table class="house-table" :data="tableData" border stripe style="width: 100%">
            <el-table-column prop="id" label="ID" width="90" />

            <el-table-column prop="community_name" label="所属小区" min-width="140" />

            <el-table-column prop="building_name" label="所属楼栋" min-width="120" />

            <el-table-column prop="unit_name" label="所属单元" min-width="120" />

            <el-table-column prop="room_no" label="房号" min-width="110" />

            <el-table-column label="面积" min-width="110">
                <template #default="{ row }">
                    {{ row.area || '-' }}㎡
                </template>
            </el-table-column>

            <el-table-column prop="house_type" label="户型" min-width="140" />

            <el-table-column label="状态" min-width="110">
                <template #default="{ row }">
                    <el-tag :type="getStatusTagType(row.status)" effect="light">
                        {{ getStatusText(row.status) }}
                    </el-tag>
                </template>
            </el-table-column>

            <el-table-column prop="owner_count" label="业主数" min-width="100" />

            <el-table-column prop="resident_count" label="居住人数" min-width="110" />
        </el-table>

        <DataPagination
            v-model:current-page="page"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50]"
            :total="total"
            background
            @change="getList"
        />
    </el-card>
</template>

<style scoped>
.house-list-card :deep(.el-card__body) {
    padding: 24px;
}

.card-subtitle {
    color: var(--text-muted);
    font-size: 13px;
    font-weight: 400;
    line-height: 20px;
}

.list-toolbar {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
    margin-bottom: 20px;
}

.filter-input {
    width: min(360px, 100%);
}

.house-table :deep(.el-table__cell) {
    padding: 14px 0;
}

.house-table :deep(.el-table__row) {
    height: 62px;
}
</style>
