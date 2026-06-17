<!-- 文件说明：按登录角色展示管理员、财务、维修员、业主的业务工作台。 -->
<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, type Component } from 'vue'
import { useRouter } from 'vue-router'
import {
    Bell,
    ChatDotRound,
    CircleCheck,
    CreditCard,
    DataAnalysis,
    Document,
    House,
    Money,
    OfficeBuilding,
    Service,
    Tickets,
    Tools,
    User,
    Van,
    Wallet,
} from '@element-plus/icons-vue'
import { getDashboard } from '@/api/dashboard'
import FeeChart from '@/components/charts/FeeChart.vue'
import RepairChart from '@/components/charts/RepairChart.vue'
import HouseChart from '@/components/charts/HouseChart.vue'
import {
    AUTH_STATE_CHANGED_EVENT,
    getStoredRole,
    getStoredUsername,
} from '@/utils/authState'

type DashboardData = {
    house_count: number
    owner_count: number
    parking_count: number
    repair_count: number
    fee_total: number
    fee_paid: number
    fee_unpaid: number
    repair_pending: number
    repair_processing: number
    repair_finished: number
    paid_count: number
    unpaid_count: number
}

type MetricCard = {
    label: string
    value: string
    unit: string
    hint: string
    tone: string
    icon: Component
}

type AdminWorkOrderRow = [string, string, string, string, string, string, string, string]
type FinanceBillRow = [string, string, string, string, string, string, string]
type RepairOrderRow = [string, string, string, string, string, string, string]
type OwnerTaskRow = [string, string, string, string, string, string]
type SimplePairRow = [string, string]
type ActivityRow = [string, string, string]

const router = useRouter()
const username = ref(getStoredUsername() || '用户')
const role = ref(getStoredRole())

