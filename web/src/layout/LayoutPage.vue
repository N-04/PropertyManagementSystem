<!-- 文件说明：实现左侧一/二级菜单、顶部三级功能菜单和内容区的后台主布局。 -->
<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { ArrowDown } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { logoutApi } from '@/api/auth'
import { getUserMenus, buildDisplayMenusByRole } from '@/api/menu'
import { getComplaintList } from '@/api/complaint'
import { getFeeList } from '@/api/fee'
import { getNoticeList } from '@/api/notice'
import { getRepairList } from '@/api/repair'
import { appMenuTitle, fallbackMenus, type AppMenuItem } from '@/menu/fallbackMenus'
import {
    AUTH_STATE_CHANGED_EVENT,
    clearAuthState,
    getStoredRefresh,
    getStoredRole,
    getStoredUsername,
} from '@/utils/authState'

defineOptions({
    name: 'LayoutPage',
})

const router = useRouter()
const username = ref(getStoredUsername())
const role = ref(getStoredRole())
const menuItems = ref<AppMenuItem[]>([])
const menuLoaded = ref(false)
const selectedSecondId = ref('')
const selectedThirdId = ref('')
const selectedFourthId = ref('')
const selectedFunctionTitle = ref('')
const hoveredSecondId = ref('')
const thirdFlyoutTop = ref(60)
const noticeMessages = ref<string[]>([])
const roleMessages = ref<string[]>([])

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

const canReceiveNotice = computed(() => {
    // 公告接收方只包含管理员和业主；财务/维修只进入公告发布列表。
    return ['owner', 'property_admin', 'admin', 'super_admin'].includes(role.value)
})

const rollingMessages = computed(() => {
    const messages = [...noticeMessages.value, ...roleMessages.value].filter(Boolean)

    if (messages.length) {
        return messages.slice(0, 8)
    }

    return ['系统运行正常，欢迎使用社区物业管理系统']
})

const rollingText = computed(() => rollingMessages.value.join('　　'))

const firstReachableMenu = (menu?: AppMenuItem): AppMenuItem | undefined => {
    if (!menu) {
        return undefined
    }

    if (menu.path) {
        return menu
    }

    for (const child of childrenOf(menu)) {
        const target = firstReachableMenu(child)

        if (target) {
            return target
        }
    }

    return undefined
}

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
    navigateMenu(firstReachableMenu(activeThirdMenu.value || activeSecondMenu.value))
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
    navigateMenu(firstReachableMenu(activeFourthMenu.value || activeThirdMenu.value))
}

const handleThirdFlyoutClick = (item: AppMenuItem) => {
    if (flyoutSecondMenu.value) {
        selectedSecondId.value = menuKey(flyoutSecondMenu.value)
    }

    handleThirdSelect(menuKey(item))
    closeThirdFlyout()
}

const handleFourthSelect = (menu: AppMenuItem) => {
    selectedFourthId.value = menuKey(menu)
    selectedFunctionTitle.value = ''
    navigateMenu(firstReachableMenu(menu))
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
    const currentRole = role.value

    try {
        const res = await getUserMenus()

        if (res.data.code === 200 && res.data.data?.length) {
            menuItems.value = buildDisplayMenusByRole(visibleMenus(res.data.data), currentRole)
            return
        }

        // 后端菜单还没配置时，使用本地菜单，并根据角色过滤
        menuItems.value = buildDisplayMenusByRole(visibleMenus(fallbackMenus), currentRole)
    } catch (error: any) {
        const status = error?.response?.status

        if (status === 401 || status === 403) {
            menuItems.value = []
            return
        }

        // 后端菜单接口异常时，使用本地兜底菜单
        menuItems.value = buildDisplayMenusByRole(visibleMenus(fallbackMenus), currentRole)
    } finally {
        menuLoaded.value = true
        syncSelectionByCurrentRoute()
    }
}

const loadNoticeMessages = async () => {
    if (!canReceiveNotice.value) {
        noticeMessages.value = []
        return
    }

    try {
        const res = await getNoticeList()
        const list = res.data.data || []

        noticeMessages.value = list
            .filter((item: any) => item.status !== 'draft')
            .slice(0, 3)
            .map((item: any) => `公告通知：${item.title}`)
    } catch (error) {
        noticeMessages.value = []
    }
}

const loadRoleMessages = async () => {
    const messages: string[] = []
    const currentRole = role.value

    try {
        if (['owner', 'finance', 'finance_staff', 'admin', 'super_admin'].includes(currentRole)) {
            const feeRes = await getFeeList()
            const fees = feeRes.data.data || []
            const unpaidFees = fees.filter((item: any) => item.status === 'unpaid' || item.status === 'overdue')

            if (unpaidFees.length) {
                messages.push(`缴费提醒：当前有 ${unpaidFees.length} 条待缴或逾期账单`)
            }
        }
    } catch (error) {
        // 滚动通知只是提醒入口，接口失败不影响页面主体。
    }

    try {
        if (['owner', 'repair_staff', 'repair', 'property_admin', 'admin', 'super_admin'].includes(currentRole)) {
            const repairRes = await getRepairList({})
            const repairs = repairRes.data.data || []
            const activeRepairs = repairs.filter((item: any) => item.status !== 'finished')

            if (activeRepairs.length) {
                messages.push(`工单通知：当前有 ${activeRepairs.length} 条待处理或进行中工单`)
            }
        }
    } catch (error) {
        // 滚动通知只是提醒入口，接口失败不影响页面主体。
    }

    try {
        if (['property_admin', 'customer_service', 'service', 'admin', 'super_admin'].includes(currentRole)) {
            const complaintRes = await getComplaintList({ status: 'pending' })
            const complaints = complaintRes.data.data || []

            if (complaints.length) {
                messages.push(`投诉提醒：当前有 ${complaints.length} 条投诉/建议待处理`)
            }
        }
    } catch (error) {
        // 滚动通知只是提醒入口，接口失败不影响页面主体。
    }

    roleMessages.value = messages
}

