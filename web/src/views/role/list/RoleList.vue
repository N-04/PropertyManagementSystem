<!-- 文件说明：实现 src/views/role/list/RoleList.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
// =====================================================
// Vue生命周期 / 响应式数据
// =====================================================
import { ref, onMounted } from 'vue'

// =====================================================
// 获取角色列表接口
// =====================================================
import { getRoleList } from '@/api/role'

// 删除接口
import { deleteRole } from '@/api/role'

// 路由
import { useRouter } from 'vue-router'
import { useClientPagination } from '@/composables/useClientPagination'
import { useKeywordFilter } from '@/composables/useKeywordFilter'
import DataPagination from '@/components/common/DataPagination.vue'
import { ElMessage } from 'element-plus'

// =====================================================
// 角色列表数据
// =====================================================
const tableData = ref<any[]>([])
const keyword = ref('')
const filteredTableData = useKeywordFilter(tableData, keyword, ['name', 'code', 'description'])
const {
    page,
    pageSize,
    total,
    pagedData: pagedTableData,
    resetPage,
} = useClientPagination(filteredTableData)

// =====================================================
// 获取角色列表
// =====================================================
const getList = async () => {
    // 调用接口
    const res = await getRoleList()

    tableData.value = res.data.data
    resetPage()
}

const handleFilter = () => {
    // 模糊搜索条件变化后回到第一页，避免停在空页。
    resetPage()
}

const resetFilter = () => {
    keyword.value = ''
    resetPage()
}

// 路由对象
const router = useRouter()

// =====================================================
// 编辑角色
// =====================================================

const handleEdit = (row: any) => {
    // 页面跳转
    router.push(`/role/edit/${row.id}`)
}

// =====================================================
// 删除角色
// =====================================================

const handleDelete = async (row: any) => {
    try {
        // 调用删除接口
        const res = await deleteRole(row.id)

        if (res.data.code !== 200) {
            ElMessage.error(res.data.msg || '删除失败')
            return
        }

        ElMessage.success('删除成功')
        // 重新获取列表
        getList()
    } catch (error: any) {
        ElMessage.error(error?.response?.data?.msg || '删除失败')
    }
}

// =====================================================
// 页面加载完成
// =====================================================
onMounted(() => {
    // 获取列表
    getList()
})
</script>

<template>
    <!-- 页面容器 -->
    <div class="page-container">
        <!-- 卡片 -->
        <el-card>
            <!-- 卡片标题 -->
            <template #header>
                <div class="header-box">
                    <span>角色列表</span>

                    <el-button type="primary" @click="$router.push('/role/create')">
                        新增角色
                    </el-button>
                </div>
            </template>

            <div class="list-toolbar">
                <el-input
                    v-model="keyword"
                    clearable
                    placeholder="角色名称/编码"
                    style="width: 260px"
                    @keyup.enter="handleFilter"
                    @clear="handleFilter"
                />
                <el-button type="primary" @click="handleFilter">筛选</el-button>
                <el-button @click="resetFilter">重置</el-button>
            </div>

            <!-- 表格 -->
            <el-table :data="pagedTableData" border>
                <!-- ID -->
                <el-table-column prop="id" label="ID" width="80" />

                <!-- 角色名称 -->
                <el-table-column prop="name" label="角色名称" />

                <!-- 角色编码 -->
                <el-table-column prop="code" label="角色编码" />

                <!-- 创建时间 -->
                <el-table-column prop="created_at" label="创建时间" />
                <!-- 操作 -->
                <el-table-column label="操作" width="220">
                    <template #default="scope">
                        <!-- 编辑 -->
                        <el-button type="primary" size="small" @click="handleEdit(scope.row)">
                            编辑
                        </el-button>

                        <!-- 删除 -->
                        <el-button type="danger" size="small" @click="handleDelete(scope.row)">
                            删除
                        </el-button>
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
    </div>
</template>

<style scoped>
/* 页面容器 */
.page-container {
    padding: 20px;
}
/* header布局 */
.header-box {
    display: flex;

    justify-content: space-between;

    align-items: center;
}

.list-toolbar {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
}
</style>
