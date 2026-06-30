<!-- 文件说明：实现 src/views/car/create/CarCreate.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

import { getOwnerList } from '@/api/owner'
import { getParkingList } from '@/api/parking'
import { createCar } from '@/api/car'

const router = useRouter()

/**
 * 表单
 */
const form = reactive({
    owner: '',
    plate_no: '',
    brand: '',
    color: '',
    car_type: 'monthly',
    parking: '',
})

// 车辆类型选项与后端 Car.TYPE_CHOICES 保持一致。
const carTypeOptions = [
    { label: '月租车', value: 'monthly' },
    { label: '临时车', value: 'temporary' },
]

/**
 * 业主列表
 */
const ownerList = reactive<any[]>([])

/**
 * 车位列表
 */
const parkingList = reactive<any[]>([])

/**
 * 获取业主
 */
const loadOwnerList = async () => {
    const res = await getOwnerList()

    ownerList.push(...res.data.data)
}

/**
 * 获取车位
 */
const loadParkingList = async () => {
    const res = await getParkingList()

    parkingList.push(...res.data.data)
}

/**
 * 提交
 */
const submitForm = async () => {
    await createCar(form)

    ElMessage.success('新增成功')

    router.push('/car/list')
}

onMounted(() => {
    loadOwnerList()
    loadParkingList()
})
</script>

<template>
    <el-card>
        <template #header>
            <span>新增车辆</span>
        </template>

        <el-form :model="form" label-width="120px" style="max-width: 700px">
            <el-form-item label="车主">
                <el-select v-model="form.owner" placeholder="请选择车主">
                    <el-option
                        v-for="item in ownerList"
                        :key="item.id"
                        :label="item.name"
                        :value="item.id"
                    />
                </el-select>
            </el-form-item>

            <el-form-item label="车牌号">
                <el-input v-model="form.plate_no" />
            </el-form-item>

            <el-form-item label="品牌">
                <el-input v-model="form.brand" />
            </el-form-item>

            <el-form-item label="颜色">
                <el-input v-model="form.color" />
            </el-form-item>

            <el-form-item label="车辆类型">
                <el-select v-model="form.car_type" placeholder="请选择车辆类型">
                    <el-option
                        v-for="item in carTypeOptions"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    />
                </el-select>
            </el-form-item>

            <el-form-item label="所属车位">
                <el-select v-model="form.parking" placeholder="请选择车位">
                    <el-option
                        v-for="item in parkingList"
                        :key="item.id"
                        :label="item.parking_no"
                        :value="item.id"
                    />
                </el-select>
            </el-form-item>

            <el-form-item>
                <el-button type="primary" @click="submitForm"> 提交 </el-button>
            </el-form-item>
        </el-form>
    </el-card>
</template>
