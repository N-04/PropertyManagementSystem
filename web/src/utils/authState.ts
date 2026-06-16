// 文件说明：统一管理前端登录态，避免多个浏览器标签页共用 localStorage 导致角色串号。

type AuthKey = 'token' | 'refresh' | 'username' | 'role' | 'roles' | 'permissions' | 'userInfo'

export const AUTH_STATE_CHANGED_EVENT = 'property-management-auth-state-changed'

const authKeys: AuthKey[] = ['token', 'refresh', 'username', 'role', 'roles', 'permissions', 'userInfo']
const authVersionKey = 'authVersion'

const rolePriority = [
    'super_admin',
    'admin',
    'property_admin',
    'customer_service',
    'finance_staff',
    'finance',
    'repair_staff',
    'repairer',
    'repair',
    'owner',
    'service',
]

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

const copyLocalAuthToSession = () => {
    let changed = false

    authKeys.forEach((key) => {
        const localValue = safeRead(localStorage, key)
        const sessionValue = safeRead(sessionStorage, key)

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
    const localVersion = readAuthVersion(localStorage)
    const sessionVersion = readAuthVersion(sessionStorage)

    if (localVersion === sessionVersion) {
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

export const getAuthItem = (key: AuthKey) => {
    syncSessionAuthStateFromLocal(false)

    // sessionStorage 是当前标签页独立的；localStorage 只作为老登录态和新标签页兜底。
    return safeRead(sessionStorage, key) ?? safeRead(localStorage, key) ?? ''
}

export const setAuthItem = (key: AuthKey, value: string) => {
    safeWrite(sessionStorage, key, value)
    safeWrite(localStorage, key, value)
}

export const removeAuthItem = (key: AuthKey) => {
    safeRemove(sessionStorage, key)
    safeRemove(localStorage, key)
}

export const clearAuthState = () => {
    const version = createAuthVersion()

    authKeys.forEach(removeAuthItem)
    writeAuthVersion(sessionStorage, version)
    writeAuthVersion(localStorage, version)
    notifyAuthStateChanged()
}

export const getStoredToken = () => getAuthItem('token')

export const getStoredRefresh = () => getAuthItem('refresh')

export const getStoredUsername = () => getAuthItem('username')

export const getStoredRole = () => getAuthItem('role')

export const resolveLoginRole = (loginData: any) => {
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

    setAuthItem('token', token)
    setAuthItem('refresh', loginData.refresh || '')
    setAuthItem('username', username)
    setAuthItem('role', role)
    setAuthItem('roles', JSON.stringify(loginData.roles || loginData.role_codes || loginData.user?.role_codes || []))
    writeAuthVersion(sessionStorage, version)
    writeAuthVersion(localStorage, version)
    notifyAuthStateChanged()

    return {
        token,
        role,
        username,
    }
}
