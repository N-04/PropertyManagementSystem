<!-- 文件说明：实现 src/views/fee/list/FeeList.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { computed, nextTick, ref, onMounted, watch } from 'vue'
import { getFeeList, payFee } from '@/api/fee'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useClientPagination } from '@/composables/useClientPagination'
import { useRealtimeRefresh } from '@/composables/useRealtimeRefresh'
import DataPagination from '@/components/common/DataPagination.vue'
import { getStoredRole } from '@/utils/authState'

const router = useRouter()
const route = useRoute()
const role = getStoredRole()
const isOwner = computed(() => role === 'owner')
const canCreateFee = computed(() => ['admin', 'super_admin', 'property_admin'].includes(role))
const paymentDialogVisible = ref(false)
const payingId = ref<number | null>(null)
const paymentMethod = ref('alipay')

const filterForm = ref({
    keyword: '',
    fee_type: '',
    status: '',
    date_from: '',
    date_to: '',
})
const endDatePickerRef = ref<any>(null)

const feeTypeOptions = [
    { label: '物业费', value: 'property' },
    { label: '水费', value: 'water' },
    { label: '电费', value: 'electric' },
    { label: '车位费', value: 'parking' },
    { label: '其他费用', value: 'other' },
]

const feeTypeTextMap = feeTypeOptions.reduce<Record<string, string>>((map, item) => {
    map[item.value] = item.label
    return map
}, {})

const feeTypeText = (row: any) => feeTypeTextMap[row.fee_type] || row.fee_type_text || row.fee_type || '-'
const normalizeFeeStatus = (status: string) => {
    const statusMap: Record<string, string> = {
        unpaid: '未缴费',
        paid: '已缴费',
        overdue: '已逾期',
    }

    return statusMap[status] || status || '-'
}
const isPaidFeeRow = (item: any) => {
    return item.status === 'paid' || item.status === '已缴费' || item.status_text === '已缴费'
}
const validFeeTypes = feeTypeOptions.map((item) => item.value)
const validStatuses = ['unpaid', 'paid', 'overdue']
const isPaidRecordPage = computed(() => filterForm.value.status === 'paid')

const paymentOptions = [
    { label: '支付宝', value: 'alipay' },
    { label: '微信', value: 'wechat' },
    { label: '银行卡', value: 'bank_card' },
    { label: 'Apple Pay', value: 'apple_pay' },
    { label: '云闪付', value: 'union_pay' },
]

const tableData = ref<any[]>([])
const {
    page,
    pageSize,
    total,
    pagedData: pagedTableData,
    resetPage,
} = useClientPagination(tableData)

const buildQueryParams = () => {
    return {
        keyword: filterForm.value.keyword || undefined,
        fee_type: filterForm.value.fee_type || undefined,
        status: filterForm.value.status || undefined,
        date_from: filterForm.value.date_from || undefined,
        date_to: filterForm.value.date_to || undefined,
    }
}

const syncRouteFilters = () => {
    const routeFeeType = String(route.query.fee_type || '')
    const routeStatus = String(route.query.status || '')

    // 菜单通过 query 区分在线缴费、缴费记录和不同费用类型，页面查询条件要跟随 URL。
    filterForm.value.fee_type = validFeeTypes.includes(routeFeeType) ? routeFeeType : ''
    filterForm.value.status = validStatuses.includes(routeStatus) ? routeStatus : ''
}

const focusEndDatePicker = () => {
    const picker = endDatePickerRef.value

    if (picker?.handleOpen) {
        picker.handleOpen()
        return
    }

    picker?.focus?.()
}

const handleStartDateChange = async () => {
    if (filterForm.value.date_to && filterForm.value.date_to < filterForm.value.date_from) {
        filterForm.value.date_to = ''
    }

    // 先选开始日期，再自动打开结束日期，避免区间控件一次展示两个日期面板。
    await nextTick()
    focusEndDatePicker()
}

const isEndDateDisabled = (date: Date) => {
    if (!filterForm.value.date_from) {
        return false
    }

    return date.getTime() < new Date(`${filterForm.value.date_from}T00:00:00`).getTime()
}

