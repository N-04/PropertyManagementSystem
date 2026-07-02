<!-- 文件说明：实现 src/views/parking/list/ParkingList.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { computed, ref, onMounted, watch } from 'vue'
import { bindParking, deleteParking, getParkingList } from '@/api/parking'
import { getVisitorList } from '@/api/visitor'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useClientPagination } from '@/composables/useClientPagination'
import { useRealtimeRefresh } from '@/composables/useRealtimeRefresh'
import DataPagination from '@/components/common/DataPagination.vue'
import { getStoredRole, getStoredUsername } from '@/utils/authState'
import { appendMessageFeedback } from '@/utils/messageCenterRows'
import { extractListRows } from '@/utils/listResponse'

type ParkingRow = {
    id: number | string
    parking_no?: string
    zone?: string
    owner?: number | string | null
    owner_name?: string
    room_no?: string
    area?: number | string
    status?: string
    status_text?: string
}

type VisitorSourceRow = {
    id?: number | string
    name?: string
    phone?: string
    owner_name?: string
    room_no?: string
    enter_time?: string
    visit_time?: string
    leave_time?: string
    status?: string
}

type VisitorParkingRow = {
    id: number | string
    parking_no: string
    visitor_name?: string
    phone?: string
    owner_name?: string
    room_no?: string
    entry_time: string
    leave_time: string
    status?: string
    status_text: string
}

type ParkingTableRow = ParkingRow

const tableData = ref<ParkingRow[]>([])
const keyword = ref('')
const statusFilter = ref('')
const showVisitorParking = ref(false)
const role = getStoredRole()
const isOwner = computed(() => role === 'owner')
const ownerParkingMode = ref<'mine' | 'available'>('mine')
const router = useRouter()
const route = useRoute()
const PARKING_FEEDBACK_EVENT = 'property-management-parking-feedback'
const PARKING_FEEDBACK_STORAGE_KEY = 'parkingPurchaseFeedback'
const PARKING_FETCH_PAGE_SIZE = 100

// 车位页数据分块：业主车位、可售车位和访客临停分开缓存，避免列表互相污染。
const visitorParkingRows = ref<VisitorParkingRow[]>([])
const availableParkingRows = ref<ParkingRow[]>([])

const parkingZoneText = (zone?: string) => {
    const zoneMap: Record<string, string> = {
        P: '普通临停区',
        PT: '普通临停区',
        SM: '售卖车位区',
    }

    return zoneMap[`${zone || ''}`.toUpperCase()] || zone || '其他'
}

const parkingNoText = (parkingNo?: string) => {
    // 数据库存原始编号，页面展示时把业务前缀换成中文，避免用户看到 SM/PT。
    const rawNo = `${parkingNo || ''}`.trim()
    const normalizedNo = rawNo.toUpperCase()

    if (normalizedNo.startsWith('SM-')) {
        return rawNo.replace(/^SM-/i, '售卖车位-')
    }

    if (normalizedNo.startsWith('PT-')) {
        return rawNo.replace(/^PT-/i, '普通临停-')
    }

    if (normalizedNo.startsWith('P-')) {
        return rawNo.replace(/^P-/i, '普通临停-')
    }

    return rawNo || '-'
}

const isSaleParking = (item: ParkingRow) => {
    // 购买区只认售卖车位，普通区车位留给访客临停使用。
    return `${item.zone || ''}`.toUpperCase() === 'SM'
        || `${item.parking_no || ''}`.trim().toUpperCase().startsWith('SM')
}

const matchesParkingKeyword = (item: ParkingRow) => {
    const keywordValue = keyword.value.trim().toLowerCase()

    if (!keywordValue) {
        return true
    }

    return [
        item.parking_no,
        parkingNoText(item.parking_no),
        item.zone,
        parkingZoneText(item.zone),
        item.owner_name,
        item.room_no,
        item.status_text,
    ].some((value) => `${value || ''}`.toLowerCase().includes(keywordValue))
}

const isOwnerParkingRecord = (item: ParkingRow) => {
    // 管理员的“业主车位”只展示已绑定业主的记录，空闲售卖车位和普通临停车位交给各自视图。
    return Boolean(item.owner || item.owner_name || item.room_no)
}

const adminOwnerParkingRows = computed(() => {
    return tableData.value.filter(isOwnerParkingRecord)
})

const ownerParkingRows = computed(() => {
    const sourceRows = isOwner.value && ownerParkingMode.value === 'available'
        ? availableParkingRows.value
        : isOwner.value
            ? tableData.value
            : adminOwnerParkingRows.value
    const rows = sourceRows.filter(matchesParkingKeyword)

    if (!statusFilter.value) {
        return rows
    }

    return rows.filter((item) => item.status === statusFilter.value)
})

