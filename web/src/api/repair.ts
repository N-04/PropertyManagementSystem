// 文件说明：封装 src/api/repair.ts 对应后端接口请求，供页面组件调用。
import request from '@/utils/request'

const clampListParams = (params: any = {}) => {
    const pageSize = Number(params.page_size || 100)

    // 报修列表作为高频工作台接口，统一把 page_size 控制在后端允许范围内。
    return {
        ...params,
        page_size: Number.isFinite(pageSize) ? Math.min(Math.max(pageSize, 1), 100) : 100,
    }
}

// 获取报修列表
export function getRepairList(params: any) {
    return request.get('/repair/list/', {
        params: clampListParams(params),
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