const loadData = async (shouldResetPage = true) => {
    const res = await getFeeList(buildQueryParams())
    const rows = res.data.data || []
    const rawRows = Array.isArray(rows) ? rows : rows.results || []

    // 缴费记录页面只展示已缴费订单；如果后端未按 query 严格过滤，前端再做一次兜底。
    tableData.value = isPaidRecordPage.value
        ? rawRows.filter(isPaidFeeRow)
        : rawRows

    if (shouldResetPage) {
        resetPage()
    }
}

const searchBills = () => {
    loadData()
}

const resetFilters = () => {
    filterForm.value = {
        keyword: '',
        fee_type: '',
        status: '',
        date_from: '',
        date_to: '',
    }
    syncRouteFilters()

    loadData()
}

const handlePay = (id: number) => {
    // 先选择支付方式，再提交支付请求。
    payingId.value = id
    paymentMethod.value = 'alipay'
    paymentDialogVisible.value = true
}

const confirmPay = async () => {
    if (!payingId.value) {
        return
    }

    const res = await payFee(payingId.value, {
        payment_method: paymentMethod.value,
    })

    if (res.data.code !== 200) {
        ElMessage.error(res.data.msg || '缴费失败')
        return
    }

    ElMessage.success('缴费成功')

    const paidFee = res.data.data

    if (paidFee?.id) {
        tableData.value = tableData.value.map((item) =>
            item.id === paidFee.id ? { ...item, ...paidFee } : item
        )
    }

    paymentDialogVisible.value = false
    payingId.value = null

    await loadData(false)
}

onMounted(() => {
    syncRouteFilters()
    loadData()
})

watch(
    () => [route.query.fee_type, route.query.status],
    () => {
        syncRouteFilters()
        loadData()
    }
)

useRealtimeRefresh(
    async () => {
        await loadData(false)
    },
    {
        scope: 'fees',
        immediate: false,
        intervalMs: 30000,
    },
)
</script>

