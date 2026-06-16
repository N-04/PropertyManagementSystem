<!-- 文件说明：实现 src/views/visitor/detail/VisitorDetail.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getVisitorDetail } from '@/api/visitor'

const route = useRoute()

const detail = ref<any>({})

/**
 * 获取详情
 */
const loading = ref(false)

// 优化状态显示

/**

 * 获取状态 Tag 类型

 */

const getStatusType = (status: string) => {
    switch (status) {
        case 'waiting':
            return 'warning'

        case 'approved':
            return 'success'

        case 'rejected':
            return 'danger'

        case 'entered':
            return 'primary'

        case 'left':
            return 'info'

        default:
            return ''
    }
}

/**
 * 获取状态文字
 */
const getStatusText = (status: string) => {
    switch (status) {
        case 'waiting':
            return '待审核'

        case 'approved':
            return '已通过'

        case 'rejected':
            return '已拒绝'

        case 'entered':
            return '已到访'

        case 'left':
            return '已离开'

        default:
            return '-'
    }
}
// 身份证号隐藏
const hideIdCard = (id: string) => {
    if (!id) return ''

    return id.substring(0, 6) + '********' + id.substring(id.length - 4)
}

const loadDetail = async () => {
    loading.value = true

    try {
        const res = await getVisitorDetail(Number(route.params.id))

        detail.value = res.data.data
    } finally {
        loading.value = false
    }
}

const formatDate = (value: string) => {
    if (!value) return ''

    return value.replace('T', ' ').substring(0, 19)
}

onMounted(() => {
    loadDetail()
})
</script>

<template>
    <el-card v-loading="loading">
        <template #header>
            <div style="display: flex; justify-content: space-between; align-items: center">
                <span>访客详情</span>

                <el-button @click="$router.back()"> 返回 </el-button>
            </div>
        </template>
        <el-descriptions border :column="2">
            <el-descriptions-item label="ID">
                {{ detail.id }}
            </el-descriptions-item>

            <el-descriptions-item label="访客姓名">
                {{ detail.name }}
            </el-descriptions-item>

            <el-descriptions-item label="手机号">
                {{ detail.phone }}
            </el-descriptions-item>

            <el-descriptions-item label="身份证号">
                {{ hideIdCard(detail.id_card) }}
            </el-descriptions-item>

            <el-descriptions-item label="被访业主">
                {{ detail.owner_name }}
            </el-descriptions-item>

            <el-descriptions-item label="来访事由">
                {{ detail.reason }}
            </el-descriptions-item>

            <el-descriptions-item label="来访时间">
                {{ detail.visit_time }}
            </el-descriptions-item>

            <el-descriptions-item label="到访时间">
                {{ detail.enter_time || '-' }}
            </el-descriptions-item>

            <el-descriptions-item label="离开时间">
                {{ detail.leave_time || '未离开' }}
            </el-descriptions-item>

            <el-descriptions-item label="状态">
                <el-tag :type="getStatusType(detail.status)">
                    {{ getStatusText(detail.status) }}
                </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="审批时间">
                {{ detail.approve_time || '未审批' }}
            </el-descriptions-item>

            <el-descriptions-item label="审批人">
                {{ detail.approve_user_name || '暂无' }}
            </el-descriptions-item>

            <el-descriptions-item label="审批备注">
                {{ detail.approve_remark || '无' }}
            </el-descriptions-item>

            <el-descriptions-item label="创建时间">
                {{ formatDate(detail.created_at) }}
            </el-descriptions-item>
        </el-descriptions>
    </el-card>
</template>
