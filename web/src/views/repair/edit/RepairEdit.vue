<!-- 文件说明：实现 src/views/repair/edit/RepairEdit.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getRepairDetail, updateRepair } from '@/api/repair'
import { toMediaURL } from '@/utils/url'
import Upload from '@/views/upload/Upload.vue'

const route = useRoute()
const router = useRouter()

const id = Number(route.params.id)
// 表单状态分块：编辑页先使用空结构占位，详情加载后合并真实数据。
const form = ref({
    title: '',
    content: '',
    phone: '',
    repairImages: [] as string[],
})

// 提交分块：编辑接口只提交允许业主修改的字段和图片列表。
const submit = async () => {
    await updateRepair(id, {
        title: form.value.title,
        content: form.value.content,
        repair_images: form.value.repairImages.join('|'),
    })

    ElMessage.success('修改成功')

    router.push('/repair/list')
}

onMounted(async () => {
    // 详情加载分块：兼容后端拆好的 repair_image_list，便于前端直接预览。
    const res = await getRepairDetail(id)

    form.value = {
        ...form.value,
        ...res.data.data,
        repairImages: res.data.data.repair_image_list || [],
    }
})

// 图片预览分块：统一把媒体路径转换成浏览器可打开的地址。
const getFileUrl = (url: string) => {
    if (!url) {
        return ''
    }

    return toMediaURL(url)
}

// 上传回调分块：新增和删除都只维护本地列表，保存时一次性提交。
const addRepairImage = (url: string) => {
    form.value.repairImages.push(url)
}

const removeRepairImage = (index: number) => {
    form.value.repairImages.splice(index, 1)
}
</script>

<template>
    <el-card>
        <template #header>编辑报修</template>

        <!-- 表单分块：编辑基础报修信息，联系电话只展示不允许修改。 -->
        <el-form label-width="100px">
            <el-form-item label="报修标题">
                <el-input v-model="form.title" />
            </el-form-item>

            <el-form-item label="报修内容">
                <el-input v-model="form.content" type="textarea" :rows="4" />
            </el-form-item>

            <el-form-item label="联系电话">
                <el-input v-model="form.phone" disabled />
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
                <el-button type="primary" @click="submit">保存</el-button>
                <el-button @click="router.back()">返回</el-button>
            </el-form-item>
        </el-form>
    </el-card>
</template>

<style scoped>
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
