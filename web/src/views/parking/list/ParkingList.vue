<!-- 文件说明：实现 src/views/parking/list/ParkingList.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { computed, ref, onMounted, watch } from 'vue'
import { bindParking, getParkingList } from '@/api/parking'
import { getVisitorList } from '@/api/visitor'
import { useRoute, useRouter } from 'vue-router'
import { deleteParking } from '@/api/parking'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useClientPagination } from '@/composables/useClientPagination'
import { useKeywordFilter } from '@/composables/useKeywordFilter'
import DataPagination from '@/components/common/DataPagination.vue'
import { getStoredRole, getStoredUsername } from '@/utils/authState'

const tableData = ref<any[]>([])
const keyword = ref('')
const statusFilter = ref('')
const parkingView = ref<'owner' | 'visitor'>('owner')
const role = getStoredRole()
const isOwner = computed(() => role === 'owner')
const router = useRouter()
const route = useRoute()
const PARKING_FEEDBACK_EVENT = 'property-management-parking-feedback'
const PARKING_FEEDBACK_STORAGE_KEY = 'parkingPurchaseFeedback'

const visitorParkingRows = ref<any[]>([])
const keywordFilteredData = useKeywordFilter(tableData, keyword, [
    'parking_no',
    'zone',
    'owner_name',
    'room_no',
    'status_text',
])
const ownerParkingRows = computed(() => {
    if (!statusFilter.value) {
        return keywordFilteredData.value
    }

    return keywordFilteredData.value.filter((item) => item.status === statusFilter.value)
})

const visitorKeywordFilteredData = useKeywordFilter(visitorParkingRows, keyword, [
    'parking_no',
    'visitor_name',
    'owner_name',
    'room_no',
    'phone',
    'status_text',
])

const filteredTableData = computed(() => {
    return parkingView.value === 'visitor'
        ? visitorKeywordFilteredData.value
        : ownerParkingRows.value
})
const {
    page,
    pageSize,
    total,
    pagedData: pagedTableData,
    resetPage,
} = useClientPagination(filteredTableData)

