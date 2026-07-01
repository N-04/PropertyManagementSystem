// 文件说明：封装 src/api/owner.ts 对应后端接口请求，供页面组件调用。
import request from '@/utils/request'

export function getOwnerList(keyword = '') {
    return request.get('/owner/list/', {
        params: {
            keyword,
            page_size: 100,
        },
    })
}
export function createOwner(data: any) {
    return request.post('/owner/create/', data)
}

export function updateOwner(id: number, data: any) {
    return request.put(`/owner/update/${id}/`, data)
}

export function deleteOwner(id: number) {
    return request.delete(`/owner/delete/${id}/`)
}

export function getOwnerDetail(id: number) {
    return request.get(`/owner/detail/${id}/`)
}