const loadRollingMessages = () => {
    loadNoticeMessages()
    loadRoleMessages()
}

const reloadMenusForCurrentRole = () => {
    selectedSecondId.value = ''
    selectedThirdId.value = ''
    selectedFourthId.value = ''
    selectedFunctionTitle.value = ''
    menuLoaded.value = false
    loadMenus()
}

const refreshLayoutAuthState = () => {
    const nextUsername = getStoredUsername()
    const nextRole = getStoredRole()
    const roleChanged = nextRole !== role.value

    username.value = nextUsername
    role.value = nextRole

    if (roleChanged) {
        reloadMenusForCurrentRole()
        loadRollingMessages()
    }
}

// 退出登录清除role权限
const handleLogout = async () => {
    const refresh = getStoredRefresh()

    try {
        await logoutApi(refresh)
    } finally {
        clearAuthState()

        router.push('/login')
    }
}

onMounted(() => {
    window.addEventListener(AUTH_STATE_CHANGED_EVENT, refreshLayoutAuthState)
    loadMenus()
    loadRollingMessages()
})

onBeforeUnmount(() => {
    window.removeEventListener(AUTH_STATE_CHANGED_EVENT, refreshLayoutAuthState)
})

watch(
    () => router.currentRoute.value.fullPath,
    () => {
        if (menuLoaded.value) {
            // 页面内跳转、浏览器前进后退后，同步二/三/四级菜单和功能下拉选中态。
            syncSelectionByCurrentRoute()
        }
    }
)
</script>

<template>
    <div class="layout-container" @mouseleave="closeThirdFlyout">
        <aside class="second-sidebar">
            <div class="logo">{{ appMenuTitle }}</div>

            <div class="sidebar-menu">
                <section v-for="item in secondMenus" :key="item.id" class="sidebar-group">
                    <button
                        type="button"
                        class="first-menu-item"
                        :class="{ active: selectedSecondId === menuKey(item) }"
                        @click="handleSecondSelect(menuKey(item))"
                        @mouseover="handleSecondMouseEnter(item, $event)"
                    >
                        <span>{{ item.title }}</span>
                        <span v-if="childrenOf(item).length" class="menu-arrow"> > </span>
                    </button>
                </section>
            </div>

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
                    {{ activeThirdMenu?.title || activeSecondMenu?.title || '后台管理系统' }}
                </div>

                <div class="header-user">
                    {{ username }}
                    <el-button link type="primary" @click="handleLogout">退出登录</el-button>
                </div>
            </header>

            <div v-if="fourthMenus.length" class="third-bar">
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

            <div class="notice-marquee" aria-label="滚动通知">
                <div class="notice-label">滚动通知</div>
                <div class="notice-track">
                    <div class="notice-content">{{ rollingText }}</div>
                </div>
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

.sidebar-menu {
    height: calc(100vh - 60px);
    padding: 12px;
    overflow-y: auto;
}

.sidebar-group + .sidebar-group {
    margin-top: 6px;
}

.first-menu-item {
    width: 100%;
    border: 0;
    border-radius: 4px;
    background: transparent;
    color: #303133;
    cursor: pointer;
    text-align: left;
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-height: 42px;
    padding: 0 14px;
    font-size: 16px;
    font-weight: 700;
}

.menu-arrow {
    color: #c0c4cc;
    font-size: 10px;
}

.first-menu-item:hover,
.first-menu-item.active {
    color: #409eff;
    background: #ecf5ff;
}

.menu-empty {
    padding: 24px 8px;
}

/* 二级菜单保持悬浮样式，避免左侧栏被深层菜单撑开。 */
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

.third-bar {
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

.notice-marquee {
    display: flex;
    align-items: center;
    gap: 12px;
    min-height: 42px;
    padding: 0 20px;
    border-bottom: 1px solid #e4e7ed;
    background: #f8fafc;
    overflow: hidden;
}

.notice-label {
    flex: 0 0 auto;
    color: #409eff;
    font-weight: 600;
}

.notice-track {
    flex: 1;
    min-width: 0;
    overflow: hidden;
    white-space: nowrap;
}

.notice-content {
    display: inline-block;
    min-width: 100%;
    color: #606266;
    text-align: left;
    animation: notice-scroll 22s linear infinite;
}

@keyframes notice-scroll {
    0% {
        transform: translateX(100%);
    }

    100% {
        transform: translateX(-100%);
    }
}

.layout-content {
    flex: 1;
    min-width: 0;
    padding: 20px;
    overflow-y: auto;
}
</style>
