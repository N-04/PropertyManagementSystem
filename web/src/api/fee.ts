// 文件说明：封装 src/api/fee.ts 对应后端接口请求，供页面组件调用。
import request from '@/utils/request'

// 物业费列表
export function getFeeList(params?: any) {
    return request({
        url: '/fee/list/',
        method: 'get',
        params,
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
