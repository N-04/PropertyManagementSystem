// 文件说明：封装 src/api/parking.ts 对应后端接口请求，供页面组件调用。
import request from '@/utils/request'

type ListParams = Record<string, unknown> & {
    page_size?: number | string
}

type ParkingPayload = Record<string, unknown>

// 列表参数保护分块：车位分区和表格都可能拉取列表，统一限制单页数量。
const clampListParams = (params: ListParams = {}) => {
    if (!params.page_size) return params

    // 车位分区也走受限分页，避免可视化区域一次性拉取过多数据。
    const pageSize = Number(params.page_size)

    return {
        ...params,
        page_size: Number.isFinite(pageSize) ? Math.min(Math.max(pageSize, 1), 100) : 100,
    }
}

// 车位列表：按 owner/available/visitor 等视图参数返回不同车位集合。
export function getParkingList(params?: ListParams) {
    return request({
        url: '/parking/list/',
        method: 'get',
        params: clampListParams(params),
    })
}

// 新增车位：物业管理员录入车位基础信息。
export function createParking(data: ParkingPayload) {
    return request({
        url: '/parking/create/',
        method: 'post',
        data,
    })
}

// 更新车位：修改绑定业主、分区、状态和售卖属性。
export function updateParking(id: number, data: ParkingPayload) {
    return request({
        url: `/parking/update/${id}/`,
        method: 'put',
        data,
    })
}

// 删除车位：管理端清理错误录入的车位数据。
export function deleteParking(id: number) {
    return request({
        url: `/parking/delete/${id}/`,
        method: 'delete',
    })
}

// 车位详情：详情页和购买确认场景复用。
export function getParkingDetail(id: number) {
    return request({
        url: `/parking/detail/${id}/`,
        method: 'get',
    })
}

// 绑定车位：业主购买或物业分配时调用。
export function bindParking(id: number, data: ParkingPayload = {}) {
    return request({
        url: `/parking/bind/${id}/`,
        method: 'put',
        data,
    })
}
