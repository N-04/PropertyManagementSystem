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
import RepairResultDrawer from '@/components/repair/RepairResultDrawer.vue'
import { getStoredRole, getStoredUsername } from '@/utils/authState'
import { appendMessageFeedback } from '@/utils/messageCenterRows'

const router = useRouter()
const route = useRoute()
const role = getStoredRole()
const isOwner = role === 'owner'
const isRepairer = ['repair_staff', 'repairer', 'repair'].includes(role)
const REPAIR_EVALUATION_FEEDBACK_EVENT = 'property-management-repair-evaluation-feedback'
const REPAIR_EVALUATION_FEEDBACK_STORAGE_KEY = 'repairEvaluationFeedback'

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

// 维修员点击“上传结果”后，在右侧抽屉内完成拍照上传和结果提交。
const finishDrawerVisible = ref(false)
const finishRow = ref<any>(null)

const handleFinish = (row: any) => {
    finishRow.value = row
    finishDrawerVisible.value = true
}

// 维修评价
const evaluateDialogVisible = ref(false)
const evaluationSubmitting = ref(false)
const evaluateRow = ref<RepairItem | null>(null)
const evaluationCompletedIds = new Set<number>()
const evaluateForm = reactive({
    score: 5,
    content: '',
})

const handleEvaluate = (row: RepairItem) => {
    if (row.evaluation_score || evaluationCompletedIds.has(row.id)) {
        ElMessage.info('该工单已评价，不能重复提交')
        return
    }

    evaluateRow.value = row
    evaluateForm.score = Number(row.evaluation_score || 5)
    evaluateForm.content = row.evaluation_content || ''
    evaluateDialogVisible.value = true
}

const emitEvaluationFeedback = (repair: RepairItem, score: number) => {
    const feedback = {
        id: Date.now(),
        repair_id: repair.id,
        title: repair.title,
        score,
        message: `${getStoredUsername() || repair.owner_name || '业主'} 已对工单「${repair.title}」提交 ${score.toFixed(1)} 分评价，请维修人员和管理员及时查看。`,
        created_at: new Date().toLocaleString('zh-CN', { hour12: false }),
    }

    appendMessageFeedback(REPAIR_EVALUATION_FEEDBACK_STORAGE_KEY, feedback)
    window.dispatchEvent(new CustomEvent(REPAIR_EVALUATION_FEEDBACK_EVENT, { detail: feedback }))
}

