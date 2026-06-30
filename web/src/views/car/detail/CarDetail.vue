<!-- 文件说明：实现 src/views/car/detail/CarDetail.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getCarDetail } from '@/api/car'

const route = useRoute()

const detail = ref<any>({})

/**
 * 获取详情
 */
const loading = ref(false)

const loadDetail = async () => {
    loading.value = true

    try {
        const res = await getCarDetail(Number(route.params.id))

        detail.value = res.data.data
    } finally {
        loading.value = false
    }
}

const formatDate = (value: string) => {
    if (!value) return ''

    return value.replace('T', ' ').substring(0, 19)
}

// 详情页兼容后端展示字段和原始枚举值，避免车辆类型为空。
const getCarTypeText = (row: any) => {
    const carTypeMap: Record<string, string> = {
        monthly: '月租车',
        temporary: '临时车',
    }

    return row.car_type_text || carTypeMap[row.car_type] || '-'
}

onMounted(() => {
    loadDetail()
})
</script>

<template>
    <el-card v-loading="loading">
        <template #header>
            <div class="card-header">
                <span>车辆详情</span>

                <el-button @click="$router.back()"> 返回 </el-button>
            </div>
        </template>

        <el-descriptions border :column="2">
            <el-descriptions-item label="ID">
                {{ detail.id }}
            </el-descriptions-item>

            <el-descriptions-item label="车牌号">
                {{ detail.plate_no }}
            </el-descriptions-item>

            <el-descriptions-item label="所属业主">
                {{ detail.owner_name }}
            </el-descriptions-item>

            <el-descriptions-item label="车辆品牌">
                {{ detail.brand }}
            </el-descriptions-item>

            <el-descriptions-item label="车辆颜色">
                {{ detail.color }}
            </el-descriptions-item>

            <el-descriptions-item label="车辆类型">
                {{ getCarTypeText(detail) }}
            </el-descriptions-item>

            <el-descriptions-item label="车位">
                {{ detail.parking_no }}
            </el-descriptions-item>

            <el-descriptions-item label="车辆状态">
                <el-tag :type="detail.status === 'normal' ? 'success' : 'danger'">
                    {{ detail.status === 'normal' ? '正常' : '禁用' }}
                </el-tag>
            </el-descriptions-item>

            <el-descriptions-item label="创建时间">
                {{ formatDate(detail.created_at) }}
            </el-descriptions-item>
        </el-descriptions>
    </el-card>
</template>
