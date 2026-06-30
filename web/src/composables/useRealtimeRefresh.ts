// 文件说明：为页面提供统一的首次加载、定时刷新、页面重新可见和跨标签数据变化刷新能力。
import { onBeforeUnmount, onMounted, ref } from 'vue'
import {
    DATA_REFRESH_EVENT,
    DATA_REFRESH_STORAGE_KEY,
    dataRefreshScopeMatches,
    type DataRefreshDetail,
} from '@/utils/dataRefresh'

type RefreshReason = 'mounted' | 'manual' | 'interval' | 'visible' | 'focus' | 'event' | 'storage'

type RealtimeRefreshOptions = {
    scope?: string | string[]
    immediate?: boolean
    intervalMs?: number
    refreshWhenVisible?: boolean
    refreshOnWindowFocus?: boolean
    events?: string[]
    storageKeys?: string[]
}

export function useRealtimeRefresh(
    refresh: (reason: RefreshReason, event?: Event) => Promise<void> | void,
    options: RealtimeRefreshOptions = {},
) {
    // 刷新状态分块：调用方可展示 loading、最近更新时间和最近一次错误。
    const loading = ref(false)
    const lastUpdatedAt = ref('')
    const error = ref<unknown>(null)
    const scopes = Array.isArray(options.scope)
        ? options.scope
        : [options.scope || 'all']
    const customEvents = options.events || []
    const customStorageKeys = options.storageKeys || []
    const immediate = options.immediate !== false
    const refreshWhenVisible = options.refreshWhenVisible !== false
    const refreshOnWindowFocus = options.refreshOnWindowFocus !== false
    let timer: ReturnType<typeof window.setInterval> | null = null
    let destroyed = false
    let activeRequestId = 0

    const runRefresh = async (reason: RefreshReason = 'manual', event?: Event) => {
        // 组件卸载后忽略后续刷新，避免异步请求回写已经销毁的页面状态。
        if (destroyed) {
            return
        }

        // 只接受最后一次请求结果，防止频繁刷新时旧响应覆盖新数据。
        const requestId = ++activeRequestId
        loading.value = true

        try {
            await refresh(reason, event)

            if (requestId === activeRequestId) {
                lastUpdatedAt.value = new Date().toLocaleString('zh-CN', { hour12: false })
                error.value = null
            }
        } catch (currentError) {
            if (requestId === activeRequestId) {
                error.value = currentError
            }
        } finally {
            if (requestId === activeRequestId) {
                loading.value = false
            }
        }
    }

    const handleDataRefresh = (event: Event) => {
        // 全局数据刷新事件按 scope 匹配，避免一个模块变更触发所有页面重载。
        const detail = (event as CustomEvent<DataRefreshDetail>).detail

        if (!dataRefreshScopeMatches(scopes, detail?.scope || 'all')) {
            return
        }

        runRefresh('event', event)
    }

    const handleCustomEvent = (event: Event) => {
        runRefresh('event', event)
    }

    const handleStorage = (event: StorageEvent) => {
        // localStorage 事件用于跨浏览器标签同步刷新。
        if (event.key === DATA_REFRESH_STORAGE_KEY) {
            try {
                const detail = event.newValue ? JSON.parse(event.newValue) as DataRefreshDetail : null

                if (!dataRefreshScopeMatches(scopes, detail?.scope || 'all')) {
                    return
                }
            } catch {
                return
            }

            runRefresh('storage', event)
            return
        }

        if (customStorageKeys.includes(event.key || '')) {
            runRefresh('storage', event)
        }
    }

    const handleVisibilityChange = () => {
        if (refreshWhenVisible && document.visibilityState === 'visible') {
            runRefresh('visible')
        }
    }

    const handleFocus = () => {
        if (refreshOnWindowFocus) {
            runRefresh('focus')
        }
    }

    onMounted(() => {
        // 生命周期分块：挂载时注册事件、定时器和可见性刷新。
        window.addEventListener(DATA_REFRESH_EVENT, handleDataRefresh)
        window.addEventListener('storage', handleStorage)
        document.addEventListener('visibilitychange', handleVisibilityChange)
        window.addEventListener('focus', handleFocus)
        customEvents.forEach((eventName) => window.addEventListener(eventName, handleCustomEvent))

        if (options.intervalMs && options.intervalMs > 0) {
            timer = window.setInterval(() => {
                if (document.visibilityState !== 'hidden') {
                    runRefresh('interval')
                }
            }, options.intervalMs)
        }

        if (immediate) {
            runRefresh('mounted')
        }
    })

    onBeforeUnmount(() => {
        // 卸载时清理事件和定时器，避免离开页面后仍持续请求接口。
        destroyed = true
        window.removeEventListener(DATA_REFRESH_EVENT, handleDataRefresh)
        window.removeEventListener('storage', handleStorage)
        document.removeEventListener('visibilitychange', handleVisibilityChange)
        window.removeEventListener('focus', handleFocus)
        customEvents.forEach((eventName) => window.removeEventListener(eventName, handleCustomEvent))

        if (timer) {
            window.clearInterval(timer)
            timer = null
        }
    })

    return {
        loading,
        lastUpdatedAt,
        error,
        refreshNow: runRefresh,
    }
}