const filteredTableData = computed<ParkingTableRow[]>(() => {
    return ownerParkingRows.value
})
const {
    page,
    pageSize,
    total,
    pagedData: pagedTableData,
    resetPage,
} = useClientPagination(filteredTableData)

const zoneList = computed(() => {
    const zoneMap = new Map<string, ParkingRow[]>()

    ownerParkingRows.value
        .filter((item) => ownerParkingMode.value !== 'available' || isSaleParking(item))
        .forEach((item) => {
            const zone = item.zone || '其他'
            zoneMap.set(zone, [...(zoneMap.get(zone) || []), item])
        })

    return Array.from(zoneMap.entries()).map(([zone, items]) => ({
        zone,
        items: items.sort((a, b) => `${a.parking_no}`.localeCompare(`${b.parking_no}`)),
        idleCount: items.filter((item) => item.status === 'idle').length,
        usedCount: items.filter((item) => item.status === 'used').length,
    }))
})

const parkingSummary = computed(() => {
    return {
        total: tableData.value.length,
        idle: tableData.value.filter((item) => item.status === 'idle').length,
        used: tableData.value.filter((item) => item.status === 'used').length,
        owner: isOwner.value ? tableData.value.length : adminOwnerParkingRows.value.length,
        available: availableParkingRows.value.length,
        visitor: visitorParkingRows.value.length,
    }
})

const normalizeOwnerParkingMode = (mode: unknown): 'mine' | 'available' => {
    return mode === 'available' ? 'available' : 'mine'
}

const statusLabel = (status?: string) => {
    const statusMap: Record<string, string> = {
        idle: '空闲',
        used: '使用中',
        occupied: '使用中',
        sold: '已售',
        disabled: '停用',
    }
    const normalizedStatus = status || ''

    return statusMap[normalizedStatus] || normalizedStatus || '-'
}

const ownerParkingStatusText = (row: ParkingRow) => {
    // 后端 status_text 偶尔可能直接返回英文枚举，这里统一转成中文显示。
    return statusLabel(row.status_text || row.status)
}

const visitorStatusText = (status = '') => {
    const statusMap: Record<string, string> = {
        waiting: '待审核',
        approved: '已预约',
        entered: '临停中',
        left: '已离场',
        rejected: '已拒绝',
    }

    return statusMap[status] || status || '-'
}

const buildVisitorParkingNo = (item: VisitorSourceRow, index: number) => {
    return `V-${String(item.id || index + 1).padStart(4, '0')}`
}

const toNumericId = (id: number | string) => {
    const numericId = Number(id)

    return Number.isFinite(numericId) ? numericId : 0
}

const getList = async () => {
    // 可视化分区需要拿到足够多的车位，再由前端分页控制表格显示。
    const res = await getParkingList({ page_size: PARKING_FETCH_PAGE_SIZE })

    tableData.value = extractListRows<ParkingRow>(res.data.data)
    resetPage()
}

const getOwnerParkingList = async () => {
    // 业主默认只看自己的车位；可购买车位通过 include_idle 单独拉取，避免混入“我的车位”。
    const [mineRes, candidateRes] = await Promise.all([
        getParkingList({ page_size: PARKING_FETCH_PAGE_SIZE }),
        getParkingList({ page_size: PARKING_FETCH_PAGE_SIZE, include_idle: true }),
    ])

    tableData.value = extractListRows<ParkingRow>(mineRes.data.data)
    availableParkingRows.value = extractListRows<ParkingRow>(candidateRes.data.data).filter((item) => {
        return item.status === 'idle' && !item.owner && isSaleParking(item)
    })
    resetPage()
}

const getVisitorParkingList = async () => {
    if (isOwner.value) {
        visitorParkingRows.value = []
        return
    }

    try {
        const res = await getVisitorList({ page_size: 100 })
        const visitors = extractListRows<VisitorSourceRow>(res.data.data)

        // 访客临停不占用业主已购买/绑定车位，按访客预约记录单独生成临停列表。
        visitorParkingRows.value = visitors.map((item, index) => ({
            id: item.id ?? buildVisitorParkingNo(item, index),
            parking_no: buildVisitorParkingNo(item, index),
            visitor_name: item.name,
            phone: item.phone,
            owner_name: item.owner_name,
            room_no: item.room_no,
            entry_time: item.enter_time || item.visit_time || '-',
            leave_time: item.leave_time || '-',
            status: item.status,
            status_text: visitorStatusText(item.status),
        }))
    } catch {
        visitorParkingRows.value = []
    }
}

