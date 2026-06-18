<!-- 文件说明：前端根组件，承载路由页面渲染。 -->
<script setup lang="ts">
import zhCn from 'element-plus/es/locale/lang/zh-cn'
</script>

<template>
    <el-config-provider :locale="zhCn">
        <router-view />
    </el-config-provider>
</template>

<style>
:root {
    --font-family-base: "PingFang SC", "Microsoft YaHei", "Noto Sans SC", Inter, Arial, sans-serif;
    --title-font-family: var(--font-family-base);
    --text-primary: #334155;
    --text-heading: #0f172a;
    --text-muted: #64748b;
    --text-subtle: #475569;
    --brand-primary: #0f766e;
    --brand-primary-hover: #0b625b;
    --brand-primary-soft: #e4f5f2;
    --brand-primary-subtle: #f3fbfa;
    --warning-primary: #f59f00;
    --surface-page: #f5f7fa;
    --surface-card: #ffffff;
    --surface-muted: #f8fafc;
    --border-color: #e4e7ed;
    --border-soft: #edf1f6;
}

body {
    color: var(--text-primary);
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
