// 文件说明：前端应用入口，创建 Vue 应用并挂载插件。
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import 'element-plus/dist/index.css'

import { createPinia } from 'pinia'
const app = createApp(App)
app.use(router)
app.use(ElementPlus, {
    locale: zhCn,
})
app.use(createPinia())
app.mount('#app')
