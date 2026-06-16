<!-- 文件说明：实现 src/views/fee/list/FeeList.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { getFeeList } from '@/api/fee'
import { useRouter } from 'vue-router'
import { payFee } from '@/api/fee'
import { ElMessage } from 'element-plus'
import { useClientPagination } from '@/composables/useClientPagination'
import DataPagination from '@/components/common/DataPagination.vue'

const router = useRouter()
const role = localStorage.getItem('role') || ''
const isOwner = computed(() => role === 'owner')
const paymentDialogVisible = ref(false)
const payingId = ref<number | null>(null)
const paymentMethod = ref('alipay')

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

const loadData = async () => {
    const res = await getFeeList()

    tableData.value = res.data.data
    resetPage()
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
    paymentDialogVisible.value = false
    payingId.value = null

    await loadData()
}

onMounted(() => {
    loadData()
})
</script>

<template>
    <el-card>
        <template #header>
            <div style="display: flex; justify-content: space-between">
                <span>物业费列表</span>

                <el-button v-if="!isOwner" type="primary" @click="router.push('/fee/create')">
                    新增账单
                </el-button>
            </div>
        </template>

        <el-alert
            v-if="isOwner"
            class="fee-tip"
            type="info"
            show-icon
            :closable="false"
            title="业主查看账单后可点击缴费；若对账单有疑问，请联系服务人员核对。"
        />

        <el-table :data="pagedTableData" border>
            <el-table-column prop="id" label="ID" width="80" />

            <el-table-column prop="building_name" label="楼栋" />

            <el-table-column prop="unit_name" label="单元" />

            <el-table-column prop="room_no" label="房号" />

            <el-table-column prop="amount" label="金额" />

            <el-table-column prop="fee_type" label="费用类型" />

            <el-table-column prop="fee_month" label="账单月份" />

            <el-table-column label="支付方式" width="110">
                <template #default="scope">
                    {{ scope.row.payment_method_text || '-' }}
                </template>
            </el-table-column>

            <el-table-column label="状态">
                <template #default="scope">
                    <el-tag type="danger" v-if="scope.row.status === 'unpaid'"> 未缴费 </el-tag>

                    <el-tag type="warning" v-else-if="scope.row.status === 'overdue'">
                        已逾期
                    </el-tag>

                    <el-tag type="success" v-else> 已缴费 </el-tag>
                </template>
            </el-table-column>

            <el-table-column label="操作" width="120">
                <template #default="scope">
                    <el-button
                        v-if="scope.row.status === 'unpaid' || scope.row.status === 'overdue'"
                        type="success"
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
.fee-tip {
    margin-bottom: 16px;
}

.payment-methods {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
}
</style>
