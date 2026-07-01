// 文件说明：封装 src/api/permission.ts 对应后端接口请求，供页面组件调用。
// =====================================================
// 导入 request
// =====================================================
import request from '@/utils/request'

// =====================================================
// 获取权限列表
// =====================================================
export const getPermissionList = (params: any = {}) => {
    return request.get('/permission/list/', {
        params,
    })
}

// 获取权限树/权限选项
export const getPermissionTree = () => {
    return request.get('/permission/tree/')
}
