// 文件说明：封装 src/api/community.ts 对应后端接口请求，供页面组件调用。
import request from '@/utils/request'

export function getCommunityList() {
    return request({
        url: '/community/list/',
        method: 'get',
    })
}
