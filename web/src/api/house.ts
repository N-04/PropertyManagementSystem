// 文件说明：封装 src/api/house.ts 对应后端接口请求，供页面组件调用。
import request from '@/utils/request'

export function getHouseList(params: any = {}) {
    return request.get('/house/list/', {
        params,
    })
}
export function createHouse(data: any) {
    return request.post('/house/create/', data)
}
