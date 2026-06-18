<!-- 文件说明：按登录角色展示管理员、财务、维修员、业主的业务工作台。 -->
<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, type Component } from 'vue'
import { useRouter } from 'vue-router'
import {
    Bell,
    Calendar,
    ChatDotRound,
    Check,
    CircleCheck,
    DataAnalysis,
    Document,
    Money,
    OfficeBuilding,
    Phone,
    Tickets,
    Tools,
    User,
    UserFilled,
    Van,
    Wallet,
} from '@element-plus/icons-vue'
import { getComplaintList } from '@/api/complaint'
import { getDashboard } from '@/api/dashboard'
import { getFeeList } from '@/api/fee'
import { getHouseList } from '@/api/house'
import { getNoticeList } from '@/api/notice'
import { getOwnerList } from '@/api/owner'
import { getRepairList } from '@/api/repair'
import FeeChart from '@/components/charts/FeeChart.vue'
import RepairChart from '@/components/charts/RepairChart.vue'
import RepairResultDrawer from '@/components/repair/RepairResultDrawer.vue'
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
type SimplePairRow = [string, string]
type ActivityRow = [string, string, string]
type RepairPriorityKey = 'all' | 'urgent' | 'high' | 'normal' | 'low'

type RepairWorkbenchOrder = {
    id?: number
    code: string
    owner: string
    room: string
    title: string
    priority: string
    status: string
    statusRaw: string
    time: string
    priorityKey: RepairPriorityKey
    raw: any
}

type OwnerTaskItem = {
    id: string
    title: string
    desc: string
    amount?: string
    progress?: number
    status: string
    statusClass: string
    action: string
    path: string
    tone: string
    icon: Component
}

type OwnerServiceItem = {
    id: string
    title: string
    meta: string
    status: string
    statusClass: string
    date: string
    path: string
}

type OwnerNoticeItem = {
    id: string
    title: string
    date: string
}

type OwnerCalendarEvent = {
    id: string
    dateKey: string
    title: string
    time: string
    path: string
}

type CalendarDay = {
    key: string
    day: number | null
    dateKey: string
    hasEvent: boolean
    isToday: boolean
}

type ConveniencePhone = {
    label: string
    phone: string
}

const router = useRouter()
const username = ref(getStoredUsername() || '用户')
const role = ref(getStoredRole())
const ownerHouses = ref<any[]>([])
const ownerProfiles = ref<any[]>([])
const ownerFees = ref<any[]>([])
const ownerRepairsData = ref<any[]>([])
const ownerComplaints = ref<any[]>([])
const ownerNotices = ref<any[]>([])
const ownerCalendarCursor = ref(new Date())
const repairerRepairs = ref<any[]>([])
const repairCalendarCursor = ref(new Date())
const selectedRepairPriority = ref<RepairPriorityKey>('all')
const repairResultDrawerVisible = ref(false)
const selectedRepairResult = ref<any | null>(null)

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
    ['BILL20250519005', '刘先生', '2栋-1单元-1103', '车位费', '¥ 180.00', '部分缴费', '2025-05-31'],
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

