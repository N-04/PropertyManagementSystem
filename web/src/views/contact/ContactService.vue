<!-- 文件说明：侧边栏“联系客服”模块，供业主、管理员、财务和维修角色发起站内会话。 -->
<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import {
    createChatConversation,
    getChatConversationList,
    sendChatMessage,
} from '@/api/chat'
import { useClientPagination } from '@/composables/useClientPagination'
import DataPagination from '@/components/common/DataPagination.vue'

type ChatMessage = {
    id: number | string
    sender_name?: string
    sender_real_name?: string
    content: string
    created_at?: string
}

type Conversation = {
    id: number
    title: string
    target_role: string
    target_role_text?: string
    status: 'active' | 'resolved' | 'closed'
    status_text?: string
    created_by_name?: string
    created_by_real_name?: string
    participant_names?: string[]
    last_message?: string
    messages?: ChatMessage[]
    updated_at?: string
}

const role = localStorage.getItem('role') || ''
const username = localStorage.getItem('username') || ''
const loading = ref(false)
const creating = ref(false)
const sending = ref(false)
const conversations = ref<Conversation[]>([])
const activeId = ref<number | null>(null)
const replyText = ref('')

const form = reactive({
    target_role: 'customer_service',
    title: '',
    content: '',
})

const targetOptions = computed(() => {
    const options = [
        { label: '客服人员', value: 'customer_service' },
        { label: '财务人员', value: 'finance_staff' },
        { label: '维修员', value: 'repair_staff' },
        { label: '物业管理员', value: 'property_admin' },
    ]

    if (['finance_staff', 'finance'].includes(role)) {
        return options.filter((item) => item.value !== 'finance_staff')
    }

    if (['repair_staff', 'repairer', 'repair'].includes(role)) {
        return options.filter((item) => item.value !== 'repair_staff')
    }

    return options
})

const {
    page,
    pageSize,
    total,
    pagedData: pagedConversations,
    resetPage,
} = useClientPagination(conversations, 5)

const activeConversation = computed(() => {
    return conversations.value.find((item) => item.id === activeId.value) || null
})

const messageRows = computed(() => {
    return (activeConversation.value?.messages || []).map((item) => ({
        ...item,
        mine: item.sender_name === username,
    }))
})

const statusTypeMap: Record<string, 'primary' | 'success' | 'info'> = {
    active: 'primary',
    resolved: 'success',
    closed: 'info',
}

const loadConversations = async () => {
    loading.value = true

    try {
        const res = await getChatConversationList({})
        conversations.value = res.data.data || []
        resetPage()

        if (!activeId.value && conversations.value[0]) {
            activeId.value = conversations.value[0].id
        }
    } finally {
        loading.value = false
    }
}

const createConversation = async () => {
    if (!form.title.trim() || !form.content.trim()) {
        ElMessage.warning('请填写标题和内容')
        return
    }

    creating.value = true

    try {
        const res = await createChatConversation({
            target_role: form.target_role,
            title: form.title.trim(),
            content: form.content.trim(),
        })

        if (res.data.code !== 200) {
            ElMessage.error(res.data.msg || '创建会话失败')
            return
        }

        ElMessage.success('会话已创建')
        form.title = ''
        form.content = ''
        await loadConversations()
        activeId.value = res.data.data?.id || activeId.value
    } finally {
        creating.value = false
    }
}

const sendReply = async () => {
    if (!activeConversation.value || !replyText.value.trim()) {
        ElMessage.warning('请输入回复内容')
        return
    }

    sending.value = true

    try {
        const res = await sendChatMessage(activeConversation.value.id, {
            content: replyText.value.trim(),
        })

        if (res.data.code !== 200) {
            ElMessage.error(res.data.msg || '发送失败')
            return
        }

        replyText.value = ''
        await loadConversations()
    } finally {
        sending.value = false
    }
}

onMounted(() => {
    loadConversations()
})
</script>

