// 文件说明：封装 src/api/repair.ts 对应后端接口请求，供页面组件调用。
import request from '@/utils/request'

// 获取报修列表
export function getRepairList(params: any) {
    return request.get('/repair/list/', {
        params,
    })
}

// 新增报修
export function createRepair(data: any) {
    return request.post('/repair/create/', data)
}

// 查看报修
export function getRepairDetail(id: number) {
    return request.get(`/repair/detail/${id}/`)
}

// 修改报修状态
export function updateRepair(id: number, data: any) {
    return request.put(`/repair/update/${id}/`, data)
}

// 删除报修
export function deleteRepair(id: number) {
    return request.delete(`/repair/delete/${id}/`)
}

// 分配维修人员
export function getRepairaAssign(id: number) {
    return request.get(`/repair/assign/${id}/`)
}

// 提交维修人员分配
export function assignRepair(id: number, data: any) {
    return request.post(`/repair/assign/${id}/`, data)
}
