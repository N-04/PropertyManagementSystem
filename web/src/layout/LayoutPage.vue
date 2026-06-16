<!-- 文件说明：实现二级侧栏、悬浮三级菜单、四级顶部菜单和功能下拉的后台主布局。 -->
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { ArrowDown } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { logoutApi } from '@/api/auth'
import { getUserMenus, buildDisplayMenusByRole } from '@/api/menu'
import { appMenuTitle, fallbackMenus, type AppMenuItem } from '@/menu/fallbackMenus'

defineOptions({
    name: 'LayoutPage',
})

const router = useRouter()
const username = localStorage.getItem('username')
const role = localStorage.getItem('role') || ''
const menuItems = ref<AppMenuItem[]>([])
const menuLoaded = ref(false)
const selectedSecondId = ref('')
const selectedThirdId = ref('')
const selectedFourthId = ref('')
const selectedFunctionTitle = ref('')
const hoveredSecondId = ref('')
const thirdFlyoutTop = ref(60)

const menuKey = (menu: AppMenuItem) => String(menu.id)

const visibleMenus = (menus: AppMenuItem[] = []): AppMenuItem[] => {
    return menus
        .filter((item) => !item.hidden)
        .map((item) => ({
            ...item,
            children: visibleMenus(item.children || []),
        }))
}

const findMenuById = (menus: AppMenuItem[], id: string): AppMenuItem | undefined => {
    for (const menu of menus) {
        if (menuKey(menu) === id) {
            return menu
        }

        const child = findMenuById(menu.children || [], id)

        if (child) {
            return child
        }
    }

    return undefined
}

const findMenuPathByRoute = (
    menus: AppMenuItem[],
    routePath: string,
    parents: AppMenuItem[] = []
): AppMenuItem[] => {
    for (const menu of menus) {
        const currentPath = [...parents, menu]

        if (menu.path === routePath) {
            return currentPath
        }

        const matchedPath = findMenuPathByRoute(menu.children || [], routePath, currentPath)

        if (matchedPath.length) {
            return matchedPath
        }
    }

    return []
}

const childrenOf = (menu?: AppMenuItem) => {
    return (menu?.children || []).filter((item) => item.menu_type !== 2)
}

const menuTargetPath = (menu?: AppMenuItem) => {
    if (!menu?.path) {
        return ''
    }

    const repairStatusMap: Record<string, string> = {
        'repairer-pending': 'assigned',
        'repairer-accepted': 'accepted',
        'repairer-fixing': 'processing',
        'repairer-finished': 'finished',
        'repairer-history': '',
    }
    const repairStatus = repairStatusMap[menuKey(menu)]

    if (repairStatus !== undefined) {
        return repairStatus ? `/repair/list?status=${repairStatus}` : '/repair/list'
    }

    return menu.path
}

const secondMenus = computed(() => {
    return menuItems.value.filter((item) => item.menu_type !== 2)
})

const activeSecondMenu = computed(() => {
    return secondMenus.value.find((item) => menuKey(item) === selectedSecondId.value)
})

const thirdMenus = computed(() => {
    return childrenOf(activeSecondMenu.value)
})

const flyoutSecondMenu = computed(() => {
    return secondMenus.value.find((item) => menuKey(item) === hoveredSecondId.value)
})

const flyoutThirdMenus = computed(() => {
    return childrenOf(flyoutSecondMenu.value)
})

const activeThirdMenu = computed(() => {
    return thirdMenus.value.find((item) => menuKey(item) === selectedThirdId.value)
})

const fourthMenus = computed(() => {
    return childrenOf(activeThirdMenu.value)
})

const activeFourthMenu = computed(() => {
    return fourthMenus.value.find((item) => menuKey(item) === selectedFourthId.value)
})

const functionMenus = computed(() => {
    return activeFourthMenu.value?.children || []
})

const resetFourthSelection = () => {
    selectedFourthId.value = fourthMenus.value[0] ? menuKey(fourthMenus.value[0]) : ''
    selectedFunctionTitle.value = ''
}

const resetThirdSelection = () => {
    selectedThirdId.value = thirdMenus.value[0] ? menuKey(thirdMenus.value[0]) : ''
    resetFourthSelection()
}

