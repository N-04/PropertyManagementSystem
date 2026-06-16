// 文件说明：封装 src/api/dashboard.ts 对应后端接口请求，供页面组件调用。
import request from '@/utils/request'

/**
 * 首页统计
 */
export function getDashboard() {
    return request({
        url: '/dashboard/',
        method: 'get',
    })
}
