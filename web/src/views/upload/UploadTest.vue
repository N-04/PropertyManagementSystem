<!-- 文件说明：实现 src/views/upload/UploadTest.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { ref } from 'vue'
import { toMediaURL } from '@/utils/url'
import Upload from './Upload.vue'

const imageUrl = ref('')

// 上传验证分块：测试页只记录最近一次上传路径，用于快速确认媒体地址可预览。
const handleUploadSuccess = (url: string) => {
    imageUrl.value = url
}
</script>

<template>
    <el-card>
        <!-- 上传组件分块：复用正式上传组件，便于联调文件接口。 -->
        <Upload @success="handleUploadSuccess" />

        <br />

        <!-- 预览分块：上传成功后展示后端返回文件的可访问地址。 -->
        <img v-if="imageUrl" :src="toMediaURL(imageUrl)" width="300" />
    </el-card>
</template>
