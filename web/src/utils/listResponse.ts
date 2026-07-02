// 文件说明：统一拆解后端列表接口，兼容数组和分页 results 两种返回结构。

type ListObject = Record<string, unknown>

const isListObject = (value: unknown): value is ListObject => {
    return typeof value === 'object' && value !== null
}

// 列表行解析分块：屏蔽后端新旧分页结构差异，页面只拿数组渲染表格。
export function extractListRows<T = ListObject>(payload: unknown): T[] {
    // 兼容后端直接返回数组、data 数组和分页 results 三种结构。
    if (Array.isArray(payload)) return payload as T[]
    if (!isListObject(payload)) return []

    if (Array.isArray(payload.results)) return payload.results as T[]
    if (Array.isArray(payload.data)) return payload.data as T[]

    const nestedData = payload.data

    if (isListObject(nestedData) && Array.isArray(nestedData.results)) {
        return nestedData.results as T[]
    }

    return []
}

// 总数解析分块：优先使用分页 total/count，老接口退回当前行数。
export function extractListTotal(payload: unknown): number {
    // 同时兼容 ResponseSuccess 外壳和直接分页对象两种返回层级。
    if (!isListObject(payload)) return 0

    const nestedData = payload.data
    const total = payload.total
        ?? payload.count
        ?? (isListObject(nestedData) ? nestedData.total : undefined)
        ?? (isListObject(nestedData) ? nestedData.count : undefined)

    if (typeof total === 'number') return total

    // 老接口没有 total 时，用行数兜底，避免分页组件显示 NaN。
    const rows = extractListRows(payload)
    return rows.length
}
