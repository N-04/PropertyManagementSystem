<!-- 文件说明：展示投诉建议列表，支持处理结果和回访记录。 -->
<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { deleteComplaint, getComplaintList, updateComplaint } from '@/api/complaint'
import { useClientPagination } from '@/composables/useClientPagination'
import DataPagination from '@/components/common/DataPagination.vue'

const role = localStorage.getItem('role') || ''
const isOwner = role === 'owner'
const tableData = ref<any[]>([])
const dialogVisible = ref(false)
const currentRow = ref<any>(null)

const queryForm = reactive({
    keyword: '',
    category: '',
    status: '',
})

const handleForm = reactive({
    status: 'processing',
    handle_result: '',
    return_visit: '',
})

const {
    page,
    pageSize,
    total,
    pagedData: pagedTableData,
    resetPage,
} = useClientPagination(tableData)

const loadData = async () => {
    const res = await getComplaintList(queryForm)

    tableData.value = res.data.data || []
    resetPage()
}

const resetSearch = () => {
    queryForm.keyword = ''
    queryForm.category = ''
    queryForm.status = ''
    loadData()
}

const openHandleDialog = (row: any) => {
    currentRow.value = row
    handleForm.status = row.status || 'processing'
    handleForm.handle_result = row.handle_result || ''
    handleForm.return_visit = row.return_visit || ''
    dialogVisible.value = true
}

const submitHandle = async () => {
    if (!currentRow.value) {
        return
    }

    const res = await updateComplaint(currentRow.value.id, handleForm)

    if (res.data.code !== 200) {
        ElMessage.error(res.data.msg || '处理失败')
        return
    }

    ElMessage.success('处理成功')
    dialogVisible.value = false
    await loadData()
}

const handleDelete = async (row: any) => {
    await ElMessageBox.confirm('确认删除该记录？', '删除提示', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning',
    })

    const res = await deleteComplaint(row.id)

    if (res.data.code !== 200) {
        ElMessage.error(res.data.msg || '删除失败')
        return
    }

    ElMessage.success('删除成功')
    await loadData()
}

onMounted(() => {
    loadData()
})
</script>

<template>
    <el-card class="search-card">
        <el-form :inline="true" :model="queryForm">
            <el-form-item>
                <el-input
                    v-model="queryForm.keyword"
                    placeholder="标题/内容/手机号"
                    clearable
                    @keyup.enter="loadData"
                />
            </el-form-item>

            <el-form-item>
                <el-select v-model="queryForm.category" placeholder="类型" clearable style="width: 120px">
                    <el-option label="投诉" value="complaint" />
                    <el-option label="建议" value="suggestion" />
                </el-select>
            </el-form-item>

            <el-form-item>
                <el-select v-model="queryForm.status" placeholder="状态" clearable style="width: 130px">
                    <el-option label="待处理" value="pending" />
                    <el-option label="处理中" value="processing" />
                    <el-option label="已完成" value="done" />
                    <el-option label="已关闭" value="closed" />
                </el-select>
            </el-form-item>

            <el-form-item>
                <el-button type="primary" @click="loadData">搜索</el-button>
                <el-button @click="resetSearch">重置</el-button>
            </el-form-item>
        </el-form>
    </el-card>

    <el-card>
        <template #header>投诉建议列表</template>

        <el-table :data="pagedTableData" border>
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="category_text" label="类型" width="90" />
            <el-table-column prop="title" label="标题" min-width="140" />
            <el-table-column prop="owner_name" label="业主" width="110" />
            <el-table-column prop="phone" label="联系电话" width="130" />

            <el-table-column label="状态" width="110">
                <template #default="scope">
                    <el-tag v-if="scope.row.status === 'pending'" type="warning">待处理</el-tag>
                    <el-tag v-else-if="scope.row.status === 'processing'" type="primary">
                        处理中
                    </el-tag>
                    <el-tag v-else-if="scope.row.status === 'done'" type="success">已完成</el-tag>
                    <el-tag v-else>已关闭</el-tag>
                </template>
            </el-table-column>

            <el-table-column prop="content" label="内容" min-width="180" show-overflow-tooltip />
            <el-table-column prop="handle_result" label="处理结果" min-width="160" show-overflow-tooltip />
            <el-table-column prop="return_visit" label="回访记录" min-width="160" show-overflow-tooltip />
            <el-table-column prop="created_at" label="提交时间" width="170" />

            <el-table-column label="操作" width="180">
                <template #default="scope">
                    <el-button v-if="!isOwner" type="primary" size="small" @click="openHandleDialog(scope.row)">
                        处理/回访
                    </el-button>
                    <el-button
                        v-if="!isOwner || scope.row.status === 'pending'"
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

    <el-dialog v-model="dialogVisible" title="处理投诉/建议" width="520px">
        <el-form label-width="90px">
            <el-form-item label="处理状态">
                <el-select v-model="handleForm.status">
                    <el-option label="待处理" value="pending" />
                    <el-option label="处理中" value="processing" />
                    <el-option label="已完成" value="done" />
                    <el-option label="已关闭" value="closed" />
                </el-select>
            </el-form-item>

            <el-form-item label="处理结果">
                <el-input v-model="handleForm.handle_result" type="textarea" :rows="4" />
            </el-form-item>

            <el-form-item label="回访记录">
                <el-input v-model="handleForm.return_visit" type="textarea" :rows="3" />
            </el-form-item>
        </el-form>

        <template #footer>
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="submitHandle">保存</el-button>
        </template>
    </el-dialog>
</template>

<style scoped>
.search-card {
    margin-bottom: 16px;
}
</style>