const data = ref<DashboardData>({
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

const isAdminRole = computed(() => adminRoles.includes(role.value))
const isFinanceRole = computed(() => financeRoles.includes(role.value))
const isRepairRole = computed(() => repairRoles.includes(role.value))
const isOwnerRole = computed(() => role.value === 'owner')

const numberOrFallback = (value: number, fallback: number) => {
    const numericValue = Number(value || 0)
    return numericValue > 0 ? numericValue : fallback
}

const formatNumber = (value: number) => Number(value || 0).toLocaleString('zh-CN')
const formatMoney = (value: number) => `¥ ${Number(value || 0).toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
})}`

const feeTotal = computed(() => numberOrFallback(data.value.fee_total, 326850))
const feePaid = computed(() => numberOrFallback(data.value.fee_paid, 283950))
const feeUnpaid = computed(() => numberOrFallback(data.value.fee_unpaid, 42900))
const feeRate = computed(() => {
    return feeTotal.value ? `${((feePaid.value / feeTotal.value) * 100).toFixed(1)}%` : '0.0%'
})

const adminMetrics = computed<MetricCard[]>(() => [
    {
        label: '待处理工单',
        value: formatNumber(numberOrFallback(data.value.repair_pending, 32)),
        unit: '件',
        hint: '较昨日 +6 件',
        tone: 'teal',
        icon: Document,
    },
    {
        label: '本月缴费率',
        value: feeRate.value,
        unit: '',
        hint: '较上月 +6.3%',
        tone: 'amber',
        icon: DataAnalysis,
    },
    {
        label: '今日访客',
        value: '128',
        unit: '人',
        hint: '较昨日 +18 人',
        tone: 'blue',
        icon: User,
    },
    {
        label: '投诉待回访',
        value: '7',
        unit: '件',
        hint: '较昨日 +2 件',
        tone: 'red',
        icon: ChatDotRound,
    },
])

const financeMetrics = computed<MetricCard[]>(() => [
    {
        label: '本月应收',
        value: formatMoney(feeTotal.value),
        unit: '',
        hint: '较上月 +8.6%',
        tone: 'teal',
        icon: Money,
    },
    {
        label: '本月实收',
        value: formatMoney(feePaid.value),
        unit: '',
        hint: '较上月 +12.3%',
        tone: 'blue',
        icon: Wallet,
    },
    {
        label: '缴费率',
        value: feeRate.value,
        unit: '',
        hint: '较上月 +6.4%',
        tone: 'amber',
        icon: DataAnalysis,
    },
    {
        label: '欠费户数',
        value: formatNumber(numberOrFallback(data.value.unpaid_count, 173)),
        unit: '户',
        hint: '较上月 -12 户',
        tone: 'red',
        icon: User,
    },
])

const repairMetrics = computed<MetricCard[]>(() => [
    {
        label: '待接单',
        value: formatNumber(numberOrFallback(data.value.repair_pending, 18)),
        unit: '单',
        hint: '较昨日 +5',
        tone: 'teal',
        icon: Tickets,
    },
    {
        label: '维修中',
        value: formatNumber(numberOrFallback(data.value.repair_processing, 12)),
        unit: '单',
        hint: '较昨日 -2',
        tone: 'blue',
        icon: Tools,
    },
    {
        label: '今日完成',
        value: '15',
        unit: '单',
        hint: '较昨日 +6',
        tone: 'green',
        icon: CircleCheck,
    },
    {
        label: '超时工单',
        value: '3',
        unit: '单',
        hint: '较昨日 +1',
        tone: 'orange',
        icon: Bell,
    },
])

const ownerCards = [
    {
        label: '待缴费用',
        value: '¥ 1,288.00',
        desc: '共 3 笔待缴',
        action: '立即缴费',
        path: '/fee/list',
        tone: 'amber',
        icon: Wallet,
    },
    {
        label: '维修进度',
        value: '2',
        desc: '个进行中，1 个待评价',
        action: '查看详情',
        path: '/repair/list',
        tone: 'blue',
        icon: Tools,
    },
    {
        label: '我的车位',
        value: 'B2-045',
        desc: '地下二层 | 月租',
        action: '查看详情',
        path: '/parking/list',
        tone: 'green',
        icon: Van,
    },
    {
        label: '未读通知',
        value: '4',
        desc: '条系统通知',
        action: '查看全部',
        path: '/message/center',
        tone: 'red',
        icon: Bell,
    },
]

const adminActions = [
    { label: '新增工单', path: '/repair/create', icon: Tools, tone: 'teal' },
    { label: '访客登记', path: '/visitor/create', icon: User, tone: 'blue' },
    { label: '发布公告', path: '/notice/create', icon: Bell, tone: 'amber' },
    { label: '录入缴费', path: '/fee/list', icon: Money, tone: 'green' },
]

const adminWorkOrders: AdminWorkOrderRow[] = [
    ['WD20250519001', '李女士', '3栋-2单元-0602', '水管漏水', '待派单', '紧急', '-', '05-19 09:28'],
    ['WD20250519002', '张先生', '1栋-1单元-1203', '电路故障', '待处理', '高', '王师傅', '05-19 09:15'],
    ['WD20250519003', '刘女士', '5栋-1单元-1101', '门锁损坏', '处理中', '中', '陈师傅', '05-19 08:54'],
    ['WD20250519004', '王先生', '2栋-2单元-0801', '空调不制冷', '待验收', '中', '孙师傅', '05-19 08:33'],
    ['WD20250518021', '陈女士', '6栋-2单元-1002', '下水道堵塞', '待处理', '高', '-', '05-18 17:25'],
]

const financeBills: FinanceBillRow[] = [
    ['BILL20250519001', '张先生', '1栋-1单元-1201', '物业费', '¥ 1,280.00', '未缴费', '2025-05-31'],
    ['BILL20250519002', '李女士', '2栋-2单元-0803', '水费', '¥ 68.00', '未缴费', '2025-05-31'],
    ['BILL20250519003', '王先生', '1栋-1单元-1502', '电费', '¥ 124.50', '未缴费', '2025-05-31'],
    ['BILL20250519004', '赵女士', '3栋-1单元-0601', '物业费', '¥ 1,280.00', '部分缴费', '2025-05-31'],
    ['BILL20250519005', '刘先生', '2栋-1单元-1103', '停车费', '¥ 180.00', '部分缴费', '2025-05-31'],
    ['BILL20250519006', '陈女士', '5栋-2单元-1002', '水费', '¥ 68.00', '已逾期', '2025-05-20'],
]

const repairOrders: RepairOrderRow[] = [
    ['WD20250519001', '李女士', '3栋-2单元-0602', '水管漏水', '紧急', '待接单', '今天 10:30'],
    ['WD20250519002', '张先生', '1栋-1单元-1203', '电路故障', '高', '待接单', '今天 11:00'],
    ['WD20250519003', '王女士', '2栋-1单元-0801', '灯具损坏', '中', '待接单', '今天 14:00'],
    ['WD20250519004', '陈先生', '5栋-3单元-1103', '门禁故障', '中', '待接单', '今天 15:30'],
    ['WD20250519005', '刘女士', '6栋-2单元-0702', '水龙头漏水', '低', '待接单', '明天 09:00'],
    ['WD20250519006', '赵先生', '4栋-1单元-0901', '插座故障', '低', '待接单', '明天 10:30'],
]

const ownerTasks: OwnerTaskRow[] = [
    ['¥', '有 3 笔费用待缴纳', '物业费、水费、电费等', '¥ 1,288.00', '去支付', '/fee/list'],
    ['修', '2 个报修工单进行中', '水管漏水、门锁故障', '', '查看进度', '/repair/list'],
    ['诉', '1 条投诉待反馈', '电梯运行噪音问题', '', '查看详情', '/complaint/list'],
    ['证', '房产认证未完善', '完成房产认证，享受更多服务', '', '去认证', '/house/list'],
]

const notices: SimplePairRow[] = [
    ['关于小区电梯维护保养的通知', '05-18'],
    ['关于2025年端午节放假安排的通知', '05-16'],
    ['小区公共区域清洁消毒通知', '05-15'],
    ['夏季用电安全温馨提示', '05-13'],
    ['关于地下车库临时管制的通知', '05-12'],
]

const activities: ActivityRow[] = [
    ['工单', 'WD20250519001 已创建，待派单', '09:28'],
    ['访客', '李女士 来访登记成功', '09:15'],
    ['缴费', '3栋-2单元-0602 已完成物业费缴纳', '09:02'],
    ['公告', '发布了新公告《关于小区电梯维护保养的通知》', '08:50'],
    ['投诉', '投诉编号 TS20250518007 已回访', '08:35'],
]

const ownerRepairs: ActivityRow[] = [
    ['卫生间水管漏水', '维修中', '05-19 09:28'],
    ['门锁故障维修', '已完成', '05-16 14:52'],
    ['客厅灯不亮', '已评价', '05-08 16:18'],
]

const statusClass = (status: string) => {
    if (status.includes('紧急') || status.includes('未缴') || status.includes('逾期')) {
        return 'danger'
    }

    if (status.includes('高') || status.includes('待处理') || status.includes('待验收') || status.includes('部分')) {
        return 'warning'
    }

    if (status.includes('完成') || status.includes('已缴') || status.includes('已评价')) {
        return 'success'
    }

    return 'info'
}

const goTo = (path: string) => {
    router.push(path)
}

const loadData = async () => {
    try {
        const res = await getDashboard()

        data.value = {
            ...data.value,
            ...res.data.data,
        }
    } catch {
        // 工作台有兜底展示数据，统计接口异常时不影响页面可用性。
    }
}

const refreshDashboardAuthState = () => {
    username.value = getStoredUsername() || '用户'
    role.value = getStoredRole()
    loadData()
}

onMounted(() => {
    window.addEventListener(AUTH_STATE_CHANGED_EVENT, refreshDashboardAuthState)
    loadData()
})

onBeforeUnmount(() => {
    window.removeEventListener(AUTH_STATE_CHANGED_EVENT, refreshDashboardAuthState)
})
</script>

<template>
    <div class="dashboard-page">
        <section v-if="isAdminRole" class="workbench">
            <div class="workbench-heading">
                <div>
                    <h1>运营工作台</h1>
                    <p>欢迎回来，{{ username }}！集中处理工单、访客、缴费和公告。</p>
                </div>

                <div class="heading-meta">
                    <span>2025年05月19日</span>
                    <span>星期一</span>
                    <span>20°C 多云</span>
                    <span>幸福里小区</span>
                </div>
            </div>

            <div class="quick-action-row">
                <button
                    v-for="item in adminActions"
                    :key="item.label"
                    type="button"
                    class="quick-action"
                    :class="`tone-${item.tone}`"
                    @click="goTo(item.path)"
                >
                    <el-icon><component :is="item.icon" /></el-icon>
                    <span>{{ item.label }}</span>
                </button>
            </div>

            <div class="metric-grid">
                <article
                    v-for="item in adminMetrics"
                    :key="item.label"
                    class="metric-card"
                    :class="`tone-${item.tone}`"
                >
                    <div class="metric-icon">
                        <el-icon><component :is="item.icon" /></el-icon>
                    </div>
                    <div>
                        <p>{{ item.label }}</p>
                        <strong>{{ item.value }} <small>{{ item.unit }}</small></strong>
                        <span>{{ item.hint }}</span>
                    </div>
                </article>
            </div>

            <div class="workbench-grid admin-grid">
                <section class="panel main-panel">
                    <div class="panel-header">
                        <h2>待办工单</h2>
                        <div class="filter-line">
                            <span>全部状态</span>
                            <span>全部类型</span>
                            <span>全部优先级</span>
                            <button type="button">查询</button>
                        </div>
                    </div>

                    <div class="tab-row">
                        <span class="active">全部 32</span>
                        <span>待派单 8</span>
                        <span>待处理 16</span>
                        <span>处理中 5</span>
                        <span>待验收 2</span>
                    </div>

                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>工单号</th>
                                <th>业主</th>
                                <th>房号</th>
                                <th>类型</th>
                                <th>状态</th>
                                <th>优先级</th>
                                <th>处理人</th>
                                <th>创建时间</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="row in adminWorkOrders" :key="row[0]">
                                <td>{{ row[0] }}</td>
                                <td>{{ row[1] }}</td>
                                <td>{{ row[2] }}</td>
                                <td>{{ row[3] }}</td>
                                <td><span class="status-pill" :class="statusClass(row[4])">{{ row[4] }}</span></td>
                                <td><span class="status-pill" :class="statusClass(row[5])">{{ row[5] }}</span></td>
                                <td>{{ row[6] }}</td>
                                <td>{{ row[7] }}</td>
                                <td><button type="button" class="text-button" @click="goTo('/repair/list')">查看</button></td>
                            </tr>
                        </tbody>
                    </table>
                </section>

                <aside class="side-stack">
                    <section class="panel">
                        <div class="panel-header">
                            <h2>紧急提醒</h2>
                            <button type="button" class="text-button">更多</button>
                        </div>
                        <ul class="compact-list">
                            <li v-for="row in adminWorkOrders.slice(0, 5)" :key="`urgent-${row[0]}`">
                                <span class="dot danger" />
                                <strong>{{ row[2] }}</strong>
                                <span>{{ row[3] }}</span>
                                <em>{{ row[7].slice(-5) }}</em>
                            </li>
                        </ul>
                    </section>

                    <section class="panel">
                        <div class="panel-header">
                            <h2>公告通知</h2>
                            <button type="button" class="text-button" @click="goTo('/notice/list')">更多</button>
                        </div>
                        <ul class="notice-list">
                            <li v-for="item in notices" :key="item[0]">
                                <span>{{ item[0] }}</span>
                                <em>{{ item[1] }}</em>
                            </li>
                        </ul>
                    </section>

                    <section class="panel">
                        <div class="panel-header">
                            <h2>近期动态</h2>
                            <button type="button" class="text-button">更多</button>
                        </div>
                        <ul class="activity-list">
                            <li v-for="item in activities" :key="`${item[0]}-${item[2]}`">
                                <span>{{ item[0] }}</span>
                                <p>{{ item[1] }}</p>
                                <em>{{ item[2] }}</em>
                            </li>
                        </ul>
                    </section>
                </aside>
            </div>

            <div class="bottom-grid three">
                <section class="panel">
                    <div class="panel-header">
                        <h2>费用概览</h2>
                        <span class="muted">本月</span>
                    </div>
                    <FeeChart :dashboard-data="data" />
                </section>

                <section class="panel resource-panel">
                    <div class="panel-header">
                        <h2>小区资源</h2>
                    </div>
                    <div class="resource-grid">
                        <div>
                            <el-icon><OfficeBuilding /></el-icon>
                            <strong>{{ formatNumber(numberOrFallback(data.house_count, 896)) }}</strong>
                            <span>房屋总数</span>
                        </div>
                        <div>
                            <el-icon><User /></el-icon>
                            <strong>{{ formatNumber(numberOrFallback(data.owner_count, 852)) }}</strong>
                            <span>业主总数</span>
                        </div>
                        <div>
                            <el-icon><Van /></el-icon>
                            <strong>{{ formatNumber(numberOrFallback(data.parking_count, 632)) }}</strong>
                            <span>总车位</span>
                        </div>
                    </div>
                </section>

                <section class="panel">
                    <div class="panel-header">
                        <h2>报修统计</h2>
                    </div>
                    <RepairChart :dashboard-data="data" />
                </section>
            </div>
        </section>

        <section v-else-if="isFinanceRole" class="workbench">
            <div class="workbench-heading">
                <div>
                    <h1>财务工作台</h1>
                    <p>聚焦账单、收费、欠费提醒和收入趋势。</p>
                </div>
            </div>

            <div class="metric-grid">
                <article
                    v-for="item in financeMetrics"
                    :key="item.label"
                    class="metric-card"
                    :class="`tone-${item.tone}`"
                >
                    <div class="metric-icon">
                        <el-icon><component :is="item.icon" /></el-icon>
                    </div>
                    <div>
                        <p>{{ item.label }}</p>
                        <strong>{{ item.value }} <small>{{ item.unit }}</small></strong>
                        <span>{{ item.hint }}</span>
                    </div>
                </article>
            </div>

            <div class="workbench-grid finance-grid">
                <section class="panel main-panel">
                    <div class="panel-header">
                        <h2>待处理账单</h2>
                        <div class="filter-line">
                            <span>小区</span>
                            <span>楼栋</span>
                            <span>费用类型</span>
                            <span>缴费状态</span>
                            <button type="button">查询</button>
                        </div>
                    </div>

                    <div class="tab-row">
                        <span class="active">全部 128</span>
                        <span>物业费 86</span>
                        <span>水费 18</span>
                        <span>电费 15</span>
                        <span>停车费 9</span>
                    </div>

                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>账单号</th>
                                <th>业主</th>
                                <th>房号</th>
                                <th>费用类型</th>
                                <th>应收金额</th>
                                <th>缴费状态</th>
                                <th>到期时间</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="row in financeBills" :key="row[0]">
                                <td>{{ row[0] }}</td>
                                <td>{{ row[1] }}</td>
                                <td>{{ row[2] }}</td>
                                <td>{{ row[3] }}</td>
                                <td>{{ row[4] }}</td>
                                <td><span class="status-pill" :class="statusClass(row[5])">{{ row[5] }}</span></td>
                                <td>{{ row[6] }}</td>
                                <td>
                                    <button type="button" class="text-button" @click="goTo('/fee/list')">提醒</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </section>

                <aside class="side-stack">
                    <section class="panel">
                        <div class="panel-header">
                            <h2>欠费提醒</h2>
                            <button type="button" class="text-button">更多</button>
                        </div>
                        <ul class="amount-list">
                            <li><span class="dot danger" />逾期 30 天以上 <strong>56 户</strong></li>
                            <li><span class="dot warning" />逾期 15-30 天 <strong>38 户</strong></li>
                            <li><span class="dot amber" />逾期 7-15 天 <strong>41 户</strong></li>
                            <li><span class="dot info" />即将到期 <strong>72 户</strong></li>
                        </ul>
                    </section>

                    <section class="panel">
                        <div class="panel-header">
                            <h2>今日收款</h2>
                            <button type="button" class="text-button">更多</button>
                        </div>
                        <strong class="money-total">¥ 12,580.00</strong>
                        <ul class="amount-list">
                            <li>微信支付 <strong>¥ 5,230.00</strong></li>
                            <li>支付宝 <strong>¥ 4,450.00</strong></li>
                            <li>银行转账 <strong>¥ 2,900.00</strong></li>
                            <li>现金 <strong>¥ 0.00</strong></li>
                        </ul>
                    </section>
                </aside>
            </div>

            <div class="bottom-grid three">
                <section class="panel">
                    <div class="panel-header">
                        <h2>收入趋势</h2>
                        <span class="muted">本月</span>
                    </div>
                    <FeeChart :dashboard-data="data" />
                </section>
                <section class="panel">
                    <div class="panel-header">
                        <h2>费用分类</h2>
                    </div>
                    <FeeChart :dashboard-data="data" />
                </section>
                <section class="panel">
                    <div class="panel-header">
                        <h2>近期缴费记录</h2>
                    </div>
                    <ul class="activity-list">
                        <li v-for="row in financeBills.slice(0, 5)" :key="`paid-${row[0]}`">
                            <span>收</span>
                            <p>{{ row[1] }} {{ row[2] }} {{ row[3] }}</p>
                            <em>{{ row[4] }}</em>
                        </li>
                    </ul>
                </section>
            </div>
        </section>

        <section v-else-if="isRepairRole" class="workbench">
            <div class="workbench-heading">
                <div>
                    <h1>维修工作台</h1>
                    <p>欢迎回来，{{ username }}！高效处理工单，及时响应业主需求。</p>
                </div>
            </div>

            <div class="metric-grid">
                <article
                    v-for="item in repairMetrics"
                    :key="item.label"
                    class="metric-card"
                    :class="`tone-${item.tone}`"
                >
                    <div class="metric-icon">
                        <el-icon><component :is="item.icon" /></el-icon>
                    </div>
                    <div>
                        <p>{{ item.label }}</p>
                        <strong>{{ item.value }} <small>{{ item.unit }}</small></strong>
                        <span>{{ item.hint }}</span>
                    </div>
                </article>
            </div>

            <div class="workbench-grid repair-grid">
                <section class="panel main-panel">
                    <div class="panel-header">
                        <h2>待处理工单</h2>
                        <div class="filter-line">
                            <span>工单号 / 业主 / 房号</span>
                            <button type="button">刷新</button>
                        </div>
                    </div>

                    <div class="tab-row">
                        <span class="active">全部 18</span>
                        <span>水电 6</span>
                        <span>门禁 3</span>
                        <span>电梯 4</span>
                        <span>公共设施 5</span>
                    </div>

                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>工单号</th>
                                <th>业主</th>
                                <th>房号</th>
                                <th>报修类型</th>
                                <th>紧急程度</th>
                                <th>状态</th>
                                <th>预约时间</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="row in repairOrders" :key="row[0]">
                                <td>{{ row[0] }}</td>
                                <td>{{ row[1] }}</td>
                                <td>{{ row[2] }}</td>
                                <td>{{ row[3] }}</td>
                                <td><span class="status-pill" :class="statusClass(row[4])">{{ row[4] }}</span></td>
                                <td><span class="status-pill info">{{ row[5] }}</span></td>
                                <td>{{ row[6] }}</td>
                                <td>
                                    <button type="button" class="solid-mini" @click="goTo('/repair/list')">接单</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </section>

                <aside class="side-stack">
                    <section class="panel">
                        <div class="panel-header">
                            <h2>紧急工单</h2>
                            <button type="button" class="text-button">更多</button>
                        </div>
                        <ul class="compact-list">
                            <li v-for="row in repairOrders.slice(0, 3)" :key="`repair-urgent-${row[0]}`">
                                <span class="dot danger" />
                                <strong>{{ row[0] }}</strong>
                                <span>{{ row[3] }}</span>
                                <em>{{ row[4] }}</em>
                            </li>
                        </ul>
                    </section>

                    <section class="panel">
                        <div class="panel-header">
                            <h2>今日安排</h2>
                            <button type="button" class="text-button">更多</button>
                        </div>
                        <ul class="schedule-list">
                            <li v-for="row in repairOrders.slice(0, 5)" :key="`schedule-${row[0]}`">
                                <span>{{ row[6].replace('今天 ', '') }}</span>
                                <p>{{ row[2] }} {{ row[3] }}</p>
                                <em>{{ row[5] }}</em>
                            </li>
                        </ul>
                    </section>

                    <section class="panel">
                        <div class="panel-header">
                            <h2>消息通知</h2>
                            <button type="button" class="text-button">更多</button>
                        </div>
                        <ul class="notice-list">
                            <li><span>新工单：WD20250519001</span><em>09:15</em></li>
                            <li><span>工单完成：WD20250518015</span><em>08:45</em></li>
                            <li><span>业主评价：WD20250518013</span><em>08:30</em></li>
                            <li><span>系统公告：端午节放假通知</span><em>昨天</em></li>
                        </ul>
                    </section>
                </aside>
            </div>

            <div class="bottom-grid two">
                <section class="panel">
                    <div class="panel-header">
                        <h2>维修进度</h2>
                    </div>
                    <div class="progress-line">
                        <span>接单</span>
                        <span>出发</span>
                        <span class="active">维修中</span>
                        <span>待验收</span>
                        <span>已完成</span>
                    </div>
                    <p class="current-order">当前工单：<strong>WD20250518012</strong> 电路故障，预计完成时间：今天 12:00</p>
                </section>
                <section class="panel">
                    <div class="panel-header">
                        <h2>常用操作</h2>
                    </div>
                    <div class="operation-grid">
                        <button type="button" @click="goTo('/upload')"><el-icon><CreditCard /></el-icon>拍照上传</button>
                        <button type="button" @click="goTo('/profile')"><el-icon><Service /></el-icon>联系业主</button>
                        <button type="button" @click="goTo('/repair/list')"><el-icon><CircleCheck /></el-icon>提交结果</button>
                    </div>
                </section>
            </div>
        </section>

        <section v-else-if="isOwnerRole" class="workbench">
            <div class="workbench-heading">
                <div>
                    <h1>业主首页</h1>
                    <p>欢迎回家，{{ username }}！</p>
                </div>
            </div>

            <section class="owner-hero panel">
                <div class="owner-house-icon">
                    <el-icon><OfficeBuilding /></el-icon>
                </div>
                <div>
                    <span>欢迎回家，{{ username }}！</span>
                    <h2>幸福里小区 3栋-2单元-0602</h2>
                    <p>房屋面积：98.56㎡　房屋类型：住宅　入住时间：2021-06-12</p>
                </div>
                <div class="owner-hero-actions">
                    <button type="button" @click="goTo('/fee/list')"><el-icon><Money /></el-icon>立即缴费</button>
                    <button type="button" @click="goTo('/repair/create')"><el-icon><Tools /></el-icon>提交报修</button>
                    <button type="button" @click="goTo('/visitor/create')"><el-icon><User /></el-icon>访客登记</button>
                    <button type="button" @click="goTo('/notice/list')"><el-icon><Bell /></el-icon>查看公告</button>
                </div>
            </section>

            <div class="workbench-grid owner-grid">
                <main>
                    <div class="owner-card-grid">
                        <article
                            v-for="item in ownerCards"
                            :key="item.label"
                            class="owner-card"
                            :class="`tone-${item.tone}`"
                        >
                            <el-icon><component :is="item.icon" /></el-icon>
                            <div>
                                <p>{{ item.label }}</p>
                                <strong>{{ item.value }}</strong>
                                <span>{{ item.desc }}</span>
                            </div>
                            <button type="button" @click="goTo(item.path)">{{ item.action }}</button>
                        </article>
                    </div>

                    <section class="panel">
                        <div class="panel-header">
                            <h2>我的待办</h2>
                        </div>
                        <ul class="owner-task-list">
                            <li v-for="item in ownerTasks" :key="item[1]">
                                <b>{{ item[0] }}</b>
                                <div>
                                    <strong>{{ item[1] }}</strong>
                                    <span>{{ item[2] }}</span>
                                </div>
                                <em>{{ item[3] }}</em>
                                <button type="button" @click="goTo(item[5])">{{ item[4] }}</button>
                            </li>
                        </ul>
                    </section>

                    <div class="bottom-grid three owner-bottom">
                        <section class="panel">
                            <div class="panel-header">
                                <h2>我的房产</h2>
                            </div>
                            <div class="owner-property">
                                <div class="building-thumb"><el-icon><House /></el-icon></div>
                                <div>
                                    <strong>3栋-2单元-0602</strong>
                                    <span>房屋面积 98.56㎡</span>
                                    <span>房屋类型 住宅</span>
                                    <span>房屋状态 已入住</span>
                                </div>
                            </div>
                            <button type="button" class="ghost-button" @click="goTo('/house/list')">查看详情</button>
                        </section>

                        <section class="panel">
                            <div class="panel-header">
                                <h2>缴费记录</h2>
                                <button type="button" class="text-button" @click="goTo('/fee/list')">更多</button>
                            </div>
                            <ul class="notice-list">
                                <li><span>物业费 ¥ 888.00</span><em>待缴费</em></li>
                                <li><span>水费 ¥ 150.00</span><em>待缴费</em></li>
                                <li><span>电费 ¥ 250.00</span><em>待缴费</em></li>
                                <li><span>停车费 ¥ 300.00</span><em>已缴费</em></li>
                            </ul>
                        </section>

                        <section class="panel">
                            <div class="panel-header">
                                <h2>最近报修</h2>
                                <button type="button" class="text-button" @click="goTo('/repair/list')">更多</button>
                            </div>
                            <ul class="notice-list">
                                <li v-for="item in ownerRepairs" :key="item[0]">
                                    <span>{{ item[0] }}</span>
                                    <em>{{ item[1] }}</em>
                                </li>
                            </ul>
                        </section>
                    </div>
                </main>

                <aside class="side-stack">
                    <section class="panel">
                        <div class="panel-header">
                            <h2>缴费提醒</h2>
                            <button type="button" class="text-button" @click="goTo('/fee/list')">更多</button>
                        </div>
                        <p class="fee-remind">您有 3 笔费用待缴纳，合计 <strong>¥ 1,288.00</strong></p>
                        <ul class="notice-list">
                            <li><span>2025年5月 物业费 ¥ 888.00</span><em>待缴费</em></li>
                            <li><span>2025年5月 水费 ¥ 150.00</span><em>待缴费</em></li>
                            <li><span>2025年5月 电费 ¥ 250.00</span><em>待缴费</em></li>
                        </ul>
                        <button type="button" class="primary-wide" @click="goTo('/fee/list')">立即缴费</button>
                    </section>

                    <section class="panel">
                        <div class="panel-header">
                            <h2>公告活动</h2>
                            <button type="button" class="text-button" @click="goTo('/notice/list')">更多</button>
                        </div>
                        <ul class="notice-list">
                            <li v-for="item in notices" :key="`owner-${item[0]}`">
                                <span>{{ item[0] }}</span>
                                <em>{{ item[1] }}</em>
                            </li>
                        </ul>
                    </section>

                    <section class="panel">
                        <div class="panel-header">
                            <h2>服务进度</h2>
                            <button type="button" class="text-button">更多</button>
                        </div>
                        <ul class="timeline-list">
                            <li><span class="dot info" />报修工单 #BX20250519001 <em>维修中</em></li>
                            <li><span class="dot success" />报修工单 #BX20250516002 <em>已完成</em></li>
                            <li><span class="dot warning" />投诉单 #TS20250515001 <em>处理中</em></li>
                        </ul>
                    </section>
                </aside>
            </div>
        </section>

        <section v-else class="workbench">
            <div class="empty-workbench panel">
                <h1>后台首页</h1>
                <p>欢迎您，{{ username }}。请选择左侧菜单开始办理业务。</p>
            </div>
        </section>
    </div>
</template>

<style scoped>
.dashboard-page {
    min-height: 100%;
    color: #172033;
}

.workbench {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.workbench-heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
}

.workbench-heading h1 {
    margin: 0;
    font-size: 28px;
    line-height: 1.25;
    font-weight: 700;
}

.workbench-heading p {
    margin: 8px 0 0;
    color: #667085;
    font-size: 14px;
}

.heading-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
    color: #475467;
    font-size: 14px;
}

.quick-action-row {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    margin-top: -4px;
}

.quick-action,
.solid-mini,
.primary-wide,
.ghost-button,
.text-button,
.filter-line button,
.operation-grid button,
.owner-hero-actions button,
.owner-card button,
.owner-task-list button {
    border: 0;
    cursor: pointer;
    font-family: inherit;
}

.quick-action {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    min-height: 42px;
    padding: 0 22px;
    border-radius: 6px;
    color: #fff;
    font-size: 15px;
    font-weight: 600;
    box-shadow: 0 8px 16px rgba(15, 118, 110, 0.14);
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 14px;
}

.metric-card,
.panel,
.owner-card,
.owner-hero {
    border: 1px solid #e4e7ed;
    border-radius: 8px;
    background: #fff;
    box-shadow: 0 8px 20px rgba(16, 24, 40, 0.04);
}

.metric-card {
    display: flex;
    align-items: center;
    gap: 18px;
    min-height: 112px;
    padding: 20px;
}

.metric-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 62px;
    height: 62px;
    flex: 0 0 62px;
    border-radius: 50%;
    font-size: 30px;
}

