// 文件说明：封装 src/api/log.ts 对应后端接口请求，供页面组件调用。
import request from '@/utils/request'

export function getOperationLogList() {
    return request.get('/log/operation/list/')
}

export function getLoginLogList() {
    return request.get('/log/login/list/')
}
