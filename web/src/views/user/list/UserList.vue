<!-- 文件说明：实现 src/views/user/list/UserList.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { auditUser, deleteUser } from '@/api/user'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUserList } from '@/api/user'
import { useRouter } from 'vue-router'
import DataPagination from '@/components/common/DataPagination.vue'

// 用户类型
interface UserItem {
    id: number

    username: string

    real_name: string

    phone: string

    roles: any[]

    status: number

    is_active: boolean

    created_at: string
}

// 表格数据
const tableData = ref<UserItem[]>([])

const keyword = ref('')

const total = ref(0)

const page = ref(1)

const pageSize = ref(5)

const router = useRouter()

// 加载数据
const loadData = async () => {
    const res = await getUserList({
        page: page.value,
        page_size: pageSize.value,
        keyword: keyword.value || undefined,
    })

    tableData.value = res.data.data
    total.value = res.data.total
    console.log(res.data.data)
}

const searchUsers = () => {
    // 服务端分页列表需要重新请求，保证模糊搜索覆盖全部用户而不是当前页。
    page.value = 1
    loadData()
}

const resetFilter = () => {
    keyword.value = ''
    page.value = 1
    loadData()
}

const handlePageSizeChange = () => {
    page.value = 1
    loadData()
}

const handleDelete = async (id: number) => {
    try {
        await ElMessageBox.confirm('确认删除该用户？', '删除提示', {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'warning',
        })

        await deleteUser(id)

        ElMessage.success('删除成功')

        await loadData()
    } catch (error) {
        ElMessage.info('已取消删除')
    }
}

const handleAudit = async (row: UserItem, auditStatus: 'approved' | 'rejected') => {
    const isApproved = auditStatus === 'approved'
    const message = isApproved ? '确认通过该用户审核？' : '确认禁用该用户？'

    try {
        await ElMessageBox.confirm(message, '审核提示', {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'warning',
        })

        const res = await auditUser(row.id, auditStatus)

        if (res.data.code !== 200) {
            ElMessage.error(res.data.msg || '操作失败')
            return
        }

        ElMessage.success(isApproved ? '审核通过，用户已成为正式业主' : '用户已禁用')
        await loadData()
    } catch (error) {
        ElMessage.info('已取消操作')
    }
}

// 页面加载执行
onMounted(() => {
    loadData()
})
</script>

<template>
    <el-card>
        <template #header> 用户列表 </template>

        <div class="list-toolbar">
            <el-input
                v-model="keyword"
                clearable
                placeholder="用户名/姓名/手机号/角色"
                style="width: 280px"
                @keyup.enter="searchUsers"
                @clear="searchUsers"
            />
            <el-button type="primary" @click="searchUsers">筛选</el-button>
            <el-button @click="resetFilter">重置</el-button>
        </div>

        <el-table :data="tableData" border>
            <el-table-column prop="id" label="ID" width="80" />

            <el-table-column prop="username" label="用户名" />

            <el-table-column prop="real_name" label="真实姓名" />

            <el-table-column prop="phone" label="手机号" />

            <el-table-column label="角色">
                <template #default="scope">
                    {{ scope.row.roles.map((item: any) => item.name).join('、') }}
                </template>
            </el-table-column>

            <el-table-column label="状态">
                <template #default="scope">
                    <el-tag v-if="scope.row.status === 1" type="success"> 正常 </el-tag>

                    <el-tag v-else type="warning"> 待审核/禁用 </el-tag>
                </template>
            </el-table-column>

            <el-table-column prop="created_at" label="创建时间" width="180" />
            <el-table-column label="操作" width="280">
                <template #default="scope">
                    <el-button type="primary" @click="router.push(`/user/edit/${scope.row.id}`)">
                        编辑
                    </el-button>

                    <el-button
                        v-if="scope.row.status !== 1"
                        type="success"
                        @click="handleAudit(scope.row, 'approved')"
                    >
                        通过审核
                    </el-button>

                    <el-button
                        v-else
                        type="warning"
                        @click="handleAudit(scope.row, 'rejected')"
                    >
                        禁用账号
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
            @size-change="handlePageSizeChange"
            @current-change="loadData"
        />
    </el-card>
</template>

<style scoped>
.list-toolbar {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
}
</style>
