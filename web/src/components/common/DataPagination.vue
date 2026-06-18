<!-- 文件说明：统一数据列表页分页条，补充首页和尾页跳转。 -->
<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
    defineProps<{
        currentPage: number
        pageSize: number
        total: number
        pageSizes?: number[]
        background?: boolean
        layout?: string
    }>(),
    {
        pageSizes: () => [5, 10, 20, 50],
        background: true,
        layout: 'total, sizes, prev, pager, next, jumper',
    }
)

const emit = defineEmits<{
    'update:currentPage': [value: number]
    'update:pageSize': [value: number]
    'current-change': [value: number]
    'size-change': [value: number]
    change: []
}>()

const lastPage = computed(() => {
    return Math.max(1, Math.ceil(props.total / props.pageSize))
})

const isFirstPage = computed(() => props.currentPage <= 1)
const isLastPage = computed(() => props.currentPage >= lastPage.value)
const paginationLayout = computed(() => {
    return props.layout
        .split(',')
        .map((item) => item.trim())
        .filter((item) => item && item !== 'total')
        .join(', ')
})

const emitCurrentPage = (value: number) => {
    emit('update:currentPage', value)
    emit('current-change', value)
    emit('change')
}

const handleCurrentChange = (value: number) => {
    emitCurrentPage(value)
}

const handleSizeChange = (value: number) => {
    emit('update:pageSize', value)

    const nextLastPage = Math.max(1, Math.ceil(props.total / value))

    if (props.currentPage > nextLastPage) {
        emit('update:currentPage', nextLastPage)
        emit('current-change', nextLastPage)
    }

    emit('size-change', value)
    emit('change')
}

const goFirstPage = () => {
    if (isFirstPage.value) {
        return
    }

    emitCurrentPage(1)
}

const goLastPage = () => {
    if (isLastPage.value) {
        return
    }

    emitCurrentPage(lastPage.value)
}
</script>

<template>
    <div class="data-pagination">
        <el-button size="small" :disabled="isFirstPage" @click="goFirstPage">首页</el-button>

        <span class="pagination-total">共 {{ total }} 条</span>

        <el-pagination
            :current-page="currentPage"
            :page-size="pageSize"
            :page-sizes="pageSizes"
            :total="total"
            :background="background"
            :layout="paginationLayout"
            @current-change="handleCurrentChange"
            @size-change="handleSizeChange"
        />

        <el-button size="small" :disabled="isLastPage" @click="goLastPage">尾页</el-button>
    </div>
</template>

<style scoped>
.data-pagination {
    display: flex;
    align-items: center;
    /* 数据页分页统一居中，首页/尾页按钮与页码保持同一行。 */
    justify-content: center;
    gap: 12px;
    margin-top: 28px;
    flex-wrap: wrap;
}

.pagination-total {
    color: var(--text-muted);
    font-size: 14px;
    line-height: 22px;
}

.data-pagination :deep(.el-button) {
    height: 36px;
    min-width: 54px;
    padding: 0 14px;
}

.data-pagination :deep(.el-pagination) {
    gap: 10px;
}

.data-pagination :deep(.el-pagination .el-select) {
    width: 112px;
}

.data-pagination :deep(.el-pagination button),
.data-pagination :deep(.el-pager li),
.data-pagination :deep(.el-pagination__editor.el-input) {
    min-width: 36px;
    height: 36px;
}
</style>