const syncSelectionByCurrentRoute = () => {
    const matchedPath = findMenuPathByRoute(menuItems.value, router.currentRoute.value.path)

    if (matchedPath.length) {
        selectedSecondId.value = matchedPath[0] ? menuKey(matchedPath[0]) : ''
        selectedThirdId.value = matchedPath[1] ? menuKey(matchedPath[1]) : ''
        selectedFourthId.value = matchedPath[2] ? menuKey(matchedPath[2]) : ''
        selectedFunctionTitle.value = matchedPath[3]?.title || ''
    }

    if (!selectedSecondId.value && secondMenus.value[0]) {
        selectedSecondId.value = menuKey(secondMenus.value[0])
    }

    if (!selectedThirdId.value) {
        resetThirdSelection()
    }

    if (!selectedFourthId.value) {
        resetFourthSelection()
    }
}

const navigateMenu = (menu?: AppMenuItem) => {
    const targetPath = menuTargetPath(menu)

    if (targetPath && router.currentRoute.value.fullPath !== targetPath) {
        router.push(targetPath)
    }
}

const handleSecondSelect = (id: string) => {
    selectedSecondId.value = id
    resetThirdSelection()
    navigateMenu(activeThirdMenu.value || activeSecondMenu.value)
}

const handleSecondMouseEnter = (item: AppMenuItem, event: MouseEvent) => {
    const target = event.currentTarget as HTMLElement
    const sidebar = target.closest('.second-sidebar')
    const sidebarTop = sidebar?.getBoundingClientRect().top || 0
    const itemTop = target.getBoundingClientRect().top - sidebarTop

    hoveredSecondId.value = menuKey(item)
    thirdFlyoutTop.value = Math.max(60, itemTop)
}

const closeThirdFlyout = () => {
    hoveredSecondId.value = ''
}

const handleThirdSelect = (id: string) => {
    selectedThirdId.value = id
    resetFourthSelection()
    navigateMenu(activeThirdMenu.value)
    closeThirdFlyout()
}

const handleThirdFlyoutClick = (item: AppMenuItem) => {
    if (flyoutSecondMenu.value) {
        selectedSecondId.value = menuKey(flyoutSecondMenu.value)
    }

    handleThirdSelect(menuKey(item))
}

const handleFourthSelect = (menu: AppMenuItem) => {
    selectedFourthId.value = menuKey(menu)
    selectedFunctionTitle.value = ''
    navigateMenu(menu)
}

const handleFunctionSelect = (id: string) => {
    const menu = findMenuById(menuItems.value, id)

    if (!menu) {
        return
    }

    selectedFunctionTitle.value = menu.title
    navigateMenu(menu)
}

const loadMenus = async () => {
    try {
        const res = await getUserMenus()

        if (res.data.code === 200 && res.data.data?.length) {
            menuItems.value = buildDisplayMenusByRole(visibleMenus(res.data.data), role)
            return
        }

        // 后端菜单还没配置时，使用本地菜单，并根据角色过滤
        menuItems.value = buildDisplayMenusByRole(visibleMenus(fallbackMenus), role)
    } catch (error: any) {
        const status = error?.response?.status

        if (status === 401 || status === 403) {
            menuItems.value = []
            return
        }

        // 后端菜单接口异常时，使用本地兜底菜单
        menuItems.value = buildDisplayMenusByRole(visibleMenus(fallbackMenus), role)
    } finally {
        menuLoaded.value = true
        syncSelectionByCurrentRoute()
    }
}

// 退出登录清除role权限
const handleLogout = async () => {
    const refresh = localStorage.getItem('refresh') || ''

    try {
        await logoutApi(refresh)
    } finally {
        localStorage.removeItem('token')
        localStorage.removeItem('refresh')
        localStorage.removeItem('username')
        localStorage.removeItem('role')
        localStorage.removeItem('permissions')
        localStorage.removeItem('userInfo')

        router.push('/login')
    }
}

onMounted(() => {
    loadMenus()
})
</script>

