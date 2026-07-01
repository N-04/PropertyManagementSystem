// 文件说明：统一拆解后端列表接口，兼容数组和分页 results 两种返回结构。

// 列表行解析分块：屏蔽后端新旧分页结构差异，页面只拿数组渲染表格。
export function extractListRows(payload: any): any[] {
    // 兼容后端直接返回数组、data 数组和分页 results 三种结构。
    if (Array.isArray(payload)) return payload
    if (Array.isArray(payload?.results)) return payload.results
    if (Array.isArray(payload?.data)) return payload.data
    if (Array.isArray(payload?.data?.results)) return payload.data.results

    return []
}

// 总数解析分块：优先使用分页 total/count，老接口退回当前行数。
export function extractListTotal(payload: any): number {
    // 同时兼容 ResponseSuccess 外壳和直接分页对象两种返回层级。
    const total = payload?.total ?? payload?.count ?? payload?.data?.total ?? payload?.data?.count

    if (typeof total === 'number') return total

    // 老接口没有 total 时，用行数兜底，避免分页组件显示 NaN。
    const rows = extractListRows(payload)
    return rows.length
}