const repairPriorityOptions: Array<{ key: RepairPriorityKey; label: string }> = [
    { key: 'all', label: '全部' },
    { key: 'urgent', label: '紧急' },
    { key: 'high', label: '高' },
    { key: 'normal', label: '普通' },
    { key: 'low', label: '低' },
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

const ownerConveniencePhones: ConveniencePhone[] = [
    { label: '物业前台', phone: '0571-6386-9274' },
    { label: '门岗电话', phone: '0571-5824-1396' },
    { label: '客服热线', phone: '400-736-5281' },
    { label: '紧急值班', phone: '0571-8507-3164' },
]

const feeTypeLabels: Record<string, string> = {
    property: '物业费',
    water: '水费',
    electric: '电费',
    parking: '车位费',
    other: '其他费用',
}

const houseStatusLabels: Record<string, string> = {
    vacant: '空置',
    occupied: '已入住',
    renting: '出租',
    repairing: '装修中',
}

const repairStatusLabels: Record<string, string> = {
    pending: '待派单',
    assigned: '待接单',
    accepted: '已接单',
    processing: '进行中',
    finished: '已完成',
}

const repairProgressMap: Record<string, number> = {
    pending: 20,
    assigned: 35,
    accepted: 50,
    processing: 60,
    finished: 100,
}

const complaintStatusLabels: Record<string, string> = {
    pending: '待处理',
    processing: '处理中',
    done: '已完成',
    closed: '已关闭',
}

const extractList = (payload: any) => {
    if (Array.isArray(payload)) return payload
    if (Array.isArray(payload?.results)) return payload.results
    if (Array.isArray(payload?.data)) return payload.data
    if (Array.isArray(payload?.data?.results)) return payload.data.results

    return []
}

const parseDateFromValue = (value?: string | null) => {
    if (!value) return null

    const match = String(value).match(
        /^(\d{4})-(\d{2})-(\d{2})(?:[ T](\d{2}):(\d{2}))?/,
    )

    if (!match) return null

    const [, year, month, day, hour = '00', minute = '00'] = match

    return new Date(
        Number(year),
        Number(month) - 1,
        Number(day),
        Number(hour),
        Number(minute),
    )
}

const toDateKey = (date: Date) => {
    const year = date.getFullYear()
    const month = `${date.getMonth() + 1}`.padStart(2, '0')
    const day = `${date.getDate()}`.padStart(2, '0')

    return `${year}-${month}-${day}`
}

const dateKeyFromValue = (value?: string | null) => {
    const date = parseDateFromValue(value)

    return date ? toDateKey(date) : ''
}

const formatDateShort = (value?: string | null) => {
    const date = parseDateFromValue(value)

    if (!date) return ''

    return `${`${date.getMonth() + 1}`.padStart(2, '0')}-${`${date.getDate()}`.padStart(2, '0')}`
}

const formatDateTimeShort = (value?: string | null) => {
    const date = parseDateFromValue(value)

    if (!date) return ''

    const month = `${date.getMonth() + 1}`.padStart(2, '0')
    const day = `${date.getDate()}`.padStart(2, '0')
    const hour = `${date.getHours()}`.padStart(2, '0')
    const minute = `${date.getMinutes()}`.padStart(2, '0')

    return `${month}-${day} ${hour}:${minute}`
}

const formatCalendarEventTime = (value?: string | null) => {
    const date = parseDateFromValue(value)

    if (!date) return ''

    return `${`${date.getHours()}`.padStart(2, '0')}:${`${date.getMinutes()}`.padStart(2, '0')}`
}

const formatMonthLabel = (date: Date) => `${date.getFullYear()}年${date.getMonth() + 1}月`

const feeTypeText = (item: any) => item.fee_type_text || feeTypeLabels[item.fee_type] || '费用'
const repairStatusText = (item: any) => item.status_text || repairStatusLabels[item.status] || '待处理'
const complaintStatusText = (item: any) => item.status_text || complaintStatusLabels[item.status] || '待处理'

const getRepairCode = (item: any) => {
    if (item.order_no || item.code) {
        return item.order_no || item.code
    }

    return item.id ? `WD${String(item.id).padStart(12, '0')}` : '未生成'
}

const getRepairRoomText = (item: any) => {
    const parts = [item.building_name, item.unit_name, item.room_no].filter(Boolean)

    return parts.length ? parts.join('-') : item.room || '-'
}

const getRepairPriorityText = (item: any) => {
    const text = `${item.title || ''}${item.content || ''}${item.priority || ''}`

    if (/紧急|爆裂|停电|电梯|严重|漏水|urgent/.test(text)) return '紧急'
    if (/高|电路|门禁|堵塞|门锁|插座|high/.test(text)) return '高'
    if (/低|咨询|轻微|low/.test(text)) return '低'

    return '普通'
}

const getRepairPriorityKey = (priority: string): RepairPriorityKey => {
    if (priority.includes('紧急')) return 'urgent'
    if (priority.includes('高')) return 'high'
    if (priority.includes('低')) return 'low'

    return 'normal'
}

const getRepairTimeText = (item: any) => {
    return item.appointment_time || item.expected_time || formatDateTimeShort(item.created_at) || item.time || '-'
}

const getRepairEventDate = (item: any) => {
    return item.appointment_time || item.expected_time || item.finish_time || item.created_at || item.time
}

const fallbackRepairWorkbenchOrders = computed<RepairWorkbenchOrder[]>(() => {
    return repairOrders.map((row, index) => {
        const raw = {
            code: row[0],
            owner: row[1],
            room: row[2],
            title: row[3],
            status: index === 0 ? 'processing' : 'assigned',
            time: row[6],
        }
        const priority = row[4]

        return {
            code: row[0],
            owner: row[1],
            room: row[2],
            title: row[3],
            priority,
            status: row[5],
            statusRaw: raw.status,
            time: row[6],
            priorityKey: getRepairPriorityKey(priority),
            raw,
        }
    })
})

const repairWorkbenchOrders = computed<RepairWorkbenchOrder[]>(() => {
    const activeOrders = repairerRepairs.value.filter((item) => item.status !== 'finished')

    if (!activeOrders.length) {
        return fallbackRepairWorkbenchOrders.value
    }

    return activeOrders.map((item) => {
        const priority = getRepairPriorityText(item)

        return {
            id: item.id,
            code: getRepairCode(item),
            owner: item.owner_name || item.owner || '业主',
            room: getRepairRoomText(item),
            title: item.title || item.content || '报修工单',
            priority,
            status: repairStatusText(item),
            statusRaw: item.status || '',
            time: getRepairTimeText(item),
            priorityKey: getRepairPriorityKey(priority),
            raw: item,
        }
    })
})

const repairPriorityTabs = computed(() => {
    return repairPriorityOptions.map((item) => {
        const count = item.key === 'all'
            ? repairWorkbenchOrders.value.length
            : repairWorkbenchOrders.value.filter((row) => row.priorityKey === item.key).length

        return {
            ...item,
            count,
        }
    })
})

const filteredRepairWorkbenchOrders = computed(() => {
    if (selectedRepairPriority.value === 'all') {
        return repairWorkbenchOrders.value
    }

    return repairWorkbenchOrders.value.filter((row) => row.priorityKey === selectedRepairPriority.value)
})

const currentVisibleRepairOrder = computed(() => {
    return filteredRepairWorkbenchOrders.value.find((row) => row.statusRaw === 'processing')
        || filteredRepairWorkbenchOrders.value.find((row) => row.statusRaw === 'accepted')
        || filteredRepairWorkbenchOrders.value[0]
        || repairWorkbenchOrders.value[0]
        || null
})

const repairCalendarEvents = computed<OwnerCalendarEvent[]>(() => {
    return repairWorkbenchOrders.value
        .map((item) => {
            const sourceDate = getRepairEventDate(item.raw)
            const dateKey = dateKeyFromValue(sourceDate)

            if (!dateKey) return null

            return {
                id: `repair-${item.code}`,
                dateKey,
                title: item.title,
                time: formatCalendarEventTime(sourceDate) || item.time,
                path: '/repair/list',
            }
        })
        .filter(Boolean)
        .sort((a, b) => a!.dateKey.localeCompare(b!.dateKey)) as OwnerCalendarEvent[]
})

const repairCalendarEventMap = computed(() => {
    return repairCalendarEvents.value.reduce<Record<string, OwnerCalendarEvent[]>>((map, item) => {
        map[item.dateKey] = [...(map[item.dateKey] || []), item]
        return map
    }, {})
})

const repairCalendarDays = computed<CalendarDay[]>(() => {
    const cursor = repairCalendarCursor.value
    const firstDay = new Date(cursor.getFullYear(), cursor.getMonth(), 1)
    const dayOffset = (firstDay.getDay() + 6) % 7
    const daysInMonth = new Date(cursor.getFullYear(), cursor.getMonth() + 1, 0).getDate()
    const todayKey = toDateKey(new Date())
    const cells: CalendarDay[] = []

    for (let index = 0; index < dayOffset; index += 1) {
        cells.push({
            key: `repair-empty-${index}`,
            day: null,
            dateKey: '',
            hasEvent: false,
            isToday: false,
        })
    }

    for (let day = 1; day <= daysInMonth; day += 1) {
        const dateKey = toDateKey(new Date(cursor.getFullYear(), cursor.getMonth(), day))

        cells.push({
            key: `repair-${dateKey}`,
            day,
            dateKey,
            hasEvent: Boolean(repairCalendarEventMap.value[dateKey]?.length),
            isToday: dateKey === todayKey,
        })
    }

    while (cells.length % 7 !== 0) {
        cells.push({
            key: `repair-tail-${cells.length}`,
            day: null,
            dateKey: '',
            hasEvent: false,
            isToday: false,
        })
    }

    return cells
})

const visibleRepairCalendarEvents = computed(() => {
    const monthKey = `${repairCalendarCursor.value.getFullYear()}-${`${repairCalendarCursor.value.getMonth() + 1}`.padStart(2, '0')}`

    return repairCalendarEvents.value
        .filter((item) => item.dateKey.startsWith(monthKey))
        .slice(0, 4)
})

const shiftRepairCalendarMonth = (offset: number) => {
    repairCalendarCursor.value = new Date(
        repairCalendarCursor.value.getFullYear(),
        repairCalendarCursor.value.getMonth() + offset,
        1,
    )
}

const goToRepairCalendarDay = (day: CalendarDay) => {
    const firstEvent = repairCalendarEventMap.value[day.dateKey]?.[0]

    if (firstEvent) {
        goTo(firstEvent.path)
    }
}

const openRepairResultDrawer = (row?: RepairWorkbenchOrder | null) => {
    selectedRepairResult.value = row?.raw || currentVisibleRepairOrder.value?.raw || null
    repairResultDrawerVisible.value = true
}

const isUnpaidFee = (item: any) => ['unpaid', 'overdue'].includes(item.status)
const isActiveRepair = (item: any) => item.status !== 'finished'
const isActiveComplaint = (item: any) => !['done', 'closed'].includes(item.status)

const primaryOwnerProfile = computed(() => {
    return ownerProfiles.value.find((item) => item.is_primary) || ownerProfiles.value[0] || null
})

const primaryOwnerHouse = computed(() => {
    return ownerHouses.value[0] || primaryOwnerProfile.value?.house || null
})

const ownerDisplayName = computed(() => {
    return primaryOwnerProfile.value?.name || username.value || '业主'
})

const ownerHouseTitle = computed(() => {
    const profile = primaryOwnerProfile.value || {}
    const house = primaryOwnerHouse.value || {}
    const communityName = profile.community_name || house.community_name || '社区'
    const buildingName = profile.building_name || house.building_name || ''
    const unitName = profile.unit_name || house.unit_name || ''
    const roomNo = profile.room_no || house.room_no || ''
    const addressParts = [buildingName, unitName, roomNo].filter(Boolean).join('-')

    return addressParts ? `${communityName} ${addressParts}` : communityName
})

const ownerHouseMeta = computed(() => {
    const house = primaryOwnerHouse.value || {}
    const metas = []

    if (house.area) metas.push(`建筑面积：${house.area}㎡`)
    if (house.house_type) metas.push(`房屋类型：${house.house_type}`)
    if (house.status) metas.push(`房屋状态：${houseStatusLabels[house.status] || house.status}`)

    return metas.length ? metas : ['暂无房屋详情']
})

const ownerProfileCompleted = computed(() => {
    const profile = primaryOwnerProfile.value

    return Boolean(profile?.phone && profile?.id_card_mask && primaryOwnerHouse.value)
})

const unpaidOwnerFees = computed(() => ownerFees.value.filter(isUnpaidFee))

const ownerFeeTotalAmount = computed(() => {
    return unpaidOwnerFees.value.reduce((total, item) => total + Number(item.amount || 0), 0)
})

const activeOwnerRepairs = computed(() => ownerRepairsData.value.filter(isActiveRepair))
const activeOwnerComplaints = computed(() => ownerComplaints.value.filter(isActiveComplaint))

const ownerRecentTasks = computed<OwnerTaskItem[]>(() => {
    const tasks: OwnerTaskItem[] = []

    if (unpaidOwnerFees.value.length) {
        const feeNames = Array.from(new Set(unpaidOwnerFees.value.map(feeTypeText))).join('、')

        tasks.push({
            id: 'fees',
            title: `本月账单待处理`,
            desc: feeNames ? `${feeNames}等费用待缴纳` : '费用待缴纳',
            amount: formatMoney(ownerFeeTotalAmount.value),
            status: '待缴费',
            statusClass: 'warning',
            action: '处理',
            path: '/fee/list',
            tone: 'amber',
            icon: Money,
        })
    }

    const repair = activeOwnerRepairs.value[0]

    if (repair) {
        const progress = repairProgressMap[repair.status] || 40

        tasks.push({
            id: `repair-${repair.id}`,
            title: '服务单待确认',
            desc: repair.title || repair.content || '报修服务单正在处理',
            progress,
            status: repairStatusText(repair),
            statusClass: statusClass(repairStatusText(repair)),
            action: '查看',
            path: '/repair/list',
            tone: 'blue',
            icon: Tools,
        })
    }

    if (!ownerProfileCompleted.value) {
        tasks.push({
            id: 'profile',
            title: '身份认证待完善',
            desc: '完善身份信息，享受更多服务',
            status: '待完善',
            statusClass: 'warning',
            action: '处理',
            path: '/profile',
            tone: 'green',
            icon: UserFilled,
        })
    }

    const complaint = activeOwnerComplaints.value[0]

    if (complaint) {
        tasks.push({
            id: `complaint-${complaint.id}`,
            title: '投诉反馈待查看',
            desc: complaint.title || complaint.content || '请查看处理进度',
            status: complaintStatusText(complaint),
            statusClass: statusClass(complaintStatusText(complaint)),
            action: '查看',
            path: '/complaint/list',
            tone: 'purple',
            icon: ChatDotRound,
        })
    }

    return tasks
})

const ownerNoticeItems = computed<OwnerNoticeItem[]>(() => {
    return ownerNotices.value
        .filter((item) => item.status !== 'draft')
        .slice(0, 5)
        .map((item) => ({
            id: String(item.id || item.title),
            title: item.title || '公告通知',
            date: formatDateShort(item.created_at),
        }))
})

const ownerServiceItems = computed<OwnerServiceItem[]>(() => {
    const repairItems = ownerRepairsData.value.map((item) => ({
        id: `repair-${item.id}`,
        title: item.title || '报修服务',
        meta: `工单号：BX${String(item.id || '').padStart(10, '0')}`,
        status: repairStatusText(item),
        statusClass: statusClass(repairStatusText(item)),
        date: formatDateTimeShort(item.finish_time || item.created_at),
        path: '/repair/list',
    }))

    const complaintItems = ownerComplaints.value.map((item) => ({
        id: `complaint-${item.id}`,
        title: item.title || '投诉建议',
        meta: `工单号：TS${String(item.id || '').padStart(10, '0')}`,
        status: complaintStatusText(item),
        statusClass: statusClass(complaintStatusText(item)),
        date: formatDateTimeShort(item.updated_at || item.created_at),
        path: '/complaint/list',
    }))

    return [...repairItems, ...complaintItems].slice(0, 3)
})

const ownerCalendarEvents = computed<OwnerCalendarEvent[]>(() => {
    const events: OwnerCalendarEvent[] = []

    ownerFees.value.forEach((item) => {
        const dateKey = dateKeyFromValue(item.deadline)
        if (!dateKey) return

        events.push({
            id: `fee-${item.id}`,
            dateKey,
            title: `${feeTypeText(item)}缴费`,
            time: formatCalendarEventTime(item.deadline),
            path: '/fee/list',
        })
    })

    ownerRepairsData.value.forEach((item) => {
        const sourceDate = item.finish_time || item.created_at
        const dateKey = dateKeyFromValue(sourceDate)
        if (!dateKey) return

        events.push({
            id: `repair-${item.id}`,
            dateKey,
            title: item.title || '报修服务',
            time: formatCalendarEventTime(sourceDate),
            path: '/repair/list',
        })
    })

    ownerComplaints.value.forEach((item) => {
        const sourceDate = item.updated_at || item.created_at
        const dateKey = dateKeyFromValue(sourceDate)
        if (!dateKey) return

        events.push({
            id: `complaint-${item.id}`,
            dateKey,
            title: item.title || '投诉建议',
            time: formatCalendarEventTime(sourceDate),
            path: '/complaint/list',
        })
    })

    ownerNotices.value.forEach((item) => {
        const dateKey = dateKeyFromValue(item.created_at)
        if (!dateKey) return

        events.push({
            id: `notice-${item.id}`,
            dateKey,
            title: item.title || '公告活动',
            time: formatCalendarEventTime(item.created_at),
            path: '/notice/list',
        })
    })

    return events.sort((a, b) => a.dateKey.localeCompare(b.dateKey))
})

const ownerCalendarEventMap = computed(() => {
    return ownerCalendarEvents.value.reduce<Record<string, OwnerCalendarEvent[]>>((map, item) => {
        map[item.dateKey] = [...(map[item.dateKey] || []), item]
        return map
    }, {})
})

const ownerCalendarDays = computed<CalendarDay[]>(() => {
    const cursor = ownerCalendarCursor.value
    const firstDay = new Date(cursor.getFullYear(), cursor.getMonth(), 1)
    const dayOffset = (firstDay.getDay() + 6) % 7
    const daysInMonth = new Date(cursor.getFullYear(), cursor.getMonth() + 1, 0).getDate()
    const todayKey = toDateKey(new Date())
    const cells: CalendarDay[] = []

    for (let index = 0; index < dayOffset; index += 1) {
        cells.push({
            key: `empty-${index}`,
            day: null,
            dateKey: '',
            hasEvent: false,
            isToday: false,
        })
    }

    for (let day = 1; day <= daysInMonth; day += 1) {
        const dateKey = toDateKey(new Date(cursor.getFullYear(), cursor.getMonth(), day))

        cells.push({
            key: dateKey,
            day,
            dateKey,
            hasEvent: Boolean(ownerCalendarEventMap.value[dateKey]?.length),
            isToday: dateKey === todayKey,
        })
    }

    while (cells.length % 7 !== 0) {
        cells.push({
            key: `tail-${cells.length}`,
            day: null,
            dateKey: '',
            hasEvent: false,
            isToday: false,
        })
    }

    return cells
})

const visibleOwnerCalendarEvents = computed(() => {
    const monthKey = `${ownerCalendarCursor.value.getFullYear()}-${`${ownerCalendarCursor.value.getMonth() + 1}`.padStart(2, '0')}`

    return ownerCalendarEvents.value
        .filter((item) => item.dateKey.startsWith(monthKey))
        .slice(0, 4)
})

const shiftOwnerCalendarMonth = (offset: number) => {
    ownerCalendarCursor.value = new Date(
        ownerCalendarCursor.value.getFullYear(),
        ownerCalendarCursor.value.getMonth() + offset,
        1,
    )
}

const goToCalendarDay = (day: CalendarDay) => {
    const firstEvent = ownerCalendarEventMap.value[day.dateKey]?.[0]

    if (firstEvent) {
        goTo(firstEvent.path)
    }
}

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

const readSettledList = (result: PromiseSettledResult<any>) => {
    if (result.status !== 'fulfilled') return []

    return extractList(result.value?.data?.data)
}

const loadOwnerHomeData = async () => {
    const [
        houseResult,
        ownerResult,
        feeResult,
        repairResult,
        complaintResult,
        noticeResult,
    ] = await Promise.allSettled([
        getHouseList(),
        getOwnerList(''),
        getFeeList({ page_size: 1000 }),
        getRepairList({ page_size: 1000 }),
        getComplaintList({ page_size: 1000 }),
        getNoticeList(),
    ])

    ownerHouses.value = readSettledList(houseResult)
    ownerProfiles.value = readSettledList(ownerResult)
    ownerFees.value = readSettledList(feeResult)
    ownerRepairsData.value = readSettledList(repairResult)
    ownerComplaints.value = readSettledList(complaintResult)
    ownerNotices.value = readSettledList(noticeResult)
}

const loadRepairerHomeData = async () => {
    const [repairResult] = await Promise.allSettled([
        getRepairList({ page_size: 1000 }),
    ])

    repairerRepairs.value = readSettledList(repairResult)
}

const handleRepairResultSubmitted = async () => {
    selectedRepairResult.value = null
    await loadRepairerHomeData()
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

    if (isOwnerRole.value) {
        await loadOwnerHomeData()
    }

    if (isRepairRole.value) {
        await loadRepairerHomeData()
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
                        <span>车位费 9</span>
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

        <section v-else-if="isRepairRole" class="workbench repair-workbench">
            <div class="workbench-heading">
                <div>
                    <h1>维修工作台</h1>
                    <p>欢迎回来，{{ username }}！</p>
                </div>
            </div>

            <div class="repair-workspace">
                <main class="repair-main-stack">
                    <section class="panel repair-summary-panel">
                        <div class="panel-header">
                            <h2>今日工作摘要</h2>
                        </div>
                        <div class="repair-summary-grid">
                            <div>
                                <span class="repair-summary-icon"><el-icon><Calendar /></el-icon></span>
                                <p>最早预约</p>
                                <strong>{{ currentVisibleRepairOrder?.time || '-' }}</strong>
                            </div>
                            <div>
                                <span class="repair-summary-icon"><el-icon><Tickets /></el-icon></span>
                                <p>待处理</p>
                                <strong>{{ filteredRepairWorkbenchOrders.length }} 单</strong>
                            </div>
                            <div>
                                <span class="repair-summary-icon"><el-icon><Tools /></el-icon></span>
                                <p>平均响应</p>
                                <strong>12分钟</strong>
                            </div>
                        </div>
                    </section>

                    <section class="panel main-panel repair-order-pool">
                        <div class="panel-header">
                            <h2>待接工单池</h2>
                            <div class="filter-line">
                                <span>工单号 / 业主 / 房号</span>
                                <button type="button" @click="loadRepairerHomeData">刷新</button>
                            </div>
                        </div>

                        <div class="tab-row">
                            <button
                                v-for="item in repairPriorityTabs"
                                :key="item.key"
                                type="button"
                                :class="{ active: selectedRepairPriority === item.key }"
                                @click="selectedRepairPriority = item.key"
                            >
                                {{ item.label }} {{ item.count }}
                            </button>
                        </div>

                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>工单号</th>
                                    <th>业主</th>
                                    <th>房号</th>
                                    <th>报修类型</th>
                                    <th>紧急程度</th>
                                    <th>期望时间</th>
                                    <th>操作</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="row in filteredRepairWorkbenchOrders.slice(0, 6)" :key="row.code">
                                    <td>{{ row.code }}</td>
                                    <td>{{ row.owner }}</td>
                                    <td>{{ row.room }}</td>
                                    <td>{{ row.title }}</td>
                                    <td><span class="status-pill" :class="statusClass(row.priority)">{{ row.priority }}</span></td>
                                    <td>{{ row.time }}</td>
                                    <td>
                                        <button
                                            v-if="row.statusRaw === 'processing'"
                                            type="button"
                                            class="outline-mini"
                                            @click="openRepairResultDrawer(row)"
                                        >
                                            上传结果
                                        </button>
                                        <button
                                            v-else
                                            type="button"
                                            class="solid-mini"
                                            @click="goTo('/repair/list')"
                                        >
                                            {{ row.statusRaw === 'assigned' ? '接单' : '查看' }}
                                        </button>
                                    </td>
                                </tr>
                                <tr v-if="filteredRepairWorkbenchOrders.length === 0">
                                    <td colspan="7" class="table-empty">当前分类暂无工单</td>
                                </tr>
                            </tbody>
                        </table>
                    </section>

                    <section class="panel repair-calendar-panel">
                        <div class="owner-calendar-header">
                            <div>
                                <el-icon><Calendar /></el-icon>
                                <h2>维修日历</h2>
                            </div>
                            <div class="owner-calendar-month">
                                <button type="button" @click="shiftRepairCalendarMonth(-1)">&lt;</button>
                                <strong>{{ formatMonthLabel(repairCalendarCursor) }}</strong>
                                <button type="button" @click="shiftRepairCalendarMonth(1)">&gt;</button>
                            </div>
                        </div>

                        <div class="owner-calendar-body repair-calendar-body">
                            <div class="owner-calendar-grid">
                                <span>一</span>
                                <span>二</span>
                                <span>三</span>
                                <span>四</span>
                                <span>五</span>
                                <span>六</span>
                                <span>日</span>
                                <button
                                    v-for="day in repairCalendarDays"
                                    :key="day.key"
                                    type="button"
                                    class="owner-calendar-cell"
                                    :class="{ 'has-event': day.hasEvent, today: day.isToday, empty: !day.day }"
                                    :disabled="!day.day"
                                    @click="goToRepairCalendarDay(day)"
                                >
                                    <span v-if="day.day" class="calendar-day-number">{{ day.day }}</span>
                                    <i v-if="day.hasEvent" />
                                </button>
                            </div>

                            <div class="owner-calendar-events">
                                <button
                                    v-for="item in visibleRepairCalendarEvents"
                                    :key="item.id"
                                    type="button"
                                    class="owner-calendar-event"
                                    @click="goTo(item.path)"
                                >
                                    <b>{{ item.dateKey.slice(5) }}</b>
                                    <span>{{ item.title }}</span>
                                    <em>{{ item.time }}</em>
                                </button>
                                <div>
                                    <button type="button" class="text-button" @click="goTo('/repair/list')">查看全部</button>
                                </div>
                            </div>
                        </div>
                    </section>
                </main>

                <aside class="repair-side-stack">
                    <section class="panel repair-route-panel">
                        <div class="panel-header">
                            <h2>今日路线</h2>
                            <button type="button" class="text-button" @click="loadRepairerHomeData">刷新</button>
                        </div>
                        <ul class="repair-route-list">
                            <li v-for="(row, index) in repairWorkbenchOrders.slice(0, 4)" :key="`route-${row.code}`">
                                <span class="route-dot" :class="{ danger: row.priorityKey === 'urgent' }" />
                                <time>{{ row.time.replace('今天 ', '') }}</time>
                                <div>
                                    <strong>{{ row.code }}</strong>
                                    <b>{{ row.title }}</b>
                                    <p>{{ row.room }} ｜ {{ row.owner }}</p>
                                </div>
                                <button
                                    v-if="index === 0 || row.statusRaw === 'processing'"
                                    type="button"
                                    class="outline-mini"
                                    @click="openRepairResultDrawer(row)"
                                >
                                    上传结果
                                </button>
                                <span v-else class="status-pill" :class="statusClass(row.priority)">{{ row.priority }}</span>
                            </li>
                        </ul>
                        <button type="button" class="route-more" @click="goTo('/repair/list')">查看全部路线</button>
                    </section>

                    <section class="panel repair-tools-panel">
                        <div class="panel-header">
                            <h2>工具与备件</h2>
                            <button type="button" class="text-button">查看更多</button>
                        </div>
                        <ul class="repair-tools-list">
                            <li><span>水管接头</span><em>库存 18 个</em></li>
                            <li><span>门禁卡扣</span><em>库存 26 个</em></li>
                            <li><span>电路测试笔</span><em>库存 12 支</em></li>
                            <li><span>绝缘胶带</span><em>库存 15 卷</em></li>
                        </ul>
                    </section>
                </aside>
            </div>
        </section>

        <section v-else-if="isOwnerRole" class="workbench owner-workbench">
            <div class="workbench-heading">
                <div>
                    <h1>业主首页</h1>
                    <p>欢迎回来，{{ ownerDisplayName }}！</p>
                </div>
            </div>

            <section class="owner-house-summary panel">
                <div class="owner-house-icon">
                    <el-icon><OfficeBuilding /></el-icon>
                </div>
                <div class="owner-house-copy">
                    <h2>{{ ownerHouseTitle }}</h2>
                    <p>
                        <span v-for="item in ownerHouseMeta" :key="item">{{ item }}</span>
                    </p>
                </div>
                <span class="owner-house-status" :class="{ pending: !ownerProfileCompleted }">
                    <el-icon><Check /></el-icon>
                    {{ ownerProfileCompleted ? '资料已完善' : '资料待完善' }}
                </span>
            </section>

            <div class="owner-home-grid">
                <main class="owner-main-stack">
                    <section class="panel owner-recent-panel">
                        <div class="panel-header">
                            <h2>近期事项</h2>
                        </div>
                        <ul v-if="ownerRecentTasks.length" class="owner-recent-list">
                            <li v-for="item in ownerRecentTasks" :key="item.id" class="owner-recent-item">
                                <div class="owner-recent-icon" :class="`tone-${item.tone}`">
                                    <el-icon><component :is="item.icon" /></el-icon>
                                </div>
                                <div class="owner-recent-copy">
                                    <strong>{{ item.title }}</strong>
                                    <span>{{ item.desc }}</span>
                                </div>
                                <div v-if="item.amount || item.progress !== undefined" class="owner-task-extra">
                                    <strong v-if="item.amount">{{ item.amount }}</strong>
                                    <div v-else class="owner-progress">
                                        <span>进行中 {{ item.progress }}%</span>
                                        <i><b :style="{ width: `${item.progress || 0}%` }" /></i>
                                    </div>
                                </div>
                                <span class="status-pill" :class="item.statusClass">{{ item.status }}</span>
                                <button type="button" class="owner-outline-button" @click="goTo(item.path)">
                                    {{ item.action }}
                                </button>
                            </li>
                        </ul>
                        <div v-else class="owner-empty-state">暂无待处理事项</div>
                    </section>

                    <section class="panel owner-calendar-panel">
                        <div class="owner-calendar-header">
                            <div>
                                <el-icon><Calendar /></el-icon>
                                <h2>社区日历</h2>
                            </div>
                            <div class="owner-calendar-month">
                                <button type="button" @click="shiftOwnerCalendarMonth(-1)">&lt;</button>
                                <strong>{{ formatMonthLabel(ownerCalendarCursor) }}</strong>
                                <button type="button" @click="shiftOwnerCalendarMonth(1)">&gt;</button>
                            </div>
                        </div>

                        <div class="owner-calendar-body">
                            <div class="owner-calendar-grid">
                                <span>一</span>
                                <span>二</span>
                                <span>三</span>
                                <span>四</span>
                                <span>五</span>
                                <span>六</span>
                                <span>日</span>
                                <button
                                    v-for="day in ownerCalendarDays"
                                    :key="day.key"
                                    type="button"
                                    class="owner-calendar-cell"
                                    :class="{ 'has-event': day.hasEvent, today: day.isToday, empty: !day.day }"
                                    :disabled="!day.day"
                                    @click="goToCalendarDay(day)"
                                >
                                    <span v-if="day.day" class="calendar-day-number">{{ day.day }}</span>
                                    <i v-if="day.hasEvent" />
                                </button>
                            </div>

                            <div class="owner-calendar-events">
                                <button
                                    v-for="item in visibleOwnerCalendarEvents"
                                    :key="item.id"
                                    type="button"
                                    class="owner-calendar-event"
                                    @click="goTo(item.path)"
                                >
                                    <b>{{ item.dateKey.slice(5) }}</b>
                                    <span>{{ item.title }}</span>
                                    <em>{{ item.time }}</em>
                                </button>
                                <div>
                                    <button type="button" class="text-button" @click="goTo('/notice/list')">查看全部</button>
                                </div>
                            </div>
                        </div>
                    </section>
                </main>

                <aside class="owner-side-stack">
                    <section class="panel">
                        <div class="panel-header">
                            <h2>公告活动</h2>
                            <button type="button" class="text-button" @click="goTo('/notice/list')">更多</button>
                        </div>
                        <ul v-if="ownerNoticeItems.length" class="owner-side-notice-list">
                            <li v-for="item in ownerNoticeItems" :key="item.id">
                                <span>{{ item.title }}</span>
                                <em>{{ item.date }}</em>
                            </li>
                        </ul>
                        <div v-else class="owner-empty-state compact">暂无公告</div>
                    </section>

                    <section class="panel">
                        <div class="panel-header">
                            <h2>服务进度</h2>
                            <button type="button" class="text-button" @click="goTo('/repair/list')">更多</button>
                        </div>
                        <ul v-if="ownerServiceItems.length" class="owner-service-list">
                            <li v-for="item in ownerServiceItems" :key="item.id">
                                <button type="button" @click="goTo(item.path)">
                                    <span class="dot" :class="item.statusClass" />
                                    <strong>{{ item.title }}</strong>
                                    <em>{{ item.status }}</em>
                                    <small>{{ item.meta }}</small>
                                    <time>{{ item.date }}</time>
                                </button>
                            </li>
                        </ul>
                        <div v-else class="owner-empty-state compact">暂无服务进度</div>
                    </section>

                    <section class="panel">
                        <div class="panel-header">
                            <h2><el-icon><Phone /></el-icon> 便民电话</h2>
                        </div>
                        <ul class="owner-phone-list">
                            <li v-for="item in ownerConveniencePhones" :key="item.label">
                                <span><el-icon><Phone /></el-icon>{{ item.label }}</span>
                                <em>{{ item.phone }}</em>
                            </li>
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
    color: var(--text-primary);
    font-family: var(--font-family-base);
    font-size: 14px;
    line-height: 1.5;
    letter-spacing: 0;
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
    color: var(--text-heading);
    font-size: 24px;
    font-weight: 700;
    line-height: 32px;
}

.workbench-heading p {
    margin: 8px 0 0;
    color: var(--text-muted);
    font-size: 14px;
    font-weight: 400;
    line-height: 22px;
}

.heading-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
    color: var(--text-muted);
    font-size: 14px;
    font-weight: 400;
    line-height: 22px;
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
    font-size: 14px;
    font-weight: 600;
    line-height: 20px;
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
    color: var(--text-primary);
    font-size: 15px;
    font-weight: 600;
    line-height: 22px;
}

.metric-card strong {
    display: block;
    margin-top: 6px;
    color: var(--text-heading);
    font-size: 28px;
    font-weight: 700;
    line-height: 36px;
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
    color: var(--text-muted);
    font-size: 13px;
    font-weight: 400;
    line-height: 20px;
}

.tone-teal {
    --tone: var(--brand-primary);
    --tone-soft: var(--brand-primary-soft);
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

.tone-purple {
    --tone: #5b5ce2;
    --tone-soft: #ecebff;
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
    background: linear-gradient(135deg, #0f766e, #0b625b);
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
    color: var(--text-primary);
    font-size: 15px;
    font-weight: 600;
    line-height: 22px;
}

.filter-line {
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--text-muted);
    font-size: 13px;
    font-weight: 400;
    line-height: 20px;
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
    color: var(--text-subtle);
    background: #f8fafc;
    font-size: 13px;
    line-height: 20px;
}

.tab-row .active {
    color: #fff;
    border-color: var(--brand-primary);
    background: var(--brand-primary);
}

.data-table {
    width: 100%;
    min-width: 760px;
    border-collapse: collapse;
    font-size: 14px;
}

.data-table th,
.data-table td {
    padding: 12px 10px;
    border-bottom: 1px solid #eef1f5;
    text-align: left;
    white-space: nowrap;
}

.data-table td {
    color: var(--text-primary);
    font-size: 14px;
    font-weight: 400;
    line-height: 22px;
}

.data-table th {
    color: var(--text-subtle);
    background: #f8fafc;
    font-size: 13px;
    font-weight: 600;
    line-height: 20px;
}

.status-pill {
    display: inline-flex;
    min-width: 52px;
    justify-content: center;
    padding: 3px 8px;
    border-radius: 5px;
    font-size: 12px;
    font-weight: 500;
    font-style: normal;
    line-height: 18px;
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
    color: var(--brand-primary);
    background: transparent;
    font-size: 14px;
    font-weight: 500;
    line-height: 20px;
}

.solid-mini {
    min-width: 54px;
    height: 28px;
    border-radius: 5px;
    color: #fff;
    font-size: 14px;
    font-weight: 600;
    line-height: 20px;
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
    color: var(--text-muted);
    font-size: 13px;
    font-weight: 400;
    line-height: 20px;
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
    color: var(--text-muted);
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
    color: var(--brand-primary);
    font-weight: 700;
}

.activity-list p {
    margin: 0;
    overflow: hidden;
    color: var(--text-muted);
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
    color: var(--text-muted);
}

.resource-grid .el-icon {
    color: var(--brand-primary);
    font-size: 28px;
}

.resource-grid strong {
    color: var(--text-heading);
    font-size: 28px;
    font-weight: 700;
    line-height: 36px;
}

.money-total {
    display: block;
    margin: 2px 0 10px;
    color: var(--text-heading);
    font-size: 28px;
    font-weight: 700;
    line-height: 36px;
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
    color: var(--text-muted);
    font-size: 14px;
    font-weight: 400;
    line-height: 22px;
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
    color: var(--brand-primary);
    font-weight: 600;
}

.progress-line .active::before {
    border-color: var(--brand-primary);
    background: #d8f3ef;
}

.current-order {
    margin: 0;
    color: var(--text-subtle);
    font-size: 14px;
    font-weight: 400;
    line-height: 22px;
}

.current-order strong {
    color: var(--brand-primary);
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
    color: var(--text-primary);
    background: #fff;
    font-size: 14px;
    font-weight: 600;
    line-height: 20px;
}

.operation-grid .el-icon {
    color: var(--brand-primary);
    font-size: 30px;
}

.owner-workbench {
    max-width: 100%;
}

.owner-house-summary {
    display: grid;
    grid-template-columns: 76px minmax(0, 1fr) auto;
    align-items: center;
    gap: 18px;
    min-height: 112px;
    padding: 18px 26px;
}

.owner-house-copy {
    min-width: 0;
}

.owner-house-copy h2 {
    margin: 0 0 8px;
    color: var(--text-heading);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-size: 24px;
    font-weight: 700;
    line-height: 32px;
}

.owner-house-copy p {
    display: flex;
    flex-wrap: wrap;
    gap: 8px 18px;
    margin: 0;
    color: var(--text-muted);
    font-size: 14px;
    line-height: 22px;
}

.owner-house-status {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    min-width: 110px;
    justify-content: center;
    padding: 8px 12px;
    border: 1px solid #bfe8e3;
    border-radius: 8px;
    color: var(--brand-primary);
    background: #eefaf8;
    font-size: 14px;
    font-weight: 600;
    line-height: 20px;
    white-space: nowrap;
}

.owner-house-status.pending {
    color: #d97706;
    border-color: #ffe0a3;
    background: #fff8eb;
}

.owner-home-grid {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 380px;
    gap: 16px;
    align-items: start;
}

.owner-main-stack,
.owner-side-stack {
    display: flex;
    min-width: 0;
    flex-direction: column;
    gap: 16px;
}

.owner-recent-list,
.owner-side-notice-list,
.owner-service-list,
.owner-phone-list {
    margin: 0;
    padding: 0;
    list-style: none;
}

.owner-recent-item {
    display: grid;
    grid-template-columns: 46px minmax(180px, 1fr) minmax(120px, 180px) 78px 78px;
    align-items: center;
    gap: 14px;
    min-height: 74px;
    padding: 12px 0;
    border-bottom: 1px solid #eef1f5;
}

.owner-recent-item:last-child {
    border-bottom: 0;
}

.owner-recent-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    color: var(--tone);
    background: var(--tone-soft);
    font-size: 22px;
}

.owner-recent-copy {
    min-width: 0;
}

.owner-recent-copy strong,
.owner-recent-copy span {
    display: block;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.owner-recent-copy strong {
    color: var(--text-primary);
    font-size: 15px;
    font-weight: 600;
    line-height: 22px;
}

.owner-recent-copy span {
    margin-top: 4px;
    color: var(--text-muted);
    font-size: 13px;
    line-height: 20px;
}

.owner-task-extra {
    min-width: 0;
}

.owner-task-extra > strong {
    display: block;
    color: #ef4444;
    overflow: hidden;
    text-align: right;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-size: 20px;
    font-weight: 700;
    line-height: 28px;
}

.owner-progress {
    min-width: 0;
}

.owner-progress span {
    display: block;
    margin-bottom: 6px;
    color: var(--text-subtle);
    font-size: 13px;
    line-height: 20px;
}

.owner-progress i {
    display: block;
    height: 8px;
    overflow: hidden;
    border-radius: 999px;
    background: #e5e7eb;
}

.owner-progress b {
    display: block;
    height: 100%;
    border-radius: inherit;
    background: var(--brand-primary);
}

.owner-outline-button {
    height: 34px;
    border: 1px solid #8ccfca;
    border-radius: 6px;
    color: var(--brand-primary);
    background: #fff;
    font-size: 14px;
    font-weight: 600;
    line-height: 20px;
    cursor: pointer;
}

.owner-empty-state {
    display: flex;
    min-height: 96px;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
    font-size: 14px;
}

.owner-empty-state.compact {
    min-height: 48px;
}

.owner-calendar-panel {
    padding: 18px 20px;
}

.owner-calendar-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    margin-bottom: 14px;
}

.owner-calendar-header > div:first-child,
.owner-calendar-month {
    display: inline-flex;
    align-items: center;
    gap: 10px;
}

.owner-calendar-header h2 {
    margin: 0;
    color: var(--text-primary);
    font-size: 15px;
    font-weight: 600;
    line-height: 22px;
}

.owner-calendar-header .el-icon {
    color: var(--text-subtle);
    font-size: 18px;
}

.owner-calendar-month strong {
    min-width: 96px;
    text-align: center;
    color: var(--text-primary);
    font-size: 15px;
    font-weight: 600;
}

.owner-calendar-month button {
    width: 28px;
    height: 28px;
    border: 0;
    border-radius: 6px;
    color: var(--text-subtle);
    background: transparent;
    font-size: 20px;
    cursor: pointer;
}

.owner-calendar-body {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 220px;
    gap: 20px;
    align-items: stretch;
}

.owner-calendar-grid {
    display: grid;
    grid-template-columns: repeat(7, minmax(0, 1fr));
    border-top: 1px solid #eef1f5;
    border-left: 1px solid #eef1f5;
}

.owner-calendar-grid > span,
.owner-calendar-cell {
    min-height: 42px;
    border-right: 1px solid #eef1f5;
    border-bottom: 1px solid #eef1f5;
}

.owner-calendar-grid > span {
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-subtle);
    font-size: 13px;
    font-weight: 600;
}

