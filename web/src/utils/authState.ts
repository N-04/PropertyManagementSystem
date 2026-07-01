// 文件说明：统一管理前端登录态，避免多个浏览器标签页共用 localStorage 导致角色串号。

type AuthKey = 'token' | 'refresh' | 'username' | 'role' | 'roles' | 'permissions' | 'userInfo'

export const AUTH_STATE_CHANGED_EVENT = 'property-management-auth-state-changed'

const authKeys: AuthKey[] = ['token', 'refresh', 'username', 'role', 'roles', 'permissions', 'userInfo']
const sensitiveAuthKeys: AuthKey[] = ['token', 'refresh']
const persistedAuthKeys = authKeys.filter((key) => !sensitiveAuthKeys.includes(key))
const authVersionKey = 'authVersion'

// 角色解析分块：后端可能返回单角色或多角色，前端统一转成主角色编码。
// 多角色账号按优先级确定当前主角色，保证菜单和首页工作台选择稳定。
const rolePriority = [
    'super_admin',
    'admin',
    'property_admin',
    'finance_staff',
    'finance',
    'repair_staff',
    'repairer',
    'repair',
    'owner',
]

// Storage 安全访问分块：浏览器隐私模式或禁用存储时不让页面直接崩溃。
const safeRead = (storage: Storage, key: AuthKey) => {
    try {
        return storage.getItem(key)
    } catch {
        return null
    }
}

const safeWrite = (storage: Storage, key: AuthKey, value: string) => {
    try {
        storage.setItem(key, value)
    } catch {
        // 浏览器隐私模式下 Storage 可能不可写，忽略后让当前流程继续。
    }
}

const safeRemove = (storage: Storage, key: AuthKey) => {
    try {
        storage.removeItem(key)
    } catch {
        // Storage 不可用时无需额外处理。
    }
}

const clearPersistedSensitiveAuth = () => {
    // refresh/access token 不再落 localStorage；这里同时清理旧版本遗留值。
    sensitiveAuthKeys.forEach((key) => safeRemove(localStorage, key))
}

const notifyAuthStateChanged = () => {
    if (typeof window === 'undefined') {
        return
    }

    // 通知当前标签页立即刷新角色相关显示，例如浏览器标题和菜单兜底逻辑。
    window.dispatchEvent(new CustomEvent(AUTH_STATE_CHANGED_EVENT))
}

const createAuthVersion = () => {
    return `${Date.now()}-${Math.random().toString(36).slice(2)}`
}

const readAuthVersion = (storage: Storage) => {
    try {
        return storage.getItem(authVersionKey) || ''
    } catch {
        return ''
    }
}

const writeAuthVersion = (storage: Storage, version: string) => {
    try {
        storage.setItem(authVersionKey, version)
    } catch {
        // Storage 不可写时忽略，后续仍可通过当前内存流程继续。
    }
}

const hasCurrentSessionAuth = () => {
    return Boolean(safeRead(sessionStorage, 'token') || safeRead(sessionStorage, 'refresh'))
}

// 标签页同步分块：localStorage 只作为新标签页初始化来源，当前会话以 sessionStorage 为准。
const copyLocalAuthToSession = () => {
    let changed = false

    persistedAuthKeys.forEach((key) => {
        const localValue = safeRead(localStorage, key)
        const sessionValue = safeRead(sessionStorage, key)

        // 只同步实际变更的字段，避免无意义触发当前标签页刷新。
        if (localValue === sessionValue) {
            return
        }

        changed = true

        if (localValue === null) {
            safeRemove(sessionStorage, key)
            return
        }

        safeWrite(sessionStorage, key, localValue)
    })

    const localVersion = readAuthVersion(localStorage)
    const sessionVersion = readAuthVersion(sessionStorage)

    if (localVersion !== sessionVersion) {
        changed = true
        writeAuthVersion(sessionStorage, localVersion)
    }

    return changed
}

export const isAuthStorageKey = (key: string | null) => {
    return key === authVersionKey || authKeys.includes(key as AuthKey)
}

