// 文件说明：封装 src/api/notice.ts 对应后端接口请求，供页面组件调用。
import request from '@/utils/request'

export function getNoticeList() {
    return request({
        url: '/notice/list/',
        method: 'get',
    })
}

export function createNotice(data: any) {
    return request({
        url: '/notice/create/',
        method: 'post',
        data,
    })
}

export function updateNotice(id: number, data: any) {
    return request({
        url: `/notice/update/${id}/`,
        method: 'put',
        data,
    })
}

export function deleteNotice(id: number) {
    return request({
        url: `/notice/delete/${id}/`,
        method: 'delete',
    })
}

export function getNoticeDetail(id: number) {
    return request({
        url: `/notice/detail/${id}/`,
        method: 'get',
    })
}
