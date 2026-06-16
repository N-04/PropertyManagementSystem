<!-- 文件说明：实现 src/views/role/edit/RoleEdit.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
// =====================================================
// 导入
// =====================================================

// vue
import { computed, reactive, onMounted, ref } from 'vue'

// 路由
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'

// API
import { assignRolePermissions, getRoleDetail, updateRole } from '@/api/role'
import { getPermissionTree } from '@/api/permission'

// =====================================================
// 路由对象
// =====================================================

const route = useRoute()

// =====================================================
// 表单数据
// =====================================================

const form = reactive({
    // 角色名称
    name: '',

    // 角色编码
    code: '',

    // 角色描述
    description: '',
})

const permissionOptions = ref<any[]>([])
const checkedPermissionIds = ref<number[]>([])
const saving = ref(false)

const groupedPermissions = computed(() => {
    const groups: Record<string, any[]> = {}

    permissionOptions.value.forEach((item) => {
        const groupName = item.menu || '未绑定菜单'

        if (!groups[groupName]) {
            groups[groupName] = []
        }

        groups[groupName].push(item)
    })

    return Object.entries(groups).map(([name, permissions]) => ({
        name,
        permissions,
    }))
})

// =====================================================
// 获取角色详情
// =====================================================

const getDetail = async () => {
    // 调用详情接口
    const res = await getRoleDetail(Number(route.params.id))

    // 回填数据
    form.name = res.data.data.name

    form.code = res.data.data.code

    form.description = res.data.data.description || ''

    checkedPermissionIds.value = (res.data.data.permissions || []).map((item: any) => item.id)
}

// =====================================================
// 获取权限选项
// =====================================================

const getPermissions = async () => {
    const res = await getPermissionTree()

    permissionOptions.value = res.data.data
}

// =====================================================
// 保存修改
// =====================================================

const handleSubmit = async () => {
    saving.value = true

    try {
        // 调用修改接口
        const res = await updateRole(
            // 角色ID
            Number(route.params.id),

            // 表单数据
            {
                name: form.name,
                code: form.code,
            }
        )

        if (res.data.code !== 200) {
            ElMessage.error(res.data.msg || '角色保存失败')
            return
        }

        const assignRes = await assignRolePermissions(
            Number(route.params.id),
            checkedPermissionIds.value
        )

        if (assignRes.data.code !== 200) {
            ElMessage.error(assignRes.data.msg || '权限分配失败')
            return
        }

        ElMessage.success('保存成功')
    } finally {
        saving.value = false
    }
}

// =====================================================
// 页面加载
// =====================================================

onMounted(() => {
    // 获取详情
    getDetail()
    getPermissions()
})
</script>

<template>
    <div class="page-container">
        <el-card>
            <!-- 标题 -->
            <template #header>
                <span>编辑角色</span>
            </template>

            <!-- 表单 -->
            <el-form label-width="100px">
                <!-- 角色名称 -->
                <el-form-item label="角色名称">
                    <el-input v-model="form.name" />
                </el-form-item>

                <!-- 角色编码 -->
                <el-form-item label="角色编码">
                    <el-input v-model="form.code" />
                </el-form-item>

                <el-form-item label="角色描述">
                    <el-input v-model="form.description" type="textarea" :rows="3" />
                </el-form-item>

                <el-form-item label="权限分配">
                    <el-checkbox-group v-model="checkedPermissionIds" class="permission-panel">
                        <div
                            v-for="group in groupedPermissions"
                            :key="group.name"
                            class="permission-group"
                        >
                            <div class="permission-group-title">
                                {{ group.name }}
                                <span>{{ group.permissions.length }}项</span>
                            </div>

                            <div class="permission-list">
                                <el-checkbox
                                    v-for="item in group.permissions"
                                    :key="item.id"
                                    :label="item.id"
                                >
                                    {{ item.name }}
                                    <span class="permission-code">{{ item.code }}</span>
                                </el-checkbox>
                            </div>
                        </div>
                    </el-checkbox-group>
                </el-form-item>

                <!-- 按钮 -->
                <el-form-item>
                    <el-button type="primary" :loading="saving" @click="handleSubmit">
                        保存
                    </el-button>
                </el-form-item>
            </el-form>
        </el-card>
    </div>
</template>

<style scoped>
.permission-panel {
    width: 100%;
}

.permission-group {
    padding: 12px 0;
    border-bottom: 1px solid #ebeef5;
}

.permission-group-title {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
    font-weight: 600;
    color: #303133;
}

.permission-group-title span {
    font-size: 12px;
    font-weight: 400;
    color: #909399;
}

.permission-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 8px 16px;
}

.permission-code {
    margin-left: 6px;
    color: #909399;
    font-size: 12px;
}
</style>
