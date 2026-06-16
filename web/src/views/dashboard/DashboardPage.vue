<!-- 文件说明：实现 src/views/dashboard/DashboardPage.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getDashboard } from '@/api/dashboard'
import { getVisitorStatistics } from '@/api/visitor'
import { getNoticeList } from '@/api/notice'
import { getFeeList } from '@/api/fee'
import { getRepairList } from '@/api/repair'
import { getComplaintList } from '@/api/complaint'

import FeeChart from '@/components/charts/FeeChart.vue'
import RepairChart from '@/components/charts/RepairChart.vue'
import HouseChart from '@/components/charts/HouseChart.vue'

const router = useRouter()

// 当前登录用户
const username = localStorage.getItem('username') || '用户'
const role = localStorage.getItem('role') || ''
const isOwner = computed(() => role === 'owner')
const noticeMessages = ref<string[]>([])
const roleMessages = ref<string[]>([])

const rollingMessages = computed(() => {
    const messages = [...noticeMessages.value, ...roleMessages.value].filter(Boolean)

    if (messages.length) {
        return messages.slice(0, 8)
    }

    return ['系统运行正常，欢迎使用社区物业管理系统']
})

const rollingText = computed(() => rollingMessages.value.join('　　'))

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
})

// 访客统计数据
const statistics = ref({
    today_count: 0,
    waiting: 0,
    approved: 0,
    entered: 0,
    left: 0,
    total: 0,
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

/**
 * 获取访客统计
 */
const loadStatistics = async () => {
    const res = await getVisitorStatistics()

    statistics.value = {
        ...statistics.value,
        ...res.data.data,
    }
}

const loadNoticeMessages = async () => {
    try {
        const res = await getNoticeList()
        const list = res.data.data || []

        noticeMessages.value = list
            .filter((item: any) => item.status !== 'draft')
            .slice(0, 3)
            .map((item: any) => `公告通知：${item.title}`)
    } catch (error) {
        noticeMessages.value = []
    }
}

const loadRoleMessages = async () => {
    const messages: string[] = []

    try {
        if (['owner', 'finance', 'finance_staff', 'admin', 'super_admin'].includes(role)) {
            const feeRes = await getFeeList()
            const fees = feeRes.data.data || []
            const unpaidFees = fees.filter((item: any) => item.status === 'unpaid' || item.status === 'overdue')

            if (unpaidFees.length) {
                messages.push(`缴费提醒：当前有 ${unpaidFees.length} 条待缴或逾期账单`)
            }
        }
    } catch (error) {
        // 首页提示不影响主统计展示。
    }

    try {
        if (['owner', 'repair_staff', 'repair', 'property_admin', 'admin', 'super_admin'].includes(role)) {
            const repairRes = await getRepairList({})
            const repairs = repairRes.data.data || []
            const activeRepairs = repairs.filter((item: any) => item.status !== 'finished')

            if (activeRepairs.length) {
                messages.push(`工单通知：当前有 ${activeRepairs.length} 条待处理或进行中工单`)
            }
        }
    } catch (error) {
        // 首页提示不影响主统计展示。
    }

    try {
        if (['property_admin', 'customer_service', 'service', 'admin', 'super_admin'].includes(role)) {
            const complaintRes = await getComplaintList({ status: 'pending' })
            const complaints = complaintRes.data.data || []

            if (complaints.length) {
                messages.push(`投诉提醒：当前有 ${complaints.length} 条投诉/建议待处理`)
            }
        }
    } catch (error) {
        // 首页提示不影响主统计展示。
    }

    roleMessages.value = messages
}

onMounted(() => {
    loadData()
    loadStatistics()
    loadNoticeMessages()
    loadRoleMessages()
})
</script>

<template>
    <el-card>
        <template #header>
            <div style="display: flex; justify-content: space-between">
                <span>首页统计</span>
                <span class="dashboard-user">
                    欢迎您：{{ username }}
                    <el-button v-if="isOwner" type="primary" link @click="router.push('/contact/service')">
                        联系客服
                    </el-button>
                </span>
            </div>
        </template>

        <div class="notice-marquee" aria-label="首页滚动通知">
            <div class="notice-label">滚动通知</div>
            <div class="notice-track">
                <div class="notice-content">{{ rollingText }}</div>
            </div>
        </div>

        <!-- 基础统计 -->
        <el-row :gutter="20">
            <el-col :span="4">
                <el-statistic title="今日来访" :value="statistics.today_count" />
            </el-col>

            <el-col :span="4">
                <el-statistic title="待审核" :value="statistics.waiting" />
            </el-col>

            <el-col :span="4">
                <el-statistic title="已通过" :value="statistics.approved" />
            </el-col>

            <el-col :span="4">
                <el-statistic title="已到访" :value="statistics.entered" />
            </el-col>

            <el-col :span="4">
                <el-statistic title="已离开" :value="statistics.left" />
            </el-col>

            <el-col :span="4">
                <el-statistic title="访客总数" :value="statistics.total" />
            </el-col>
        </el-row>
        <br />

        <el-row :gutter="20">
            <el-col :span="6">
                <el-card shadow="hover">
                    <div>房屋总数</div>
                    <h2>{{ data.house_count }}</h2>
                </el-card>
            </el-col>

            <el-col :span="6">
                <el-card shadow="hover">
                    <div>业主总数</div>
                    <h2>{{ data.owner_count }}</h2>
                </el-card>
            </el-col>

            <el-col :span="6">
                <el-card shadow="hover">
                    <div>车位总数</div>
                    <h2>{{ data.parking_count }}</h2>
                </el-card>
            </el-col>

            <el-col :span="6">
                <el-card shadow="hover">
                    <div>报修总数</div>
                    <h2>{{ data.repair_count }}</h2>
                </el-card>
            </el-col>
        </el-row>

        <br />
        <el-row :gutter="20">
            <el-col :span="12">
                <el-card>
                    <!-- 房屋统计 -->
                    <HouseChart />
                </el-card>
            </el-col>
        </el-row>
        <br />

        <!-- 费用统计 -->
        <el-row :gutter="20">
            <el-col :span="8">
                <el-card shadow="hover">
                    <div>物业费总额</div>
                    <h2>¥ {{ data.fee_total }}</h2>
                </el-card>
            </el-col>

            <el-col :span="8">
                <el-card shadow="hover">
                    <div>已缴费金额</div>
                    <h2 style="color: #67c23a">
                        {{ data.fee_paid }}
                    </h2>
                </el-card>
            </el-col>

            <el-col :span="8">
                <el-card shadow="hover">
                    <div>未缴费金额</div>
                    <h2 style="color: #f56c6c">
                        {{ data.fee_unpaid }}
                    </h2>
                </el-card>
            </el-col>
        </el-row>

        <br />
        <el-row :gutter="20">
            <el-col :span="12">
                <el-card>
                    <!-- 缴费统计 -->
                    <FeeChart />
                </el-card>
            </el-col>
        </el-row>

        <!-- 报修统计 -->
        <el-row :gutter="20">
            <el-col :span="8">
                <el-card shadow="hover">
                    <div>待派单报修</div>
                    <h2 style="color: #e6a23c">
                        {{ data.repair_pending }}
                    </h2>
                </el-card>
            </el-col>

            <el-col :span="8">
                <el-card shadow="hover">
                    <div>进行中报修</div>
                    <h2 style="color: #409eff">
                        {{ data.repair_processing }}
                    </h2>
                </el-card>
            </el-col>

            <el-col :span="8">
                <el-card shadow="hover">
                    <div>已完成报修</div>
                    <h2 style="color: #67c23a">
                        {{ data.repair_finished }}
                    </h2>
                </el-card>
            </el-col>
        </el-row>

        <br />
        <el-row :gutter="20">
            <el-col :span="12">
                <el-card>
                    <!-- 报修统计 -->
                    <RepairChart />
                </el-card>
            </el-col>
        </el-row>
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

.notice-marquee {
    display: flex;
    align-items: center;
    gap: 12px;
    height: 42px;
    margin-bottom: 18px;
    padding: 0 12px;
    border: 1px solid #e4e7ed;
    border-radius: 6px;
    background: #f5f7fa;
    overflow: hidden;
}

.notice-label {
    flex: 0 0 auto;
    color: #409eff;
    font-weight: 600;
}

.notice-track {
    flex: 1;
    overflow: hidden;
    white-space: nowrap;
}

.notice-content {
    display: inline-block;
    min-width: 100%;
    color: #606266;
    text-align: left;
    animation: notice-scroll 22s linear infinite;
}

@keyframes notice-scroll {
    0% {
        transform: translateX(100%);
    }

    100% {
        transform: translateX(-100%);
    }
}
</style>
