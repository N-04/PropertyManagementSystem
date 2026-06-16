<!-- 文件说明：实现 src/views/dashboard/DashboardPage.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { getDashboard } from '@/api/dashboard'

import FeeChart from '@/components/charts/FeeChart.vue'
import RepairChart from '@/components/charts/RepairChart.vue'
import HouseChart from '@/components/charts/HouseChart.vue'
import { getStoredRole, getStoredUsername } from '@/utils/authState'

// 当前登录用户
const username = getStoredUsername() || '用户'
const role = getStoredRole()

// 首页统计数据
const data = ref({
    house_count: 0,
    owner_count: 0,
    parking_count: 0,
    repair_count: 0,

    fee_total: 0,
    fee_paid: 0,
    fee_unpaid: 0,

    repair_pending: 0,
    repair_processing: 0,
    repair_finished: 0,
    paid_count: 0,
    unpaid_count: 0,
})

const adminRoles = ['admin', 'super_admin', 'property_admin']
const financeRoles = ['finance_staff', 'finance']
const repairRoles = ['repair_staff', 'repairer', 'repair']

const showHouseChart = computed(() => {
    return adminRoles.includes(role)
})

const showFeeChart = computed(() => {
    return adminRoles.includes(role) || financeRoles.includes(role)
})

const showRepairChart = computed(() => {
    return adminRoles.includes(role) || repairRoles.includes(role)
})

const chartCount = computed(() => {
    return [showHouseChart.value, showFeeChart.value, showRepairChart.value].filter(Boolean).length
})

const chartColumnSpan = computed(() => {
    if (chartCount.value >= 3) {
        return 8
    }

    if (chartCount.value === 2) {
        return 12
    }

    return 16
})

/**
 * 获取首页统计数据
 */
const loadData = async () => {
    const res = await getDashboard()

    data.value = {
        ...data.value,
        ...res.data.data,
    }
}

onMounted(() => {
    if (chartCount.value) {
        loadData()
    }
})
</script>

<template>
    <el-card v-if="chartCount">
        <template #header>
            <div style="display: flex; justify-content: space-between">
                <span>首页统计</span>
                <span class="dashboard-user">
                    欢迎您：{{ username }}
                </span>
            </div>
        </template>

        <el-row :gutter="20" class="dashboard-chart-row">
            <el-col v-if="showHouseChart" :span="chartColumnSpan">
                <el-card>
                    <!-- 管理员查看房屋、业主、车位和报修总量图表。 -->
                    <HouseChart :dashboard-data="data" />
                </el-card>
            </el-col>

            <el-col v-if="showFeeChart" :span="chartColumnSpan">
                <el-card>
                    <!-- 管理员和财务人员查看费用图表。 -->
                    <FeeChart :dashboard-data="data" />
                </el-card>
            </el-col>

            <el-col v-if="showRepairChart" :span="chartColumnSpan">
                <el-card>
                    <!-- 管理员和维修员查看维修工单图表。 -->
                    <RepairChart :dashboard-data="data" />
                </el-card>
            </el-col>
        </el-row>
    </el-card>

    <el-card v-else class="plain-home-card">
        <template #header>
            <div style="display: flex; justify-content: space-between">
                <span>首页</span>
                <span class="dashboard-user">
                    欢迎您：{{ username }}
                </span>
            </div>
        </template>

        <el-empty
            description="请通过左侧业主模块办理业务"
            :image-size="120"
        />
    </el-card>
</template>

<style scoped>
h2 {
    margin-top: 10px;
    text-align: center;
    color: #409eff;
}

.el-card {
    text-align: center;
}

.dashboard-chart-row {
    justify-content: center;
}

.plain-home-card {
    min-height: 260px;
}
</style>
