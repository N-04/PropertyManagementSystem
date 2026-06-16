// 文件说明：封装 src/api/house.ts 对应后端接口请求，供页面组件调用。
import request from '@/utils/request'

export function getHouseList() {
    return request.get('/house/list/')
}
export function createHouse(data: any) {
    return request.post('/house/create/', data)
}
