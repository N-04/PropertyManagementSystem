// 文件说明：封装前端通用 axios 请求、JWT 携带和 401 自动刷新逻辑。
import axios, { type AxiosError, type InternalAxiosRequestConfig } from 'axios'
import {
    clearAuthState,
    getStoredRefresh,
    getStoredToken,
    setAuthItem,
} from '@/utils/authState'

const baseURL = 'http://127.0.0.1:8000/api'

type RetriableRequestConfig = InternalAxiosRequestConfig & {
    _retry?: boolean
}

// 创建 axios 实例
const request = axios.create({
    // Django 地址
    baseURL,

    // 超时时间
    timeout: 5000,
})

let refreshTokenPromise: Promise<string> | null = null

const publicRequestPaths = [
    '/login/',
    '/login/phone/',
    '/captcha/',
    '/sms-code/',
    '/register/',
    '/password/reset/',
    '/token/refresh/',
]

const normalizeRequestPath = (url = '') => {
    if (url.startsWith(baseURL)) {
        return url.slice(baseURL.length).split('?')[0] ?? ''
    }

    return url.split('?')[0] ?? ''
}

const isPublicOrRefreshRequest = (url = '') => {
    return publicRequestPaths.includes(normalizeRequestPath(url))
}

const redirectToLogin = () => {
    clearAuthState()

    if (window.location.pathname !== '/login') {
        window.location.href = '/login'
    }
}

const requestNewAccessToken = async () => {
    const refresh = getStoredRefresh()

    if (!refresh) {
        throw new Error('缺少 refresh token')
    }

    // 用独立 axios 请求刷新 token，避免进入当前 request 实例的 401 拦截循环。
    const res = await axios.post(`${baseURL}/token/refresh/`, {
        refresh,
    })
    const token = res.data?.access || res.data?.token || res.data?.data?.access || res.data?.data?.token

    if (!token) {
        throw new Error('刷新 token 接口未返回 access token')
    }

    setAuthItem('token', token)
    return token
}

const getFreshAccessToken = () => {
    if (!refreshTokenPromise) {
        refreshTokenPromise = requestNewAccessToken().finally(() => {
            refreshTokenPromise = null
        })
    }

    return refreshTokenPromise
}

// axios 请求拦截器
request.interceptors.request.use((config) => {
    // 获取 token
    const token = getStoredToken()

    // 如果 token 存在
    if (token) {
        // 自动携带 token
        config.headers.Authorization = `Bearer ${token}`
    }

    return config
})

request.interceptors.response.use(
    (response) => response,
    async (error: AxiosError) => {
        const status = error.response?.status
        const originalConfig = error.config as RetriableRequestConfig | undefined

        if (
            status !== 401
            || !originalConfig
            || originalConfig._retry
            || isPublicOrRefreshRequest(originalConfig.url)
        ) {
            return Promise.reject(error)
        }

        originalConfig._retry = true

        try {
            const token = await getFreshAccessToken()
            originalConfig.headers.Authorization = `Bearer ${token}`

            return request(originalConfig)
        } catch (refreshError) {
            redirectToLogin()
            return Promise.reject(refreshError)
        }
    }
)

// 导出
export default request
