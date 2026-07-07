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

// 提交分块：业主端先做最小必填校验，再交给后端生成投诉/建议记录。
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

        <!-- 表单分块：投诉和建议共用同一套标题、电话和内容字段。 -->
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
                <!-- 操作分块：提交后回列表，查看进度按钮用于快速返回处理状态页。 -->
                <el-button type="primary" :loading="loading" @click="handleSubmit">
                    提交
                </el-button>
                <el-button @click="router.push('/complaint/list')">查看进度</el-button>
            </el-form-item>
        </el-form>
    </el-card>
</template>
