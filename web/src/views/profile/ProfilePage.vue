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
import { getHouseList } from '@/api/house'
import { getOwnerList } from '@/api/owner'
import { uploadFile } from '@/api/upload'
import { clearAuthState, setAuthItem } from '@/utils/authState'

const router = useRouter()
const route = useRoute()
const profileLoading = ref(false)
const passwordLoading = ref(false)
const ownerHouses = ref<any[]>([])
const ownerProfiles = ref<any[]>([])
const availableHouses = ref<any[]>([])
const selectedHouseId = ref<number | null>(null)
const selectedRelationship = ref('self')

const profileForm = reactive({
    username: '',
    real_name: '',
    phone: '',
    avatar: '',
    id_card_masked: '',
    roles: [] as string[],
    role_codes: [] as string[],
})

const passwordForm = reactive({
    old_password: '',
    password: '',
    confirm_password: '',
})

const houseStatusLabels: Record<string, string> = {
    vacant: '空置',
    occupied: '已入住',
    renting: '出租',
    repairing: '装修中',
}

const relationshipLabels: Record<string, string> = {
    self: '本人',
    spouse: '配偶',
    child: '子女',
    parent: '父母',
    other: '其他',
}

const extractList = (payload: any) => {
    if (Array.isArray(payload)) return payload
    if (Array.isArray(payload?.results)) return payload.results
    if (Array.isArray(payload?.data)) return payload.data
    if (Array.isArray(payload?.data?.results)) return payload.data.results

    return []
}

const toNumberId = (value: unknown) => {
    if (value === null || value === undefined || value === '') return null

    const numberValue = Number(value)

    return Number.isFinite(numberValue) ? numberValue : null
}

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
const isOwnerProfile = computed(() => {
    return profileForm.role_codes.includes('owner')
        || profileForm.roles.includes('业主')
        || profileForm.roles.includes('owner')
})
const primaryOwnerProfile = computed(() => {
    return ownerProfiles.value.find((item) => item.is_primary) || ownerProfiles.value[0] || null
})
const ownerProfileHouse = computed(() => {
    const profile = primaryOwnerProfile.value

    if (!profile) return null

    if (profile.house && typeof profile.house === 'object') {
        return profile.house
    }

    if (profile.room_no || profile.unit_name || profile.building_name || profile.community_name) {
        return {
            id: toNumberId(profile.house),
            room_no: profile.room_no,
            unit_name: profile.unit_name,
            building_name: profile.building_name,
            community_name: profile.community_name,
        }
    }

    return null
})
const houseOptionLabel = (house: any) => {
    const address = [house.community_name, house.building_name, house.unit_name, house.room_no]
        .filter(Boolean)
        .join(' ')

    return address || `房屋 ${house.id}`
}
const houseOptions = computed(() => {
    const houseMap = new Map<number, any>()

    availableHouses.value.forEach((house) => {
        const id = toNumberId(house.id)

        if (id) houseMap.set(id, house)
    })

    ownerHouses.value.forEach((house) => {
        const id = toNumberId(house.id)

        if (id) houseMap.set(id, house)
    })

    const profileHouse = ownerProfileHouse.value
    const profileHouseId = toNumberId(profileHouse?.id)

    if (profileHouse && profileHouseId) {
        houseMap.set(profileHouseId, profileHouse)
    }

    return Array.from(houseMap.values())
})
const selectedProfileHouse = computed(() => {
    if (!selectedHouseId.value) return null

    return houseOptions.value.find((house) => toNumberId(house.id) === selectedHouseId.value) || null
})
const primaryProfileHouse = computed(() => {
    return selectedProfileHouse.value || ownerHouses.value[0] || ownerProfileHouse.value
})
const ownerRelationshipText = computed(() => {
    const relationship = selectedRelationship.value || primaryOwnerProfile.value?.relationship

    return relationship ? relationshipLabels[relationship] || relationship : ''
})
const houseInfoItems = computed(() => {
    const house = primaryProfileHouse.value

    if (!house) return []

    return [
        { label: '所属小区', value: house.community_name },
        { label: '所属楼栋', value: house.building_name },
        { label: '所属单元', value: house.unit_name },
        { label: '房号', value: house.room_no },
        { label: '建筑面积', value: house.area ? `${house.area}㎡` : '' },
        { label: '户型', value: house.house_type },
        { label: '房屋状态', value: houseStatusLabels[house.status] || house.status },
        { label: '家庭关系', value: ownerRelationshipText.value },
    ].filter((item) => item.value)
})