const submitEvaluation = async () => {
    if (!evaluateRow.value || evaluationSubmitting.value) {
        return
    }

    if (!evaluateForm.score) {
        ElMessage.warning('请选择维修评分')
        return
    }

    evaluationSubmitting.value = true

    try {
        const currentRow = evaluateRow.value
        const score = Number(evaluateForm.score.toFixed(1))
        const res = await updateRepair(currentRow.id, {
            evaluation_score: score,
            evaluation_content: evaluateForm.content,
        })

        if (res.data.code !== 200) {
            // 后端判定已评价时同步关闭弹窗并隐藏按钮，避免用户在旧弹窗里重复点击。
            if ((res.data.msg || '').includes('已评价') || (res.data.msg || '').includes('重复提交')) {
                evaluationCompletedIds.add(currentRow.id)
                evaluateDialogVisible.value = false
                evaluateRow.value = null
                await loadData()
            }

            ElMessage.error(res.data.msg || '评价提交失败')
            return
        }

        evaluationCompletedIds.add(currentRow.id)
        emitEvaluationFeedback(res.data.data || currentRow, score)
        ElMessage.success(res.data.msg || '评价已提交')
        evaluateDialogVisible.value = false
        evaluateRow.value = null

        await loadData()
    } finally {
        evaluationSubmitting.value = false
    }
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
    <el-card>
        <template #header>
            <div class="card-header">
                <span>报修工单</span>
                <el-button v-if="isOwner" type="primary" @click="router.push('/repair/create')">
                    新增报修
                </el-button>
            </div>
        </template>

        <el-form class="filter-form" :inline="true" :model="queryForm">
            <el-form-item label="搜索">
                <el-input
                    v-model="queryForm.keyword"
                    clearable
                    placeholder="标题/业主"
                    style="width: 220px"
                    @keyup.enter="loadData"
                />
            </el-form-item>

            <el-form-item label="状态">
                <el-select
                    v-model="queryForm.status"
                    clearable
                    placeholder="全部状态"
                    style="width: 140px"
                >
                    <el-option label="待派单" value="pending" />
                    <el-option label="待接单" value="assigned" />
                    <el-option label="已接单" value="accepted" />
                    <el-option label="维修中" value="processing" />
                    <el-option label="已完成" value="finished" />
                </el-select>
            </el-form-item>

            <el-form-item label="提交日期">
                <div class="date-filter">
                    <el-date-picker
                        ref="startRef"
                        v-model="queryForm.start_time"
                        type="date"
                        placeholder="开始日期"
                        value-format="YYYY-MM-DD"
                        @change="handleStartChange"
                    />
                    <span class="date-separator">至</span>
                    <el-date-picker
                        ref="endRef"
                        v-model="queryForm.end_time"
                        type="date"
                        placeholder="结束日期"
                        value-format="YYYY-MM-DD"
                    />
                </div>
            </el-form-item>

            <el-form-item>
                <el-button type="primary" @click="loadData">筛选</el-button>
                <el-button @click="resetSearch">重置</el-button>
            </el-form-item>
        </el-form>

        <el-table :data="pagedTableData" border style="width: 100%" align="middle">
            <el-table-column prop="id" label="ID" width="80" />

            <el-table-column prop="title" label="报修标题" min-width="140" show-overflow-tooltip />

            <el-table-column prop="content" label="报修内容" min-width="180" show-overflow-tooltip />

            <el-table-column prop="owner_name" label="报修业主" width="110" />

            <el-table-column prop="phone" label="联系电话" width="130" />

            <el-table-column prop="repair_user_name" label="维修人员" width="120" />

            <el-table-column label="状态" width="100">
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

            <el-table-column prop="created_at" label="创建时间" width="180" />

            <el-table-column prop="finish_time" label="完成时间" width="180" />

            <el-table-column label="操作" width="230" fixed="right">
                <template #default="scope">
                    <el-button type="primary" size="small" @click="handleDetail(scope.row)">
                        查看
                    </el-button>

                    <el-button
                        v-if="scope.row.status === 'pending'"
                        type="primary"
                        size="small"
                        @click="handleEdit(scope.row)"
                    >
                        编辑
                    </el-button>

                    <el-button
                        v-if="!isOwner && !isRepairer && scope.row.status === 'pending'"
                        type="warning"
                        size="small"
                        @click="handleAssign(scope.row)"
                    >
                        分配
                    </el-button>

                    <el-button
                        v-if="isRepairer && scope.row.status === 'assigned'"
                        type="primary"
                        size="small"
                        @click="updateRepairStatus(scope.row, 'accepted', '接单成功')"
                    >
                        接单
                    </el-button>

                    <el-button
                        v-if="isRepairer && scope.row.status === 'accepted'"
                        type="primary"
                        size="small"
                        @click="updateRepairStatus(scope.row, 'processing', '已开始维修')"
                    >
                        开始维修
                    </el-button>

                    <el-button
                        v-if="isRepairer && scope.row.status === 'processing'"
                        type="primary"
                        size="small"
                        @click="handleFinish(scope.row)"
                    >
                        上传结果
                    </el-button>

                    <el-button
                        v-if="isOwner && scope.row.status === 'finished' && !scope.row.evaluation_score && !evaluationCompletedIds.has(scope.row.id)"
                        type="warning"
                        size="small"
                        @click="handleEvaluate(scope.row)"
                    >
                        评价
                    </el-button>

                    <el-tag
                        v-else-if="isOwner && scope.row.status === 'finished'"
                        type="success"
                    >
                        已评价
                    </el-tag>

                    <el-button
                        v-if="scope.row.status === 'pending'"
                        type="danger"
                        size="small"
                        @click="handleDelete(scope.row)"
                    >
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

    <RepairResultDrawer
        v-model="finishDrawerVisible"
        :repair="finishRow"
        @submitted="loadData"
    />

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
            <el-button
                type="primary"
                :loading="evaluationSubmitting"
                :disabled="evaluationSubmitting"
                @click="submitEvaluation"
            >
                提交评价
            </el-button>
        </template>
    </el-dialog>
</template>

<style scoped>
.date-filter {
    display: flex;
    align-items: center;
    gap: 8px;
}

.date-separator {
    color: var(--text-muted);
}

</style>
