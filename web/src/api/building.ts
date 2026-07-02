// 文件说明：封装 src/api/building.ts 对应后端接口请求，供页面组件调用。
import request from '@/utils/request'

// 楼栋列表
export function getBuildingList(params: any = {}) {
    return request({
        url: '/building/list/',
        method: 'get',
        params,
    })
}

// 创建楼栋
export function createBuilding(data: any) {
    return request({
        url: '/building/create/',
        method: 'post',
        data,
    })
}
