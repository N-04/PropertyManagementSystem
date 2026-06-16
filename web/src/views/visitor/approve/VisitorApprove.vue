<!-- 文件说明：实现 src/views/visitor/approve/VisitorApprove.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

import { getVisitorDetail } from '@/api/visitor'
import { approveVisitor } from '@/api/visitor'



const route = useRoute()
const router = useRouter()

const loading = ref(false)

const detail = ref<any>({})
const status = ref('approved')
const remark = ref('')

/**
 * 获取访客详情
 */
const loadDetail = async () => {
    const res = await getVisitorDetail(Number(route.params.id))

    detail.value = res.data.data
}



/**
 * 提交审批
 */
const submitApprove = async () => {
    await approveVisitor(Number(route.params.id), {
        // 审批结果
        status: status.value,

        // 审批备注
        approve_remark: remark.value,
    })

    ElMessage.success('审批成功')

    router.push('/visitor/list')
}

onMounted(() => {
    loadDetail()
})
</script>

<template>
    <el-card v-loading="loading">
        <el-form label-width="120px">
            <template #header>
                <span>访客审批</span>
            </template>
            <el-form-item label="访客姓名">
                {{ detail.name }}
            </el-form-item>

            <el-form-item label="手机号">
                {{ detail.phone }}
            </el-form-item>

            <el-form-item label="被访业主">
                {{ detail.owner_name }}
            </el-form-item>

            <el-form-item label="来访事由">
                {{ detail.reason }}
            </el-form-item>

            <el-form-item label="来访时间">
                {{ detail.visit_time }}
            </el-form-item>

            <el-form-item label="审批结果">
                <el-radio-group v-model="status">
                    <el-radio label="approved"> 通过 </el-radio>

                    <el-radio label="rejected"> 拒绝 </el-radio>
                </el-radio-group>
            </el-form-item>

            <el-form-item label="审批备注">
                <el-input v-model="remark" type="textarea" :rows="4" />
            </el-form-item>

            <el-form-item>
                <el-button type="primary" @click="submitApprove"> 提交审批 </el-button>

                <el-button @click="router.back()"> 返回 </el-button>
            </el-form-item>


        </el-form>
    </el-card>
</template>
