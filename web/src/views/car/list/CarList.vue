<!-- 文件说明：实现 src/views/car/list/CarList.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { getCarList } from '@/api/car'
import { deleteCar, disableCar, enableCar } from '@/api/car'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import { useClientPagination } from '@/composables/useClientPagination'
import { useRealtimeRefresh } from '@/composables/useRealtimeRefresh'
import DataPagination from '@/components/common/DataPagination.vue'

const router = useRouter()

const tableData = ref<any[]>([])
const keyword = ref('')
const statusFilter = ref('')
const filteredTableData = computed(() => {
    if (!statusFilter.value) {
        return tableData.value
    }

    return tableData.value.filter((item) => item.status === statusFilter.value)
})
const {
    page,
    pageSize,
    total,
    pagedData: pagedTableData,
    resetPage,
} = useClientPagination(filteredTableData)

/**
 * 获取车辆列表
 */
const getList = async (shouldResetPage = true) => {
    const res = await getCarList(keyword.value)

    tableData.value = res.data.data

    if (shouldResetPage) {
        resetPage()
    }
}

const handleFilter = () => {
    // 车辆关键字走接口模糊搜索，状态在当前结果内继续筛选。
    page.value = 1
    getList()
}

const resetSearch = () => {
    keyword.value = ''
    statusFilter.value = ''
    getList()
}

// 列表兼容后端展示字段和原始枚举值，避免车辆类型列为空。
const getCarTypeText = (row: any) => {
    const carTypeMap: Record<string, string> = {
        monthly: '月租车',
        temporary: '临时车',
    }

    return row.car_type_text || carTypeMap[row.car_type] || '-'
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

useRealtimeRefresh(() => getList(false), {
    scope: 'cars',
    immediate: false,
    intervalMs: 30000,
})
</script>

<template>
    <el-card>
        <template #header>
            <div class="card-header">
                <span>车辆列表</span>
                <el-button type="primary" @click="router.push('/car/create')"> 新增车辆 </el-button>
            </div>
        </template>

        <div class="list-toolbar">
            <el-input
                v-model="keyword"
                clearable
                placeholder="车牌号/业主"
                style="width: 250px"
                @keyup.enter="handleFilter"
                @clear="handleFilter"
            />
            <el-select v-model="statusFilter" clearable placeholder="车辆状态" style="width: 130px">
                <el-option label="正常" value="normal" />
                <el-option label="禁用" value="disabled" />
            </el-select>
            <el-button type="primary" @click="handleFilter">筛选</el-button>
            <el-button @click="resetSearch">重置</el-button>
        </div>

        <el-table :data="pagedTableData" border style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />

            <el-table-column prop="plate_no" label="车牌号" />

            <el-table-column prop="owner_name" label="所属业主" />

            <el-table-column label="车辆类型">
                <template #default="scope">
                    {{ getCarTypeText(scope.row) }}
                </template>
            </el-table-column>

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
                    <el-button type="primary" size="small" @click="handleDetail(scope.row)">
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

                    <el-button v-else type="primary" size="small" @click="handleEnable(scope.row)">
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
