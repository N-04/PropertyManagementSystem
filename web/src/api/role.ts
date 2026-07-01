// 文件说明：封装 src/api/role.ts 对应后端接口请求，供页面组件调用。
// =====================================================
// 请求工具
// =====================================================
import request from '@/utils/request'

// =====================================================
// 获取角色列表
// =====================================================
export const getRoleList = (params: any = {}) => {
    // GET请求
    return request.get('/role/list/', {
        params,
    })
}

// =====================================================
// 新增角色
// =====================================================
export const createRole = (data: any) => {
    // POST请求
    return request.post('/role/create/', data)
}

// =====================================================
// 删除角色
// =====================================================

export const deleteRole = (id: number) => {
    return request.delete(`/role/delete/${id}/`)
}

// =====================================================
// 获取角色详情
// =====================================================

export const getRoleDetail = (id: number) => {
    return request.get(`/role/info/${id}/`)
}

// =====================================================
// 修改角色
// =====================================================

export const updateRole = (id: number, data: any) => {
    return request.put(
        `/role/update/${id}/`,

        data
    )
}

// 给角色分配权限
export const assignRolePermissions = (roleId: number, permissionIds: number[]) => {
    return request.post('/role/assign_permission/', {
        role_id: roleId,
        permission_ids: permissionIds,
    })
}