const loadParkingPageData = async () => {
    if (isOwner.value) {
        await getOwnerParkingList()
        visitorParkingRows.value = []
        return
    }

    await Promise.all([getList(), getVisitorParkingList()])
}

const handleFilter = () => {
    // 车位可视化和表格共用同一组筛选结果。
    resetPage()
}

const resetFilter = () => {
    keyword.value = ''
    statusFilter.value = ''
    resetPage()
}

const switchOwnerParkingMode = (mode: 'mine' | 'available') => {
    ownerParkingMode.value = mode
    showVisitorParking.value = false
    resetFilter()

    // 购买车位通过 query 定位到可购买视图；回到我的车位时移除该 query，避免菜单高亮串位。
    router.replace({
        path: '/parking/list',
        query: mode === 'available'
            ? { parking_view: 'owner', parking_mode: 'available' }
            : { parking_view: 'owner' },
    })
}

const clearLegacyVisitorRoute = () => {
    if (route.query.parking_view !== 'visitor') {
        return
    }

    router.replace({
        path: '/parking/list',
        query: {
            ...route.query,
            parking_view: 'owner',
        },
    })
}

const showOwnerParking = () => {
    showVisitorParking.value = false
    resetFilter()
    clearLegacyVisitorRoute()
}

const toggleVisitorParking = () => {
    if (isOwner.value) {
        return
    }

    showVisitorParking.value = true
    resetFilter()
    clearLegacyVisitorRoute()
}

const emitParkingFeedback = (parking: ParkingRow) => {
    const feedback = {
        id: Date.now(),
        parking_no: parking.parking_no,
        message: `${parking.owner_name || getStoredUsername() || '业主'} 已成功购买/绑定车位 ${parking.parking_no}，请管理员及时跟进。`,
        created_at: new Date().toLocaleString('zh-CN', { hour12: false }),
    }

    appendMessageFeedback(PARKING_FEEDBACK_STORAGE_KEY, feedback)
    window.dispatchEvent(new CustomEvent(PARKING_FEEDBACK_EVENT, { detail: feedback }))
}

const handleBind = async (row: ParkingRow) => {
    if (!isOwner.value || row.status !== 'idle') {
        return
    }

    await ElMessageBox.confirm(
        `确认购买并绑定车位 ${row.parking_no}？系统会同步反馈给物业管理员。`,
        '购买车位',
        {
            confirmButtonText: '确认购买',
            cancelButtonText: '取消',
            type: 'warning',
        }
    )

    const parkingId = toNumericId(row.id)

    if (!parkingId) {
        ElMessage.error('车位编号异常，无法绑定')
        return
    }

    const res = await bindParking(parkingId)

    if (res.data.code !== 200) {
        ElMessage.error(res.data.msg || '绑定失败')
        return
    }

    emitParkingFeedback(res.data.data || row)
    ElMessage.success(res.data.msg || '车位购买成功，已反馈管理员')
    await loadParkingPageData()
}

const handleEdit = (row: ParkingRow) => {
    router.push(`/parking/edit/${row.id}`)
}

const handleDelete = async (row: ParkingRow) => {
    const parkingId = toNumericId(row.id)

    if (!parkingId) {
        ElMessage.error('车位编号异常，无法删除')
        return
    }

    await deleteParking(parkingId)

    ElMessage.success('删除成功')

    await getList()
}

onMounted(() => {
    ownerParkingMode.value = normalizeOwnerParkingMode(route.query.parking_mode)

    if (!isOwner.value && route.query.parking_view === 'visitor') {
        showVisitorParking.value = true
    }
    clearLegacyVisitorRoute()

    loadParkingPageData()
})

useRealtimeRefresh(loadParkingPageData, {
    scope: ['parking', 'visitors'],
    immediate: false,
    intervalMs: 30000,
})

watch(
    () => [route.query.parking_view, route.query.parking_mode],
    ([parkingViewQuery, parkingModeQuery]) => {
        ownerParkingMode.value = normalizeOwnerParkingMode(parkingModeQuery)

        if (!isOwner.value && parkingViewQuery === 'visitor') {
            showVisitorParking.value = true
        }
        clearLegacyVisitorRoute()

        resetPage()
    }
)
</script>