.owner-calendar-cell {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    border-top: 0;
    border-left: 0;
    color: var(--text-primary);
    background: #fff;
    cursor: pointer;
}

.owner-calendar-cell.empty {
    cursor: default;
}

.owner-calendar-cell:disabled {
    color: transparent;
    cursor: default;
}

.calendar-day-number {
    display: inline-flex;
    width: 30px;
    height: 30px;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
}

.owner-calendar-cell.has-event .calendar-day-number {
    color: #fff;
    background: var(--brand-primary);
    font-weight: 700;
}

.owner-calendar-cell.today:not(.has-event) .calendar-day-number {
    color: var(--brand-primary);
    background: #e0f4f1;
    font-weight: 700;
}

.owner-calendar-cell i {
    position: absolute;
    bottom: 6px;
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: #f59f00;
}

.owner-calendar-events {
    display: flex;
    flex-direction: column;
    gap: 12px;
    border-left: 1px solid #eef1f5;
    padding-left: 18px;
}

.owner-calendar-event {
    display: grid;
    grid-template-columns: 52px minmax(0, 1fr);
    gap: 2px 10px;
    border: 0;
    text-align: left;
    background: transparent;
    cursor: pointer;
}

.owner-calendar-event b {
    grid-row: span 2;
    color: var(--brand-primary);
    font-size: 14px;
    line-height: 22px;
}

