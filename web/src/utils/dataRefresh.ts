// 文件说明：统一广播业务数据变化，供工作台、列表页和顶部消息统计实时刷新。

export const DATA_REFRESH_EVENT = 'property-management-data-refresh'
export const DATA_REFRESH_STORAGE_KEY = 'propertyManagementDataRefresh'

export type DataRefreshDetail = {
    scope: string
    source: string
    version: string
}

export const emitDataRefresh = (scope = 'all', source = 'manual', persist = true) => {
    if (typeof window === 'undefined') {
        return
    }

    const detail: DataRefreshDetail = {
        scope,
        source,
        version: `${Date.now()}-${Math.random().toString(36).slice(2)}`,
    }

    window.dispatchEvent(new CustomEvent<DataRefreshDetail>(DATA_REFRESH_EVENT, { detail }))

    if (!persist) {
        return
    }

    try {
        window.localStorage.setItem(DATA_REFRESH_STORAGE_KEY, JSON.stringify(detail))
    } catch {
        // localStorage 不可写时，当前标签页的事件仍然可以完成即时刷新。
    }
}

export const dataRefreshScopeMatches = (targetScopes: string[], scope = 'all') => {
    return scope === 'all' || targetScopes.includes('all') || targetScopes.includes(scope)
}
