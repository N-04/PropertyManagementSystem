<!-- 文件说明：实现 src/views/repair/assign/RepairAssign.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getUserList } from '@/api/user'
import { assignRepair } from '@/api/repair'

import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const loadUser = async () => {
    const res = await getUserList()

    console.log(res)
    console.log(res.data)
    console.log(res.data.data)

    userList.value = res.data.data
}

// 报修ID
const repairId = Number(route.params.id)

// 表单
const form = ref({
    repair_user: [] as number[],
})

const submit = async () => {
    if (form.value.repair_user.length === 0) {
        ElMessage.warning('请选择维修人员')
        return
    }

    await assignRepair(repairId, form.value)

    ElMessage.success('分配成功')

    router.push('/repair/list')
}

// 用户列表
interface UserItem {
    id: number
    username: string
}

const userList = ref<UserItem[]>([])

onMounted(() => {
    console.log(repairId)
    loadUser()
})
</script>

<template>
    <el-card>
        <template #header> 分配维修人员 </template>
        <el-form label-width="100px">
            <el-form-item label="维修人员">
                <el-select v-model="form.repair_user" multiple style="width: 100%">
                    <el-option
                        v-for="item in userList"
                        :key="item.id"
                        :label="item.username"
                        :value="item.id"
                    />
                </el-select>
            </el-form-item>

            <el-form-item>
                <el-button type="primary" @click="submit"> 确定 </el-button>

                <el-button @click="router.back()"> 返回 </el-button>
            </el-form-item>
        </el-form>
    </el-card>
</template>
