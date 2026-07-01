<!-- 文件说明：实现 src/views/upload/UploadTest.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { ref } from 'vue'
import { toMediaURL } from '@/utils/url'
import Upload from './Upload.vue'

const imageUrl = ref('')

const handleUploadSuccess = (url: string) => {
    imageUrl.value = url
}
</script>

<template>
    <el-card>
        <Upload @success="handleUploadSuccess" />

        <br />

        <img v-if="imageUrl" :src="toMediaURL(imageUrl)" width="300" />
    </el-card>
</template>