.metric-card p,
.owner-card p {
    margin: 0;
    color: #344054;
    font-size: 15px;
}

.metric-card strong {
    display: block;
    margin-top: 6px;
    font-size: 28px;
    line-height: 1.1;
    font-weight: 700;
}

.metric-card small {
    font-size: 14px;
    font-weight: 500;
}

.metric-card span,
.owner-card span,
.muted {
    display: block;
    margin-top: 8px;
    color: #667085;
    font-size: 13px;
}

.tone-teal {
    --tone: #009688;
    --tone-soft: #d8f3ef;
}

.tone-blue {
    --tone: #1677ff;
    --tone-soft: #e8f1ff;
}

.tone-amber {
    --tone: #f59f00;
    --tone-soft: #fff2d9;
}

.tone-green {
    --tone: #16a34a;
    --tone-soft: #dcfce7;
}

.tone-red {
    --tone: #ef4444;
    --tone-soft: #fee2e2;
}

.tone-orange {
    --tone: #f97316;
    --tone-soft: #ffedd5;
}

.metric-card .metric-icon,
.owner-card > .el-icon {
    color: var(--tone);
    background: var(--tone-soft);
}

.quick-action.tone-teal,
.solid-mini,
.primary-wide,
.filter-line button {
    background: linear-gradient(135deg, #009688, #00796b);
}

.quick-action.tone-blue {
    background: linear-gradient(135deg, #1677ff, #1558d6);
}

.quick-action.tone-amber {
    background: linear-gradient(135deg, #f59f00, #f97316);
}

.quick-action.tone-green {
    background: linear-gradient(135deg, #16a34a, #0f8a3b);
}

.workbench-grid {
    display: grid;
    gap: 16px;
    align-items: start;
}

.admin-grid,
.finance-grid,
.repair-grid,
.owner-grid {
    grid-template-columns: minmax(0, 1fr) 330px;
}

.panel {
    min-width: 0;
    padding: 16px;
}

.main-panel {
    overflow-x: auto;
}

.panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 14px;
}

.panel-header h2 {
    margin: 0;
    font-size: 18px;
    font-weight: 700;
}

.filter-line {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #667085;
    font-size: 13px;
}

.filter-line span {
    min-width: 92px;
    padding: 8px 12px;
    border: 1px solid #e4e7ed;
    border-radius: 6px;
    background: #fff;
}

.filter-line button {
    min-width: 58px;
    height: 34px;
    border-radius: 6px;
    color: #fff;
}

.tab-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 12px;
}

.tab-row span {
    padding: 7px 16px;
    border: 1px solid #e4e7ed;
    border-radius: 6px;
    color: #475467;
    background: #f8fafc;
    font-size: 13px;
}

.tab-row .active {
    color: #fff;
    border-color: #009688;
    background: #009688;
}

.data-table {
    width: 100%;
    min-width: 760px;
    border-collapse: collapse;
    font-size: 13px;
}

.data-table th,
.data-table td {
    padding: 12px 10px;
    border-bottom: 1px solid #eef1f5;
    text-align: left;
    white-space: nowrap;
}

.data-table th {
    color: #475467;
    background: #f8fafc;
    font-weight: 600;
}

.status-pill {
    display: inline-flex;
    min-width: 52px;
    justify-content: center;
    padding: 3px 8px;
    border-radius: 5px;
    font-size: 12px;
    font-style: normal;
}

.status-pill.danger {
    color: #ef4444;
    background: #fee2e2;
}

.status-pill.warning {
    color: #d97706;
    background: #fff2d9;
}

.status-pill.success {
    color: #16a34a;
    background: #dcfce7;
}

.status-pill.info {
    color: #1677ff;
    background: #e8f1ff;
}

.text-button {
    color: #00897b;
    background: transparent;
    font-weight: 600;
}

.solid-mini {
    min-width: 54px;
    height: 28px;
    border-radius: 5px;
    color: #fff;
    font-size: 13px;
}

.side-stack {
    display: flex;
    flex-direction: column;
    gap: 14px;
}

.compact-list,
.notice-list,
.activity-list,
.amount-list,
.schedule-list,
.timeline-list,
.owner-task-list {
    margin: 0;
    padding: 0;
    list-style: none;
}

.compact-list li,
.notice-list li,
.amount-list li,
.schedule-list li,
.timeline-list li {
    display: flex;
    align-items: center;
    gap: 8px;
    min-height: 34px;
    border-bottom: 1px solid #eef1f5;
    color: #475467;
    font-size: 13px;
}

.compact-list li:last-child,
.notice-list li:last-child,
.amount-list li:last-child,
.schedule-list li:last-child,
.timeline-list li:last-child {
    border-bottom: 0;
}

.compact-list strong,
.notice-list span,
.schedule-list p,
.activity-list p,
.amount-list span {
    flex: 1;
    min-width: 0;
}

.compact-list em,
.notice-list em,
.schedule-list em,
.activity-list em,
.timeline-list em {
    margin-left: auto;
    color: #98a2b3;
    font-style: normal;
    white-space: nowrap;
}

.dot {
    width: 7px;
    height: 7px;
    flex: 0 0 7px;
    border-radius: 50%;
    background: #1677ff;
}

.dot.danger {
    background: #ef4444;
}

.dot.warning,
.dot.amber {
    background: #f59f00;
}

.dot.success {
    background: #16a34a;
}

.dot.info {
    background: #1677ff;
}

.notice-list li {
    justify-content: space-between;
}

.notice-list span {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.activity-list li {
    display: grid;
    grid-template-columns: 42px minmax(0, 1fr) 48px;
    align-items: center;
    gap: 8px;
    min-height: 36px;
    border-bottom: 1px solid #eef1f5;
    font-size: 13px;
}

.activity-list span {
    color: #00897b;
    font-weight: 700;
}

.activity-list p {
    margin: 0;
    overflow: hidden;
    color: #475467;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.bottom-grid {
    display: grid;
    gap: 16px;
}

.bottom-grid.three {
    grid-template-columns: repeat(3, minmax(0, 1fr));
}

.bottom-grid.two {
    grid-template-columns: repeat(2, minmax(0, 1fr));
}

.resource-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 14px;
    height: 400px;
    align-items: center;
}

.resource-grid div {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    color: #667085;
}

.resource-grid .el-icon {
    color: #00897b;
    font-size: 28px;
}

.resource-grid strong {
    color: #00897b;
    font-size: 32px;
}

.money-total {
    display: block;
    margin: 2px 0 10px;
    font-size: 24px;
}

.progress-line {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 8px;
    margin: 28px 0;
    text-align: center;
}

.progress-line span {
    position: relative;
    color: #667085;
    font-size: 14px;
}

.progress-line span::before {
    content: '';
    display: block;
    width: 36px;
    height: 36px;
    margin: 0 auto 8px;
    border: 2px solid #d0d5dd;
    border-radius: 50%;
    background: #fff;
}

.progress-line .active {
    color: #00897b;
    font-weight: 700;
}

.progress-line .active::before {
    border-color: #00897b;
    background: #d8f3ef;
}

.current-order {
    margin: 0;
    color: #475467;
    font-size: 14px;
}

.current-order strong {
    color: #00897b;
}

.operation-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 14px;
}

.operation-grid button {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 8px;
    min-height: 116px;
    border: 1px solid #e4e7ed;
    border-radius: 8px;
    color: #172033;
    background: #fff;
    font-size: 16px;
}

.operation-grid .el-icon {
    color: #00897b;
    font-size: 30px;
}

.owner-hero {
    display: grid;
    grid-template-columns: 78px minmax(0, 1fr) auto;
    align-items: center;
    gap: 18px;
}

.owner-house-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 64px;
    height: 64px;
    border-radius: 50%;
    color: #00897b;
    background: #d8f3ef;
    font-size: 34px;
}

