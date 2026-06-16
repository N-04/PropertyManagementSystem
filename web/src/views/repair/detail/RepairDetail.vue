<!-- 文件说明：实现 src/views/repair/detail/RepairDetail.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getRepairDetail } from '@/api/repair'

const route = useRoute()
const detail = ref<any>({})
const loading = ref(false)
const loadRepairDetail = async () => {
    const id = Number(route.params.id)

    console.log(id)
    const res = await getRepairDetail(id)

    detail.value = res.data.data
}

// 优化状态显示

/**

 * 获取状态 Tag 类型

 */

const getStatusType = (status: string) => {
    switch (status) {
        case 'pending':
            return 'warning'

        case 'assigned':
            return 'warning'

        case 'accepted':
            return 'info'

        case 'processing':
            return 'primary'

        case 'finished':
            return 'success'

        default:
            return ''
    }
}

/**
 * 获取状态文字
 */
const getStatusText = (status: string) => {
    switch (status) {
        case 'pending':
            return '待派单'

        case 'assigned':
            return '待接单'

        case 'accepted':
            return '已接单'

        case 'processing':
            return '维修中'

        case 'finished':
            return '已完成'

        default:
            return '-'
    }
}

const getFileUrl = (url: string) => {
    if (!url) {
        return ''
    }

    return url.startsWith('http') ? url : `http://127.0.0.1:8000${url}`
}

onMounted(() => {
    loadRepairDetail()
})
</script>

<template>
    <el-card v-loading="loading">
        <template #header>
            <div style="display: flex; justify-content: space-between; align-items: center">
                <span>维修详情</span>

                <el-button @click="$router.back()"> 返回 </el-button>
            </div>
        </template>

        <el-descriptions border :column="2">
            <el-descriptions-item label="ID">
                {{ detail.id }}
            </el-descriptions-item>

            <el-descriptions-item label="报修标题">
                {{ detail.title }}
            </el-descriptions-item>

            <el-descriptions-item label="报修内容">
                {{ detail.content }}
            </el-descriptions-item>

            <el-descriptions-item label="报修业主">
                {{ detail.owner_name }}
            </el-descriptions-item>

            <el-descriptions-item label="联系电话">
                {{ detail.phone }}
            </el-descriptions-item>

            <el-descriptions-item label="维修人员">
                {{ detail.repair_user_name?.join('、') || '-' }}
            </el-descriptions-item>

            <el-descriptions-item label="维修状态">
                <el-tag :type="getStatusType(detail.status)">
                    {{ getStatusText(detail.status) }}
                </el-tag>
            </el-descriptions-item>

            <el-descriptions-item label="创建时间">
                {{ detail.created_at }}
            </el-descriptions-item>

            <el-descriptions-item label="完成时间">
                {{ detail.finish_time || '未完成' }}
            </el-descriptions-item>

            <el-descriptions-item label="维修结果" :span="2">
                {{ detail.repair_result || '-' }}
            </el-descriptions-item>

            <el-descriptions-item label="维修评分">
                <el-rate
                    v-if="detail.evaluation_score"
                    :model-value="Number(detail.evaluation_score)"
                    allow-half
                    disabled
                    show-score
                    text-color="#ff9900"
                    score-template="{value} 分"
                />
                <span v-else>-</span>
            </el-descriptions-item>

            <el-descriptions-item label="评价时间">
                {{ detail.evaluation_time || '-' }}
            </el-descriptions-item>

            <el-descriptions-item label="维修评价" :span="2">
                {{ detail.evaluation_content || '-' }}
            </el-descriptions-item>

            <el-descriptions-item label="报修图片" :span="2">
                <div v-if="detail.repair_image_list?.length" class="image-list">
                    <el-image
                        v-for="image in detail.repair_image_list"
                        :key="image"
                        :src="getFileUrl(image)"
                        :preview-src-list="detail.repair_image_list.map(getFileUrl)"
                        fit="cover"
                    />
                </div>
                <span v-else>-</span>
            </el-descriptions-item>

            <el-descriptions-item label="维修结果图片" :span="2">
                <div v-if="detail.result_image_list?.length" class="image-list">
                    <el-image
                        v-for="image in detail.result_image_list"
                        :key="image"
                        :src="getFileUrl(image)"
                        :preview-src-list="detail.result_image_list.map(getFileUrl)"
                        fit="cover"
                    />
                </div>
                <span v-else>-</span>
            </el-descriptions-item>
        </el-descriptions>
    </el-card>
</template>

<style scoped>
.image-list {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}

.image-list :deep(.el-image) {
    width: 120px;
    height: 90px;
    border-radius: 4px;
    border: 1px solid #ebeef5;
}
</style>
