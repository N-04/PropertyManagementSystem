<!-- 文件说明：实现 src/views/repair/list/RepairList.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { onMounted, reactive, ref, nextTick, watch } from 'vue'
import { deleteRepair } from '@/api/repair'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getRepairList } from '@/api/repair'
import { updateRepair } from '@/api/repair'
import { useRoute, useRouter } from 'vue-router'
import { useClientPagination } from '@/composables/useClientPagination'
import DataPagination from '@/components/common/DataPagination.vue'
import Upload from '@/views/upload/Upload.vue'

const router = useRouter()
const route = useRoute()
const role = localStorage.getItem('role') || ''
const isOwner = role === 'owner'
const isRepairer = role === 'repairer'

const startRef = ref()
const endRef = ref()

const handleStartChange = () => {
    nextTick(() => {
        endRef.value?.focus()
    })
}
// 定义维修数据类型
interface RepairItem {
    id: number
    title: string
    content: string
    status: 'pending' | 'assigned' | 'accepted' | 'processing' | 'finished'
    owner_name?: string
    phone?: string
    repair_user_name?: string[]
    repair_result?: string
    result_image_list?: string[]
    evaluation_score?: number | string | null
    evaluation_content?: string
    evaluation_time?: string | null
}

// 表格数据
const tableData = ref<RepairItem[]>([])
const {
    page,
    pageSize,
    total,
    pagedData: pagedTableData,
    resetPage,
} = useClientPagination(tableData)

// 加载数据
const loadData = async () => {
    const res = await getRepairList(queryForm.value)

    tableData.value = res.data.data
    resetPage()
}
// 点击搜索
const handleSearch = () => {
    loadData()
}

// 重置搜索
const handleReset = () => {
    queryForm.value = {
        keyword: '',
        status: '',
        start_time: '',
        end_time: '',
    }

    dateRange.value = []

    loadData()
}
const resetSearch = handleReset

// 查看
const handleDetail = (row: any) => {
    router.push('/repair/detail/' + row.id)
}

// 编辑
const handleEdit = (row: any) => {
    router.push('/repair/edit/' + row.id)
}

// 分配
const handleAssign = (row: any) => {
    router.push('/repair/assign/' + row.id)
}

const updateRepairStatus = async (row: RepairItem, status: RepairItem['status'], message: string) => {
    await updateRepair(row.id, {
        status,
    })

    ElMessage.success(message)

    await loadData()
}

// 已完成
const finishDialogVisible = ref(false)
const finishRow = ref<any>(null)
const finishForm = reactive({
    repair_result: '',
    resultImages: [] as string[],
})

const handleFinish = (row: any) => {
    finishRow.value = row
    finishForm.repair_result = row.repair_result || ''
    finishForm.resultImages = row.result_image_list || []
    finishDialogVisible.value = true
}

const submitFinish = async () => {
    if (!finishRow.value) {
        return
    }

    if (!finishForm.repair_result) {
        ElMessage.warning('请填写维修结果')
        return
    }

    await updateRepair(finishRow.value.id, {
        status: 'finished',
        repair_result: finishForm.repair_result,
        result_images: finishForm.resultImages.join('|'),
    })

    ElMessage.success('维修完成')
    finishDialogVisible.value = false

    await loadData()
}

const getFileUrl = (url: string) => {
    if (!url) {
        return ''
    }

    return url.startsWith('http') ? url : `http://127.0.0.1:8000${url}`
}

const addResultImage = (url: string) => {
    finishForm.resultImages.push(url)
}

const removeResultImage = (index: number) => {
    finishForm.resultImages.splice(index, 1)
}

// 维修评价
const evaluateDialogVisible = ref(false)
const evaluateRow = ref<RepairItem | null>(null)
const evaluateForm = reactive({
    score: 5,
    content: '',
})

const handleEvaluate = (row: RepairItem) => {
    evaluateRow.value = row
    evaluateForm.score = Number(row.evaluation_score || 5)
    evaluateForm.content = row.evaluation_content || ''
    evaluateDialogVisible.value = true
}

const submitEvaluation = async () => {
    if (!evaluateRow.value) {
        return
    }

    if (!evaluateForm.score) {
        ElMessage.warning('请选择维修评分')
        return
    }

    await updateRepair(evaluateRow.value.id, {
        evaluation_score: evaluateForm.score,
        evaluation_content: evaluateForm.content,
    })

    ElMessage.success('评价已提交')
    evaluateDialogVisible.value = false

    await loadData()
}

