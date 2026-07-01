// 文件说明：封装前端通用 axios 请求、JWT 携带和 401 自动刷新逻辑。
import axios, { type AxiosError, type InternalAxiosRequestConfig } from 'axios'
import {
    clearAuthState,
    getStoredRefresh,
    getStoredToken,
    setAuthItem,
} from '@/utils/authState'
import { emitDataRefresh } from '@/utils/dataRefresh'
import { apiBaseURL } from '@/utils/url'

const baseURL = apiBaseURL

type RetriableRequestConfig = InternalAxiosRequestConfig & {
    _retry?: boolean
}

// 请求实例分块：所有业务接口统一走同一个 baseURL、超时和拦截器。
const request = axios.create({
    baseURL,
    timeout: 5000,
})

// 多个接口同时发现 token 过期时，共用同一次 refresh 请求，避免刷新风暴。
let refreshTokenPromise: Promise<string> | null = null

// 公共接口不需要携带 access token，也不参与 401 自动刷新重试。
const publicRequestPaths = [
    '/auth/login/',
    '/auth/login/phone/',
    '/auth/captcha/',
    '/auth/sms-code/',
    '/auth/register/',
    '/auth/password/reset/',
    '/auth/token/refresh/',
]

// 请求路径规范化分块：拦截器只比较接口路径，不受 baseURL 和 query 参数影响。
const normalizeRequestPath = (url = '') => {
    if (url.startsWith(baseURL)) {
        return url.slice(baseURL.length).split('?')[0] ?? ''
    }

    return url.split('?')[0] ?? ''
}

// 公开接口判断分块：登录、注册和刷新 token 自身不能被认证拦截器二次处理。
const isPublicOrRefreshRequest = (url = '') => {
    return publicRequestPaths.includes(normalizeRequestPath(url))
}

const mutationMethods = new Set(['post', 'put', 'patch', 'delete'])

// 写操作刷新范围映射：把后端资源路径转换成前端页面关心的数据域。
const refreshScopeRules: Array<{ pattern: string; scopes: string[] }> = [
    { pattern: '/fee/', scopes: ['fees', 'dashboard', 'messages'] },
    { pattern: '/repair/', scopes: ['repairs', 'dashboard', 'messages'] },
    { pattern: '/complaint/', scopes: ['complaints', 'dashboard', 'messages'] },
    { pattern: '/visitor/', scopes: ['visitors', 'dashboard', 'messages'] },
    { pattern: '/notice/', scopes: ['notices', 'dashboard', 'messages'] },
    { pattern: '/parking/', scopes: ['parking', 'dashboard', 'fees', 'messages'] },
    { pattern: '/car/', scopes: ['cars', 'dashboard'] },
    { pattern: '/house/', scopes: ['houses', 'dashboard'] },
    { pattern: '/owner/', scopes: ['owners', 'dashboard'] },
    { pattern: '/user/', scopes: ['users', 'owners', 'dashboard'] },
    { pattern: '/role/', scopes: ['roles', 'menus', 'users', 'dashboard'] },
    { pattern: '/permission/', scopes: ['permissions', 'roles'] },
    { pattern: '/menu/', scopes: ['menus', 'dashboard'] },
    { pattern: '/community/', scopes: ['community', 'dashboard'] },
    { pattern: '/building/', scopes: ['community', 'houses', 'dashboard'] },
    { pattern: '/unit/', scopes: ['community', 'houses', 'dashboard'] },
    { pattern: '/upload/', scopes: ['profile', 'dashboard'] },
    { pattern: '/chat/', scopes: ['messages', 'dashboard'] },
    { pattern: '/log/', scopes: ['logs'] },
]

const getDataRefreshScopes = (url = '') => {
    const path = normalizeRequestPath(url)
    // 一个接口可能影响多个页面模块，所以按路径聚合所有命中的刷新域。
    const matchedScopes = refreshScopeRules
        .filter((rule) => path.includes(rule.pattern))
        .flatMap((rule) => rule.scopes)

    if (!matchedScopes.length) {
        matchedScopes.push('dashboard')
    }

    // 后端会为不少写操作生成审计日志，统一补一条 logs 刷新，避免日志页刷新后滞后。
    matchedScopes.push('logs')

    return Array.from(new Set(matchedScopes))
}

