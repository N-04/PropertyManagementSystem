// 文件说明：封装前端通用工具逻辑。
import axios from 'axios'

// 创建 axios 实例
const request = axios.create({
    // Django 地址
    baseURL: 'http://127.0.0.1:8000/api',

    // 超时时间
    timeout: 5000,
})

// axios 请求拦截器
request.interceptors.request.use((config) => {
    // 获取 token
    const token = localStorage.getItem('token')

    // 如果 token 存在
    if (token) {
        // 自动携带 token
        config.headers.Authorization = `Bearer ${token}`
    }

    return config
})

// 导出
export default request
