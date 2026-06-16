<!-- 文件说明：实现 src/views/parking/list/ParkingList.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { bindParking, getParkingList } from '@/api/parking'
import { useRouter } from 'vue-router'
import { deleteParking } from '@/api/parking'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useClientPagination } from '@/composables/useClientPagination'
import DataPagination from '@/components/common/DataPagination.vue'

const tableData = ref<any[]>([])
const role = localStorage.getItem('role') || ''
const isOwner = computed(() => role === 'owner')
const {
    page,
    pageSize,
    total,
    pagedData: pagedTableData,
    resetPage,
} = useClientPagination(tableData)

const router = useRouter()

const zoneList = computed(() => {
    const zoneMap = new Map<string, any[]>()

    tableData.value.forEach((item) => {
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

const statusLabel = (status: string) => {
    return status === 'idle' ? '空闲' : '使用中'
}

const getList = async () => {
    // 可视化分区需要拿到足够多的车位，再由前端分页控制表格显示。
    const res = await getParkingList(isOwner.value ? { include_idle: 1, page_size: 1000 } : { page_size: 1000 })

    tableData.value = res.data.data
    resetPage()
}

const handleBind = async (row: any) => {
    if (!isOwner.value || row.status !== 'idle') {
        return
    }

    await ElMessageBox.confirm(
        `确认选择并绑定车位 ${row.parking_no}？`,
        '选择车位',
        {
            confirmButtonText: '确认绑定',
            cancelButtonText: '取消',
            type: 'warning',
        }
    )

    const res = await bindParking(row.id)

    if (res.data.code !== 200) {
        ElMessage.error(res.data.msg || '绑定失败')
        return
    }

    ElMessage.success('绑定成功')
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
    getList()
})
</script>

<template>
    <div class="parking-visual">
        <div class="visual-header">
            <span>车位分区</span>
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
                        <small>{{ statusLabel(item.status) }}</small>
                    </button>
                </div>
            </section>
        </div>
    </div>

    <el-table :data="pagedTableData" border>
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
                    选择
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
.parking-visual {
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
</style>