<template>
    <el-card class="page-card fee-page-card">
        <template #header>
            <div class="card-header">
                <span>费用账单</span>

                <el-button v-if="canCreateFee" type="primary" @click="router.push('/fee/create')">
                    新增账单
                </el-button>
            </div>
        </template>

        <el-alert
            v-if="isOwner && !isPaidRecordPage"
            class="fee-tip"
            type="info"
            show-icon
            :closable="false"
            title="业主查看账单后可点击缴费；若对账单有疑问，请联系服务人员核对。"
        />

        <el-form class="filter-form" :model="filterForm" inline>
            <el-form-item label="搜索">
                <el-input
                    v-model="filterForm.keyword"
                    clearable
                    placeholder="业主/手机号/房号/备注"
                    @keyup.enter="searchBills"
                />
            </el-form-item>

            <el-form-item label="费用类型">
                <el-select
                    v-model="filterForm.fee_type"
                    clearable
                    placeholder="全部类型"
                    style="width: 140px"
                >
                    <el-option
                        v-for="item in feeTypeOptions"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    />
                </el-select>
            </el-form-item>

            <el-form-item label="截止日期">
                <div class="date-filter">
                    <el-date-picker
                        v-model="filterForm.date_from"
                        type="date"
                        placeholder="开始日期"
                        value-format="YYYY-MM-DD"
                        @change="handleStartDateChange"
                    />
                    <span class="date-separator">至</span>
                    <el-date-picker
                        ref="endDatePickerRef"
                        v-model="filterForm.date_to"
                        type="date"
                        placeholder="结束日期"
                        value-format="YYYY-MM-DD"
                        :disabled-date="isEndDateDisabled"
                    />
                </div>
            </el-form-item>

            <el-form-item>
                <el-button type="primary" @click="searchBills">筛选</el-button>
                <el-button @click="resetFilters">重置</el-button>
            </el-form-item>
        </el-form>

        <el-table class="comfortable-table" :data="pagedTableData" border>
            <el-table-column prop="id" label="ID" width="80" />

            <el-table-column prop="building_name" label="楼栋" />

            <el-table-column prop="unit_name" label="单元" />

            <el-table-column prop="room_no" label="房号" />

            <el-table-column prop="amount" label="金额" />

            <el-table-column label="费用类型">
                <template #default="scope">
                    {{ feeTypeText(scope.row) }}
                </template>
            </el-table-column>

            <el-table-column prop="deadline" label="截止日期" min-width="160" />

            <el-table-column label="支付方式" width="110">
                <template #default="scope">
                    {{ scope.row.payment_method_text || '-' }}
                </template>
            </el-table-column>

            <el-table-column label="状态">
                <template #default="scope">
                    <el-tag type="danger" v-if="scope.row.status === 'unpaid'">
                        {{ normalizeFeeStatus(scope.row.status) }}
                    </el-tag>

                    <el-tag type="warning" v-else-if="scope.row.status === 'overdue'">
                        {{ normalizeFeeStatus(scope.row.status) }}
                    </el-tag>

                    <el-tag type="success" v-else>
                        {{ normalizeFeeStatus(scope.row.status) }}
                    </el-tag>
                </template>
            </el-table-column>

            <el-table-column label="操作" width="120">
                <template #default="scope">
                    <el-button
                        v-if="isOwner && (scope.row.status === 'unpaid' || scope.row.status === 'overdue')"
                        type="primary"
                        size="small"
                        @click="handlePay(scope.row.id)"
                    >
                        缴费
                    </el-button>
                </template>
            </el-table-column>

            <el-table-column prop="remark" label="备注" />
        </el-table>

        <DataPagination
            v-model:current-page="page"
            v-model:page-size="pageSize"
            :page-sizes="[5, 10, 20, 50]"
            :total="total"
            background
            layout="total, sizes, prev, pager, next, jumper"
        />

        <el-dialog v-model="paymentDialogVisible" title="选择支付方式" width="420px">
            <el-radio-group v-model="paymentMethod" class="payment-methods">
                <el-radio
                    v-for="item in paymentOptions"
                    :key="item.value"
                    :label="item.value"
                    border
                >
                    {{ item.label }}
                </el-radio>
            </el-radio-group>

            <template #footer>
                <el-button @click="paymentDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="confirmPay">确认支付</el-button>
            </template>
        </el-dialog>
    </el-card>
</template>

<style scoped>
.fee-page-card {
    border: 1px solid var(--border-color);
    border-radius: 8px;
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
}

:deep(.fee-page-card > .el-card__header) {
    padding: 22px 24px;
    border-bottom-color: var(--border-color);
}

:deep(.fee-page-card > .el-card__body) {
    padding: 24px;
}

.card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    color: var(--text-heading);
    font-size: 18px;
    font-weight: 700;
    line-height: 26px;
}

.fee-tip {
    margin-bottom: 22px;
}

.filter-form {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 14px 18px;
    margin-bottom: 24px;
}

:deep(.filter-form .el-form-item) {
    margin: 0;
    align-items: center;
}

:deep(.filter-form .el-form-item__label) {
    height: 36px;
    display: inline-flex;
    align-items: center;
    color: var(--text-subtle);
    font-weight: 600;
}

:deep(.filter-form .el-input__wrapper),
:deep(.filter-form .el-select__wrapper) {
    min-height: 38px;
    border-radius: 6px;
}

.filter-form .el-input {
    width: 220px;
}

.date-filter {
    display: flex;
    align-items: center;
    gap: 8px;
}

.date-separator {
    color: #64748b;
}

.payment-methods {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
}

.comfortable-table {
    width: 100%;
}

:deep(.comfortable-table .el-table__header th) {
    height: 48px;
    background: var(--surface-muted);
    color: var(--text-subtle);
    font-size: 13px;
    font-weight: 600;
    line-height: 20px;
}

:deep(.comfortable-table .el-table__body td) {
    padding: 14px 0;
    color: var(--text-primary);
    font-size: 14px;
    line-height: 22px;
}

:deep(.el-pagination) {
    margin-top: 24px;
    justify-content: center;
}
</style>