// 写操作广播判断分块：只有真正修改数据的成功请求才触发页面自动刷新。
const shouldBroadcastDataRefresh = (response: any) => {
    const method = String(response.config?.method || '').toLowerCase()

    if (!mutationMethods.has(method) || isPublicOrRefreshRequest(response.config?.url)) {
        return false
    }

    const businessCode = response.data?.code

    return businessCode === undefined || businessCode === 200
}

// 登录态失效处理分块：清掉本地状态并回到登录页。
const redirectToLogin = () => {
    clearAuthState()

    if (window.location.pathname !== '/login') {
        window.location.href = '/login'
    }
}

// access token 刷新分块：用 refresh token 换取新 access token。
const requestNewAccessToken = async () => {
    const refresh = getStoredRefresh()

    if (!refresh) {
        throw new Error('缺少 refresh token')
    }

    // 用独立 axios 请求刷新 token，避免进入当前 request 实例的 401 拦截循环。
    const res = await axios.post(`${baseURL}/auth/token/refresh/`, {
        refresh,
    })
    const token = res.data?.access || res.data?.token || res.data?.data?.access || res.data?.data?.token
    const nextRefresh = res.data?.refresh || res.data?.data?.refresh

    if (!token) {
        throw new Error('刷新 token 接口未返回 access token')
    }

    setAuthItem('token', token, true, true)

    if (nextRefresh) {
        // 后端开启 refresh token 轮换后，必须保存新 refresh，否则下一次刷新会使用已黑名单的旧 token。
        setAuthItem('refresh', nextRefresh, true, true)
    }

    return token
}

// 刷新并发控制分块：同一时刻多个 401 只触发一次 refresh 请求。
const getFreshAccessToken = () => {
    if (!refreshTokenPromise) {
        refreshTokenPromise = requestNewAccessToken().finally(() => {
            refreshTokenPromise = null
        })
    }

    return refreshTokenPromise
}

// JWT 解析分块：只解析 exp 等公开 payload，不在前端验证签名。
const decodeJwtPayload = (token: string) => {
    try {
        const payload = token.split('.')[1]

        if (!payload) {
            return null
        }

        const normalizedPayload = payload.replace(/-/g, '+').replace(/_/g, '/')
        const paddedPayload = normalizedPayload.padEnd(
            normalizedPayload.length + ((4 - normalizedPayload.length % 4) % 4),
            '='
        )

        return JSON.parse(window.atob(paddedPayload))
    } catch {
        return null
    }
}

// token 过期判断分块：预留 leeway，避免请求刚发出 token 就过期。
const isAccessTokenExpiring = (token: string, leewaySeconds = 30) => {
    const payload = decodeJwtPayload(token)
    const exp = Number(payload?.exp || 0)

    if (!exp) {
        return false
    }

    return exp * 1000 <= Date.now() + leewaySeconds * 1000
}

const setAuthorizationHeader = (config: InternalAxiosRequestConfig, token: string) => {
    config.headers.Authorization = `Bearer ${token}`
}

// 请求拦截器：优先使用未过期 access token，临近过期时静默刷新。
request.interceptors.request.use(async (config) => {
    if (isPublicOrRefreshRequest(config.url)) {
        return config
    }

    const token = getStoredToken()
    const refresh = getStoredRefresh()

    if (token && !isAccessTokenExpiring(token)) {
        setAuthorizationHeader(config, token)
        return config
    }

    if (refresh) {
        try {
            const freshToken = await getFreshAccessToken()
            setAuthorizationHeader(config, freshToken)
            return config
        } catch (refreshError) {
            redirectToLogin()
            return Promise.reject(refreshError)
        }
    }

    if (token) {
        setAuthorizationHeader(config, token)
    }

    return config
})

request.interceptors.response.use(
    (response) => {
        if (shouldBroadcastDataRefresh(response)) {
            // 写操作成功后异步广播，避免阻塞当前接口响应。
            window.setTimeout(() => {
                getDataRefreshScopes(response.config?.url).forEach((scope) => {
                    emitDataRefresh(scope, 'mutation')
                })
            }, 0)
        }

        return response
    },
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
            // 401 重试只执行一次；刷新成功后带新 token 重新发起原请求。
            const token = await getFreshAccessToken()
            originalConfig.headers.Authorization = `Bearer ${token}`

            return request(originalConfig)
        } catch (refreshError) {
            redirectToLogin()
            return Promise.reject(refreshError)
        }
    }
)

export default request
