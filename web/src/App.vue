<!-- 文件说明：前端根组件，承载路由页面渲染。 -->
<script setup lang="ts">
// Element Plus 语言包分块：全局统一组件库的中文文案。
import zhCn from 'element-plus/es/locale/lang/zh-cn'
</script>

<template>
    <!-- 全局容器分块：在根节点注入中文 locale，再交给路由渲染具体页面。 -->
    <el-config-provider :locale="zhCn">
        <router-view />
    </el-config-provider>
</template>

<style>
/* 主题变量分块：集中维护后台 UI 的字体、颜色、阴影和状态色 token。 */
:root {
    --font-family-base: Inter, "PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", "Noto Sans SC", Arial, sans-serif;
    --title-font-family: var(--font-family-base);
    --text-primary: #17283a;
    --text-heading: #0f172a;
    --text-muted: #6a7b8f;
    --text-subtle: #41536a;
    --brand-primary: #008f7a;
    --brand-primary-hover: #00b69b;
    --brand-primary-soft: #dff8f3;
    --brand-primary-subtle: #eefaf7;
    --warning-primary: #ff9f3d;
    --danger-primary: #ff6448;
    --success-primary: #38b86f;
    --blue-primary: #2d7ff9;
    --blue-primary-soft: #e8f1ff;
    --surface-page: #f4f8fb;
    --surface-card: #ffffff;
    --surface-muted: #f7fbfd;
    --border-color: #dce7ee;
    --border-soft: #edf3f6;
    --shadow-panel: 0 18px 45px rgba(39, 64, 89, 0.08);
    --shadow-panel-strong: 0 18px 45px rgba(39, 64, 89, 0.12);
    --shadow-active: 0 14px 28px rgba(0, 143, 122, 0.22);
}

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    color: var(--text-primary);
    background: var(--surface-page);
    font-family: var(--font-family-base);
    font-size: 14px;
    font-weight: 400;
    line-height: 1.5;
    letter-spacing: 0;
}

button,
input,
textarea {
    font-family: inherit;
    letter-spacing: 0;
}

h1,
h2,
h3,
.logo,
.page-title,
.panel-title,
.workbench-heading h1,
.panel-header h2 {
    font-family: var(--title-font-family);
}
</style>
