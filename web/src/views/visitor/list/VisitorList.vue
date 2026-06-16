<!-- 文件说明：实现 src/views/visitor/list/VisitorList.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
// =====================================================
// Vue 相关
// =====================================================
import { ref, onMounted } from 'vue'

// =====================================================
// 路由
// =====================================================
import { useRouter } from 'vue-router'

// =====================================================
// Element Plus
// =====================================================
import { ElMessage, ElMessageBox } from 'element-plus'

// =====================================================
// API
// =====================================================
import { getVisitorList, deleteVisitor } from '@/api/visitor'

import { enterVisitor } from '@/api/visitor'
import { leaveVisitor } from '@/api/visitor'
import { useClientPagination } from '@/composables/useClientPagination'
import DataPagination from '@/components/common/DataPagination.vue'

// =====================================================
// 路由实例
// =====================================================
const router = useRouter()

// =====================================================
// 表格数据
// =====================================================
const tableData = ref<any[]>([])
const {
    page,
    pageSize,
    total,
    pagedData: pagedTableData,
    resetPage,
} = useClientPagination(tableData)

// =====================================================
// 搜索关键字
// =====================================================
const keyword = ref('')

/**
 * 重置搜索条件
 */
const resetSearch = () => {
    keyword.value = ''

    getList()
}

/**
 * 查看访客详情
 */
const handleDetail = (row: any) => {
    router.push('/visitor/detail/' + row.id)
}

/**
 * 编辑访客信息
 */
const handleEdit = (row: any) => {
    router.push('/visitor/edit/' + row.id)
}

/**
 * 跳转访客审批页
 */
const handleApprove = (row: any) => {
    router.push('/visitor/approve/' + row.id)
}

/**
 * 删除访客
 */
const handleDelete = async (row: any) => {
    // 二次确认
    await ElMessageBox.confirm('确认删除该访客吗？', '提示')

    // 调用删除接口
    await deleteVisitor(row.id)

    // 成功提示
    ElMessage.success('删除成功')

    // 刷新列表
    getList()
}

/**
 * 到访登记
 */
const handleEnter = async (row: any) => {
    await ElMessageBox.confirm('确认登记该访客到访吗？', '提示')

    await enterVisitor(row.id)

    ElMessage.success('登记成功')

    getList()
}

/**
 * 离开登记
 */
const handleLeave = async (row: any) => {
    await ElMessageBox.confirm('确认登记离开吗？', '提示')

    await leaveVisitor(row.id)

    ElMessage.success('登记成功')

    getList()
}

/**
 * 获取访客列表
 */
const getList = async () => {
    const res = await getVisitorList(keyword.value)

    tableData.value = res.data.data
    resetPage()
}

onMounted(() => {
    getList()
})
</script>

<template>
    <el-card>
        <template #header>
            <div style="display: flex; justify-content: space-between">
                <span>访客列表</span>
                <el-input v-model="keyword" placeholder="访客姓名" style="width: 250px" />

                <el-button type="primary" @click="getList"> 搜索 </el-button>

                <el-button @click="resetSearch"> 重置 </el-button>

                <el-button type="primary" @click="router.push('/visitor/create')">
                    新增访客
                </el-button>
            </div>
        </template>

        <el-table :data="pagedTableData" border style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />

            <el-table-column prop="name" label="访客姓名" />

            <el-table-column prop="phone" label="手机号" />

            <el-table-column prop="owner_name" label="被访业主" />

            <el-table-column prop="reason" label="来访事由" />

            <el-table-column prop="visit_time" label="来访时间" />

            <el-table-column prop="created_at" label="创建时间" width="180" />

            <el-table-column label="状态">
                <template #default="scope">
                    <el-tag type="warning" v-if="scope.row.status === 'waiting'"> 待审核 </el-tag>

                    <el-tag type="success" v-else-if="scope.row.status === 'approved'">
                        已通过
                    </el-tag>

                    <el-tag type="danger" v-else-if="scope.row.status === 'rejected'">
                        已拒绝
                    </el-tag>

                    <el-tag type="primary" v-else-if="scope.row.status === 'entered'">
                        已到访
                    </el-tag>

                    <el-tag v-else> 已离开 </el-tag>
                </template>
            </el-table-column>

            <el-table-column label="操作" width="360">
                <template #default="scope">
                    <el-button type="success" size="small" @click="handleDetail(scope.row)">
                        查看
                    </el-button>

                    <el-button
                        v-if="scope.row.status === 'waiting'"
                        type="warning"
                        size="small"
                        @click="handleApprove(scope.row)"
                    >
                        审批
                    </el-button>
                    <el-button
                        v-if="scope.row.status === 'approved'"
                        type="success"
                        size="small"
                        @click="handleEnter(scope.row)"
                    >
                        到访登记
                    </el-button>

                    <el-button
                        v-if="scope.row.status === 'entered'"
                        type="primary"
                        size="small"
                        @click="handleLeave(scope.row)"
                    >
                        离开登记
                    </el-button>

                    <el-button
                        v-if="scope.row.status === 'waiting'"
                        type="primary"
                        size="small"
                        @click="handleEdit(scope.row)"
                    >
                        编辑
                    </el-button>

                    <el-button
                        v-if="scope.row.status === 'waiting'"
                        type="danger"
                        size="small"
                        @click="handleDelete(scope.row)"
                    >
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
</template>