.owner-calendar-event span,
.owner-calendar-event em {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.owner-calendar-event span {
    color: var(--text-primary);
    font-size: 14px;
    font-weight: 600;
    line-height: 22px;
}

.owner-calendar-event em {
    color: var(--text-muted);
    font-size: 12px;
    font-style: normal;
    line-height: 18px;
}

.owner-side-notice-list li,
.owner-phone-list li {
    display: flex;
    align-items: center;
    gap: 10px;
    min-height: 34px;
    border-bottom: 1px solid #eef1f5;
    color: var(--text-muted);
    font-size: 13px;
    line-height: 20px;
}

.owner-side-notice-list li:last-child,
.owner-phone-list li:last-child {
    border-bottom: 0;
}

.owner-side-notice-list span {
    position: relative;
    flex: 1;
    min-width: 0;
    overflow: hidden;
    padding-left: 12px;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.owner-side-notice-list span::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 0;
    width: 4px;
    height: 4px;
    border-radius: 50%;
    background: var(--text-muted);
    transform: translateY(-50%);
}

.owner-side-notice-list em,
.owner-phone-list em {
    color: var(--text-muted);
    font-style: normal;
    white-space: nowrap;
}

.owner-service-list li + li {
    margin-top: 8px;
}

.owner-service-list button {
    display: grid;
    width: 100%;
    grid-template-columns: 20px minmax(0, 1fr) auto;
    gap: 2px 10px;
    border: 0;
    text-align: left;
    background: transparent;
    cursor: pointer;
}

.owner-service-list .dot {
    grid-row: span 2;
    align-self: center;
    width: 12px;
    height: 12px;
}

.owner-service-list strong,
.owner-service-list small {
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.owner-service-list strong {
    color: var(--text-primary);
    font-size: 14px;
    font-weight: 600;
    line-height: 22px;
}

.owner-service-list small {
    color: var(--text-muted);
    font-size: 12px;
    line-height: 18px;
}

.owner-service-list em {
    color: var(--brand-primary);
    font-size: 13px;
    font-style: normal;
    font-weight: 600;
    line-height: 20px;
    white-space: nowrap;
}

.owner-service-list time {
    color: var(--text-muted);
    font-size: 12px;
    line-height: 18px;
    white-space: nowrap;
}

.owner-phone-list span {
    display: inline-flex;
    flex: 1;
    min-width: 0;
    align-items: center;
    gap: 8px;
    color: var(--text-primary);
}

.owner-phone-list .el-icon {
    display: inline-flex;
    width: 24px;
    height: 24px;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    color: var(--brand-primary);
    background: #d8f3ef;
}

.owner-hero {
    display: grid;
    grid-template-columns: 78px minmax(0, 1fr) auto;
    align-items: center;
    gap: 18px;
}

.owner-hero > div:not(.owner-house-icon):not(.owner-hero-actions) {
    min-width: 0;
}

.owner-house-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 64px;
    height: 64px;
    border-radius: 50%;
    color: var(--brand-primary);
    background: #d8f3ef;
    font-size: 34px;
}

.owner-hero h2 {
    margin: 5px 0 8px;
    color: var(--text-heading);
    font-size: 24px;
    font-weight: 700;
    line-height: 32px;
    overflow-wrap: anywhere;
}

.owner-hero span,
.owner-hero p {
    margin: 0;
    color: var(--text-muted);
    font-size: 14px;
    font-weight: 400;
    line-height: 22px;
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
    color: var(--brand-primary);
    background: #fff;
    font-size: 14px;
    font-weight: 600;
    line-height: 20px;
}

.owner-card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 14px;
    margin-bottom: 16px;
}

