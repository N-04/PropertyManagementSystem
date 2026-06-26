<!-- 文件说明：实现注册页面的手机号验证、图形验证码、短信验证码、密码确认和协议勾选。 -->
<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getCaptchaApi, registerApi, sendSmsCodeApi } from '@/api/auth'

const router = useRouter()
const captchaImage = ref('')
const captchaKey = ref('')
const smsDebugCode = ref('')
const smsCountdown = ref(0)
const isSendingSms = ref(false)
const isRegistering = ref(false)
const agreementVisible = ref(false)
const agreementRead = ref(false)
const verifiedSmsPhone = ref('')
const verifiedCaptchaKey = ref('')
const verifiedCaptchaCode = ref('')
let smsTimer: ReturnType<typeof setInterval> | null = null

const form = reactive({
    phone: '',
    real_name: '',
    id_card: '',
    password: '',
    confirm_password: '',
    captcha_code: '',
    sms_code: '',
    agreed: false,
})

const getResponseMessage = (data: any, fallback: string) => {
    if (!data) {
        return fallback
    }

    if (typeof data === 'string') {
        return data
    }

    if (data.msg) {
        return data.msg
    }

    if (data.detail) {
        return data.detail
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

const loadCaptcha = async () => {
    const res = await getCaptchaApi()
    captchaKey.value = res.data.data.captcha_key
    captchaImage.value = res.data.data.captcha_image
    form.captcha_code = ''
    verifiedCaptchaKey.value = ''
    verifiedCaptchaCode.value = ''
}

const smsButtonText = computed(() => {
    return smsCountdown.value > 0 ? `${smsCountdown.value}s后重试` : '获取验证码'
})

const canSubmit = computed(() => {
    return agreementRead.value && form.agreed && !isSendingSms.value && !isRegistering.value
})

const hasVerifiedSmsCaptcha = computed(() => {
    return Boolean(
        verifiedSmsPhone.value === form.phone &&
            verifiedCaptchaKey.value &&
            verifiedCaptchaCode.value
    )
})

const effectiveCaptchaKey = computed(() => {
    return hasVerifiedSmsCaptcha.value ? verifiedCaptchaKey.value : captchaKey.value
})

const effectiveCaptchaCode = computed(() => {
    return hasVerifiedSmsCaptcha.value ? verifiedCaptchaCode.value : form.captcha_code
})

const validatePhone = () => {
    if (!form.phone) {
        ElMessage.warning('手机号不能为空')
        return false
    }

    if (!/^1[3-9]\d{9}$/.test(form.phone)) {
        ElMessage.warning('请输入11位有效手机号')
        return false
    }

    return true
}

const validateIdentity = () => {
    form.real_name = form.real_name.trim()
    form.id_card = form.id_card.trim().toUpperCase()

    if (!form.real_name) {
        ElMessage.warning('真实姓名不能为空')
        return false
    }

    if (form.real_name.length > 50) {
        ElMessage.warning('真实姓名长度不能超过50位')
        return false
    }

    if (!/^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dX]$/.test(form.id_card)) {
        ElMessage.warning('请输入18位有效身份证号')
        return false
    }

    const year = Number(form.id_card.slice(6, 10))
    const month = Number(form.id_card.slice(10, 12))
    const day = Number(form.id_card.slice(12, 14))
    const birthday = new Date(year, month - 1, day)

    if (
        birthday.getFullYear() !== year ||
        birthday.getMonth() !== month - 1 ||
        birthday.getDate() !== day
    ) {
        ElMessage.warning('身份证出生日期不合法')
        return false
    }

    const today = new Date()
    const todayDate = new Date(today.getFullYear(), today.getMonth(), today.getDate())

    if (birthday > todayDate) {
        ElMessage.warning('身份证出生日期不能晚于今天')
        return false
    }

    const weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    const checkMap = '10X98765432'
    const total = weights.reduce((sum, weight, index) => {
        return sum + Number(form.id_card[index]) * weight
    }, 0)

    if (form.id_card[17] !== checkMap[total % 11]) {
        ElMessage.warning('身份证校验位不正确')
        return false
    }

    return true
}

const validatePassword = () => {
    if (form.password.length < 8 || form.password.length > 20) {
        ElMessage.warning('密码长度必须为8-20位')
        return false
    }

    if (/^\d+$/.test(form.password)) {
        ElMessage.warning('密码不能为纯数字')
        return false
    }

    if (/^[A-Za-z]+$/.test(form.password)) {
        ElMessage.warning('密码不能为纯字母')
        return false
    }

    if (form.password !== form.confirm_password) {
        ElMessage.warning('两次密码不一致')
        return false
    }

    return true
}

const validateRegisterForm = () => {
    if (!validatePhone() || !validateIdentity() || !validatePassword()) {
        return false
    }

    if (!effectiveCaptchaCode.value) {
        ElMessage.warning('请输入图形验证码')
        return false
    }

    if (!form.sms_code) {
        ElMessage.warning('请输入短信验证码')
        return false
    }

    if (!agreementRead.value || !form.agreed) {
        ElMessage.warning('请先阅读并勾选用户协议')
        return false
    }

    return true
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

const sendSmsCode = async () => {
    if (smsCountdown.value > 0 || isSendingSms.value) {
        return
    }

    if (!validatePhone()) {
        return
    }

    if (!form.captcha_code) {
        ElMessage.warning('请先填写图形验证码')
        return
    }

    isSendingSms.value = true

    try {
        const res = await sendSmsCodeApi({
            phone: form.phone,
            purpose: 'register',
            captcha_key: captchaKey.value,
            captcha_code: form.captcha_code,
        })

        if (res.data.code !== 200) {
            ElMessage.error(getResponseMessage(res.data, '短信验证码发送失败'))
            await loadCaptcha()
            return
        }

        verifiedSmsPhone.value = form.phone
        verifiedCaptchaKey.value = captchaKey.value
        verifiedCaptchaCode.value = form.captcha_code
        smsDebugCode.value = res.data.data.debug_code || ''
        if (smsDebugCode.value) {
            form.sms_code = smsDebugCode.value
            ElMessage.success(`短信验证码：${smsDebugCode.value}`)
        } else {
            ElMessage.success('短信验证码已发送')
        }

        startSmsCountdown(res.data.data.cooldown_seconds || 60)
    } catch (error: any) {
        ElMessage.error(getResponseMessage(error?.response?.data, '短信验证码发送失败'))
        await loadCaptcha()
    } finally {
        isSendingSms.value = false
    }
}

const openAgreement = () => {
    agreementVisible.value = true
}

const confirmAgreement = () => {
    agreementRead.value = true
    form.agreed = true
    agreementVisible.value = false
}

const handleRegister = async () => {
    if (!validateRegisterForm()) {
        return
    }

    isRegistering.value = true

    try {
        const res = await registerApi({
            phone: form.phone,
            real_name: form.real_name,
            id_card: form.id_card,
            password: form.password,
            confirm_password: form.confirm_password,
            captcha_key: effectiveCaptchaKey.value,
            captcha_code: effectiveCaptchaCode.value,
            sms_code: form.sms_code,
            agreed: form.agreed,
        })

        if (res.data.code !== 200) {
            ElMessage.error(getResponseMessage(res.data, '注册失败'))
            await loadCaptcha()
            return
        }

        ElMessage.success(res.data.msg)
        router.push('/login')
    } catch (error: any) {
        ElMessage.error(getResponseMessage(error?.response?.data, '注册失败，请检查后端服务'))
        await loadCaptcha()
    } finally {
        isRegistering.value = false
    }
}

watch(
    () => form.phone,
    () => {
        if (verifiedSmsPhone.value && verifiedSmsPhone.value !== form.phone) {
            verifiedSmsPhone.value = ''
            verifiedCaptchaKey.value = ''
            verifiedCaptchaCode.value = ''
            smsDebugCode.value = ''
            form.sms_code = ''
            smsCountdown.value = 0
            clearSmsTimer()
        }
    }
)

onMounted(() => {
    loadCaptcha()
})

onBeforeUnmount(() => {
    clearSmsTimer()
})
</script>

<template>
    <div class="register-page">
        <el-card class="register-card">
            <template #header>
                <div class="title">业主注册</div>
            </template>

            <el-form :model="form" class="register-form" label-width="100px">
                <el-form-item label="真实姓名">
                    <el-input v-model="form.real_name" maxlength="50" />
                </el-form-item>

                <el-form-item label="手机号">
                    <el-input v-model="form.phone" maxlength="11" />
                </el-form-item>

                <el-form-item label="身份证号">
                    <el-input v-model="form.id_card" maxlength="18" />
                </el-form-item>

                <el-form-item label="密码">
                    <el-input v-model="form.password" type="password" show-password />
                </el-form-item>

                <el-form-item label="确认密码">
                    <el-input v-model="form.confirm_password" type="password" show-password />
                </el-form-item>

                <el-form-item label="图形验证码">
                    <div class="captcha-row">
                        <el-input v-model="form.captcha_code" maxlength="4" />
                        <img
                            v-if="captchaImage"
                            class="captcha-img"
                            :src="captchaImage"
                            @click="loadCaptcha"
                        />
                    </div>
                </el-form-item>

                <el-form-item label="短信验证码">
                    <div class="captcha-row">
                        <el-input v-model="form.sms_code" maxlength="6" />
                        <el-button
                            :disabled="smsCountdown > 0 || isSendingSms"
                            @click="sendSmsCode"
                        >
                            {{ smsButtonText }}
                        </el-button>
                    </div>
                </el-form-item>

                <el-form-item class="form-action-item">
                    <div class="agreement-row">
                        <el-checkbox v-model="form.agreed" :disabled="!agreementRead">
                            我已阅读并同意
                        </el-checkbox>
                        <el-button link type="primary" @click="openAgreement"> 用户协议 </el-button>
                    </div>
                </el-form-item>

                <el-form-item class="form-action-item">
                    <el-button
                        class="submit-button"
                        type="primary"
                        :disabled="!canSubmit"
                        :loading="isRegistering"
                        @click="handleRegister"
                    >
                        提交注册
                    </el-button>
                </el-form-item>

                <el-form-item class="form-action-item">
                    <el-button class="login-link" link type="primary" @click="router.push('/login')">
                        返回登录
                    </el-button>
                </el-form-item>
            </el-form>
        </el-card>

        <el-dialog v-model="agreementVisible" title="用户协议" width="520px">
            <div class="agreement-content">
                <p>请确认注册信息真实有效，并同意物业管理系统用于业主身份审核。</p>
                <p>系统会对手机号、真实姓名和身份证号进行校验，并在审核通过后开通业主账号。</p>
                <p>请妥善保管登录密码，不要将短信验证码、账号信息透露给他人。</p>
            </div>
            <template #footer>
                <el-button @click="agreementVisible = false">稍后再看</el-button>
                <el-button type="primary" @click="confirmAgreement">已阅读并同意</el-button>
            </template>
        </el-dialog>
    </div>
</template>

<style scoped>
.register-page {
    min-height: 100vh;
    box-sizing: border-box;
    display: grid;
    place-items: center;
    padding: 40px 16px;
    background: #f5f7fa;
}

.register-card {
    width: min(520px, 100%);
}

.title {
    text-align: center;
    font-size: 22px;
    font-weight: bold;
}

.register-form {
    width: 100%;
}

.captcha-row {
    display: flex;
    width: 100%;
    gap: 12px;
    align-items: center;
}

.captcha-img {
    width: 120px;
    height: 42px;
    cursor: pointer;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
}

.agreement-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    width: 100%;
    flex-wrap: wrap;
}

.form-action-item {
    margin-bottom: 20px;
}

.form-action-item :deep(.el-form-item__content) {
    justify-content: center;
    margin-left: 0 !important;
}

.submit-button {
    width: 320px;
    max-width: 100%;
}

.login-link {
    font-size: 16px;
    font-weight: 600;
}

.agreement-content {
    line-height: 1.8;
    color: #303133;
}
</style>
