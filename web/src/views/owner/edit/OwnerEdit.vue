<!-- 文件说明：实现 src/views/owner/edit/OwnerEdit.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
defineOptions({
    name: 'OwnerEdit',
})

import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { getHouseList } from '@/api/house'
import Upload from '@/views/upload/Upload.vue'
import { useRoute } from 'vue-router'
import { updateOwner, getOwnerDetail } from '@/api/owner'
import { toMediaURL } from '@/utils/url'

const route = useRoute()
const router = useRouter()

const form = ref({
    house: '',
    name: '',
    phone: '',
    avatar: '',
    id_card: '',
    id_card_image: '',
    gender: '男',
    relationship: '本人',
    is_primary: false,
})

const houseList = ref<any[]>([])

// const uploadSuccess = (res: any) => {
//     form.value.avatar = res.data.url
// }

const loadHouseList = async () => {
    const res = await getHouseList()
    houseList.value = res.data.data
}

const loadDetail = async () => {
    const res = await getOwnerDetail(Number(route.query.id))

    form.value = {
        ...res.data.data,
        id_card: '',
    }
}

const submitForm = async () => {
    const payload = {
        ...form.value,
    }

    if (!payload.id_card) {
        delete (payload as Partial<typeof form.value>).id_card
    }

    await updateOwner(Number(route.query.id), payload)

    ElMessage.success('修改成功')

    router.push('/owner/list')
}

onMounted(() => {
    loadHouseList()
    loadDetail()
})
</script>

<template>
    <el-card>
        <template #header>
            <span>编辑业主</span>
        </template>

        <el-form :model="form" label-width="120px" style="max-width: 700px">
            <el-form-item label="所属房屋">
                <el-select v-model="form.house">
                    <el-option
                        v-for="item in houseList"
                        :key="item.id"
                        :label="item.room_no"
                        :value="item.id"
                    />
                </el-select>
            </el-form-item>

            <el-form-item label="头像">
                <Upload
                    upload-type="avatar"
                    @success="
                        (url: string) => {
                            form.avatar = url
                        }
                    "
                />

                <div v-if="form.avatar" style="margin-top: 10px">
                    <el-image
                        :src="toMediaURL(form.avatar)"
                        style="width: 100px; height: 100px"
                        fit="cover"
                    />
                </div>
            </el-form-item>

            <el-form-item label="业主姓名">
                <el-input v-model="form.name" />
            </el-form-item>

            <el-form-item label="手机号">
                <el-input v-model="form.phone" />
            </el-form-item>

            <el-form-item label="身份证">
                <el-input v-model="form.id_card" placeholder="留空则不修改身份证号" />
            </el-form-item>
            <el-form-item label="身份证照片">
                <Upload
                    upload-type="id_card"
                    @success="
                        (url: string) => {
                            form.id_card_image = url
                        }
                    "
                />
                <div v-if="form.id_card_image" style="margin-top: 10px">
                    <el-image
                        :src="toMediaURL(form.id_card_image)"
                        style="width: 200px"
                        fit="cover"
                    />
                </div>
            </el-form-item>

            <el-form-item label="性别">
                <el-radio-group v-model="form.gender">
                    <el-radio label="男">男</el-radio>
                    <el-radio label="女">女</el-radio>
                </el-radio-group>
            </el-form-item>

            <el-form-item label="关系">
                <el-select v-model="form.relationship">
                    <el-option label="本人" value="本人" />
                    <el-option label="配偶" value="配偶" />
                    <el-option label="子女" value="子女" />
                    <el-option label="父母" value="父母" />
                    <el-option label="其他" value="其他" />
                </el-select>
            </el-form-item>

            <el-form-item label="主业主">
                <el-switch v-model="form.is_primary" />
            </el-form-item>

            <el-form-item>
                <el-button type="primary" @click="submitForm"> 提交 </el-button>
            </el-form-item>
        </el-form>
    </el-card>
</template>