<template>
    <!-- 鼠标从二级菜单移动到三级浮窗不会立刻消失 -->
    <div class="layout-container" @mouseleave="closeThirdFlyout">
        <aside class="second-sidebar">
            <div class="logo">{{ appMenuTitle }}</div>

            <el-menu
                :default-active="selectedSecondId"
                class="second-menu"
                @select="handleSecondSelect"
            >
                <!-- 三级悬浮菜单增加箭头提示 -->
                <el-menu-item
                    v-for="item in secondMenus"
                    :key="item.id"
                    :index="menuKey(item)"
                    @mouseover="handleSecondMouseEnter(item, $event)"
                >
                    <span>{{ item.title }}</span>
                    <span v-if="childrenOf(item).length" class="menu-arrow"> > </span>
                </el-menu-item>
            </el-menu>

            <div
                v-if="hoveredSecondId && flyoutThirdMenus.length"
                class="third-flyout"
                :style="{ top: `${thirdFlyoutTop}px` }"
            >
                <button
                    v-for="item in flyoutThirdMenus"
                    :key="item.id"
                    type="button"
                    class="third-flyout-item"
                    :class="{ active: selectedThirdId === menuKey(item) }"
                    @click="handleThirdFlyoutClick(item)"
                >
                    {{ item.title }}
                </button>
            </div>

            <el-empty
                v-if="menuLoaded && secondMenus.length === 0"
                class="menu-empty"
                description="暂无可访问菜单"
                :image-size="72"
            />
        </aside>

        <main class="layout-main">
            <header class="layout-header">
                <div class="header-title">
                    {{ activeThirdMenu?.title || '后台管理系统' }}
                </div>

                <div class="header-user">
                    {{ username }}
                    <el-button link type="primary" @click="handleLogout">退出登录</el-button>
                </div>
            </header>

            <div v-if="fourthMenus.length" class="fourth-bar">
                <el-dropdown
                    v-for="item in fourthMenus"
                    :key="item.id"
                    trigger="click"
                    @command="handleFunctionSelect"
                >
                    <template #default>
                        <el-button
                            :type="selectedFourthId === menuKey(item) ? 'primary' : 'default'"
                            @click="handleFourthSelect(item)"
                        >
                            {{ item.title }}
                            <el-icon v-if="item.children?.length" class="dropdown-icon">
                                <ArrowDown />
                            </el-icon>
                        </el-button>
                    </template>

                    <template #dropdown>
                        <el-dropdown-menu>
                            <el-dropdown-item v-if="!item.children?.length" disabled command="">
                                暂无功能
                            </el-dropdown-item>
                            <el-dropdown-item
                                v-for="child in item.children"
                                :key="child.id"
                                :command="menuKey(child)"
                            >
                                {{ child.title }}
                            </el-dropdown-item>
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>

                <span v-if="selectedFunctionTitle" class="selected-function">
                    当前功能：{{ selectedFunctionTitle }}
                </span>
            </div>

            <section class="layout-content">
                <router-view />
            </section>
        </main>
    </div>
</template>

<style scoped>
.layout-container {
    display: flex;
    min-width: 1024px;
    height: 100vh;
    background: #f4f6f8;
}

.second-sidebar {
    position: relative;
    width: 220px;
    flex: 0 0 220px;
    background: #ffffff;
    border-right: 1px solid #e4e7ed;
    z-index: 20;
}

.logo {
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 16px;
    font-size: 18px;
    font-weight: 700;
    color: #1f2d3d;
    border-bottom: 1px solid #e4e7ed;
}

.second-menu :deep(.el-menu-item) {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.menu-arrow {
    color: #c0c4cc;
    font-size: 10px;
}

.menu-empty {
    padding: 24px 8px;
}

/* 悬浮菜单 */
.third-flyout {
    position: absolute;
    left: 102%;
    top: 50%;
    transform: translateY(-50%);
    width: 150px;
    max-height: calc(100vh - 72px);
    padding: 8px;
    background: #ffffff;
    border: 1px solid #e4e7ed;
    box-shadow: 0 8px 24px rgb(0 0 0 / 12%);
    overflow-y: auto;
}

.third-flyout-title {
    padding: 8px 10px 10px;
    margin-bottom: 4px;
    font-weight: 600;
    color: #303133;
    border-bottom: 1px solid #ebeef5;
}

.third-flyout-item {
    width: 100%;
    min-height: 38px;
    padding: 8px 10px;
    border: 0;
    border-radius: 4px;
    background: transparent;
    color: #303133;
    text-align: center;
    font-size: 14px;
    cursor: pointer;
}

.third-flyout-item:hover,
.third-flyout-item.active {
    color: #409eff;
    background: #ecf5ff;
}

.layout-main {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
}

.layout-header {
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    background: #ffffff;
    border-bottom: 1px solid #e4e7ed;
}

.header-title {
    font-size: 20px;
    font-weight: 600;
    color: #303133;
}

.header-user {
    display: flex;
    align-items: center;
    gap: 15px;
}

.fourth-bar {
    display: flex;
    align-items: center;
    gap: 10px;
    min-height: 52px;
    padding: 8px 20px;
    background: #ffffff;
    border-bottom: 1px solid #e4e7ed;
    overflow-x: auto;
}

.dropdown-icon {
    margin-left: 6px;
}

.selected-function {
    flex: 0 0 auto;
    margin-left: 8px;
    color: #606266;
    font-size: 15px;
}

.layout-content {
    flex: 1;
    min-width: 0;
    padding: 20px;
    overflow-y: auto;
}
</style>