const zoneList = computed(() => {
    const zoneMap = new Map<string, any[]>()

    ownerParkingRows.value.forEach((item) => {
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
        visitor: visitorParkingRows.value.length,
    }
})

const statusLabel = (status: string) => {
    return status === 'idle' ? '空闲' : '使用中'
}

const visitorStatusText = (status: string) => {
    const statusMap: Record<string, string> = {
        waiting: '待审核',
        approved: '已预约',
        entered: '临停中',
        left: '已离场',
        rejected: '已拒绝',
    }

    return statusMap[status] || status || '-'
}

const buildVisitorParkingNo = (item: any, index: number) => {
    return `V-${String(item.id || index + 1).padStart(4, '0')}`
}

const getList = async () => {
    // 可视化分区需要拿到足够多的车位，再由前端分页控制表格显示。
    const res = await getParkingList(isOwner.value ? { include_idle: 1, page_size: 1000 } : { page_size: 1000 })

    tableData.value = res.data.data
    resetPage()
}

const getVisitorParkingList = async () => {
    try {
        const res = await getVisitorList()
        const visitors = res.data.data || []

        // 访客临停不占用业主已购买/绑定车位，按访客预约记录单独生成临停列表。
        visitorParkingRows.value = visitors.map((item: any, index: number) => ({
            id: item.id,
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

const switchParkingView = (view: 'owner' | 'visitor') => {
    parkingView.value = view
    resetFilter()
    router.replace({
        path: '/parking/list',
        query: {
            ...route.query,
            parking_view: view,
        },
    })
}

const emitParkingFeedback = (parking: any) => {
    const feedback = {
        id: Date.now(),
        parking_no: parking.parking_no,
        message: `${parking.owner_name || getStoredUsername() || '业主'} 已成功购买/绑定车位 ${parking.parking_no}，请管理员及时跟进。`,
        created_at: new Date().toLocaleString('zh-CN', { hour12: false }),
    }

    localStorage.setItem(PARKING_FEEDBACK_STORAGE_KEY, JSON.stringify(feedback))
    window.dispatchEvent(new CustomEvent(PARKING_FEEDBACK_EVENT, { detail: feedback }))
}

const handleBind = async (row: any) => {
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

    const res = await bindParking(row.id)

    if (res.data.code !== 200) {
        ElMessage.error(res.data.msg || '绑定失败')
        return
    }

    emitParkingFeedback(res.data.data || row)
    ElMessage.success(res.data.msg || '车位购买成功，已反馈管理员')
    await getList()
}

const handleEdit = (row: any) => {
    router.push(`/parking/edit/${row.id}`)
}

const handleDelete = async (row: any) => {
    await deleteParking(row.id)

    ElMessage.success('删除成功')

    await getList()
}

onMounted(() => {
    parkingView.value = route.query.parking_view === 'visitor' ? 'visitor' : 'owner'
    loadParkingPageData()
})

watch(
    () => route.query.parking_view,
    (value) => {
        parkingView.value = value === 'visitor' ? 'visitor' : 'owner'
        resetPage()
    }
)
</script>

<template>
    <div class="parking-dashboard">
        <button
            type="button"
            class="parking-summary-card"
            :class="{ active: parkingView === 'owner' }"
            @click="switchParkingView('owner')"
        >
            <span>业主车位</span>
            <strong>{{ parkingSummary.used }}</strong>
            <small>已绑定车位</small>
        </button>
        <button
            type="button"
            class="parking-summary-card"
            :class="{ active: parkingView === 'visitor' }"
            @click="switchParkingView('visitor')"
        >
            <span>访客临停</span>
            <strong>{{ parkingSummary.visitor }}</strong>
            <small>访客预约/临停车位</small>
        </button>
        <div class="parking-summary-card">
            <span>可购买车位</span>
            <strong>{{ parkingSummary.idle }}</strong>
            <small>业主可选择空闲车位</small>
        </div>
        <div class="parking-summary-card">
            <span>车位总数</span>
            <strong>{{ parkingSummary.total }}</strong>
            <small>不含访客临停记录</small>
        </div>
    </div>

    <div class="list-toolbar">
        <el-input
            v-model="keyword"
            clearable
            :placeholder="parkingView === 'visitor' ? '临停车位/访客/手机号/业主/房屋' : '车位号/分区/业主/房屋'"
            style="width: 280px"
            @keyup.enter="handleFilter"
            @clear="handleFilter"
        />
        <el-select
            v-if="parkingView === 'owner'"
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

    <div v-if="parkingView === 'owner'" class="parking-visual">
        <div class="visual-header">
            <span>业主车位分区</span>
            <el-button type="primary" link @click="getList">刷新</el-button>
        </div>

        <div class="zone-grid">
            <section v-for="zone in zoneList" :key="zone.zone" class="zone-card">
                <div class="zone-title">
                    <span>{{ zone.zone }}区</span>
                    <small>空闲 {{ zone.idleCount }} / 使用 {{ zone.usedCount }}</small>
                </div>

                <div class="parking-grid">
                    <button
                        v-for="item in zone.items"
                        :key="item.id"
                        type="button"
                        class="parking-slot"
                        :class="{ idle: item.status === 'idle', used: item.status === 'used' }"
                        :disabled="!isOwner || item.status !== 'idle'"
                        @click="handleBind(item)"
                    >
                        <span>{{ item.parking_no }}</span>
                        <small>{{ item.status === 'idle' && isOwner ? '可购买' : statusLabel(item.status) }}</small>
                    </button>
                </div>
            </section>
        </div>
    </div>

    <div v-else class="visitor-parking-visual">
        <div class="visual-header">
            <span>访客临停记录</span>
            <small>访客车位与业主购买车位分开管理，避免占用业主产权/租赁车位。</small>
        </div>
    </div>

    <el-table v-if="parkingView === 'owner'" :data="pagedTableData" border>
        <el-table-column prop="id" label="ID" />

        <el-table-column prop="parking_no" label="车位号" />

        <el-table-column prop="zone" label="分区" />

        <el-table-column prop="owner_name" label="业主" />

        <el-table-column prop="room_no" label="房屋" />

        <el-table-column prop="area" label="面积" />

        <el-table-column label="状态">
            <template #default="scope">
                <el-tag :type="scope.row.status === 'idle' ? 'success' : 'info'">
                    {{ scope.row.status_text || statusLabel(scope.row.status) }}
                </el-tag>
            </template>
        </el-table-column>

        <el-table-column label="操作" width="200">
            <template #default="scope">
                <el-button
                    v-if="isOwner && scope.row.status === 'idle'"
                    type="success"
                    size="small"
                    @click="handleBind(scope.row)"
                >
                    购买
                </el-button>

                <el-button v-if="!isOwner" type="primary" size="small" @click="handleEdit(scope.row)">
                    编辑
                </el-button>

                <el-button v-if="!isOwner" type="danger" size="small" @click="handleDelete(scope.row)">
                    删除
                </el-button>
            </template>
        </el-table-column>
    </el-table>

    <el-table v-else :data="pagedTableData" border>
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

    <DataPagination
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :page-sizes="[5, 10, 20, 50]"
        :total="total"
        background
        layout="total, sizes, prev, pager, next, jumper"
    />
</template>

<style scoped>
.parking-dashboard {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 12px;
    margin-bottom: 14px;
}

.parking-summary-card {
    min-height: 92px;
    padding: 14px 16px;
    border: 1px solid #e5eaf2;
    border-radius: 8px;
    color: #334155;
    background: #ffffff;
    text-align: left;
}

button.parking-summary-card {
    cursor: pointer;
}

.parking-summary-card.active {
    border-color: #009688;
    background: #e4f5f2;
}

.parking-summary-card span,
.parking-summary-card small {
    display: block;
}

.parking-summary-card strong {
    display: block;
    margin: 8px 0 4px;
    color: #00897b;
    font-size: 28px;
}

.parking-summary-card small {
    color: #64748b;
}

.list-toolbar {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
}

.parking-visual {
    margin-bottom: 16px;
    padding: 16px;
    border: 1px solid #e5eaf2;
    border-radius: 6px;
    background: #ffffff;
}

.visitor-parking-visual {
    margin-bottom: 16px;
    padding: 16px;
    border: 1px solid #e5eaf2;
    border-radius: 6px;
    background: #ffffff;
}

.visual-header,
.zone-title {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.visual-header {
    margin-bottom: 12px;
    font-size: 16px;
    font-weight: 700;
}

.zone-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 12px;
}

.zone-card {
    padding: 12px;
    border: 1px solid #edf1f6;
    border-radius: 6px;
    background: #f8fafc;
}

.zone-title {
    margin-bottom: 10px;
    font-weight: 600;
}

.zone-title small {
    color: #64748b;
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
}
</style>
