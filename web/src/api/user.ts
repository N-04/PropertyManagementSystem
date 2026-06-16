// 文件说明：封装 src/api/user.ts 对应后端接口请求，供页面组件调用。
import request from '@/utils/request'

export function getUserInfo() {
    return request.get('/user/info/')
}

export function updateCurrentUserProfile(data: any) {
    return request.put('/user/profile/', data)
}

export function updateCurrentUserPassword(data: any) {
    return request.put('/user/password/', data)
}

export const getUserList = (params: any = {}) => {
    return request.get('/user/list/', {
        params,
    })
}

export const createUser = (data: any) => {
    return request.post('/user/create/', data)
}

export const deleteUser = (id: number) => {
    return request.delete(`/user/delete/${id}/`)
}

export const getUserDetail = (id: number) => {
    return request.get(`/user/info/${id}/`)
}

// =====================================================
// 修改用户
// =====================================================
export const updateUser = (id: number, data: any) => {
    return request.put(
        // 接口地址
        `/user/info/${id}/`,

        // 提交数据
        data
    )
}

// 用户审核：approved 通过审核，rejected 禁用/驳回
export const auditUser = (id: number, auditStatus: 'approved' | 'rejected') => {
    return request.put(`/user/audit/${id}/`, {
        audit_status: auditStatus,
    })
}
