<!-- 文件说明：实现 src/views/parking/create/ParkingCreate.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getOwnerList } from '@/api/owner'
import { createParking } from '@/api/parking'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { extractListRows } from '@/utils/listResponse'

const ownerList = ref<any[]>([])

// 数据源分块：管理员新增车位时可选择绑定业主，也可先创建空闲车位。
const loadOwnerList = async () => {
    const res = await getOwnerList()

    ownerList.value = extractListRows(res.data.data)
}

// 表单状态分块：默认新建为空闲车位，后续可在列表页绑定或售卖。
const form = ref({
    owner: '',
    parking_no: '',
    area: '',
    status: 'idle',
})

const router = useRouter()

// 提交分块：保存成功后清空表单并回到车位列表核对结果。
const submitForm = async () => {
    await createParking(form.value)

    ElMessage.success('新增成功')

    form.value = {
        owner: '',
        parking_no: '',
        area: '',
        status: 'idle',
    }
    router.push('/parking/list')
}

onMounted(() => {
    loadOwnerList()
})
</script>

<template>
    <!-- 表单分块：录入业主、车位号、面积和当前状态。 -->
    <el-form-item label="所属业主">
        <el-select v-model="form.owner" placeholder="请选择业主">
            <el-option
                v-for="item in ownerList"
                :key="item.id"
                :label="item.name"
                :value="item.id"
            />
        </el-select>
    </el-form-item>

    <el-form-item label="车位号">
        <el-input v-model="form.parking_no" />
    </el-form-item>

    <el-form-item label="面积">
        <el-input v-model="form.area" />
    </el-form-item>

    <el-form-item label="状态">
        <el-select v-model="form.status">
            <el-option label="空闲" value="idle" />
            <el-option label="使用中" value="used" />
        </el-select>
    </el-form-item>
    <el-form-item>
        <el-button type="primary" @click="submitForm"> 提交 </el-button>
    </el-form-item>
</template>
