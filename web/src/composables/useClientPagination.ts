// 文件说明：为数据表格提供前端分页切片和页码状态。
import { computed, type ComputedRef, type Ref, ref } from 'vue'

export function useClientPagination<T>(source: Ref<T[]> | ComputedRef<T[]>, defaultPageSize = 10) {
    // 分页状态分块：页面和每页数量交给调用方双向绑定，数据切片在 composable 内统一处理。
    const page = ref(1)
    const pageSize = ref(defaultPageSize)

    const total = computed(() => source.value.length)

    const pagedData = computed(() => {
        // 本地列表页通常一次拉取足量数据，再按当前页截取展示。
        const start = (page.value - 1) * pageSize.value

        return source.value.slice(start, start + pageSize.value)
    })

    const resetPage = () => {
        // 筛选条件变化后统一回到第一页，避免停留在没有数据的旧页码。
        page.value = 1
    }

    return {
        page,
        pageSize,
        total,
        pagedData,
        resetPage,
    }
}
