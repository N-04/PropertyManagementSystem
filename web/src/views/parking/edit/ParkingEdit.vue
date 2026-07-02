<!-- 文件说明：实现管理员车位编辑页，负责车位详情回显、基础资料修改和保存跳转。 -->
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getOwnerList } from '@/api/owner'
import { getParkingDetail, updateParking } from '@/api/parking'
import { extractListRows } from '@/utils/listResponse'

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const saving = ref(false)

type OwnerOption = {
    id: number | string
    name?: string
    username?: string
    phone?: string
}

const ownerList = ref<OwnerOption[]>([])
const form = ref({
    owner: '' as string | number,
    parking_no: '',
    area: '',
    status: 'idle',
})

const parkingId = computed(() => Number(route.params.id))

const loadPageData = async () => {
    // 页面初始化分块：业主列表和车位详情并行加载，避免编辑页出现空白。
    if (!Number.isFinite(parkingId.value)) {
        ElMessage.error('车位编号无效')
        router.back()
        return
    }

    loading.value = true

    try {
        const [ownerRes, detailRes] = await Promise.all([
            getOwnerList(),
            getParkingDetail(parkingId.value),
        ])
        const detail = detailRes.data.data || {}

        ownerList.value = extractListRows<OwnerOption>(ownerRes.data.data)
        form.value = {
            owner: detail.owner || '',
            parking_no: detail.parking_no || '',
            area: `${detail.area ?? ''}`,
            status: detail.status || 'idle',
        }
    } finally {
        loading.value = false
    }
}

const buildPayload = () => {
    // 保存前只提交后端可写字段，避免把只读展示字段回传给序列化器。
    const owner = form.value.owner || null

    return {
        owner,
        parking_no: form.value.parking_no.trim(),
        area: form.value.area === '' ? 0 : Number(form.value.area),
        status: owner ? 'used' : form.value.status,
    }
}

const submitForm = async () => {
    if (!form.value.parking_no.trim()) {
        ElMessage.warning('请输入车位号')
        return
    }

    saving.value = true

    try {
        const payload = buildPayload()
        const res = await updateParking(parkingId.value, payload)

        if (res.data.code !== 200) {
            ElMessage.error(res.data.msg || '保存失败')
            return
        }

        ElMessage.success('保存成功')
        router.push('/parking/list')
    } finally {
        saving.value = false
    }
}

onMounted(loadPageData)
</script>

<template>
    <el-card class="parking-edit-card" v-loading="loading">
        <template #header>
            <div class="card-header">
                <span>编辑车位</span>
                <el-button @click="router.back()">返回</el-button>
            </div>
        </template>

        <el-form class="parking-edit-form" label-width="96px">
            <div class="form-grid">
                <el-form-item label="所属业主">
                    <el-select
                        v-model="form.owner"
                        clearable
                        filterable
                        placeholder="请选择业主"
                    >
                        <el-option
                            v-for="item in ownerList"
                            :key="item.id"
                            :label="`${item.name || item.username || '业主'}${item.phone ? `（${item.phone}）` : ''}`"
                            :value="item.id"
                        />
                    </el-select>
                </el-form-item>

                <el-form-item label="车位号">
                    <el-input v-model="form.parking_no" placeholder="请输入车位号，例如 售卖车位-000301" />
                </el-form-item>

                <el-form-item label="面积">
                    <el-input v-model="form.area" placeholder="请输入面积">
                        <template #append>㎡</template>
                    </el-input>
                </el-form-item>

                <el-form-item label="状态">
                    <el-select v-model="form.status" :disabled="Boolean(form.owner)">
                        <el-option label="空闲" value="idle" />
                        <el-option label="使用中" value="used" />
                    </el-select>
                </el-form-item>
            </div>

            <div class="form-hint">
                选择业主后系统会自动将车位状态保存为“使用中”；清空业主后可手动改为空闲。
            </div>

            <div class="form-actions">
                <el-button @click="router.back()">取消</el-button>
                <el-button type="primary" :loading="saving" @click="submitForm">保存</el-button>
            </div>
        </el-form>
    </el-card>
</template>

<style scoped>
.parking-edit-card {
    max-width: 980px;
}

.card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.parking-edit-form {
    max-width: 860px;
}

.form-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    column-gap: 28px;
    row-gap: 6px;
}

.parking-edit-form :deep(.el-select),
.parking-edit-form :deep(.el-input) {
    width: 100%;
}

.form-hint {
    margin: 8px 0 22px 96px;
    color: var(--text-muted);
    font-size: 13px;
    line-height: 20px;
}

.form-actions {
    display: flex;
    justify-content: center;
    gap: 12px;
}

@media (max-width: 1100px) {
    .form-grid {
        grid-template-columns: 1fr;
    }

    .form-hint {
        margin-left: 96px;
    }
}
</style>
