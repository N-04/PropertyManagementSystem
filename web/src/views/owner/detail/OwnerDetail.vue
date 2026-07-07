<!-- 文件说明：实现 src/views/owner/detail/OwnerDetail.vue 对应业务页面的展示、表单和交互逻辑。 -->
<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getOwnerDetail } from '@/api/owner'
import { toMediaURL } from '@/utils/url'

const route = useRoute()
const ownerDetail = ref<any>(null)
// 字典分块：接口返回关系编码，详情页统一转换成中文展示。
const relationshipMap: Record<string, string> = {
    self: '本人',
    spouse: '配偶',
    child: '子女',
    parent: '父母',
    other: '其他',
}

// 数据加载分块：详情页只按路由 id 拉取当前业主资料。
const loadOwnerDetail = async () => {
    const res = await getOwnerDetail(Number(route.params.id))
    ownerDetail.value = res.data
}
onMounted(() => {
    loadOwnerDetail()
})
</script>

<template>
    <el-card v-if="ownerDetail">
        <template #header>
            <span>业主详情</span>
        </template>

        <!-- 资料分块：身份信息、家庭关系和房屋归属集中在描述表格中展示。 -->
        <el-descriptions :column="2" border>
            <el-descriptions-item label="头像">
                <el-avatar :size="100" :src="toMediaURL(ownerDetail.data.avatar)" />
            </el-descriptions-item>

            <el-descriptions-item label="姓名">{{ ownerDetail.data.name }}</el-descriptions-item>

            <el-descriptions-item label="手机号">{{ ownerDetail.data.phone }}</el-descriptions-item>

            <el-descriptions-item label="身份证号">
                <!-- 身份证只做脱敏展示，避免详情页暴露完整证件号。 -->
                {{ ownerDetail.data.id_card?.replace(/^(.{6}).*(.{4})$/, '$1********$2') }}
            </el-descriptions-item>

            <el-descriptions-item label="性别">
                {{
                    ownerDetail.data.gender === 'male'
                        ? '男'
                        : ownerDetail.data.gender === 'female'
                          ? '女'
                          : ownerDetail.data.gender
                }}
            </el-descriptions-item>

            <el-descriptions-item label="与户主关系">
                {{ relationshipMap[ownerDetail.data.relationship] || ownerDetail.data.relationship }}
            </el-descriptions-item>

            <el-descriptions-item label="是否户主">{{
                ownerDetail.data.is_primary ? '是' : '否'
            }}</el-descriptions-item>

            <el-descriptions-item label="身份证照片"
                >{{ ownerDetail.data.id_card_image ? '有' : '无' }}
                <div style="display: flex; align-items: center; margin-bottom: 20px">
                    <el-image
                        :src="toMediaURL(ownerDetail.data.id_card_image)"
                        style="width: 300px"
                        fit="contain"
                        :preview-src-list="[
                            toMediaURL(ownerDetail.data.id_card_image),
                        ]"
                    />
                </div>
            </el-descriptions-item>

            <el-descriptions-item label="所属房屋">
                {{ ownerDetail.data.room_no }}
            </el-descriptions-item>

            <el-descriptions-item label="创建时间">
                {{ ownerDetail.data.created_at?.replace('T', ' ')?.substring(0, 19) }}
            </el-descriptions-item>
        </el-descriptions>
    </el-card>
</template>