// 日期筛选
const dateRange = ref([])

const handleDateChange = (val: any) => {
    if (val) {
        queryForm.value.start_time = val[0]
        queryForm.value.end_time = val[1]
    } else {
        queryForm.value.start_time = ''
        queryForm.value.end_time = ''
    }
}

const queryForm = ref({
    keyword: '',
    status: '',
    start_time: '',
    end_time: '',
})

const availableStatuses = ['pending', 'assigned', 'accepted', 'processing', 'finished']

const syncStatusFromRoute = () => {
    const routeStatus = String(route.query.status || '')

    queryForm.value.status = availableStatuses.includes(routeStatus) ? routeStatus : ''
}

watch(
    () => route.query.status,
    () => {
        syncStatusFromRoute()
        loadData()
    }
)

// 删除报修记录
const handleDelete = async (row: any) => {
    await ElMessageBox.confirm('确认删除该报修记录吗？', '提示')

    await deleteRepair(row.id)

    ElMessage.success('删除成功')

    await loadData()
}

// 页面加载
onMounted(() => {
    syncStatusFromRoute()
    loadData()
})
</script>

<template>
    <el-card class="search-card">
        <!-- 按钮自动靠右 -->
        <el-row justify="space-between" align="middle">
            <el-col :span="20">
                <el-form :inline="true" :model="queryForm">
                    <el-form-item>
                        <div
                            style="
                                display: flex;
                                justify-content: space-between;
                                align-items: center;
                            "
                        >
                            <!-- 输入框回车搜索 -->
                            <el-form-item>
                                <el-input
                                    v-model="queryForm.keyword"
                                    @keyup.enter="loadData"
                                    placeholder="标题/业主"
                                    style="width: 220px"
                                />
                            </el-form-item>

                            <el-form-item>
                                <el-select
                                    v-model="queryForm.status"
                                    placeolder="全部状态"
                                    clearable
                                    style="width: 140px"
                                >
                                    <el-option label="待派单" value="pending" />
                                    <el-option label="待接单" value="assigned" />
                                    <el-option label="已接单" value="accepted" />
                                    <el-option label="维修中" value="processing" />
                                    <el-option label="已完成" value="finished" />
                                </el-select>
                            </el-form-item>
                            <!-- 输start_time时候显示开始日期框，输完start_time自动跳转end_time和日期框 -->
                            <!-- 选开始日期,自动 focus,结束日期弹出来 -->
                            <el-form-item>
                                <el-date-picker
                                    ref="startRef"
                                    v-model="queryForm.start_time"
                                    type="date"
                                    placeholder="开始日期"
                                    value-format="YYYY-MM-DD"
                                    @change="handleStartChange"
                                />
                            </el-form-item>

                            <el-form-item>
                                <el-date-picker
                                    ref="endRef"
                                    v-model="queryForm.end_time"
                                    type="date"
                                    placeholder="结束日期"
                                    value-format="YYYY-MM-DD"
                                />
                            </el-form-item>
                            <el-form-item>
                                <el-button type="primary" @click="loadData"> 搜索 </el-button>
                                <el-button @click="resetSearch"> 重置 </el-button>
                            </el-form-item>
                        </div>
                    </el-form-item>
                </el-form>
            </el-col>
            <el-form-item>
                <el-col :span="4" style="text-align: right">
                    <el-button
                        v-if="isOwner"
                        type="primary"
                        @click="router.push('/repair/create')"
                    >
                        新增报修
                    </el-button>
                </el-col>
            </el-form-item>
        </el-row>
    </el-card>

    <el-card>
        <el-row>
            <el-table :data="pagedTableData" border height="250" style="width: 100%" align="middle">
                <el-table-column prop="id" label="ID" width="80" />

                <el-table-column prop="title" label="报修标题" />

                <el-table-column prop="content" label="报修内容" />

                <el-table-column prop="owner_name" label="报修业主" />

                <el-table-column prop="phone" label="联系电话" />

                <el-table-column prop="repair_user_name" label="维修人员" />

                <el-table-column label="状态">
                    <template #default="scope">
                        <el-tag v-if="scope.row.status === 'pending'" type="warning">
                            待派单
                        </el-tag>

                        <el-tag v-else-if="scope.row.status === 'assigned'" type="warning">
                            待接单
                        </el-tag>

                        <el-tag v-else-if="scope.row.status === 'accepted'" type="info">
                            已接单
                        </el-tag>

                        <el-tag v-else-if="scope.row.status === 'processing'" type="primary">
                            维修中
                        </el-tag>

                        <el-tag v-else-if="scope.row.status === 'finished'" type="success">
                            已完成
                        </el-tag>
                    </template>
                </el-table-column>

                <el-table-column prop="created_at" label="创建时间" width="200" />

                <el-table-column label="操作" width="260">
                    <template #default="scope">
                        <el-button type="success" @click="handleDetail(scope.row)">
                            查看
                        </el-button>

                        <el-button
                            v-if="scope.row.status === 'pending'"
                            type="primary"
                            @click="handleEdit(scope.row)"
                        >
                            编辑
                        </el-button>

                        <el-button
                            v-if="!isOwner && !isRepairer && scope.row.status === 'pending'"
                            type="warning"
                            @click="handleAssign(scope.row)"
                        >
                            分配
                        </el-button>

                        <el-button
                            v-if="isRepairer && scope.row.status === 'assigned'"
                            type="primary"
                            @click="updateRepairStatus(scope.row, 'accepted', '接单成功')"
                        >
                            接单
                        </el-button>

                        <el-button
                            v-if="isRepairer && scope.row.status === 'accepted'"
                            type="primary"
                            @click="updateRepairStatus(scope.row, 'processing', '已开始维修')"
                        >
                            开始维修
                        </el-button>

                        <el-button
                            v-if="isRepairer && scope.row.status === 'processing'"
                            type="success"
                            @click="handleFinish(scope.row)"
                        >
                            完成维修
                        </el-button>

                        <el-button
                            v-if="isOwner && scope.row.status === 'finished'"
                            type="warning"
                            @click="handleEvaluate(scope.row)"
                        >
                            {{ scope.row.evaluation_score ? '修改评价' : '评价' }}
                        </el-button>

                        <el-button
                            v-if="scope.row.status === 'pending'"
                            type="danger"
                            @click="handleDelete(scope.row)"
                        >
                            删除
                        </el-button>
                    </template>
                </el-table-column>

                <el-table-column prop="finish_time" label="完成时间" width="180" />
            </el-table>
        </el-row>

        <DataPagination
            v-model:current-page="page"
            v-model:page-size="pageSize"
            :page-sizes="[5, 10, 20, 50]"
            :total="total"
            background
            layout="total, sizes, prev, pager, next, jumper"
        />
    </el-card>

    <el-dialog v-model="finishDialogVisible" title="上传维修结果" width="560px">
        <el-form label-width="100px">
            <el-form-item label="维修结果">
                <el-input v-model="finishForm.repair_result" type="textarea" :rows="4" />
            </el-form-item>

            <el-form-item label="结果图片">
                <Upload upload-type="repair_image" @success="addResultImage" />

                <div v-if="finishForm.resultImages.length" class="image-list">
                    <div
                        v-for="(image, index) in finishForm.resultImages"
                        :key="image"
                        class="image-item"
                    >
                        <el-image
                            :src="getFileUrl(image)"
                            :preview-src-list="finishForm.resultImages.map(getFileUrl)"
                            fit="cover"
                        />
                        <el-button type="danger" link @click="removeResultImage(index)">
                            删除
                        </el-button>
                    </div>
                </div>
            </el-form-item>
        </el-form>

        <template #footer>
            <el-button @click="finishDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="submitFinish">提交结果</el-button>
        </template>
    </el-dialog>

    <el-dialog v-model="evaluateDialogVisible" title="维修评价" width="520px">
        <el-form label-width="100px">
            <el-form-item label="维修评分">
                <el-rate
                    v-model="evaluateForm.score"
                    :max="5"
                    allow-half
                    show-score
                    text-color="#ff9900"
                    score-template="{value} 分"
                />
            </el-form-item>

            <el-form-item label="评价内容">
                <el-input
                    v-model="evaluateForm.content"
                    type="textarea"
                    :rows="4"
                    maxlength="300"
                    show-word-limit
                />
            </el-form-item>
        </el-form>

        <template #footer>
            <el-button @click="evaluateDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="submitEvaluation">提交评价</el-button>
        </template>
    </el-dialog>
</template>

<style scoped>
.image-list {
    display: flex;
    gap: 12px;
    margin-top: 12px;
    flex-wrap: wrap;
}

.image-item {
    width: 96px;
}

.image-item :deep(.el-image) {
    width: 96px;
    height: 72px;
    border-radius: 4px;
    border: 1px solid #ebeef5;
}
</style>
