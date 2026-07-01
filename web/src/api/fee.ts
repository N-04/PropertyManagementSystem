// 文件说明：封装 src/api/fee.ts 对应后端接口请求，供页面组件调用。
import request from '@/utils/request'

const clampListParams = (params: any = {}) => {
    if (!params.page_size) return params

    // 列表接口统一限制前端请求上限，避免页面传 1000 造成大响应。
    const pageSize = Number(params.page_size)

    return {
        ...params,
        page_size: Number.isFinite(pageSize) ? Math.min(Math.max(pageSize, 1), 100) : 100,
    }
}

// 物业费列表
export function getFeeList(params?: any) {
    return request({
        url: '/fee/list/',
        method: 'get',
        params: clampListParams(params),
    })
}

// 新增物业费
export function createFee(data: any) {
    return request({
        url: '/fee/create/',
        method: 'post',
        data,
    })
}

// 缴费
export const payFee = (id: number, data: { payment_method: string }) => {
    return request.put(`/fee/pay/${id}/`, data)
}

// 发送缴费提醒给账单对应业主
export const remindFee = (id: number) => {
    return request.post(`/fee/remind/${id}/`)
}
