<!-- 文件说明：提供最小可用的找回密码页面，避免路由动态导入空组件失败。 -->
<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getCaptchaApi, resetPasswordApi, sendSmsCodeApi } from '@/api/auth'

const router = useRouter()
const loading = ref(false)
const isSendingSms = ref(false)
const smsCountdown = ref(0)
const captchaImage = ref('')
const captchaKey = ref('')
let smsTimer: ReturnType<typeof setInterval> | null = null

const form = reactive({
    phone: '',
    captcha_code: '',
    sms_code: '',
    password: '',
    confirm_password: '',
})

const smsButtonText = computed(() => {
    return smsCountdown.value > 0 ? `${smsCountdown.value}s后重试` : '获取验证码'
})

const getResponseMessage = (data: any, fallback: string) => {
    if (!data) {
        return fallback
    }

    if (data.msg) {
        return data.msg
    }

    if (Array.isArray(data.non_field_errors)) {
        return data.non_field_errors.join('、')
    }

    const firstValue = Object.values(data)[0]

    if (Array.isArray(firstValue)) {
        return firstValue.join('、')
    }

    if (typeof firstValue === 'string') {
        return firstValue
    }

    return fallback
}

const clearSmsTimer = () => {
    if (smsTimer) {
        clearInterval(smsTimer)
        smsTimer = null
    }
}

const startSmsCountdown = (seconds = 60) => {
    clearSmsTimer()
    smsCountdown.value = seconds

    smsTimer = setInterval(() => {
        smsCountdown.value -= 1

        if (smsCountdown.value <= 0) {
            smsCountdown.value = 0
            clearSmsTimer()
        }
    }, 1000)
}

const loadCaptcha = async () => {
    const res = await getCaptchaApi()

    captchaKey.value = res.data.data.captcha_key
    captchaImage.value = res.data.data.captcha_image
    form.captcha_code = ''
}

const sendResetSmsCode = async () => {
    if (smsCountdown.value > 0 || isSendingSms.value) {
        return
    }

    if (!form.phone) {
        ElMessage.warning('请输入手机号')
        return
    }

    if (!form.captcha_code) {
        ElMessage.warning('请输入图形验证码')
        return
    }

    isSendingSms.value = true

    try {
        const res = await sendSmsCodeApi({
            phone: form.phone,
            purpose: 'reset_password',
            captcha_key: captchaKey.value,
            captcha_code: form.captcha_code,
        })

        if (res.data.code !== 200) {
            ElMessage.error(getResponseMessage(res.data, '短信验证码发送失败'))
            await loadCaptcha()
            return
        }

        if (res.data.data?.debug_code) {
            form.sms_code = res.data.data.debug_code
            ElMessage.success(`短信验证码：${res.data.data.debug_code}`)
        } else {
            ElMessage.success('短信验证码已发送')
        }

        startSmsCountdown(res.data.data?.cooldown_seconds || 60)
        await loadCaptcha()
    } catch (error: any) {
        ElMessage.error(getResponseMessage(error?.response?.data, '短信验证码发送失败'))
        await loadCaptcha()
    } finally {
        isSendingSms.value = false
    }
}

const handleReset = async () => {
    if (!form.phone || !form.sms_code || !form.password || !form.confirm_password) {
        ElMessage.warning('请完整填写手机号、短信验证码和新密码')
        return
    }

    loading.value = true

    try {
        const res = await resetPasswordApi(form)

        if (res.data.code !== 200) {
            ElMessage.error(res.data.msg || '重置失败')
            return
        }

        ElMessage.success('密码重置成功')
        router.push('/login')
    } catch (error: any) {
        ElMessage.error(error?.response?.data?.msg || '重置失败，请检查后端服务')
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    loadCaptcha()
})

onBeforeUnmount(() => {
    clearSmsTimer()
})
</script>

<template>
    <div class="forgot-page">
        <div class="forgot-card">
            <div class="forgot-title">找回密码</div>

            <el-form label-width="0">
                <el-form-item>
                    <el-input v-model="form.phone" placeholder="手机号" maxlength="11" />
                </el-form-item>

                <el-form-item>
                    <div class="captcha-row">
                        <el-input
                            v-model="form.captcha_code"
                            placeholder="图形验证码"
                            maxlength="4"
                            clearable
                        />

                        <img
                            v-if="captchaImage"
                            class="captcha-img"
                            :src="captchaImage"
                            title="点击刷新验证码"
                            @click="loadCaptcha"
                        />
                    </div>
                </el-form-item>

                <el-form-item>
                    <div class="sms-row">
                        <el-input
                            v-model="form.sms_code"
                            placeholder="短信验证码"
                            maxlength="6"
                            clearable
                        />

                        <el-button
                            :disabled="smsCountdown > 0 || isSendingSms"
                            :loading="isSendingSms"
                            @click="sendResetSmsCode"
                        >
                            {{ smsButtonText }}
                        </el-button>
                    </div>
                </el-form-item>

                <el-form-item>
                    <el-input
                        v-model="form.password"
                        type="password"
                        placeholder="新密码"
                        show-password
                    />
                </el-form-item>

                <el-form-item>
                    <el-input
                        v-model="form.confirm_password"
                        type="password"
                        placeholder="确认新密码"
                        show-password
                        @keyup.enter="handleReset"
                    />
                </el-form-item>

                <el-form-item>
                    <el-button
                        type="primary"
                        class="forgot-button"
                        :loading="loading"
                        @click="handleReset"
                    >
                        重置密码
                    </el-button>
                </el-form-item>
            </el-form>

            <el-button link type="primary" @click="router.push('/login')">
                返回登录
            </el-button>
        </div>
    </div>
</template>

<style scoped>
.forgot-page {
    width: 100vw;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f5f7fa;
}

.forgot-card {
    width: 400px;
    padding: 32px 36px;
    background: #ffffff;
    border-radius: 8px;
    box-shadow: 0 12px 32px rgb(0 0 0 / 12%);
}

.forgot-title {
    margin-bottom: 24px;
    text-align: center;
    font-size: 22px;
    font-weight: 700;
    color: #303133;
}

.forgot-button {
    width: 100%;
}

.captcha-row,
.sms-row {
    display: flex;
    width: 100%;
    gap: 12px;
    align-items: center;
}

.captcha-img {
    width: 120px;
    height: 38px;
    flex: 0 0 120px;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    cursor: pointer;
    background: #f5f7fa;
}
</style>
