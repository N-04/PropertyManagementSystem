<!-- 文件说明：实现 src/views/visitor/edit/VisitorEdit.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter, useRoute } from 'vue-router'
import { getOwnerList } from '@/api/owner'
import { getVisitorDetail, updateVisitor } from '@/api/visitor'
import { extractListRows } from '@/utils/listResponse'

const router = useRouter()
const route = useRoute()

// 详情加载分块：按路由 id 拉取访客资料并回填表单。
const loadDetail = async () => {
    const res = await getVisitorDetail(Number(route.params.id))

    Object.assign(
        form,

        res.data.data
    )
}
/**
 * 表单
 */
const form = reactive({
    name: '',
    phone: '',
    id_card: '',
    owner: '',
    reason: '',
    status: 'waiting',
})

/**
 * 业主列表
 */
const ownerList = reactive<any[]>([])

/**
 * 获取业主
 */
const loadOwnerList = async () => {
    const res = await getOwnerList()

    // 列表响应兼容分块：统一提取分页或数组接口里的真实行数据。
    ownerList.push(...extractListRows(res.data.data))
}

/**
 * 提交
 */
const submitForm = async () => {
    await updateVisitor(Number(route.params.id), form)

    ElMessage.success('修改成功')

    router.push('/visitor/list')
}

onMounted(() => {
    loadOwnerList()
    loadDetail()
})
</script>

<template>
    <el-card>
        <template #header>
            <span>修改访客信息</span>
        </template>

        <!-- 表单分块：修改访客基础资料、被访业主和来访事由。 -->
        <el-form :model="form" label-width="120px" style="max-width: 700px">
            <el-form-item label="访客姓名">
                <el-input v-model="form.name" />
            </el-form-item>

            <el-form-item label="手机号">
                <el-input v-model="form.phone" />
            </el-form-item>

            <el-form-item label="身份证号">
                <el-input v-model="form.id_card" />
            </el-form-item>

            <el-form-item label="被访业主">
                <el-select v-model="form.owner">
                    <el-option
                        v-for="item in ownerList"
                        :key="item.id"
                        :label="item.name"
                        :value="item.id"
                    />
                </el-select>
            </el-form-item>

            <el-form-item label="来访事由">
                <el-input v-model="form.reason" />
            </el-form-item>

            <el-form-item>
                <el-button type="primary" @click="submitForm"> 提交 </el-button>
            </el-form-item>
        </el-form>
    </el-card>
</template>
