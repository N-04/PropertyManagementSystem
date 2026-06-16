<!-- 文件说明：业主提交投诉或建议。 -->
<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { createComplaint } from '@/api/complaint'

const router = useRouter()
const loading = ref(false)

const form = reactive({
    title: '',
    category: 'complaint',
    phone: '',
    content: '',
})

const handleSubmit = async () => {
    if (!form.title || !form.content) {
        ElMessage.warning('请填写标题和内容')
        return
    }

    loading.value = true

    try {
        const res = await createComplaint(form)

        if (res.data.code !== 200) {
            ElMessage.error(res.data.msg || '提交失败')
            return
        }

        ElMessage.success('提交成功')
        router.push('/complaint/list')
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <el-card>
        <template #header>提交投诉/建议</template>

        <el-form label-width="100px">
            <el-form-item label="类型">
                <el-radio-group v-model="form.category">
                    <el-radio-button label="complaint">投诉</el-radio-button>
                    <el-radio-button label="suggestion">建议</el-radio-button>
                </el-radio-group>
            </el-form-item>

            <el-form-item label="标题">
                <el-input v-model="form.title" maxlength="100" show-word-limit />
            </el-form-item>

            <el-form-item label="联系电话">
                <el-input v-model="form.phone" maxlength="20" placeholder="可选，默认使用账号手机号" />
            </el-form-item>

            <el-form-item label="内容">
                <el-input
                    v-model="form.content"
                    type="textarea"
                    :rows="6"
                    placeholder="请描述需要处理的问题或建议"
                />
            </el-form-item>

            <el-form-item>
                <el-button type="primary" :loading="loading" @click="handleSubmit">
                    提交
                </el-button>
                <el-button @click="router.push('/complaint/list')">查看进度</el-button>
            </el-form-item>
        </el-form>
    </el-card>
</template>
