<!-- 文件说明：实现 src/views/user/create/UserCreate.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { createUser } from '@/api/user'

const router = useRouter()

const form = reactive({
    username: '',
    password: '',
    real_name: '',
    phone: '',
    role_ids: [1],
    status: 1,
})

const handleSubmit = async () => {
    const res = await createUser(form)

    console.log(res.data)

    if (res.data.code === 200) {
        ElMessage.success(res.data.msg)
        router.push('/user/list')
    } else {
        ElMessage.error(JSON.stringify(res.data.msg))
    }
}
</script>

<template>
    <div class="page-container">
        <el-card>
            <template #header>
                <span>新增用户</span>
            </template>

            <el-form label-width="100px" @submit.prevent>
                <el-form-item label="用户名">
                    <el-input v-model="form.username" />
                </el-form-item>

                <el-form-item label="密码">
                    <el-input v-model="form.password" type="password" />
                </el-form-item>

                <el-form-item label="真实姓名">
                    <el-input v-model="form.real_name" />
                </el-form-item>

                <el-form-item label="手机号">
                    <el-input v-model="form.phone" />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleSubmit"> 提交 </el-button>
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
