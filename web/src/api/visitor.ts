// 文件说明：封装 src/api/visitor.ts 对应后端接口请求，供页面组件调用。
import request from '@/utils/request'

type VisitorListParams = {
    keyword?: string
    status?: string
    page?: number
    page_size?: number
}

export function getVisitorList(params: VisitorListParams | string = {}) {
    const requestParams = typeof params === 'string' ? { keyword: params } : params

    return request.get('/visitor/list/', {
        // 访客列表已改为后端分页，调用方按需传 page/page_size。
        params: requestParams,
    })
}

export function createVisitor(data: any) {
    return request.post('/visitor/create/', data)
}

export function getVisitorDetail(id: number) {
    return request.get(`/visitor/detail/${id}/`)
}

export function updateVisitor(id: number, data: any) {
    return request.put(`/visitor/update/${id}/`, data)
}

export function deleteVisitor(id: number) {
    return request.delete(`/visitor/delete/${id}/`)
}
export function approveVisitor(id: number, data: any) {
    return request.put(`/visitor/approve/${id}/`, data)
}
export const enterVisitor = (id: number) => {
    return request.put(`/visitor/enter/${id}/`)
}
export const leaveVisitor = (id: number) => {
    return request.put(`/visitor/leave/${id}/`)
}
/**
 * 获取访客统计
 */
export const getVisitorStatistics = () => {
    return request.get('/dashboard/statistics/')
}
