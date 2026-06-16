<!-- 文件说明：实现 src/views/car/list/CarList.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getCarList } from '@/api/car'
import { deleteCar, disableCar, enableCar } from '@/api/car'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import { useClientPagination } from '@/composables/useClientPagination'
import DataPagination from '@/components/common/DataPagination.vue'

const router = useRouter()

const tableData = ref<any[]>([])
const {
    page,
    pageSize,
    total,
    pagedData: pagedTableData,
    resetPage,
} = useClientPagination(tableData)
const keyword = ref('')
const resetSearch = () => {
    keyword.value = ''
    getList()
}
/**
 * 获取车辆列表
 */
const getList = async () => {
    const res = await getCarList(keyword.value)

    tableData.value = res.data.data
    resetPage()
}

const handleDetail = (row: any) => {
    router.push('/car/detail/' + row.id)
}
const handleEdit = (row: any) => {
    router.push('/car/edit/' + row.id)
}

/**
 * 启用车辆
 */
const handleEnable = async (row: any) => {
    await ElMessageBox.confirm('确认启用该车辆吗？', '提示')

    await enableCar(row.id)

    ElMessage.success('启用成功')

    getList()
}

/**
 * 禁用车辆
 */
const handleDisable = async (row: any) => {
    await ElMessageBox.confirm('确认禁用该车辆吗？', '提示')

    await disableCar(row.id)

    ElMessage.success('禁用成功')

    getList()
}

const handleDelete = async (row: any) => {
    await ElMessageBox.confirm('确认删除该车辆吗？', '提示')

    await deleteCar(row.id)

    ElMessage.success('删除成功')

    getList()
}

onMounted(() => {
    getList()
})
</script>

<template>
    <el-card>
        <template #header>
            <div style="display: flex; justify-content: space-between">
                <span>车辆列表</span>
                <el-input v-model="keyword" placeholder="车牌号/业主" style="width: 250px" />

                <el-button type="primary" @click="getList"> 搜索 </el-button>

                <el-button @click="resetSearch"> 重置 </el-button>

                <el-button type="primary" @click="router.push('/car/create')"> 新增车辆 </el-button>
            </div>
        </template>

        <el-table :data="pagedTableData" border style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />

            <el-table-column prop="plate_no" label="车牌号" />

            <el-table-column prop="owner_name" label="所属业主" />

            <el-table-column prop="TYPE_CHOICES" label="车辆类型" />

            <el-table-column prop="brand" label="品牌" />

            <el-table-column prop="color" label="颜色" />

            <el-table-column prop="parking_no" label="车位" />

            <el-table-column label="状态">
                <template #default="scope">
                    <el-tag v-if="scope.row.status === 'normal'" type="success"> 正常 </el-tag>

                    <el-tag v-else type="danger"> 禁用 </el-tag>
                </template>
            </el-table-column>

            <el-table-column prop="created_at" label="创建时间" width="180" />

            <el-table-column label="操作" width="260">
                <template #default="scope">
                    <el-button type="success" size="small" @click="handleDetail(scope.row)">
                        查看
                    </el-button>

                    <el-button type="primary" size="small" @click="handleEdit(scope.row)">
                        编辑
                    </el-button>

                    <el-button
                        v-if="scope.row.status === 'normal'"
                        type="warning"
                        size="small"
                        @click="handleDisable(scope.row)"
                    >
                        禁用
                    </el-button>

                    <el-button v-else type="success" size="small" @click="handleEnable(scope.row)">
                        启用
                    </el-button>

                    <el-button type="danger" size="small" @click="handleDelete(scope.row)">
                        删除
                    </el-button>
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
