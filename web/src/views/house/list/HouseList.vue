<!-- 文件说明：实现 src/views/house/list/HouseList.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getHouseList } from '@/api/house'
import { useClientPagination } from '@/composables/useClientPagination'
import DataPagination from '@/components/common/DataPagination.vue'

const tableData = ref<any[]>([])
const {
    page,
    pageSize,
    total,
    pagedData: pagedTableData,
} = useClientPagination(tableData)

/**
 * 获取房屋列表
 */
const getList = async () => {
    const res = await getHouseList()

    tableData.value = res.data.data
}

onMounted(() => {
    getList()
})
</script>

<template>
    <el-card>
        <template #header>
            <span>房屋列表</span>
        </template>

        <el-table :data="pagedTableData" border>
            <el-table-column prop="id" label="ID" width="80" />

            <el-table-column prop="community_name" label="所属小区" />

            <el-table-column prop="building_name" label="所属楼栋" />

            <el-table-column prop="unit_name" label="所属单元" />

            <el-table-column prop="room_no" label="房号" />

            <el-table-column prop="area" label="面积" />

            <el-table-column prop="house_type" label="户型" />

            <el-table-column prop="status" label="状态" />

            <el-table-column prop="owner_count" label="业主数" />

            <el-table-column prop="resident_count" label="居住人数" />
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
