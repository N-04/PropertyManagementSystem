// 文件说明：为本地列表页提供统一的关键字模糊搜索能力。
import { computed, type Ref } from 'vue'

const normalizeValue = (value: unknown) => {
    return String(value ?? '').trim().toLowerCase()
}

export function useKeywordFilter<T extends Record<string, any>>(
    source: Ref<T[]>,
    keyword: Ref<string>,
    fields: Array<keyof T | string>
) {
    return computed(() => {
        const text = normalizeValue(keyword.value)

        if (!text) {
            return source.value
        }

        // 只匹配页面声明的字段，避免把无关隐藏数据误纳入搜索结果。
        return source.value.filter((item) => {
            return fields.some((field) => normalizeValue(item[field as keyof T]).includes(text))
        })
    })
}
