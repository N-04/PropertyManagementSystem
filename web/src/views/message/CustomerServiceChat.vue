<!-- 文件说明：客服人员专用即时通讯工作台，不显示后台侧边栏。 -->
<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ChatDotRound, Finished, Refresh, SwitchButton } from '@element-plus/icons-vue'
import { logoutApi } from '@/api/auth'
import {
    getChatConversationList,
    sendChatMessage,
    updateChatConversationStatus,
} from '@/api/chat'
import { clearAuthState, getStoredRefresh, getStoredUsername } from '@/utils/authState'
import { extractListRows } from '@/utils/listResponse'

type Conversation = {
    id: number
    title: string
    target_role: string
    target_role_text?: string
    created_by_name?: string
    created_by_real_name?: string
    participant_names?: string[]
    status: 'active' | 'resolved' | 'closed'
    end_reason?: 'manual' | 'timeout' | null
    end_reason_text?: string
    ended_at?: string
    rating_score?: number | string | null
    rating_comment?: string | null
    rating_at?: string | null
    last_message?: string
    messages?: ChatMessage[]
    created_at?: string
    updated_at?: string
}

type ChatMessage = {
    id: number | string
    sender_name?: string
    sender_real_name?: string
    sender_role_codes?: string[]
    content: string
    created_at?: string
    mine?: boolean
}

const router = useRouter()
const username = getStoredUsername() || '客服'
const conversations = ref<Conversation[]>([])
const activeId = ref<number | null>(null)
const loading = ref(false)
const sending = ref(false)
const keyword = ref('')
const statusFilter = ref('')
const replyText = ref('')
let refreshTimer: ReturnType<typeof setInterval> | null = null

const statusTextMap: Record<string, string> = {
    active: '沟通中',
    resolved: '已解决',
    closed: '已关闭',
}

const statusTypeMap: Record<string, 'warning' | 'primary' | 'success' | 'info'> = {
    active: 'primary',
    resolved: 'success',
    closed: 'info',
}

const activeConversation = computed(() => {
    return conversations.value.find((item) => item.id === activeId.value) || null
})

const activeConversationEnded = computed(() => {
    return Boolean(activeConversation.value && activeConversation.value.status !== 'active')
})

const filteredConversations = computed(() => {
    const text = keyword.value.trim().toLowerCase()

    return conversations.value.filter((item) => {
        const matchedStatus = statusFilter.value ? item.status === statusFilter.value : true
        const matchedText = text
            ? `${item.title}${item.last_message}${item.created_by_name}${item.created_by_real_name}${item.participant_names?.join('')}`.toLowerCase().includes(text)
            : true

        return matchedStatus && matchedText
    })
})

const activeCount = computed(() => {
    return conversations.value.filter((item) => item.status === 'active').length
})

const resolvedCount = computed(() => {
    return conversations.value.filter((item) => item.status === 'resolved').length
})

const chatMessages = computed<ChatMessage[]>(() => {
    const current = activeConversation.value

    if (!current) {
        return []
    }

    return (current.messages || []).map((item) => ({
        ...item,
        mine: item.sender_name === username,
    }))
})

const loadConversations = async (options: { silent?: boolean } = {}) => {
    const { silent = false } = options

    if (!silent) {
        loading.value = true
    }

    try {
        const res = await getChatConversationList({ page_size: 100 })
        conversations.value = extractListRows(res.data.data)

        if (!activeId.value && conversations.value[0]) {
            activeId.value = conversations.value[0].id
        }

        if (activeId.value && !conversations.value.some((item) => item.id === activeId.value)) {
            activeId.value = conversations.value[0]?.id || null
        }
    } finally {
        if (!silent) {
            loading.value = false
        }
    }
}

const appendServiceMessage = async (content: string, status?: 'active' | 'resolved' | 'closed') => {
    const current = activeConversation.value

    if (!current || !content.trim()) {
        return
    }

    if (current.status !== 'active') {
        ElMessage.warning('会话已结束，不能继续发送消息')
        return
    }

    sending.value = true

    try {
        const res = await sendChatMessage(current.id, { content: content.trim() })

        if (res.data.code !== 200) {
            ElMessage.error(res.data.msg || '发送失败')
            return
        }

        if (status) {
            const statusRes = await updateChatConversationStatus(current.id, { status })

            if (statusRes.data.code !== 200) {
                ElMessage.error(statusRes.data.msg || '状态更新失败')
                return
            }
        }

        replyText.value = ''
        await loadConversations({ silent: true })
    } finally {
        sending.value = false
    }
}

