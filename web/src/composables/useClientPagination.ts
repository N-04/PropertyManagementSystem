// 文件说明：为数据表格提供前端分页切片和页码状态。
import { computed, type Ref, ref } from 'vue'

export function useClientPagination<T>(source: Ref<T[]>, defaultPageSize = 10) {
    const page = ref(1)
    const pageSize = ref(defaultPageSize)

    const total = computed(() => source.value.length)

    const pagedData = computed(() => {
        const start = (page.value - 1) * pageSize.value

        return source.value.slice(start, start + pageSize.value)
    })

    const resetPage = () => {
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
