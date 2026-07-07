<!-- 文件说明：实现 src/views/repair/create/RepairCreate.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { createRepair } from '@/api/repair'
import { toMediaURL } from '@/utils/url'
import Upload from '@/views/upload/Upload.vue'
const router = useRouter()

// 表单状态分块：报修图片只存后端返回路径，提交时再拼成接口约定格式。
const form = reactive({
    title: '',
    content: '',
    repairImages: [] as string[],
})

// 提交分块：新增报修要求标题和内容齐全，图片作为可选附件上传。
const submit = async () => {
    if (!form.title || !form.content) {
        ElMessage.warning('请填写报修标题和内容')
        return
    }

    await createRepair({
        title: form.title,
        content: form.content,
        repair_images: form.repairImages.join('|'),
    })
    ElMessage.success('新增成功')
    router.push('/repair/list')
}

// 图片预览分块：后端可能返回相对路径，统一转换成可访问媒体地址。
const getFileUrl = (url: string) => {
    if (!url) {
        return ''
    }

    return toMediaURL(url)
}

// 上传回调分块：上传组件只负责返回路径，当前页维护图片列表顺序。
const addRepairImage = (url: string) => {
    form.repairImages.push(url)
}

const removeRepairImage = (index: number) => {
    form.repairImages.splice(index, 1)
}
</script>

<template>
    <div class="page">
        <el-card>
            <template #header>
                <span>新增报修</span>
            </template>

            <!-- 表单分块：报修信息、图片附件和提交操作在同一张卡片内完成。 -->
            <el-form :model="form" label-width="100px">
                <el-form-item label="报修标题">
                    <el-input v-model="form.title" />
                </el-form-item>

                <el-form-item label="报修内容">
                    <el-input v-model="form.content" type="textarea" :rows="4" />
                </el-form-item>

                <el-form-item label="报修图片">
                    <Upload upload-type="repair_image" @success="addRepairImage" />

                    <div v-if="form.repairImages.length" class="image-list">
                        <div
                            v-for="(image, index) in form.repairImages"
                            :key="image"
                            class="image-item"
                        >
                            <el-image
                                :src="getFileUrl(image)"
                                :preview-src-list="form.repairImages.map(getFileUrl)"
                                fit="cover"
                            />
                            <el-button type="danger" link @click="removeRepairImage(index)">
                                删除
                            </el-button>
                        </div>
                    </div>
                </el-form-item>

                <el-form-item>
                    <el-button type="primary" @click="submit"> 提交 </el-button>
                </el-form-item>
            </el-form>
        </el-card>
    </div>
</template>

<style scoped>
.page {
    padding: 20px;
}

.image-list {
    display: flex;
    gap: 12px;
    margin-top: 12px;
    flex-wrap: wrap;
}

.image-item {
    width: 96px;
}

.image-item :deep(.el-image) {
    width: 96px;
    height: 72px;
    border-radius: 4px;
    border: 1px solid #ebeef5;
}
</style>
