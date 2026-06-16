// 文件说明：封装 src/api/upload.ts 对应后端接口请求，供页面组件调用。
import request from '@/utils/request'

export function uploadFile(data: FormData) {
    return request({
        url: '/upload/',

        method: 'post',

        data,

        headers: {
            'Content-Type': 'multipart/form-data',
        },
    })
}