.owner-hero h2 {
    margin: 5px 0 8px;
    font-size: 24px;
}

.owner-hero span,
.owner-hero p {
    margin: 0;
    color: #667085;
}

.owner-hero-actions {
    display: grid;
    grid-template-columns: repeat(4, 92px);
    gap: 8px;
}

.owner-hero-actions button {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 6px;
    min-height: 68px;
    border: 1px solid #e4e7ed;
    border-radius: 6px;
    color: #00897b;
    background: #fff;
    font-size: 13px;
    font-weight: 600;
}

.owner-card-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 14px;
    margin-bottom: 16px;
}

.owner-card {
    display: grid;
    grid-template-columns: 54px minmax(0, 1fr);
    gap: 12px;
    align-items: center;
    min-height: 128px;
    padding: 16px;
}

.owner-card > .el-icon {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    font-size: 26px;
}

.owner-card strong {
    display: block;
    margin-top: 4px;
    font-size: 24px;
}

.owner-card button {
    grid-column: 1 / -1;
    height: 32px;
    border-top: 1px solid #eef1f5;
    color: #00897b;
    background: transparent;
    font-weight: 600;
}

.owner-task-list li {
    display: grid;
    grid-template-columns: 42px minmax(0, 1fr) 150px 92px;
    align-items: center;
    gap: 12px;
    min-height: 58px;
    border-bottom: 1px solid #eef1f5;
}