const loadProfile = async () => {
    try {
        const [userResult, houseResult, ownerResult] = await Promise.allSettled([
            getUserInfo(),
            getHouseList({ page_size: 100 }),
            getOwnerList(''),
        ])

        if (userResult.status !== 'fulfilled') {
            throw userResult.reason
        }

        const data = userResult.value.data.data || {}

        profileForm.username = data.username || ''
        profileForm.real_name = data.real_name || ''
        profileForm.phone = data.phone || ''
        profileForm.avatar = data.avatar || ''
        profileForm.id_card_masked = data.id_card_masked || ''
        profileForm.roles = data.roles || []
        profileForm.role_codes = data.role_codes || []
        ownerHouses.value = houseResult.status === 'fulfilled'
            ? extractList(houseResult.value?.data?.data)
            : []
        ownerProfiles.value = ownerResult.status === 'fulfilled'
            ? extractList(ownerResult.value?.data?.data)
            : []

        if (isOwnerProfile.value) {
            try {
                const availableHouseResult = await getHouseList({
                    page_size: 100,
                    profile_select: 1,
                })

                availableHouses.value = extractList(availableHouseResult.data?.data)
            } catch {
                availableHouses.value = [...ownerHouses.value]
            }
        } else {
            availableHouses.value = []
        }

        const currentProfile = primaryOwnerProfile.value
        const currentHouse = ownerHouses.value[0] || ownerProfileHouse.value

        selectedHouseId.value = toNumberId(currentHouse?.id || currentProfile?.house)
        selectedRelationship.value = currentProfile?.relationship || 'self'
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
            house_id: isOwnerProfile.value ? selectedHouseId.value : undefined,
            relationship: isOwnerProfile.value ? selectedRelationship.value : undefined,
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
                    </div>
                </el-form>
            </div>

            <section v-if="isOwnerProfile" class="profile-house-panel">
                <div class="profile-house-header">
                    <h3>房屋信息</h3>
                    <el-tag v-if="primaryProfileHouse" type="success">已绑定</el-tag>
                    <el-tag v-else type="warning">待绑定</el-tag>
                </div>

                <div class="profile-house-selector">
                    <el-form class="profile-form" label-width="100px">
                        <div class="profile-house-select-grid">
                            <el-form-item label="选择房屋">
                                <el-select
                                    v-model="selectedHouseId"
                                    clearable
                                    filterable
                                    placeholder="请选择小区/楼栋/单元/房号"
                                >
                                    <el-option
                                        v-for="house in houseOptions"
                                        :key="house.id"
                                        :label="houseOptionLabel(house)"
                                        :value="toNumberId(house.id)"
                                    />
                                </el-select>
                            </el-form-item>

                            <el-form-item label="家庭关系">
                                <el-select v-model="selectedRelationship" placeholder="请选择关系">
                                    <el-option label="本人" value="self" />
                                    <el-option label="配偶" value="spouse" />
                                    <el-option label="子女" value="child" />
                                    <el-option label="父母" value="parent" />
                                    <el-option label="其他" value="other" />
                                </el-select>
                            </el-form-item>
                        </div>
                    </el-form>
                </div>

                <div v-if="primaryProfileHouse" class="profile-house-grid">
                    <div v-for="item in houseInfoItems" :key="item.label" class="profile-house-item">
                        <span>{{ item.label }}</span>
                        <strong>{{ item.value }}</strong>
                    </div>
                </div>
                <div v-else class="profile-house-empty">暂无绑定房屋信息</div>
            </section>

            <div class="profile-save-footer">
                <el-button type="primary" :loading="profileLoading" @click="saveProfile">
                    保存资料
                </el-button>
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
    padding: 36px 48px 48px;
}

.profile-section {
    width: 100%;
}

.profile-editor {
    display: grid;
    grid-template-columns: 260px minmax(0, 1fr);
    column-gap: 44px;
    row-gap: 24px;
    align-items: start;
    max-width: 1320px;
    margin: 0 auto;
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
    row-gap: 2px;
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

.profile-form :deep(.el-select) {
    width: 100%;
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

.profile-house-panel {
    grid-column: 1 / -1;
    padding: 20px 24px;
    border: 1px solid #dfe5ef;
    border-radius: 8px;
    background: #ffffff;
}

.profile-house-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    margin-bottom: 18px;
}

.profile-house-header h3 {
    margin: 0;
    color: #0f172a;
    font-size: 16px;
    font-weight: 700;
    line-height: 24px;
}

.profile-house-selector {
    margin-bottom: 18px;
    padding-bottom: 2px;
}

.profile-house-select-grid {
    display: grid;
    grid-template-columns: minmax(360px, 1fr) minmax(260px, 0.6fr);
    column-gap: 32px;
    align-items: start;
}

.profile-house-selector :deep(.el-form-item) {
    margin-bottom: 0;
}

.profile-house-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 14px 18px;
}

.profile-house-item {
    min-height: 72px;
    padding: 14px 16px;
    border: 1px solid #e6ebf2;
    border-radius: 8px;
    background: #f8fafc;
}

.profile-house-item span {
    display: block;
    margin-bottom: 6px;
    color: #64748b;
    font-size: 13px;
    font-weight: 500;
    line-height: 20px;
}

.profile-house-item strong {
    display: block;
    overflow: hidden;
    color: #334155;
    font-size: 15px;
    font-weight: 600;
    line-height: 22px;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.profile-house-empty {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 96px;
    color: #64748b;
    border: 1px dashed #d7e0eb;
    border-radius: 8px;
    background: #f8fafc;
}

.profile-save-footer {
    display: flex;
    grid-column: 1 / -1;
    justify-content: center;
    padding-top: 4px;
}

.profile-save-footer :deep(.el-button) {
    min-width: 132px;
    height: 44px;
    border-radius: 8px;
    font-size: 15px;
    font-weight: 600;
}

@media (max-width: 768px) {
    .profile-card :deep(.el-card__body) {
        padding: 24px 16px;
    }

    .profile-editor,
    .profile-fields-grid,
    .avatar-field-row,
    .profile-house-select-grid {
        display: block;
    }

    .avatar-label {
        justify-content: flex-start;
        margin-bottom: 8px;
    }

    .profile-house-panel {
        margin-top: 24px;
        padding: 16px;
    }

    .profile-house-grid {
        grid-template-columns: 1fr;
    }
}
</style>
