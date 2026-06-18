<!-- 文件说明：当前登录用户个人中心，支持资料查看、手机号修改、头像上传和修改密码。 -->
<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
    getUserInfo,
    updateCurrentUserPassword,
    updateCurrentUserProfile,
} from '@/api/user'
import { uploadFile } from '@/api/upload'
import { clearAuthState, setAuthItem } from '@/utils/authState'

const router = useRouter()
const route = useRoute()
const profileLoading = ref(false)
const passwordLoading = ref(false)

const profileForm = reactive({
    username: '',
    real_name: '',
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

const avatarActionText = computed(() => avatarUrl.value ? '更改头像' : '上传头像')
const profileTitle = computed(() => route.path === '/profile/password' ? '修改密码' : '个人中心')
const isPasswordPage = computed(() => route.path === '/profile/password')

const loadProfile = async () => {
    try {
        const res = await getUserInfo()
        const data = res.data.data || {}

        profileForm.username = data.username || ''
        profileForm.real_name = data.real_name || ''
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
            username: profileForm.username,
            real_name: profileForm.real_name,
            phone: profileForm.phone,
            avatar: profileForm.avatar,
        })

        if (res.data.code !== 200) {
            ElMessage.error(res.data.msg || '保存失败')
            return
        }

        const savedUser = res.data.data || {}

        profileForm.username = savedUser.username || profileForm.username
        setAuthItem('username', profileForm.username, true, true)
        ElMessage.success('资料已保存')
        await loadProfile()
        await router.push('/dashboard')
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
    <el-card class="profile-card">
        <template #header>{{ profileTitle }}</template>

        <div v-if="!isPasswordPage" class="profile-section profile-editor">
            <div class="avatar-panel">
                <div class="avatar-field-row">
                    <span class="avatar-label">头像</span>
                    <el-upload
                        class="avatar-uploader"
                        :show-file-list="false"
                        :http-request="uploadAvatar"
                        :before-upload="beforeAvatarUpload"
                    >
                        <div class="profile-avatar">
                            <img
                                v-if="avatarUrl"
                                :src="avatarUrl"
                                :alt="profileForm.real_name || profileForm.username"
                            >
                            <span v-else class="avatar-placeholder">
                                {{ profileForm.real_name || profileForm.username || '头像' }}
                            </span>
                            <span class="avatar-mask">{{ avatarActionText }}</span>
                        </div>
                    </el-upload>
                </div>
            </div>

            <div class="profile-fields-panel">
                <el-form class="profile-form" label-width="100px">
                    <div class="profile-fields-grid">
                        <el-form-item label="用户名">
                            <el-input v-model="profileForm.username" maxlength="150" />
                        </el-form-item>

                        <el-form-item label="真实姓名">
                            <el-input v-model="profileForm.real_name" maxlength="50" />
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

                        <el-form-item class="profile-actions">
                            <el-button type="primary" :loading="profileLoading" @click="saveProfile">
                                保存资料
                            </el-button>
                        </el-form-item>
                    </div>
                </el-form>
            </div>
        </div>

        <div v-else class="profile-section password-section">
            <el-form class="profile-form" label-width="100px">
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
        </div>
    </el-card>
</template>

<style scoped>
.profile-card {
    min-height: 680px;
    border-radius: 8px;
}

.profile-card :deep(.el-card__header) {
    display: flex;
    align-items: center;
    min-height: 64px;
    padding: 0 24px;
    color: #0f172a;
    font-size: 18px;
    font-weight: 700;
    line-height: 28px;
}

.profile-card :deep(.el-card__body) {
    padding: 40px 56px;
}

.profile-section {
    width: 100%;
}

.profile-editor {
    display: grid;
    grid-template-columns: 240px minmax(0, 880px);
    column-gap: 56px;
    align-items: start;
    max-width: 1220px;
}

.avatar-panel {
    min-width: 0;
}

.avatar-field-row {
    display: grid;
    grid-template-columns: 100px 112px;
    column-gap: 16px;
    align-items: center;
}

.avatar-label {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    min-height: 44px;
    color: #475569;
    font-size: 14px;
    font-weight: 500;
    line-height: 22px;
}

.profile-fields-panel {
    min-width: 0;
}

.profile-form {
    width: 100%;
    max-width: none;
}

.profile-fields-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(280px, 1fr));
    column-gap: 36px;
    align-items: start;
}

.password-section .profile-form {
    max-width: 680px;
}

.profile-form :deep(.el-form-item) {
    align-items: center;
    margin-bottom: 24px;
}

.profile-form :deep(.el-form-item__label) {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    min-height: 44px;
    color: #475569;
    font-size: 14px;
    font-weight: 500;
    line-height: 22px;
}

.profile-form :deep(.el-input__wrapper) {
    min-height: 44px;
    border-radius: 6px;
}

.profile-form :deep(.el-input__inner) {
    height: 44px;
    font-size: 14px;
    line-height: 44px;
}

.avatar-uploader {
    display: inline-flex;
    align-items: center;
    justify-content: center;
}

.profile-avatar {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 112px;
    height: 112px;
    overflow: hidden;
    border: 1px solid #dfe5ef;
    border-radius: 6px;
    cursor: pointer;
    color: var(--text-muted);
    background: #eef2f7;
    font-size: 14px;
    font-weight: 600;
    line-height: 20px;
    text-align: center;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.profile-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.profile-avatar:hover {
    border-color: #0f766e;
    box-shadow: 0 8px 18px rgba(15, 118, 110, 0.14);
}

.avatar-placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    padding: 8px;
}

.avatar-mask {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 8px;
    color: #ffffff;
    background: rgba(15, 118, 110, 0.78);
    font-size: 14px;
    font-weight: 600;
    line-height: 20px;
    opacity: 0;
    transition: opacity 0.2s ease;
}

.profile-avatar:hover .avatar-mask {
    opacity: 1;
}

.role-tag {
    margin-right: 8px;
}

.profile-actions {
    grid-column: 1 / -1;
}

@media (max-width: 768px) {
    .profile-card :deep(.el-card__body) {
        padding: 24px 16px;
    }

    .profile-editor,
    .profile-fields-grid,
    .avatar-field-row {
        display: block;
    }

    .avatar-label {
        justify-content: flex-start;
        margin-bottom: 8px;
    }
}
</style>
