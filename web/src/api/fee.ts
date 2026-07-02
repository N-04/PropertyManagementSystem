// 文件说明：封装 src/api/fee.ts 对应后端接口请求，供页面组件调用。
import request from '@/utils/request'

type ListParams = Record<string, unknown> & {
    page_size?: number | string
}

type FeePayload = Record<string, unknown>

// 列表参数保护分块：费用列表数据量较大，前端统一限制单页数量。
const clampListParams = (params: ListParams = {}) => {
    if (!params.page_size) return params

    // 列表接口统一限制前端请求上限，避免页面传 1000 造成大响应。
    const pageSize = Number(params.page_size)

    return {
        ...params,
        page_size: Number.isFinite(pageSize) ? Math.min(Math.max(pageSize, 1), 100) : 100,
    }
}

// 费用账单列表：支持缴费状态、费用类型、日期和关键字筛选。
export function getFeeList(params?: ListParams) {
    return request({
        url: '/fee/list/',
        method: 'get',
        params: clampListParams(params),
    })
}

// 新增费用账单：主要供财务管理端调用。
export function createFee(data: FeePayload) {
    return request({
        url: '/fee/create/',
        method: 'post',
        data,
    })
}

// 缴费操作：业主或财务侧确认支付后更新账单状态。
export const payFee = (id: number, data: { payment_method: string }) => {
    return request.put(`/fee/pay/${id}/`, data)
}

// 发送缴费提醒：后端会根据账单找到对应业主并写入消息中心。
export const remindFee = (id: number) => {
    return request.post(`/fee/remind/${id}/`)
}
