// 文件说明：统一广播业务数据变化，供工作台、列表页和顶部消息统计实时刷新。

export const DATA_REFRESH_EVENT = 'property-management-data-refresh'
export const DATA_REFRESH_STORAGE_KEY = 'propertyManagementDataRefresh'

export type DataRefreshDetail = {
    // scope 标识业务域，例如 fees、repairs、dashboard。
    scope: string
    // source 标识触发来源，便于排查是手动刷新还是写操作广播。
    source: string
    // version 每次变化，保证跨标签页 storage 事件稳定触发。
    version: string
}

// 刷新广播分块：当前标签页用 CustomEvent，其他标签页用 localStorage 同步。
export const emitDataRefresh = (scope = 'all', source = 'manual', persist = true) => {
    // SSR 或测试环境没有 window 时直接跳过广播。
    if (typeof window === 'undefined') {
        return
    }

    // version 保证每次写入 localStorage 都会触发其他标签页的 storage 事件。
    const detail: DataRefreshDetail = {
        scope,
        source,
        version: `${Date.now()}-${Math.random().toString(36).slice(2)}`,
    }

    window.dispatchEvent(new CustomEvent<DataRefreshDetail>(DATA_REFRESH_EVENT, { detail }))

    // persist=false 只刷新当前标签页，适合不需要跨标签同步的轻量场景。
    if (!persist) {
        return
    }

    try {
        window.localStorage.setItem(DATA_REFRESH_STORAGE_KEY, JSON.stringify(detail))
    } catch {
        // localStorage 不可写时，当前标签页的事件仍然可以完成即时刷新。
    }
}

// 作用域匹配分块：页面声明自己关心的业务域，只响应相关刷新。
export const dataRefreshScopeMatches = (targetScopes: string[], scope = 'all') => {
    // all 是全局刷新；页面声明 all 时也接收任意业务域刷新。
    return scope === 'all' || targetScopes.includes('all') || targetScopes.includes(scope)
}
