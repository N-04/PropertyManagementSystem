// 文件说明：封装 src/api/repair.ts 对应后端接口请求，供页面组件调用。
import request from '@/utils/request'

type ListParams = Record<string, unknown> & {
    page_size?: number | string
}

type RepairPayload = Record<string, unknown>

// 列表参数保护分块：维修工作台和列表页统一按后端分页上限取数。
const clampListParams = (params: ListParams = {}) => {
    const pageSize = Number(params.page_size || 100)

    // 报修列表作为高频工作台接口，统一把 page_size 控制在后端允许范围内。
    return {
        ...params,
        page_size: Number.isFinite(pageSize) ? Math.min(Math.max(pageSize, 1), 100) : 100,
    }
}

// 报修列表：按角色返回业主报修、维修员工单或物业管理工单。
export function getRepairList(params: ListParams) {
    return request.get('/repair/list/', {
        params: clampListParams(params),
    })
}

// 新增报修：业主提交标题、内容、图片等报修信息。
export function createRepair(data: RepairPayload) {
    return request.post('/repair/create/', data)
}

// 查看报修详情：用于进度、评价、维修结果抽屉等场景。
export function getRepairDetail(id: number) {
    return request.get(`/repair/detail/${id}/`)
}

// 修改报修状态：接单、维修中、完成、验收等状态流转共用。
export function updateRepair(id: number, data: RepairPayload) {
    return request.put(`/repair/update/${id}/`, data)
}

// 删除报修：管理侧清理无效工单时使用。
export function deleteRepair(id: number) {
    return request.delete(`/repair/delete/${id}/`)
}

// 获取派单信息：进入分配维修人员页面前拉取当前工单。
export function getRepairaAssign(id: number) {
    return request.get(`/repair/assign/${id}/`)
}

// 提交维修人员分配：物业管理员把工单指派给维修员。
export function assignRepair(id: number, data: RepairPayload) {
    return request.post(`/repair/assign/${id}/`, data)
}
