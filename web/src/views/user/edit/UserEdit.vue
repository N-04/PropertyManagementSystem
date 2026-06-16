<!-- 文件说明：实现 src/views/user/edit/UserEdit.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { useRoute } from 'vue-router'
import { reactive } from 'vue'
import { onMounted } from 'vue'
// 修改用户接口
import { getUserDetail, updateUser } from '@/api/user'

// 获取用户id
const route = useRoute()
console.log(route.params.id)
const form = reactive({
    username: '',

    real_name: '',

    phone: '',
})
const getDetail = async () => {
    const res = await getUserDetail(Number(route.params.id))

    form.username = res.data.data.username

    form.real_name = res.data.data.real_name

    form.phone = res.data.data.phone
}
// =====================================================
// 保存修改
// =====================================================
const handleSubmit = async () => {
    // 调用修改接口
    const res = await updateUser(
        // 用户ID
        Number(route.params.id),

        // 表单数据
        form
    )

    // 打印结果
    console.log(res.data)
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
