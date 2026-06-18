<!-- 文件说明：实现 src/views/upload/Upload.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { ElMessage } from 'element-plus'

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

const handleSuccess = (response: any) => {
    ElMessage.success('上传成功')

    emit('success', response.data.url)
}
</script>

<template>
    <el-upload
        class="upload-trigger"
        action="http://127.0.0.1:8000/api/upload/"
        :data="{ type: props.uploadType }"
        :show-file-list="false"
        :on-success="handleSuccess"
    >
        <el-button type="primary">{{ props.buttonText }}</el-button>
    </el-upload>
</template>

<style scoped>
.upload-trigger,
.upload-trigger :deep(.el-upload) {
    display: inline-flex;
    align-items: center;
}
</style>
