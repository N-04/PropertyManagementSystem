// 文件说明：封装 src/api/parking.ts 对应后端接口请求，供页面组件调用。
import request from '@/utils/request'

const clampListParams = (params: any = {}) => {
    if (!params.page_size) return params

    // 车位分区也走受限分页，避免可视化区域一次性拉取过多数据。
    const pageSize = Number(params.page_size)

    return {
        ...params,
        page_size: Number.isFinite(pageSize) ? Math.min(Math.max(pageSize, 1), 100) : 100,
    }
}

export function getParkingList(params?: any) {
    return request({
        url: '/parking/list/',
        method: 'get',
        params: clampListParams(params),
    })
}

export function createParking(data: any) {
    return request({
        url: '/parking/create/',
        method: 'post',
        data,
    })
}

export function updateParking(id: number, data: any) {
    return request({
        url: `/parking/update/${id}/`,
        method: 'put',
        data,
    })
}

export function deleteParking(id: number) {
    return request({
        url: `/parking/delete/${id}/`,
        method: 'delete',
    })
}

export function getParkingDetail(id: number) {
    return request({
        url: `/parking/detail/${id}/`,
        method: 'get',
    })
}

export function bindParking(id: number, data: any = {}) {
    return request({
        url: `/parking/bind/${id}/`,
        method: 'put',
        data,
    })
}