export const syncSessionAuthStateFromLocal = (notify = true) => {
    clearPersistedSensitiveAuth()

    // 复制标签页会复制 sessionStorage；已有会话必须保持当前标签独立，不再被 localStorage 覆盖。
    if (hasCurrentSessionAuth()) {
        return false
    }

    if (!persistedAuthKeys.some((key) => safeRead(localStorage, key))) {
        return false
    }

    const changed = copyLocalAuthToSession()

    if (changed && notify) {
        notifyAuthStateChanged()
    }

    return changed
}

const roleCodeFromValue = (value: any): string => {
    if (!value) {
        return ''
    }

    if (typeof value === 'string') {
        return value
    }

    if (typeof value === 'object') {
        return value.code || value.role_code || value.role || value.value || ''
    }

    return ''
}

const collectRoleCodes = (value: any): string[] => {
    if (!value) {
        return []
    }

    if (Array.isArray(value)) {
        return value.flatMap((item) => collectRoleCodes(item))
    }

    const code = roleCodeFromValue(value)
    return code ? [code] : []
}

// 登录态读写分块：令牌只进入 sessionStorage，降低复制标签和持久化存储带来的串号风险。
export const getAuthItem = (key: AuthKey) => {
    syncSessionAuthStateFromLocal(false)

    // sessionStorage 是当前标签页独立会话；localStorage 只在当前标签没有会话时初始化。
    return safeRead(sessionStorage, key) ?? ''
}

export const setAuthItem = (key: AuthKey, value: string, persist = false, notify = false) => {
    safeWrite(sessionStorage, key, value)

    if (sensitiveAuthKeys.includes(key)) {
        safeRemove(localStorage, key)
    } else if (persist) {
        safeWrite(localStorage, key, value)
    }

    if (notify) {
        notifyAuthStateChanged()
    }
}

export const removeAuthItem = (key: AuthKey, persist = false) => {
    safeRemove(sessionStorage, key)

    if (persist) {
        safeRemove(localStorage, key)
    }
}

export const clearAuthState = () => {
    const version = createAuthVersion()

    authKeys.forEach((key) => removeAuthItem(key, true))
    writeAuthVersion(sessionStorage, version)
    writeAuthVersion(localStorage, version)
    notifyAuthStateChanged()
}

export const getStoredToken = () => getAuthItem('token')

export const getStoredRefresh = () => getAuthItem('refresh')

export const getStoredUsername = () => getAuthItem('username')

export const getStoredRole = () => getAuthItem('role')

export const resolveLoginRole = (loginData: any) => {
    // 登录接口可能返回 role、roles 或 user.role_codes，统一抽取成角色编码。
    const explicitRole = collectRoleCodes(loginData?.role || loginData?.user?.role)[0]

    if (explicitRole) {
        return explicitRole
    }

    const roleCodes = [
        ...collectRoleCodes(loginData?.roles),
        ...collectRoleCodes(loginData?.role_codes),
        ...collectRoleCodes(loginData?.user?.roles),
        ...collectRoleCodes(loginData?.user?.role_codes),
    ]
    const uniqueRoleCodes = Array.from(new Set(roleCodes))

    return rolePriority.find((item) => uniqueRoleCodes.includes(item)) || uniqueRoleCodes[0] || ''
}

export const saveAuthState = (loginData: any) => {
    const token = loginData.access || loginData.token
    const role = resolveLoginRole(loginData)
    const username = loginData.username || loginData.user?.username || ''
    const version = createAuthVersion()

    clearPersistedSensitiveAuth()

    // token 仅写入 sessionStorage，localStorage 只保存角色等非令牌元数据。
    setAuthItem('token', token, true)
    setAuthItem('refresh', loginData.refresh || '', true)
    setAuthItem('username', username, true)
    setAuthItem('role', role, true)
    setAuthItem('roles', JSON.stringify(loginData.roles || loginData.role_codes || loginData.user?.role_codes || []), true)
    writeAuthVersion(sessionStorage, version)
    writeAuthVersion(localStorage, version)
    notifyAuthStateChanged()

    return {
        token,
        role,
        username,
    }
}
