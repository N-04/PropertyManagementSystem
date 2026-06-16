// 文件说明：封装站内即时通讯接口请求。
import request from '@/utils/request'

export function getChatConversationList(params?: any) {
    return request({
        url: '/chat/conversation/list/',
        method: 'get',
        params,
    })
}

export function getChatConversationDetail(id: number) {
    return request({
        url: `/chat/conversation/detail/${id}/`,
        method: 'get',
    })
}

export function createChatConversation(data: any) {
    return request({
        url: '/chat/conversation/create/',
        method: 'post',
        data,
    })
}

export function sendChatMessage(id: number, data: { content: string }) {
    return request({
        url: `/chat/conversation/${id}/message/create/`,
        method: 'post',
        data,
    })
}

export function updateChatConversationStatus(id: number, data: { status: string }) {
    return request({
        url: `/chat/conversation/status/${id}/`,
        method: 'put',
        data,
    })
}
