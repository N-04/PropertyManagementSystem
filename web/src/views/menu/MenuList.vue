<!-- 文件说明：实现 src/views/menu/MenuList.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getMenuTree } from '@/api/menu'
import { useClientPagination } from '@/composables/useClientPagination'
import DataPagination from '@/components/common/DataPagination.vue'

const tableData = ref<any[]>([])
const keyword = ref('')
const loading = ref(false)
const normalizedKeyword = computed(() => keyword.value.trim().toLowerCase())
const filterMenuTree = (menus: any[]): any[] => {
    if (!normalizedKeyword.value) {
        return menus
    }

    return menus
        .map((menu) => {
            const children = filterMenuTree(menu.children || [])
            const searchableText = [
                menu.title,
                menu.path,
                menu.component,
                menu.code,
            ].join(' ').toLowerCase()

            if (searchableText.includes(normalizedKeyword.value) || children.length) {
                return {
                    ...menu,
                    children,
                }
            }

            return null
        })
        .filter(Boolean)
}
const filteredTableData = computed(() => filterMenuTree(tableData.value))
const {
    page,
    pageSize,
    total,
    pagedData: pagedTableData,
    resetPage,
} = useClientPagination(filteredTableData)

const getList = async () => {
    loading.value = true

    try {
        const res = await getMenuTree()

        if (res.data.code !== 200) {
            ElMessage.error(res.data.msg || '菜单加载失败')
            return
        }

        tableData.value = res.data.data || []
        resetPage()
    } finally {
        loading.value = false
    }
}

const handleFilter = () => {
    // 菜单树搜索保留命中的父子层级，并从第一页展示。
    resetPage()
}

const resetFilter = () => {
    keyword.value = ''
    resetPage()
}

onMounted(() => {
    getList()
})
</script>

<template>
    <el-card>
        <template #header>
            <div class="card-header">
                <span>菜单管理</span>
                <el-button type="primary" @click="getList">刷新</el-button>
            </div>
        </template>

        <div class="list-toolbar">
            <el-input
                v-model="keyword"
                clearable
                placeholder="菜单名称/路由/组件"
                style="width: 300px"
                @keyup.enter="handleFilter"
                @clear="handleFilter"
            />
            <el-button type="primary" @click="handleFilter">筛选</el-button>
            <el-button @click="resetFilter">重置</el-button>
        </div>

        <el-table
            v-loading="loading"
            :data="pagedTableData"
            row-key="id"
            default-expand-all
            border
            empty-text="暂无菜单数据"
            style="width: 100%"
        >
            <el-table-column prop="title" label="菜单名称" min-width="180" />

            <el-table-column prop="path" label="路由" min-width="180" />

            <el-table-column prop="component" label="组件" min-width="220" />

            <el-table-column prop="sort" label="排序" width="90" />

            <el-table-column prop="menu_type" label="类型" width="90">
                <template #default="scope">
                    <el-tag v-if="scope.row.menu_type === 1" type="primary">菜单</el-tag>
                    <el-tag v-else type="info">按钮</el-tag>
                </template>
            </el-table-column>

            <el-table-column prop="hidden" label="状态" width="90">
                <template #default="scope">
                    <el-tag v-if="scope.row.hidden" type="warning">隐藏</el-tag>
                    <el-tag v-else type="success">显示</el-tag>
                </template>
            </el-table-column>
        </el-table>

        <DataPagination
            v-model:current-page="page"
            v-model:page-size="pageSize"
            :page-sizes="[5, 10, 20, 50]"
            :total="total"
            background
            layout="total, sizes, prev, pager, next, jumper"
        />
    </el-card>
</template>

<style scoped>
.card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.list-toolbar {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
}
</style>
