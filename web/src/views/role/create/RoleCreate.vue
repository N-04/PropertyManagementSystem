<!-- 文件说明：实现 src/views/role/create/RoleCreate.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
// =====================================================
// Vue响应式
// =====================================================
import { reactive } from 'vue'

// =====================================================
// 路由跳转
// =====================================================
import { useRouter } from 'vue-router'

// =====================================================
// Element消息提示
// =====================================================
import { ElMessage } from 'element-plus'

// =====================================================
// 创建角色接口
// =====================================================
import { createRole } from '@/api/role'

// =====================================================
// 路由实例
// =====================================================
const router = useRouter()

// =====================================================
// 表单数据
// =====================================================
const form = reactive({
    // 角色名称
    name: '',

    // 角色编码
    code: '',
})

// =====================================================
// 提交表单
// =====================================================
const handleSubmit = async () => {
    // 调用新增接口
    const res = await createRole(form)

    // 打印结果
    console.log(res.data)

    // 判断是否成功
    if (res.data.code === 200) {
        // 成功提示
        ElMessage.success('创建成功')

        // 跳转列表页
        router.push('/role/list')
    } else {
        // 错误提示
        ElMessage.error(res.data.msg)
    }
}
</script>

<template>
    <!-- 页面容器 -->
    <div class="page-container">
        <!-- 卡片 -->
        <el-card>
            <!-- 卡片标题 -->
            <template #header>
                <span>新增角色</span>
            </template>

            <!-- 表单 -->
            <el-form label-width="100px">
                <!-- 角色名称 -->
                <el-form-item label="角色名称">
                    <el-input v-model="form.name" />
                </el-form-item>

                <!-- 角色编码 -->
                <el-form-item label="角色编码">
                    <el-input v-model="form.code" />
                </el-form-item>

                <!-- 提交按钮 -->
                <el-form-item>
                    <el-button type="primary" @click="handleSubmit"> 提交 </el-button>
                </el-form-item>
            </el-form>
        </el-card>
    </div>
</template>

<style scoped>
/* 页面容器 */
.page-container {
    padding: 20px;
}
</style>
