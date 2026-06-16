// 文件说明：封装 src/api/car.ts 对应后端接口请求，供页面组件调用。
import request from '@/utils/request'

export function getCarList(keyword = '') {
    return request.get('/car/list/', {
        params: {
            keyword,
        },
    })
}

export function createCar(data: any) {
    return request.post('/car/create/', data)
}

export function getCarDetail(id: number) {
    return request.get(`/car/detail/${id}/`)
}

export function updateCar(id: number, data: any) {
    return request.put(`/car/update/${id}/`, data)
}

export function deleteCar(id: number) {
    return request.delete(`/car/delete/${id}/`)
}

/**
 * 启用车辆
 */
export function enableCar(id: number) {
    return request.put(`/car/enable/${id}/`)
}

/**
 * 禁用车辆
 */
export function disableCar(id: number) {
    return request.put(`/car/disable/${id}/`)
}
