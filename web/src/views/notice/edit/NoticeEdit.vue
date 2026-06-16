<!-- 文件说明：实现 src/views/notice/edit/NoticeEdit.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
// =====================================================
// 导入
// =====================================================

// vue
import { reactive, onMounted } from 'vue'

// API
import { getNoticeDetail, updateNotice } from '@/api/notice'

import { useRoute } from 'vue-router'

import { useRouter } from 'vue-router'

import { ElMessage } from 'element-plus'

// =====================================================
// 路由对象
// =====================================================

const router = useRouter()

const route = useRoute()
// =====================================================
// 表单数据
// =====================================================

const form = reactive({
    // 公告标题
    title: '',

    // 公告内容
    content: '',
})

// =====================================================
// 获取公告详情
// =====================================================

const getDetail = async () => {
    // 调用详情接口
    const res = await getNoticeDetail(Number(route.params.id))

    // 回填数据
    form.title = res.data.data.title

    form.content = res.data.data.content
}

// =====================================================
// 保存修改
// =====================================================

const handleSubmit = async () => {
    // 调用修改接口
    const res = await updateNotice(
        // 公告ID
        Number(route.params.id),

        // 表单数据
        form
    )

    // 打印结果
    console.log(res.data)

    // 提示成功
    ElMessage.success('修改成功')
    router.push('/notice/list')
}

// =====================================================
// 页面加载
// =====================================================

onMounted(() => {
    // 获取详情
    getDetail()
})
</script>

<template>
    <div class="page-container">
        <el-card>
            <!-- 标题 -->
            <template #header>
                <span>编辑公告</span>
            </template>

            <!-- 表单 -->
            <el-form label-width="100px">
                <!-- 公告标题 -->
                <el-form-item label="公告标题">
                    <el-input v-model="form.title" />
                </el-form-item>

                <!-- 公告内容 -->
                <el-form-item label="公告内容">
                    <el-input v-model="form.content" type="textarea" />
                </el-form-item>

                <!-- 按钮 -->
                <el-form-item>
                    <el-button type="primary" @click="handleSubmit"> 保存 </el-button>
                </el-form-item>
            </el-form>
        </el-card>
    </div>
</template>
