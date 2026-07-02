// 文件说明：同步顶部社区下拉选择，供资源列表按当前社区过滤数据。
import { onBeforeUnmount, onMounted, ref } from 'vue'

const COMMUNITY_STORAGE_KEY = 'selectedCommunityId'
const COMMUNITY_CHANGED_EVENT = 'property-management-community-changed'

export const readSelectedCommunityId = () => {
    return localStorage.getItem(COMMUNITY_STORAGE_KEY) || ''
}

export const getSelectedCommunityParams = (selectedId: string): Record<string, string> => {
    if (!selectedId || selectedId === 'default') {
        return {}
    }

    return { community: selectedId }
}

export const matchesSelectedCommunity = (
    row: Record<string, unknown>,
    selectedId: string,
    fields: string[] = ['community', 'community_id']
) => {
    if (!selectedId || selectedId === 'default') {
        return true
    }

    return fields.some((field) => row[field] != null && String(row[field]) === selectedId)
}

export const useSelectedCommunity = (onChange?: () => void) => {
    const selectedCommunityId = ref(readSelectedCommunityId())

    const syncSelectedCommunity = () => {
        selectedCommunityId.value = readSelectedCommunityId()
        onChange?.()
    }

    onMounted(() => {
        window.addEventListener(COMMUNITY_CHANGED_EVENT, syncSelectedCommunity)
    })

    onBeforeUnmount(() => {
        window.removeEventListener(COMMUNITY_CHANGED_EVENT, syncSelectedCommunity)
    })

    return {
        selectedCommunityId,
        syncSelectedCommunity,
    }
}
