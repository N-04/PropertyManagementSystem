<!-- 文件说明：实现 src/views/owner/list/OwnerList.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getOwnerList, deleteOwner } from '@/api/owner'
import { useRouter } from 'vue-router'
import { useClientPagination } from '@/composables/useClientPagination'
import DataPagination from '@/components/common/DataPagination.vue'

// =====================================================
// 响应式数据
// =====================================================
const isAdmin = true
const router = useRouter()
// =====================================================
// 角色列表数据
// =====================================================
const tableData = ref<any[]>([])
const {
    page,
    pageSize,
    total,
    pagedData: pagedTableData,
    resetPage,
} = useClientPagination(tableData)
const getList = async () => {
    const res = await getOwnerList()

    tableData.value = res.data.data
    resetPage()
}

const handleCreate = () => {
    router.push('/owner/create')
}

const handleDetail = (row: any) => {
    router.push('/owner/detail/' + row.id)
}

const keyword = ref('')
const searchOwner = async () => {
    const res = await getOwnerList(keyword.value)
    tableData.value = res.data.data
    resetPage()
}

// =====================================================
// 编辑角色
// =====================================================
const handleEdit = (row: any) => {
    router.push({
        path: '/owner/edit',
        query: {
            id: row.id,
        },
    })
}

// =====================================================
// 删除角色
// =====================================================

const handleDelete = async (row: any) => {
    await deleteOwner(row.id)

    await getList()
}

onMounted(() => {
    getList()
})
</script>

<template>
    <el-card>
        <template #header>
            <div class="card-header">
                <span>业主列表</span>
                <el-button type="primary" @click="handleCreate"> 新增业主 </el-button>
            </div>
        </template>

        <div class="list-toolbar">
            <el-input
                v-model="keyword"
                clearable
                placeholder="姓名/手机号"
                style="width: 260px"
                @keyup.enter="searchOwner"
                @clear="searchOwner"
            />
            <el-button type="primary" @click="searchOwner">筛选</el-button>
        </div>

        <el-table :data="pagedTableData" border style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />

            <el-table-column prop="name" label="姓名" />

            <el-table-column label="手机号">
                <template #default="scope">
                    {{
                        scope.row.phone
                            ? scope.row.phone.replace(/^(\d{3})\d{4}(\d{4})$/, '$1****$2')
                            : ''
                    }}
                </template>
            </el-table-column>

            <el-table-column label="身份证">
                <template #default="scope">
                    {{
                        scope.row.id_card
                            ? scope.row.id_card.replace(/^(.{6}).*(.{4})$/, '$1********$2')
                            : ''
                    }}
                </template>
            </el-table-column>
            <el-table-column label="身份证照片" width="180">
                <template #default="scope">
                    <el-tooltip content="点击查看大图">
                        <el-image
                            v-if="scope.row.id_card_image"
                            :src="'http://127.0.0.1:8000' + scope.row.id_card_image"
                            :preview-src-list="['http://127.0.0.1:8000' + scope.row.id_card_image]"
                            preview-teleported
                            style="width: 120px; height: 80px; cursor: pointer"
                            fit="cover"
                        />
                    </el-tooltip>
                </template>
            </el-table-column>

            <el-table-column label="操作" width="240">
                <template #default="scope">
                    <el-button type="primary" size="small" @click="handleDetail(scope.row)"> 查看 </el-button>

                    <el-button type="primary" size="small" @click="handleEdit(scope.row)"> 编辑 </el-button>

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
</template>
