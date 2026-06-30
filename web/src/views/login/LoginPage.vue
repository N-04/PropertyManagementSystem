<!-- 文件说明：实现用户登录页，支持密码登录、手机号登录、图形验证码和短信验证码。 -->
<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { refreshBrowserTitle } from '@/router'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getCaptchaApi, loginApi, phoneLoginApi, sendSmsCodeApi } from '@/api/auth'
import { saveAuthState } from '@/utils/authState'

const router = useRouter()

// 表单状态分块：两种登录方式共用同一张验证码，表单值分开维护。
const loginMode = ref<'password' | 'phone'>('password')
const passwordForm = ref({
    username: '',
    password: '',
    captcha_code: '',
})
const phoneForm = ref({
    phone: '',
    sms_code: '',
    captcha_code: '',
})
const captchaImage = ref('')
const captchaKey = ref('')
const captchaLoading = ref(false)
const captchaError = ref('')
const smsCountdown = ref(0)
const isSendingSms = ref(false)
let smsTimer: ReturnType<typeof setInterval> | null = null

const loading = ref(false)

// 短信按钮文案跟随倒计时变化，避免用户重复请求验证码。
const smsButtonText = computed(() => {
    return smsCountdown.value > 0 ? `${smsCountdown.value}s后重试` : '获取验证码'
})

// 后端错误结构不完全统一，统一抽出可读提示后再交给页面弹窗。
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

const getErrorMessage = (error: any) => {
    return getResponseMessage(error?.response?.data, error?.message || '登录失败，请检查后端服务')
}

const clearSmsTimer = () => {
    // 组件卸载和重新倒计时时都先清理旧定时器，避免多个倒计时同时运行。
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
    // 图形验证码每次刷新都会清空输入，避免旧验证码继续提交。
    captchaLoading.value = true
    captchaError.value = ''

    try {
        const res = await getCaptchaApi()
        const data = res.data?.data || res.data || {}
        const nextKey = data.captcha_key || data.key || ''
        const nextImage = data.captcha_image || data.image || data.url || ''

        if (!nextKey || !nextImage) {
            throw new Error('图形验证码返回数据不完整')
        }

        captchaKey.value = nextKey
        captchaImage.value = nextImage
        passwordForm.value.captcha_code = ''
        phoneForm.value.captcha_code = ''
    } catch (error: any) {
        captchaKey.value = ''
        captchaImage.value = ''
        captchaError.value = getErrorMessage(error) || '验证码加载失败'
    } finally {
        captchaLoading.value = false
    }
}

const saveLoginDataAndEnter = async (loginData: any) => {
    const token = loginData.access || loginData.token

    if (!token) {
        ElMessage.error('登录成功但未返回 token，请检查后端登录接口')
        return
    }

    // 登录态写入当前标签页，避免复制标签后切换角色造成菜单和角色互相覆盖。
    saveAuthState(loginData)

    try {
        // 登录成功与进入后台分开提示，避免接口成功后路由异常又误报“登录失败”。
        await router.push('/dashboard')
        refreshBrowserTitle()
        ElMessage.success('登录成功')
    } catch {
        ElMessage.error('登录成功，但进入后台失败，请检查路由或菜单配置')
    }
}

const handlePasswordLogin = async () => {
    // 密码登录必须先完成本地必填校验，减少无效接口请求。
    if (!passwordForm.value.username) {
        ElMessage.warning('请输入用户名')
        return
    }

    if (!passwordForm.value.password) {
        ElMessage.warning('请输入密码')
        return
    }

    if (!passwordForm.value.captcha_code) {
        ElMessage.warning('请输入图形验证码')
        return
    }

    if (!captchaKey.value) {
        ElMessage.warning('图形验证码未加载，请点击刷新')
        return
    }

    loading.value = true

    let loginData: any = null

    try {
        const res = await loginApi({
            username: passwordForm.value.username,
            password: passwordForm.value.password,
            captcha_key: captchaKey.value,
            captcha_code: passwordForm.value.captcha_code,
        })

        if (res.data.code !== 200) {
            ElMessage.error(getResponseMessage(res.data, '账号不存在或密码错误'))
            await loadCaptcha()
            return
        }

        loginData = res.data.data || {}
    } catch (error: any) {
        ElMessage.error(getErrorMessage(error))
        await loadCaptcha()
        return
    } finally {
        loading.value = false
    }

    await saveLoginDataAndEnter(loginData)
}

