<!-- 文件说明：实现 src/views/house/create/HouseCreate.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
defineOptions({
    name: 'HouseCreate',
})

import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { createHouse } from '@/api/house'
import { getUnitList } from '@/api/unit'

const router = useRouter()

const unitList = ref<any[]>([])

const form = reactive({
    unit: '',
    room_no: '',
    area: '',
    house_type: '',
    status: 'vacant',
})

const loadUnitList = async () => {
    const res = await getUnitList()
    unitList.value = res.data.data
}

const submitForm = async () => {
    await createHouse(form)

    ElMessage.success('新增成功')

    router.push('/house/list')
}

onMounted(() => {
    loadUnitList()
})
</script>

<template>
    <el-card>
        <template #header>
            <span>新增房屋</span>
        </template>

        <el-form :model="form" label-width="120px" style="max-width: 600px">
            <el-form-item label="所属单元">
                <el-select v-model="form.unit" placeholder="请选择单元">
                    <el-option
                        v-for="item in unitList"
                        :key="item.id"
                        :label="item.name"
                        :value="item.id"
                    />
                </el-select>
            </el-form-item>

            <el-form-item label="房号">
                <el-input v-model="form.room_no" />
            </el-form-item>

            <el-form-item label="面积">
                <el-input v-model="form.area" />
            </el-form-item>

            <el-form-item label="户型">
                <el-input v-model="form.house_type" />
            </el-form-item>

            <el-form-item label="状态">
                <el-select v-model="form.status">
                    <el-option label="空置" value="vacant" />
                    <el-option label="已入住" value="occupied" />
                    <el-option label="出租" value="renting" />
                    <el-option label="装修中" value="repairing" />
                </el-select>
            </el-form-item>

            <el-form-item>
                <el-button type="primary" @click="submitForm"> 提交 </el-button>
            </el-form-item>
        </el-form>
    </el-card>
</template>
