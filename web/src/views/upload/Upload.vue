<!-- 文件说明：实现 src/views/upload/Upload.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { computed, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { uploadFile } from '@/api/upload'

const emit = defineEmits(['success'])

const props = withDefaults(
    defineProps<{
        uploadType?: string
        buttonText?: string
    }>(),
    {
        uploadType: 'file',
        buttonText: '上传文件',
    }
)

const uploading = ref(false)

// 图片上传类型限制选择器文件类型，普通文件上传保留默认选择能力。
const accept = computed(() => {
    const imageTypes = ['avatar', 'id_card', 'repair_image', 'image']

    return imageTypes.includes(props.uploadType) ? 'image/*' : undefined
})

const handleUpload = async (options: any) => {
    // 使用项目 axios 实例上传，统一携带 JWT、自动刷新 token 和后端错误提示。
    const formData = new FormData()
    formData.append('file', options.file)
    formData.append('type', props.uploadType)

    uploading.value = true

    try {
        const res = await uploadFile(formData)
        const url = res.data?.data?.url

        if (res.data?.code !== 200 || !url) {
            throw new Error(res.data?.msg || '上传失败')
        }

        ElMessage.success('上传成功')
        emit('success', url)
        options.onSuccess?.(res.data, options.file)
    } catch (error: any) {
        ElMessage.error(error?.response?.data?.msg || error?.message || '上传失败')
        options.onError?.(error)
    } finally {
        uploading.value = false
    }
}
</script>

<template>
    <el-upload
        class="upload-trigger"
        action="#"
        :accept="accept"
        :disabled="uploading"
        :http-request="handleUpload"
        :show-file-list="false"
    >
        <el-button type="primary" :loading="uploading">{{ props.buttonText }}</el-button>
    </el-upload>
</template>

<style scoped>
.upload-trigger,
.upload-trigger :deep(.el-upload) {
    display: inline-flex;
    align-items: center;
}
</style>