.owner-task-list b {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    color: #fff;
    background: #f59f00;
    font-size: 14px;
}

.owner-task-list strong,
.owner-task-list span {
    display: block;
}

.owner-task-list span {
    margin-top: 4px;
    color: #667085;
    font-size: 13px;
}

.owner-task-list em {
    color: #ef4444;
    font-size: 20px;
    font-style: normal;
}

.owner-task-list button,
.ghost-button,
.primary-wide {
    height: 32px;
    border-radius: 6px;
    font-weight: 600;
}

.owner-task-list button,
.ghost-button {
    border: 1px solid #d0ebe8;
    color: #00897b;
    background: #fff;
}

.owner-property {
    display: flex;
    gap: 14px;
    margin-bottom: 14px;
}

.building-thumb {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 92px;
    min-height: 112px;
    border-radius: 8px;
    color: #00897b;
    background: #e7f7f5;
    font-size: 48px;
}

.owner-property strong,
.owner-property span {
    display: block;
}

.owner-property strong {
    margin-bottom: 10px;
}

.owner-property span {
    margin-top: 8px;
    color: #475467;
    font-size: 13px;
}

.fee-remind {
    margin: 0 0 12px;
    color: #667085;
}

.fee-remind strong {
    color: #ef4444;
}

.primary-wide {
    width: 100%;
    margin-top: 12px;
    color: #fff;
}

.timeline-list li {
    justify-content: flex-start;
}

.timeline-list em {
    color: #1677ff;
}

.empty-workbench {
    min-height: 260px;
}

@media (max-width: 1400px) {
    .metric-grid,
    .owner-card-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .admin-grid,
    .finance-grid,
    .repair-grid,
    .owner-grid,
    .bottom-grid.three,
    .bottom-grid.two {
        grid-template-columns: 1fr;
    }

    .owner-hero {
        grid-template-columns: 72px minmax(0, 1fr);
    }

    .owner-hero-actions {
        grid-column: 1 / -1;
        grid-template-columns: repeat(4, minmax(0, 1fr));
    }
}
</style>