<template>
    <el-card class="parking-page-card">
        <template #header>
            <div class="card-header">
                <span>车位信息</span>
                <el-button type="primary" link @click="loadParkingPageData">刷新</el-button>
            </div>
        </template>

        <div
            class="parking-dashboard"
            :class="{
                'owner-dashboard': isOwner,
                'visitor-dashboard': showVisitorParking && !isOwner,
            }"
        >
            <button
                type="button"
                class="parking-summary-card"
                :class="{ active: !showVisitorParking && (!isOwner || ownerParkingMode === 'mine') }"
                @click="isOwner ? switchOwnerParkingMode('mine') : showOwnerParking()"
            >
                <span>{{ isOwner ? '我的车位' : '业主车位' }}</span>
                <strong>{{ isOwner ? parkingSummary.total : parkingSummary.owner }}</strong>
                <small>{{ isOwner ? '当前登录用户名下车位' : '已绑定车位' }}</small>
            </button>
            <button
                v-if="!isOwner"
                type="button"
                class="parking-summary-card"
                :class="{ active: showVisitorParking }"
                @click="toggleVisitorParking"
            >
                <span>访客临停</span>
                <strong>{{ parkingSummary.visitor }}</strong>
                <small>访客预约/临停车位</small>
            </button>
            <button
                v-if="isOwner"
                type="button"
                class="parking-summary-card"
                :class="{ active: ownerParkingMode === 'available' }"
                @click="switchOwnerParkingMode('available')"
            >
                <span>可购买车位</span>
                <strong>{{ parkingSummary.available }}</strong>
                <small>售卖区空闲车位</small>
            </button>
            <div v-else-if="!showVisitorParking" class="parking-summary-card">
                <span>空闲车位</span>
                <strong>{{ parkingSummary.idle }}</strong>
                <small>含售卖区和普通临停区</small>
            </div>
            <div v-if="!isOwner && !showVisitorParking" class="parking-summary-card">
                <span>车位总数</span>
                <strong>{{ parkingSummary.total }}</strong>
                <small>{{ isOwner ? '仅统计当前用户车位' : '不含访客临停记录' }}</small>
            </div>
        </div>

        <template v-if="showVisitorParking && !isOwner">
            <section class="visitor-parking-panel">
                <div class="visual-header">
                    <span>访客临停记录</span>
                    <small>访客车位与业主购买车位分开管理，避免占用业主产权/租赁车位。</small>
                </div>

                <el-table :data="visitorParkingRows" border empty-text="暂无访客临停记录">
                    <el-table-column prop="parking_no" label="临停车位" />
                    <el-table-column prop="visitor_name" label="访客" />
                    <el-table-column prop="phone" label="访客手机号" />
                    <el-table-column prop="owner_name" label="被访业主" />
                    <el-table-column prop="room_no" label="被访房屋" />
                    <el-table-column prop="entry_time" label="入场时间" />
                    <el-table-column prop="leave_time" label="预计离场" />
                    <el-table-column label="状态">
                        <template #default="scope">
                            <el-tag :type="scope.row.status_text === '临停中' ? 'warning' : 'success'">
                                {{ scope.row.status_text }}
                            </el-tag>
                        </template>
                    </el-table-column>
                </el-table>
            </section>
        </template>

        <template v-else>
            <div class="list-toolbar">
                <el-input
                    v-model="keyword"
                    clearable
                    :placeholder="ownerParkingMode === 'available' ? '售卖车位号/分区' : '车位号/分区/房屋'"
                    style="width: 280px"
                    @keyup.enter="handleFilter"
                    @clear="handleFilter"
                />
                <el-select
                    v-if="!isOwner || ownerParkingMode !== 'available'"
                    v-model="statusFilter"
                    clearable
                    placeholder="车位状态"
                    style="width: 130px"
                >
                    <el-option label="空闲" value="idle" />
                    <el-option label="使用中" value="used" />
                </el-select>
                <el-button type="primary" @click="handleFilter">筛选</el-button>
                <el-button @click="resetFilter">重置</el-button>
            </div>

            <div class="parking-visual">
                <div class="visual-header">
                    <span>{{ isOwner && ownerParkingMode === 'available' ? '售卖车位分区' : isOwner ? '我的车位分区' : '业主车位分区' }}</span>
                </div>

                <div class="zone-grid">
                    <section v-for="zone in zoneList" :key="zone.zone" class="zone-card">
                        <div class="zone-title">
                            <span>{{ parkingZoneText(zone.zone) }}</span>
                            <small>空闲 {{ zone.idleCount }} / 使用 {{ zone.usedCount }}</small>
                        </div>

                        <div class="parking-grid">
                            <button
                                v-for="item in zone.items"
                                :key="item.id"
                                type="button"
                                class="parking-slot"
                                :class="{ idle: item.status === 'idle', used: item.status === 'used' }"
                                :disabled="!isOwner || ownerParkingMode !== 'available' || item.status !== 'idle'"
                                @click="handleBind(item)"
                            >
                                <span>{{ parkingNoText(item.parking_no) }}</span>
                                <small>
                                    {{ ownerParkingMode === 'available' && item.status === 'idle' ? '点击购买' : statusLabel(item.status) }}
                                </small>
                            </button>
                        </div>
                    </section>
                </div>
            </div>

            <el-table
                v-if="!isOwner || ownerParkingMode !== 'available'"
                :data="pagedTableData"
                border
            >
                <el-table-column prop="id" label="ID" />

                <el-table-column label="车位号">
                    <template #default="scope">
                        {{ parkingNoText(scope.row.parking_no) }}
                    </template>
                </el-table-column>

                <el-table-column label="分区">
                    <template #default="scope">
                        {{ parkingZoneText(scope.row.zone) }}
                    </template>
                </el-table-column>

                <el-table-column prop="owner_name" label="业主" />

                <el-table-column prop="room_no" label="房屋" />

                <el-table-column prop="area" label="面积" />

                <el-table-column label="状态">
                    <template #default="scope">
                        <el-tag :type="scope.row.status === 'idle' ? 'success' : 'info'">
                            {{ ownerParkingStatusText(scope.row) }}
                        </el-tag>
                    </template>
                </el-table-column>

                <el-table-column v-if="!isOwner" label="操作" width="200">
                    <template #default="scope">
                        <el-button v-if="!isOwner" type="primary" size="small" @click="handleEdit(scope.row)">
                            编辑
                        </el-button>

                        <el-button v-if="!isOwner" type="danger" size="small" @click="handleDelete(scope.row)">
                            删除
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>

            <DataPagination
                v-if="!(isOwner && ownerParkingMode === 'available')"
                v-model:current-page="page"
                v-model:page-size="pageSize"
                :page-sizes="[5, 10, 20, 50]"
                :total="total"
                background
                layout="total, sizes, prev, pager, next, jumper"
            />
        </template>

    </el-card>
