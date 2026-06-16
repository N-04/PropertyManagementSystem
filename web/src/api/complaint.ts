// 文件说明：封装投诉建议模块接口请求。
import request from '@/utils/request'

export function getComplaintList(params?: any) {
    return request({
        url: '/complaint/list/',
        method: 'get',
        params,
    })
}

export function createComplaint(data: any) {
    return request({
        url: '/complaint/create/',
        method: 'post',
        data,
    })
}

export function updateComplaint(id: number, data: any) {
    return request({
        url: `/complaint/update/${id}/`,
        method: 'put',
        data,
    })
}

export function deleteComplaint(id: number) {
    return request({
        url: `/complaint/delete/${id}/`,
        method: 'delete',
    })
}
