// 文件说明：封装 src/api/auth.ts 对应后端接口请求，供页面组件调用。
import request from '@/utils/request'

// 登录接口
export function loginApi(data: any) {
    return request.post('/auth/login/', data)
}

// 手机号验证码登录
export function phoneLoginApi(data: { phone: string; sms_code: string }) {
    return request.post('/auth/login/phone/', data)
}

// 获取图形验证码
export function getCaptchaApi() {
    return request.get('/auth/captcha/')
}

// 获取短信验证码
export function sendSmsCodeApi(data: {
    phone: string
    purpose: 'register' | 'reset_password' | 'login'
    captcha_key: string
    captcha_code: string
}) {
    return request.post('/auth/sms-code/', data)
}

// 注册
export function registerApi(data: {
    phone: string
    real_name: string
    id_card: string
    password: string
    confirm_password: string
    captcha_key: string
    captcha_code: string
    sms_code: string
    agreed: boolean
}) {
    return request.post('/auth/register/', data)
}

// 找回密码
export function resetPasswordApi(data: {
    phone: string
    sms_code: string
    password: string
    confirm_password: string
}) {
    return request.post('/auth/password/reset/', data)
}

// 退出登录
export function logoutApi(refresh: string) {
    return request.post('/auth/logout/', {
        refresh,
    })
}
