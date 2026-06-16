<!-- 文件说明：实现 src/views/building/list/BuildingList.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getBuildingList } from '@/api/building'
import { useClientPagination } from '@/composables/useClientPagination'
import DataPagination from '@/components/common/DataPagination.vue'

const tableData = ref<any[]>([])
const {
    page,
    pageSize,
    total,
    pagedData: pagedTableData,
} = useClientPagination(tableData)

const getList = async () => {
    const res = await getBuildingList()

    tableData.value = res.data.data
}

onMounted(() => {
    getList()
})
</script>

<template>
    <el-card>
        <template #header>
            <span>楼栋列表</span>
        </template>

        <el-table :data="pagedTableData" border>
            <el-table-column prop="id" label="ID" width="80" />

            <el-table-column prop="community_name" label="所属小区" />

            <el-table-column prop="name" label="楼栋名称" />

            <el-table-column prop="code" label="楼栋编码" />

            <el-table-column prop="floor_count" label="总楼层" />

            <el-table-column prop="unit_count" label="单元数" />

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