const sendLoginSmsCode = async () => {
    // 倒计时期间直接拦截，避免用户连点导致短信接口被限流。
    if (smsCountdown.value > 0 || isSendingSms.value) {
        return
    }

    if (!phoneForm.value.phone) {
        ElMessage.warning('请输入手机号')
        return
    }

    if (!phoneForm.value.captcha_code) {
        ElMessage.warning('请输入图形验证码')
        return
    }

    if (!captchaKey.value) {
        ElMessage.warning('图形验证码未加载，请点击刷新')
        return
    }

    isSendingSms.value = true

    try {
        const res = await sendSmsCodeApi({
            phone: phoneForm.value.phone,
            purpose: 'login',
            captcha_key: captchaKey.value,
            captcha_code: phoneForm.value.captcha_code,
        })

        if (res.data.code !== 200) {
            ElMessage.error(getResponseMessage(res.data, '短信验证码发送失败'))
            await loadCaptcha()
            return
        }

        if (res.data.data?.debug_code) {
            phoneForm.value.sms_code = res.data.data.debug_code
            ElMessage.success(`短信验证码：${res.data.data.debug_code}`)
        } else {
            ElMessage.success('短信验证码已发送')
        }

        startSmsCountdown(res.data.data?.cooldown_seconds || 60)
        await loadCaptcha()
    } catch (error: any) {
        ElMessage.error(getErrorMessage(error))
        await loadCaptcha()
    } finally {
        isSendingSms.value = false
    }
}

const handlePhoneLogin = async () => {
    // 手机号登录在短信已校验的基础上提交，不再重复要求图形验证码。
    if (!phoneForm.value.phone) {
        ElMessage.warning('请输入手机号')
        return
    }

    if (!phoneForm.value.sms_code) {
        ElMessage.warning('请输入短信验证码')
        return
    }

    loading.value = true

    let loginData: any = null

    try {
        const res = await phoneLoginApi({
            phone: phoneForm.value.phone,
            sms_code: phoneForm.value.sms_code,
        })

        if (res.data.code !== 200) {
            ElMessage.error(getResponseMessage(res.data, '手机号或短信验证码错误'))
            return
        }

        loginData = res.data.data || {}
    } catch (error: any) {
        ElMessage.error(getErrorMessage(error))
        return
    } finally {
        loading.value = false
    }

    await saveLoginDataAndEnter(loginData)
}

const handleLogin = () => {
    // 入口按钮根据当前登录方式分发，模板里只需要绑定一个方法。
    if (loginMode.value === 'phone') {
        handlePhoneLogin()
        return
    }

    handlePasswordLogin()
}

const goRegister = () => {
    router.push('/register')
}

const goForgotPassword = () => {
    router.push('/forgot-password')
}

onMounted(() => {
    loadCaptcha()
})

onBeforeUnmount(() => {
    clearSmsTimer()
})
</script>

