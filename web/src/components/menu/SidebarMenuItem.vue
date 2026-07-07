<!-- 文件说明：递归渲染后台左侧菜单树，支持多级菜单和叶子路由。 -->
<script setup lang="ts">
import { computed } from 'vue'

defineOptions({
    name: 'SidebarMenuItem',
})

type SidebarMenu = {
    id: number | string
    title?: string
    path?: string
    hidden?: boolean
    menu_type?: number
    children?: SidebarMenu[]
}

const props = defineProps<{
    item: SidebarMenu
}>()

// 菜单数据分块：过滤隐藏菜单和接口权限节点，只把可见菜单交给侧边栏渲染。
const visibleChildren = computed(() => {
    return (props.item.children || []).filter((child) => {
        return !child.hidden && child.menu_type !== 2
    })
})

const hasVisibleChildren = computed(() => visibleChildren.value.length > 0)
const menuIndex = computed(() => props.item.path || `menu-${props.item.id}`)
// 叶子节点只有具备真实 path 时才允许跳转，避免空路径菜单变成可点击项。
const canNavigate = computed(() => props.item.menu_type !== 2 && Boolean(props.item.path))
</script>

<template>
    <!-- 子菜单分块：有可见子节点时递归渲染。 -->
    <el-sub-menu v-if="hasVisibleChildren" :index="menuIndex">
        <template #title>
            <span class="menu-title">{{ item.title }}</span>
        </template>

        <SidebarMenuItem v-for="child in visibleChildren" :key="child.id" :item="child" />
    </el-sub-menu>

    <!-- 叶子菜单分块：没有子节点时渲染最终路由入口。 -->
    <el-menu-item v-else-if="canNavigate" :index="item.path">
        <span class="menu-title">{{ item.title }}</span>
    </el-menu-item>
</template>

<style scoped>
.menu-title {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
</style>