const sendReply = () => {
    appendServiceMessage(replyText.value)
}

const transferTo = (target: string) => {
    appendServiceMessage(`已转接${target}协同处理，请保持在线。`)
}

const markDone = () => {
    appendServiceMessage('本次沟通已处理完成。', 'resolved')
}

const handleLogout = async () => {
    const refresh = getStoredRefresh()

    try {
        await logoutApi(refresh)
    } finally {
        clearAuthState()
        router.push('/login')
    }
}

onMounted(() => {
    loadConversations()
    // 客服工作台保持轮询刷新，让新会话和新消息能自动进入当前列表。
    refreshTimer = setInterval(() => {
        loadConversations({ silent: true })
    }, 8000)
})

onBeforeUnmount(() => {
    if (refreshTimer) {
        clearInterval(refreshTimer)
    }
})
</script>

<template>
    <div class="service-chat-page">
        <header class="chat-header">
            <div>
                <div class="app-title">社区物业客服工作台</div>
                <div class="app-subtitle">
                    <span>沟通中 {{ activeCount }}</span>
                    <span>已解决 {{ resolvedCount }}</span>
                </div>
            </div>

            <div class="header-actions">
                <el-button :icon="Refresh" :loading="loading" @click="loadConversations()">刷新</el-button>
                <el-button :icon="SwitchButton" type="primary" plain @click="handleLogout">退出登录</el-button>
            </div>
        </header>

        <main class="chat-shell">
            <aside class="conversation-panel">
                <div class="conversation-tools">
                    <el-input v-model="keyword" placeholder="搜索会话" clearable />
                    <el-segmented
                        v-model="statusFilter"
                        :options="[
                            { label: '全部', value: '' },
                            { label: '沟通中', value: 'active' },
                            { label: '已解决', value: 'resolved' },
                            { label: '已关闭', value: 'closed' },
                        ]"
                    />
                </div>

                <div v-loading="loading" class="conversation-list">
                    <button
                        v-for="item in filteredConversations"
                        :key="item.id"
                        type="button"
                        class="conversation-item"
                        :class="{ active: item.id === activeId }"
                        @click="activeId = item.id"
                    >
                        <span class="conversation-title">{{ item.title }}</span>
                        <el-tag size="small" :type="statusTypeMap[item.status]">
                            {{ statusTextMap[item.status] || item.status }}
                        </el-tag>
                        <span class="conversation-meta">
                            {{ item.created_by_real_name || item.created_by_name || '访客' }}
                            <span v-if="item.last_message"> · {{ item.last_message }}</span>
                        </span>
                    </button>

                    <el-empty
                        v-if="!loading && filteredConversations.length === 0"
                        description="暂无会话"
                        :image-size="90"
                    />
                </div>
            </aside>

            <section class="chat-panel">
                <template v-if="activeConversation">
                    <div class="chat-titlebar">
                        <div>
                            <div class="chat-title">{{ activeConversation.title }}</div>
                            <div class="chat-meta">
                                {{ activeConversation.created_by_real_name || activeConversation.created_by_name || '访客' }}
                                <span v-if="activeConversation.participant_names?.length">
                                    · {{ activeConversation.participant_names.join('、') }}
                                </span>
                            </div>
                        </div>

                        <el-tag :type="statusTypeMap[activeConversation.status]">
                            {{ statusTextMap[activeConversation.status] || activeConversation.status }}
                        </el-tag>
                    </div>

                    <div class="channel-row">
                        <el-button :icon="ChatDotRound" :disabled="activeConversationEnded" @click="transferTo('业主')">
                            业主
                        </el-button>
                        <el-button :disabled="activeConversationEnded" @click="transferTo('财务人员')">财务</el-button>
                        <el-button :disabled="activeConversationEnded" @click="transferTo('维修员')">维修</el-button>
                        <el-button :disabled="activeConversationEnded" @click="transferTo('管理员')">管理员</el-button>
                        <el-button
                            :icon="Finished"
                            type="success"
                            plain
                            :disabled="activeConversationEnded"
                            @click="markDone"
                        >
                            完成
                        </el-button>
                    </div>

                    <el-alert
                        v-if="activeConversationEnded"
                        class="ended-alert"
                        type="warning"
                        :closable="false"
                        :title="activeConversation.end_reason === 'timeout' ? '会话已超时结束' : '会话已结束'"
                        :description="activeConversation.rating_score ? `用户评分：${activeConversation.rating_score} 分` : '等待会话发起人评分。'"
                    />

                    <div class="message-list">
                        <div
                            v-for="message in chatMessages"
                            :key="message.id"
                            class="message-row"
                            :class="{ mine: message.mine }"
                        >
                            <div class="message-bubble">
                                <div class="message-author">
                                    {{ message.sender_real_name || message.sender_name || '用户' }}
                                    <span v-if="message.sender_role_codes?.length">
                                        · {{ message.sender_role_codes.join(', ') }}
                                    </span>
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
                            :disabled="activeConversationEnded"
                            :placeholder="activeConversationEnded ? '会话已结束，不能继续发送消息' : '输入回复内容'"
                            @keyup.enter.exact.prevent="sendReply"
                        />
                        <el-button type="primary" :loading="sending" :disabled="activeConversationEnded" @click="sendReply">
                            发送
                        </el-button>
                    </div>
                </template>

                <el-empty v-else description="请选择会话" :image-size="120" />
            </section>
        </main>
    </div>
