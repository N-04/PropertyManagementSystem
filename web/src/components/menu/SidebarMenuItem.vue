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

const visibleChildren = computed(() => {
    return (props.item.children || []).filter((child) => {
        return !child.hidden && child.menu_type !== 2
    })
})

const hasVisibleChildren = computed(() => visibleChildren.value.length > 0)
const menuIndex = computed(() => props.item.path || `menu-${props.item.id}`)
const canNavigate = computed(() => props.item.menu_type !== 2 && Boolean(props.item.path))
</script>

<template>
    <el-sub-menu v-if="hasVisibleChildren" :index="menuIndex">
        <template #title>
            <span class="menu-title">{{ item.title }}</span>
        </template>

        <SidebarMenuItem v-for="child in visibleChildren" :key="child.id" :item="child" />
    </el-sub-menu>

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
