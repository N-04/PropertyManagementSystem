// 文件说明：为本地列表页提供统一的关键字模糊搜索能力。
import { computed, type ComputedRef, type Ref } from 'vue'

const normalizeValue = (value: unknown) => {
    // 搜索比较统一转小写字符串，兼容数字、空值和后端返回的枚举字段。
    return String(value ?? '').trim().toLowerCase()
}

export function useKeywordFilter<T extends Record<string, any>>(
    source: Ref<T[]> | ComputedRef<T[]>,
    keyword: Ref<string>,
    fields: Array<keyof T | string>
) {
    return computed(() => {
        // 关键字为空时直接返回原数据，避免不必要的数组复制。
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
