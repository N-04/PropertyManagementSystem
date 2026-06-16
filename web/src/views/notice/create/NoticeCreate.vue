<!-- 文件说明：实现 src/views/notice/create/NoticeCreate.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { createNotice } from '@/api/notice'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const role = localStorage.getItem('role') || ''
const canPublishNotice = computed(() => {
    // 业主只接收公告，客服无公告业务；发布入口仅开放给管理、财务和维修角色。
    return [
        'admin',
        'super_admin',
        'property_admin',
        'finance_staff',
        'finance',
        'repair_staff',
        'repairer',
        'repair',
    ].includes(role)
})

const form = ref({
    title: '',
    content: '',
    status: 'published',
})

const submitForm = async () => {
    if (!canPublishNotice.value) {
        ElMessage.warning('当前角色不能发布公告')
        return
    }

    await createNotice(form.value)

    ElMessage.success('新增成功')

    form.value = {
        title: '',
        content: '',
        status: 'published',
    }
    router.push('/notice/list')
}

onMounted(() => {
    if (!canPublishNotice.value) {
        router.replace('/notice/list')
    }
})
</script>

<template>
    <el-card>
        <template #header>
            <span>新增公告</span>
        </template>

        <el-form :model="form" label-width="120px" style="max-width: 600px">
            <el-form-item label="标题">
                <el-input v-model="form.title" />
            </el-form-item>

            <el-form-item label="内容">
                <el-input v-model="form.content" type="textarea" />
            </el-form-item>

            <el-form-item label="状态">
                <el-select v-model="form.status" placeholder="请选择状态">
                    <el-option label="已发布" value="published" />
                    <el-option label="草稿" value="draft" />
                </el-select>
            </el-form-item>

            <el-form-item>
                <el-button type="primary" @click="submitForm">提交</el-button>
            </el-form-item>
        </el-form>
    </el-card>
</template>
