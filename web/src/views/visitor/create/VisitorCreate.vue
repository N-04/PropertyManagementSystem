<!-- 文件说明：实现 src/views/visitor/create/VisitorCreate.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
// =====================================================
// Vue响应式
// =====================================================
import { reactive } from 'vue'

// =====================================================
// 路由跳转
// =====================================================
import { useRouter } from 'vue-router'
import { onMounted } from 'vue'

// =====================================================
// Element消息提示
// =====================================================
import { ElMessage } from 'element-plus'

// =====================================================
// 创建角色接口
// =====================================================
import { createVisitor } from '@/api/visitor'
// =====================================================
// 获取业主列表接口
// =====================================================
import { getOwnerList } from '@/api/owner'

// =====================================================
// 路由实例
// =====================================================
const router = useRouter()

// 限制只能选择当天日期
const disabledDate = (time: Date) => {
    const today = new Date()

    // 将时间统一重置到凌晨 00:00:00 进行精确的天数对比
    const dateStr = time.toDateString()
    const todayStr = today.toDateString()

    // 如果不是今天，则全部禁用
    return dateStr !== todayStr
}

// =====================================================
// 表单数据
// =====================================================
const form = reactive({
    name: '',
    phone: '',
    id_card: '',
    owner: '',
    reason: '',
    // 默认显示当前日期
    visit_time: formatDateTime(new Date()),
    status: 'waiting',
})

// 辅助函数：格式化当前时间为 YYYY-MM-DD HH:mm:ss
function formatDateTime(date: Date) {
    const pad = (num: number) => String(num).padStart(2, '0')
    return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`
}

const ownerList = reactive<any[]>([])

const loadOwnerList = async () => {
    try {
        const res = await getOwnerList()
        const rows = res.data.data

        ownerList.splice(0, ownerList.length, ...(Array.isArray(rows) ? rows : rows?.results || []))
    } catch (error: any) {
        ElMessage.error(error?.response?.data?.msg || '业主列表加载失败')
    }
}

// =====================================================
// 提交表单
// =====================================================
const handleSubmit = async () => {
    try {
        // 调用新增接口
        const res = await createVisitor(form)

        // 判断是否成功
        if (res.data.code === 200) {
            // 成功提示
            ElMessage.success('创建成功')

            // 跳转列表页
            router.push('/visitor/list')
            return
        }

        // 错误提示
        ElMessage.error(res.data.msg)
    } catch (error: any) {
        ElMessage.error(error?.response?.data?.msg || '创建失败')
    }
}
onMounted(() => {
    loadOwnerList()
})
</script>

<template>
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
        <el-input v-model="form.reason" type="textarea" />
    </el-form-item>

    <el-form-item label="来访时间">
        <el-date-picker
            v-model="form.visit_time"
            type="datetime"
            value-format="YYYY-MM-DD HH:mm:ss"
            placeholder="请选择日期"
            :disabled-date="disabledDate"
        />
    </el-form-item>
    <el-form-item>
        <el-button type="primary" @click="handleSubmit"> 提交 </el-button>
    </el-form-item>
</template>
