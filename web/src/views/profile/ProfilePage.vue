<!-- 文件说明：当前登录用户个人中心，支持资料查看、手机号修改、头像上传和修改密码。 -->
<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
    getUserInfo,
    updateCurrentUserPassword,
    updateCurrentUserProfile,
} from '@/api/user'
import { uploadFile } from '@/api/upload'
import { clearAuthState, setAuthItem } from '@/utils/authState'

const router = useRouter()
const profileLoading = ref(false)
const passwordLoading = ref(false)

const profileForm = reactive({
    username: '',
    real_name: '',
    nickname: '',
    phone: '',
    avatar: '',
    id_card_masked: '',
    roles: [] as string[],
})

const passwordForm = reactive({
    old_password: '',
    password: '',
    confirm_password: '',
})

const getErrorMessage = (error: any, fallback: string) => {
    return error?.response?.data?.msg || error?.response?.data?.detail || fallback
}

const avatarUrl = computed(() => {
    if (!profileForm.avatar) {
        return ''
    }

    if (profileForm.avatar.startsWith('http')) {
        return profileForm.avatar
    }

    return `http://127.0.0.1:8000${profileForm.avatar}`
})

const loadProfile = async () => {
    try {
        const res = await getUserInfo()
        const data = res.data.data || {}

        profileForm.username = data.username || ''
        profileForm.real_name = data.real_name || ''
        profileForm.nickname = data.nickname || ''
        profileForm.phone = data.phone || ''
        profileForm.avatar = data.avatar || ''
        profileForm.id_card_masked = data.id_card_masked || ''
        profileForm.roles = data.roles || []
    } catch (error) {
        ElMessage.error(getErrorMessage(error, '个人资料加载失败'))
    }
}

const saveProfile = async () => {
    profileLoading.value = true

    try {
        const res = await updateCurrentUserProfile({
            real_name: profileForm.real_name,
            nickname: profileForm.nickname,
            phone: profileForm.phone,
            avatar: profileForm.avatar,
        })

        if (res.data.code !== 200) {
            ElMessage.error(res.data.msg || '保存失败')
            return
        }

        setAuthItem('username', profileForm.username)
        ElMessage.success('资料已保存')
        await loadProfile()
    } catch (error) {
        ElMessage.error(getErrorMessage(error, '保存失败'))
    } finally {
        profileLoading.value = false
    }
}

const beforeAvatarUpload = (file: File) => {
    const isImage = file.type.startsWith('image/')

    if (!isImage) {
        ElMessage.error('请上传图片文件')
    }

    return isImage
}

const uploadAvatar = async (options: any) => {
    const formData = new FormData()
    formData.append('file', options.file)
    formData.append('type', 'avatar')

    try {
        const res = await uploadFile(formData)

        if (res.data.code !== 200) {
            ElMessage.error(res.data.msg || '头像上传失败')
            options.onError?.(new Error(res.data.msg || '头像上传失败'))
            return
        }

        profileForm.avatar = res.data.data.url
        await saveProfile()
        options.onSuccess?.(res.data)
    } catch (error) {
        ElMessage.error(getErrorMessage(error, '头像上传失败'))
        options.onError?.(error)
    }
}

const savePassword = async () => {
    if (!passwordForm.old_password || !passwordForm.password || !passwordForm.confirm_password) {
        ElMessage.warning('请完整填写原密码和新密码')
        return
    }

    passwordLoading.value = true

    try {
        const res = await updateCurrentUserPassword(passwordForm)

        if (res.data.code !== 200) {
            ElMessage.error(res.data.msg || '密码修改失败')
            return
        }

        ElMessage.success('密码修改成功，请重新登录')
        clearAuthState()
        router.push('/login')
    } catch (error) {
        ElMessage.error(getErrorMessage(error, '密码修改失败'))
    } finally {
        passwordLoading.value = false
    }
}

onMounted(() => {
    loadProfile()
})
</script>

<template>
    <el-card>
        <template #header>个人中心</template>

        <el-row :gutter="24">
            <el-col :span="10">
                <el-form label-width="100px">
                    <el-form-item label="头像">
                        <div class="avatar-box">
                            <el-avatar :size="72" :src="avatarUrl">
                                {{ profileForm.real_name || profileForm.username }}
                            </el-avatar>

                            <el-upload
                                :show-file-list="false"
                                :http-request="uploadAvatar"
                                :before-upload="beforeAvatarUpload"
                            >
                                <el-button type="primary">上传头像</el-button>
                            </el-upload>
                        </div>
                    </el-form-item>

                    <el-form-item label="用户名">
                        <el-input v-model="profileForm.username" disabled />
                    </el-form-item>

                    <el-form-item label="真实姓名">
                        <el-input v-model="profileForm.real_name" maxlength="50" />
                    </el-form-item>

                    <el-form-item label="昵称">
                        <el-input v-model="profileForm.nickname" maxlength="50" />
                    </el-form-item>

                    <el-form-item label="手机号">
                        <el-input v-model="profileForm.phone" maxlength="11" />
                    </el-form-item>

                    <el-form-item label="身份证">
                        <el-input v-model="profileForm.id_card_masked" disabled />
                    </el-form-item>

                    <el-form-item label="角色">
                        <el-tag v-for="item in profileForm.roles" :key="item" class="role-tag">
                            {{ item }}
                        </el-tag>
                    </el-form-item>

                    <el-form-item>
                        <el-button type="primary" :loading="profileLoading" @click="saveProfile">
                            保存资料
                        </el-button>
                    </el-form-item>
                </el-form>
            </el-col>

            <el-col :span="10">
                <el-form label-width="100px">
                    <el-form-item label="原密码">
                        <el-input
                            v-model="passwordForm.old_password"
                            type="password"
                            show-password
                        />
                    </el-form-item>

                    <el-form-item label="新密码">
                        <el-input v-model="passwordForm.password" type="password" show-password />
                    </el-form-item>

                    <el-form-item label="确认密码">
                        <el-input
                            v-model="passwordForm.confirm_password"
                            type="password"
                            show-password
                            @keyup.enter="savePassword"
                        />
                    </el-form-item>

                    <el-form-item>
                        <el-button
                            type="warning"
                            :loading="passwordLoading"
                            @click="savePassword"
                        >
                            修改密码
                        </el-button>
                    </el-form-item>
                </el-form>
            </el-col>
        </el-row>
    </el-card>
</template>

<style scoped>
.avatar-box {
    display: flex;
    align-items: center;
    gap: 16px;
}

.role-tag {
    margin-right: 8px;
}
</style>