.owner-card {
    display: grid;
    grid-template-columns: 50px minmax(0, 1fr);
    gap: 12px;
    align-items: center;
    min-height: 128px;
    padding: 16px;
    overflow: hidden;
}

.owner-card > div {
    min-width: 0;
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
    color: var(--text-heading);
    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-size: clamp(20px, 1.35vw, 28px);
    font-weight: 700;
    line-height: 32px;
}

.owner-card p,
.owner-card span {
    overflow: hidden;
    text-overflow: ellipsis;
}

.owner-card button {
    grid-column: 1 / -1;
    height: 32px;
    border-top: 1px solid #eef1f5;
    color: var(--brand-primary);
    background: transparent;
    font-size: 14px;
    font-weight: 500;
    line-height: 20px;
}

.owner-task-list li {
    display: grid;
    grid-template-columns: 42px minmax(0, 1fr) minmax(108px, max-content) 92px;
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
    font-weight: 600;
    line-height: 20px;
}

.owner-task-list strong,
.owner-task-list span {
    display: block;
}

.owner-task-list span {
    margin-top: 4px;
    color: var(--text-muted);
    font-size: 13px;
    font-weight: 400;
    line-height: 20px;
}

.owner-task-list em {
    color: #ef4444;
    max-width: 100%;
    overflow: hidden;
    text-align: right;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-size: clamp(22px, 1.35vw, 28px);
    font-weight: 700;
    font-style: normal;
    line-height: 32px;
}

