// 文件说明：集中管理前端访问后端接口和媒体文件的地址拼接。

// 路径规范化分块：去掉尾部斜杠，避免拼接接口时出现双斜杠。
const trimTrailingSlash = (value: string) => value.replace(/\/+$/, '')

// 本地 Vite 开发默认连 Django 8000；生产环境默认使用当前站点同源地址。
const defaultApiOrigin = import.meta.env.DEV
    ? 'http://127.0.0.1:8000'
    : window.location.origin

export const apiOrigin = trimTrailingSlash(
    import.meta.env.VITE_API_ORIGIN || defaultApiOrigin,
)

export const apiBaseURL = trimTrailingSlash(
    import.meta.env.VITE_API_BASE_URL || `${apiOrigin}/api`,
)

// API 地址分块：给 axios、导出下载和手工拼接接口共用同一个根路径。
export const toApiURL = (path = '') => {
    // 导出、下载等非 axios 场景复用同一 API 根地址，避免硬编码本机 HTTP。
    const normalizedPath = path.startsWith('/') ? path : `/${path}`

    return `${apiBaseURL}${normalizedPath}`
}

// 媒体地址分块：把后端返回的媒体相对路径转换为完整浏览器 URL。
export const toMediaURL = (path = '') => {
    // 上传接口可能返回绝对 URL 或相对媒体路径，这里统一转成浏览器可访问地址。
    if (!path) {
        return ''
    }

    if (/^https?:\/\//i.test(path)) {
        return path
    }

    const normalizedPath = path.startsWith('/') ? path : `/${path}`

    return `${apiOrigin}${normalizedPath}`
}