<template>
    <div class="contact-page">
        <section class="contact-panel">
            <div class="panel-title">联系客服</div>
            <el-form label-width="88px">
                <el-form-item label="联系对象">
                    <el-select v-model="form.target_role">
                        <el-option
                            v-for="item in targetOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        />
                    </el-select>
                </el-form-item>
                <el-form-item label="标题">
                    <el-input v-model="form.title" maxlength="120" show-word-limit />
                </el-form-item>
                <el-form-item label="内容">
                    <el-input v-model="form.content" type="textarea" :rows="4" maxlength="500" show-word-limit />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" :loading="creating" @click="createConversation">
                        发起联系
                    </el-button>
                    <el-button :loading="loading" @click="loadConversations">刷新</el-button>
                </el-form-item>
            </el-form>
        </section>

        <section class="conversation-panel">
            <div class="panel-title">会话列表</div>
            <el-table v-loading="loading" :data="pagedConversations" border highlight-current-row>
                <el-table-column prop="title" label="标题" min-width="150" show-overflow-tooltip />
                <el-table-column prop="target_role_text" label="联系对象" width="110" />
                <el-table-column label="状态" width="100">
                    <template #default="scope">
                        <el-tag :type="statusTypeMap[scope.row.status] || 'info'">
                            {{ scope.row.status_text || scope.row.status }}
                        </el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="last_message" label="最后消息" min-width="200" show-overflow-tooltip />
                <el-table-column prop="updated_at" label="更新时间" width="170" />
                <el-table-column label="操作" width="90">
                    <template #default="scope">
                        <el-button type="primary" size="small" @click="activeId = scope.row.id">
                            打开
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>

            <DataPagination
                v-model:current-page="page"
                v-model:page-size="pageSize"
                :total="total"
                :page-sizes="[5, 10, 20, 50]"
            />
        </section>

        <section class="chat-panel">
            <template v-if="activeConversation">
                <div class="chat-title">
                    <span>{{ activeConversation.title }}</span>
                    <el-tag :type="statusTypeMap[activeConversation.status] || 'info'">
                        {{ activeConversation.status_text || activeConversation.status }}
                    </el-tag>
                </div>

                <div class="message-list">
                    <div
                        v-for="message in messageRows"
                        :key="message.id"
                        class="message-row"
                        :class="{ mine: message.mine }"
                    >
                        <div class="message-bubble">
                            <div class="message-author">
                                {{ message.sender_real_name || message.sender_name || '用户' }}
                            </div>
                            <div class="message-content">{{ message.content }}</div>
                            <div class="message-time">{{ message.created_at || '-' }}</div>
                        </div>
                    </div>
                </div>

                <div class="reply-box">
                    <el-input
                        v-model="replyText"
                        type="textarea"
                        :rows="3"
                        maxlength="500"
                        show-word-limit
                        placeholder="输入回复内容"
                    />
                    <el-button type="primary" :loading="sending" @click="sendReply">发送</el-button>
                </div>
            </template>

            <el-empty v-else description="请选择会话" :image-size="100" />
        </section>
    </div>
</template>

<style scoped>
.contact-page {
    display: grid;
    grid-template-columns: 360px minmax(0, 1fr);
    gap: 16px;
}

.contact-panel,
.conversation-panel,
.chat-panel {
    padding: 16px;
    border: 1px solid #e5eaf2;
    border-radius: 6px;
    background: #ffffff;
}

.conversation-panel,
.chat-panel {
    grid-column: span 2;
}

.panel-title,
.chat-title {
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 16px;
    font-weight: 700;
}

.message-list {
    min-height: 240px;
    max-height: 420px;
    overflow-y: auto;
    padding: 10px 4px;
    background: #f8fafc;
    border-radius: 6px;
}

.message-row {
    display: flex;
    margin-bottom: 12px;
}

.message-row.mine {
    justify-content: flex-end;
}

.message-bubble {
    max-width: min(680px, 72%);
    padding: 10px 12px;
    border: 1px solid #e5eaf2;
    border-radius: 8px;
    background: #ffffff;
}

.message-row.mine .message-bubble {
    color: #ffffff;
    background: #2563eb;
    border-color: #2563eb;
}

.message-author {
    margin-bottom: 4px;
    font-size: 12px;
    color: #64748b;
}

.message-row.mine .message-author,
.message-row.mine .message-time {
    color: #dbeafe;
}

.message-content {
    white-space: pre-wrap;
    line-height: 1.55;
}

.message-time {
    margin-top: 6px;
    font-size: 12px;
    color: #94a3b8;
}

.reply-box {
    margin-top: 12px;
    display: grid;
    grid-template-columns: minmax(0, 1fr) 96px;
    gap: 12px;
}

@media (max-width: 960px) {
    .contact-page {
        grid-template-columns: 1fr;
    }

    .conversation-panel,
    .chat-panel {
        grid-column: span 1;
    }
}
</style>