.owner-task-list button,
.ghost-button,
.primary-wide {
    height: 32px;
    border-radius: 6px;
    font-weight: 600;
    line-height: 20px;
}

.owner-task-list button,
.ghost-button {
    border: 1px solid #d0ebe8;
    color: var(--brand-primary);
    background: #fff;
    font-size: 14px;
    font-weight: 500;
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
    color: var(--brand-primary);
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
    color: var(--text-muted);
    font-size: 13px;
    font-weight: 400;
    line-height: 20px;
}

.fee-remind {
    margin: 0 0 12px;
    color: var(--text-muted);
    font-size: 13px;
    font-weight: 400;
    line-height: 20px;
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
    .owner-home-grid,
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

    .owner-recent-item {
        grid-template-columns: 46px minmax(0, 1fr) minmax(110px, 150px) 76px 76px;
    }
}

@media (max-width: 900px) {
    .owner-house-summary {
        grid-template-columns: 64px minmax(0, 1fr);
    }

    .owner-house-status {
        grid-column: 1 / -1;
        justify-self: start;
    }

    .owner-recent-item {
        grid-template-columns: 42px minmax(0, 1fr);
    }

    .owner-task-extra,
    .owner-recent-item > .status-pill,
    .owner-outline-button {
        grid-column: 2;
        justify-self: start;
    }

    .owner-calendar-body {
        grid-template-columns: 1fr;
    }

    .owner-calendar-events {
        border-left: 0;
        border-top: 1px solid #eef1f5;
        padding-top: 14px;
        padding-left: 0;
    }
}
</style>