<template>
    <div class="login-page">
        <div class="login-card">
            <div class="login-title">社区物业管理系统</div>

            <div class="login-subtitle">用户登录</div>

            <el-segmented
                v-model="loginMode"
                class="login-mode"
                :options="[
                    { label: '密码登录', value: 'password' },
                    { label: '手机号登录', value: 'phone' },
                ]"
            />

            <el-form label-width="0">
                <el-form-item v-if="loginMode === 'password'">
                    <el-input
                        v-model="passwordForm.username"
                        placeholder="请输入用户名或手机号"
                        size="large"
                        clearable
                    />
                </el-form-item>

                <el-form-item v-if="loginMode === 'password'">
                    <el-input
                        v-model="passwordForm.password"
                        placeholder="请输入密码"
                        type="password"
                        size="large"
                        show-password
                        clearable
                        @keyup.enter="handleLogin"
                    />
                </el-form-item>

                <el-form-item v-if="loginMode === 'phone'">
                    <el-input
                        v-model="phoneForm.phone"
                        placeholder="请输入手机号"
                        size="large"
                        maxlength="11"
                        clearable
                    />
                </el-form-item>

                <el-form-item>
                    <div class="captcha-row">
                        <el-input
                            v-if="loginMode === 'password'"
                            v-model="passwordForm.captcha_code"
                            placeholder="图形验证码"
                            size="large"
                            maxlength="4"
                            clearable
                            @keyup.enter="handleLogin"
                        />

                        <el-input
                            v-else
                            v-model="phoneForm.captcha_code"
                            placeholder="图形验证码"
                            size="large"
                            maxlength="4"
                            clearable
                        />

                        <button
                            type="button"
                            class="captcha-box"
                            :class="{ loading: captchaLoading, error: captchaError }"
                            title="点击刷新验证码"
                            @click="loadCaptcha"
                        >
                            <img
                                v-if="captchaImage"
                                class="captcha-img"
                                :src="captchaImage"
                                alt="图形验证码"
                            >
                            <span v-else>{{ captchaLoading ? '加载中' : '点击刷新' }}</span>
                        </button>
                    </div>
                    <p v-if="captchaError" class="captcha-error">{{ captchaError }}</p>
                </el-form-item>

                <el-form-item v-if="loginMode === 'phone'">
                    <div class="sms-row">
                        <el-input
                            v-model="phoneForm.sms_code"
                            placeholder="请输入短信验证码"
                            size="large"
                            maxlength="6"
                            clearable
                            @keyup.enter="handleLogin"
                        />

                        <el-button
                            size="large"
                            :disabled="smsCountdown > 0 || isSendingSms"
                            :loading="isSendingSms"
                            @click="sendLoginSmsCode"
                        >
                            {{ smsButtonText }}
                        </el-button>
                    </div>
                </el-form-item>

                <el-form-item>
                    <el-button
                        type="primary"
                        size="large"
                        class="login-button"
                        :loading="loading"
                        @click="handleLogin"
                    >
                        登录
                    </el-button>
                </el-form-item>
            </el-form>

            <div class="login-links">
                <el-button link type="primary" @click="goRegister"> 立即注册 </el-button>

                <el-button link type="primary" @click="goForgotPassword"> 找回密码 </el-button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.login-page {
    /* 铺满整个屏幕 */
    width: 100vw;
    height: 100vh;
    /* 登录卡片居中 */
    display: flex;
    justify-content: center;
    align-items: center;

    /* 设置背景图片 */
    background-image: url('@/views/image/background.png');

    /* 居中、不重复、等比例缩放铺满 */
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
}

.login-card {
    width: 400px;
    padding: 36px 40px;
    border: none;
    border-radius: 10px;
    /* 半透明效果 */
    background: rgba(255, 255, 255, 0.28);
    /* 毛玻璃效果 */
    backdrop-filter: blur(10px);
    box-shadow: 0 12px 32px rgb(0 0 0 / 18%);
}

.login-title {
    text-align: center;
    font-size: 24px;
    font-weight: 700;
    color: #303133;
    margin-bottom: 8px;
}

.login-subtitle {
    text-align: center;
    font-size: 15px;
    color: #909399;
    margin-bottom: 28px;
}

.login-button {
    width: 100%;
}

.login-mode {
    width: 100%;
    margin-bottom: 18px;
}

.captcha-row,
.sms-row {
    display: flex;
    width: 100%;
    gap: 12px;
    align-items: center;
}

.captcha-row :deep(.el-input) {
    flex: 1 1 auto;
    min-width: 0;
}

.captcha-box {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 120px;
    height: 42px;
    flex: 0 0 120px;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    cursor: pointer;
    background: #f5f7fa;
    color: #409eff;
    font-family: inherit;
    font-size: 13px;
    font-weight: 600;
    line-height: 20px;
    overflow: hidden;
    padding: 0;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.captcha-box:hover,
.captcha-box:focus-visible {
    border-color: #409eff;
    box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.12);
    outline: none;
}

.captcha-box.loading {
    color: #909399;
    cursor: wait;
}

.captcha-box.error {
    color: #f56c6c;
    border-color: #fbc4c4;
    background: #fef0f0;
}

.captcha-img {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.captcha-error {
    margin: 6px 0 0;
    color: #f56c6c;
    font-size: 12px;
    line-height: 18px;
}

.login-links {
    display: flex;
    justify-content: center;
    gap: 16px;
    margin-top: 8px;
}
</style>
