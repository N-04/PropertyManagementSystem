// 文件说明：封装 src/api/unit.ts 对应后端接口请求，供页面组件调用。
import request from '@/utils/request'

// 单元列表
export function getUnitList(params: any = {}) {
    return request({
        url: '/unit/list/',
        method: 'get',
        params,
    })
}