</template>

<style scoped>
.parking-dashboard {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 12px;
    margin-bottom: 14px;
}

.parking-dashboard.owner-dashboard {
    grid-template-columns: repeat(2, minmax(0, 1fr));
}

.parking-dashboard.visitor-dashboard {
    grid-template-columns: repeat(2, minmax(0, 1fr));
}

.parking-summary-card {
    min-height: 92px;
    padding: 14px 16px;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    color: var(--text-primary);
    background: var(--surface-card);
    text-align: left;
}

button.parking-summary-card {
    cursor: pointer;
}

.parking-summary-card.active {
    border-color: var(--brand-primary);
    background: var(--brand-primary-soft);
}

.parking-summary-card span,
.parking-summary-card small {
    display: block;
}

.parking-summary-card strong {
    display: block;
    margin: 8px 0 4px;
    color: var(--brand-primary);
    font-size: 28px;
    line-height: 36px;
}

.parking-summary-card small {
    color: var(--text-muted);
}

.parking-visual {
    margin-bottom: 16px;
    padding: 16px;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    background: var(--surface-card);
}

.visitor-parking-panel {
    margin-top: 16px;
    margin-bottom: 16px;
    padding: 16px;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    background: var(--surface-card);
}

.visual-header,
.zone-title {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.visual-header {
    margin-bottom: 12px;
    color: var(--text-heading);
    font-size: 15px;
    font-weight: 600;
    line-height: 22px;
}

.zone-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 12px;
}

.zone-card {
    padding: 12px;
    border: 1px solid var(--border-soft);
    border-radius: 6px;
    background: var(--surface-muted);
}

.zone-title {
    margin-bottom: 10px;
    font-weight: 600;
}

.zone-title small {
    color: var(--text-muted);
    font-weight: 400;
}

.parking-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(72px, 1fr));
    gap: 8px;
}

.parking-slot {
    min-height: 56px;
    display: grid;
    place-items: center;
    gap: 2px;
    border: 1px solid #d8e6d8;
    border-radius: 6px;
    background: #f0f9eb;
    color: #1f7a1f;
    cursor: pointer;
}

.parking-slot.used {
    border-color: #e5eaf2;
    background: #eef2f7;
    color: #64748b;
    cursor: default;
}

.parking-slot:disabled {
    cursor: default;
}

.parking-slot span {
    font-weight: 700;
}

.parking-slot small {
    font-size: 12px;
}

@media (max-width: 1200px) {
    .parking-dashboard {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .parking-dashboard.owner-dashboard {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .parking-dashboard.visitor-dashboard {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}
</style>
