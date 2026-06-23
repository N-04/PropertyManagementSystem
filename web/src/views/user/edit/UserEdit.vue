<!-- 文件说明：实现 src/views/user/edit/UserEdit.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
// 修改用户接口
import { getUserDetail, updateUser } from '@/api/user'

// 获取用户id
const route = useRoute()
const router = useRouter()
const form = reactive({
    username: '',

    real_name: '',

    phone: '',
})
const getDetail = async () => {
    try {
        const res = await getUserDetail(Number(route.params.id))

        form.username = res.data.data.username

        form.real_name = res.data.data.real_name

        form.phone = res.data.data.phone
    } catch (error: any) {
        ElMessage.error(error?.response?.data?.msg || '用户详情加载失败')
    }
}
// =====================================================
// 保存修改
// =====================================================
const handleSubmit = async () => {
    try {
        // 调用修改接口
        const res = await updateUser(
            // 用户ID
            Number(route.params.id),

            // 表单数据
            form
        )

        if (res.data.code !== 200) {
            ElMessage.error(res.data.msg || '保存失败')
            return
        }

        ElMessage.success('保存成功')
        router.push('/user/list')
    } catch (error: any) {
        ElMessage.error(error?.response?.data?.msg || '保存失败')
    }
}

onMounted(() => {
    getDetail()
})
</script>

<template>
    <div class="page-container">
        <el-card>
            <template #header>
                <span>编辑用户</span>
            </template>

            <el-form label-width="100px">
                <el-form-item label="用户名">
                    <el-input v-model="form.username" />
                </el-form-item>

                <el-form-item label="真实姓名">
                    <el-input v-model="form.real_name" />
                </el-form-item>

                <el-form-item label="手机号">
                    <el-input v-model="form.phone" />
                </el-form-item>

                <el-form-item>
                    <!-- 保存按钮 -->
                    <el-button type="primary" @click="handleSubmit"> 保存 </el-button>
                </el-form-item>
            </el-form>
        </el-card>
    </div>
</template>

<style scoped>
.page-container {
    padding: 20px;
}
</style>
