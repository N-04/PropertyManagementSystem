<!-- 文件说明：实现 src/views/fee/create/FeeCreate.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { getHouseList } from '@/api/house'
import { createFee } from '@/api/fee'
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

const router = useRouter()

const form = ref({
    house: '',
    amount: '',
    fee_type: 'property',
    fee_month: '',
    status: 'unpaid',
    remark: '',
})

// 数据源分块：费用账单需要先加载房屋列表，供新增账单绑定到具体房屋。
const houseList = ref<any[]>([])

const loadHouseList = async () => {
    const res = await getHouseList()

    houseList.value = res.data.data
}

// 提交分块：创建成功后回到费用列表，并重置本地表单避免残留输入。
const submitForm = async () => {
    await createFee(form.value)

    ElMessage.success('新增成功')

    router.push('/fee/list')

    form.value = {
        house: '',
        amount: '',
        fee_type: 'property',
        fee_month: '',
        status: 'unpaid',
        remark: '',
    }
}

onMounted(() => {
    loadHouseList()
})
</script>

<template>
    <!-- 表单分块：录入房屋、费用类型、月份和缴费状态。 -->
    <el-form-item label="房屋">
        <el-select v-model="form.house" placeholder="请选择房屋">
            <el-option
                v-for="item in houseList"
                :key="item.id"
                :label="item.room_no"
                :value="item.id"
            />
        </el-select>
    </el-form-item>

    <el-form-item label="金额">
        <el-input v-model="form.amount" />
    </el-form-item>

    <el-form-item label="费用类型">
        <el-select v-model="form.fee_type">
            <el-option label="物业费" value="property" />
            <el-option label="车位费" value="parking" />
            <el-option label="水费" value="water" />
            <el-option label="电费" value="electric" />
        </el-select>
    </el-form-item>

    <el-form-item label="账单月份">
        <el-input v-model="form.fee_month" placeholder="2026-06" />
    </el-form-item>

    <el-form-item label="状态">
        <el-select v-model="form.status">
            <el-option label="未缴费" value="unpaid" />
            <el-option label="已缴费" value="paid" />
        </el-select>
    </el-form-item>
    <el-form-item label="备注">
        <el-input v-model="form.remark" />
    </el-form-item>
    <!-- 操作分块：新增账单只保留提交入口。 -->
    <el-form-item label="提交">
        <el-button type="primary" @click="submitForm"> 提交 </el-button>
    </el-form-item>
</template>