</template>

<style scoped>
.service-chat-page {
    min-width: 1080px;
    height: 100vh;
    display: flex;
    flex-direction: column;
    background: #eef2f7;
    color: #1f2937;
}

.chat-header {
    height: 72px;
    padding: 0 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #ffffff;
    border-bottom: 1px solid #dfe5ee;
}

.app-title {
    font-size: 20px;
    font-weight: 700;
}

.app-subtitle {
    display: flex;
    gap: 16px;
    margin-top: 6px;
    color: #64748b;
    font-size: 13px;
}

.header-actions {
    display: flex;
    gap: 10px;
}

.chat-shell {
    min-height: 0;
    flex: 1;
    display: grid;
    grid-template-columns: 340px minmax(0, 1fr);
}

.conversation-panel {
    min-height: 0;
    background: #ffffff;
    border-right: 1px solid #dfe5ee;
    display: flex;
    flex-direction: column;
}

.conversation-tools {
    padding: 16px;
    display: grid;
    gap: 12px;
    border-bottom: 1px solid #edf1f6;
}

.conversation-list {
    min-height: 0;
    flex: 1;
    overflow-y: auto;
    padding: 8px;
}

.conversation-item {
    width: 100%;
    min-height: 86px;
    padding: 12px;
    margin-bottom: 8px;
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 8px;
    text-align: left;
    border: 1px solid #e5eaf2;
    border-radius: 6px;
    background: #ffffff;
    cursor: pointer;
}

.conversation-item.active {
    border-color: #409eff;
    background: #ecf5ff;
}

.conversation-title {
    font-weight: 600;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.conversation-meta {
    grid-column: 1 / -1;
    color: #64748b;
    font-size: 13px;
}

.chat-panel {
    min-height: 0;
    padding: 18px;
    display: flex;
    flex-direction: column;
}

.chat-titlebar {
    min-height: 72px;
    padding: 0 4px 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #dfe5ee;
}

.chat-title {
    font-size: 20px;
    font-weight: 700;
}

.chat-meta {
    margin-top: 6px;
    color: #64748b;
}

.channel-row {
    padding: 14px 0;
    display: flex;
    gap: 10px;
    border-bottom: 1px solid #dfe5ee;
}

.ended-alert {
    margin: 12px 0 0;
}

.message-list {
    min-height: 0;
    flex: 1;
    overflow-y: auto;
    padding: 18px 4px;
}

.message-row {
    display: flex;
    margin-bottom: 14px;
}

.message-row.mine {
    justify-content: flex-end;
}

.message-bubble {
    max-width: min(680px, 72%);
    padding: 12px 14px;
    border-radius: 8px;
    background: #ffffff;
    border: 1px solid #e5eaf2;
    box-shadow: 0 4px 14px rgb(15 23 42 / 6%);
}

.message-row.mine .message-bubble {
    color: #ffffff;
    background: #2563eb;
    border-color: #2563eb;
}

.message-author {
    margin-bottom: 6px;
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
    margin-top: 8px;
    font-size: 12px;
    color: #94a3b8;
}

.reply-box {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 96px;
    gap: 12px;
    padding-top: 14px;
    border-top: 1px solid #dfe5ee;
}
</style>
