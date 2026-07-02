<!-- 文件说明：实现左侧一/二级菜单、顶部三级功能菜单和内容区的后台主布局。 -->
<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch, type Component } from 'vue'
import {
    ArrowDown,
    ArrowRight,
    Bell,
    ChatDotRound,
    DataAnalysis,
    Document,
    HomeFilled,
    Menu as MenuIcon,
    Money,
    OfficeBuilding,
    Operation,
    Search,
    Setting,
    Tickets,
    Tools,
    User,
    Van,
} from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { logoutApi } from '@/api/auth'
import { getCommunityList } from '@/api/community'
import { getUserMenus, buildDisplayMenusByRole } from '@/api/menu'
import { useRealtimeRefresh } from '@/composables/useRealtimeRefresh'
import { appMenuTitle, fallbackMenus, type AppMenuItem } from '@/menu/fallbackMenus'
import {
    getImmediateMessageRows,
    loadMessageCenterRows,
    MESSAGE_FEEDBACK_EVENTS,
    MESSAGE_FEEDBACK_STORAGE_KEYS,
    type MessageRow,
} from '@/utils/messageCenterRows'
import {
    AUTH_STATE_CHANGED_EVENT,
    clearAuthState,
    getStoredRefresh,
    getStoredRole,
    getStoredUsername,
} from '@/utils/authState'
import { extractListRows } from '@/utils/listResponse'

defineOptions({
    name: 'LayoutPage',
})

const router = useRouter()
// 布局状态分块：当前用户、菜单选中态和消息角标都随标签页登录态独立刷新。
const username = ref(getStoredUsername())
const role = ref(getStoredRole())
const menuItems = ref<AppMenuItem[]>([])
const menuLoaded = ref(false)
const selectedFirstId = ref('')
const selectedSecondId = ref('')
const selectedThirdId = ref('')
const selectedFunctionTitle = ref('')
const expandedFirstIds = ref<string[]>([])
const messageCenterRows = ref<MessageRow[]>(getImmediateMessageRows(role.value))
const selectedCommunityId = ref(localStorage.getItem('selectedCommunityId') || '')
const communityOptions = ref([
    {
        id: 'default',
        name: '幸福里小区',
    },
])
let menuLoadRequestId = 0
let messageLoadRequestId = 0

type RequestError = {
    response?: {
        status?: number
    }
}

type CommunityRow = {
    id?: number | string
    name?: string
    community_name?: string
}

const getErrorStatus = (error: unknown) => {
    return (error as RequestError | undefined)?.response?.status
}

// 角色展示映射：兼容后端历史角色编码，顶部身份胶囊始终显示中文。
const roleTitleMap: Record<string, string> = {
    admin: '物业管理员',
    super_admin: '超级管理员',
    property_admin: '物业管理员',
    finance_staff: '财务人员',
    finance: '财务人员',
    repair_staff: '维修员',
    repairer: '维修员',
    repair: '维修员',
    owner: '业主',
}

const roleTitle = computed(() => roleTitleMap[role.value] || '用户')
const usernameInitial = computed(() => (username.value || '用').slice(0, 1).toUpperCase())
const notificationCount = computed(() => messageCenterRows.value.length)
const selectedCommunityName = computed(() => {
    return communityOptions.value.find((item) => item.id === selectedCommunityId.value)?.name
        || communityOptions.value[0]?.name
        || '幸福里小区'
})

// 顶部搜索提示按角色切换，避免不同工作台看到无关的业务关键词。
const searchPlaceholder = computed(() => {
    if (['repair_staff', 'repairer', 'repair'].includes(role.value)) {
        return '搜索工单号、业主、房号、报修类型等'
    }

    if (['finance_staff', 'finance'].includes(role.value)) {
        return '搜索功能、账单、业主、房号等'
    }

    if (role.value === 'owner') {
        return '搜索功能、公告、服务等'
    }

    return '搜索功能、业主、房号、电话等'
})

const resolveMenuIcon = (menu: AppMenuItem): Component => {
    // 后端未配置图标时，通过标题语义兜底出统一的菜单图标。
    const title = menu.title || ''

    if (title.includes('工作台') || title.includes('首页')) return HomeFilled
    if (title.includes('用户') || title.includes('业主') || title.includes('个人')) return User
    if (title.includes('小区') || title.includes('房产') || title.includes('房屋') || title.includes('楼栋')) return OfficeBuilding
    if (title.includes('车位') || title.includes('车辆')) return Van
    if (title.includes('工单') || title.includes('维修') || title.includes('报修')) return Tools
    if (title.includes('收费') || title.includes('缴费') || title.includes('费用') || title.includes('财务')) return Money
    if (title.includes('公告') || title.includes('消息') || title.includes('通知')) return Bell
    if (title.includes('投诉') || title.includes('建议')) return ChatDotRound
    if (title.includes('访客')) return Tickets
    if (title.includes('日志') || title.includes('审计')) return Operation
    if (title.includes('报表') || title.includes('统计')) return DataAnalysis
    if (title.includes('系统') || title.includes('设置') || title.includes('角色')) return Setting
    if (title.includes('文件') || title.includes('上传')) return Document

    return MenuIcon
}

const menuKey = (menu: AppMenuItem) => String(menu.id)

const visibleMenus = (menus: AppMenuItem[] = []): AppMenuItem[] => {
    // 隐藏菜单不参与导航和高亮，但保留可见子节点的层级结构。
    return menus
        .filter((item) => !item.hidden)
        .map((item) => ({
            ...item,
            children: visibleMenus(item.children || []),
        }))
}

const buildFallbackMenusForRole = (targetRole = role.value) => {
    // 本地兜底菜单仍按角色过滤，避免菜单接口异常时暴露其他角色入口。
    return buildDisplayMenusByRole(visibleMenus(fallbackMenus), targetRole)
}

const applyImmediateMenus = (targetRole = role.value) => {
    // 首屏先使用本地菜单，后端菜单回来后再无感替换。
    menuItems.value = buildFallbackMenusForRole(targetRole)
    menuLoaded.value = true
    syncSelectionByCurrentRoute()
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

// 路由匹配分块：优先完整匹配 query，防止同路径不同 query 的菜单互相串位。
const findMenuPathByRoute = (
    menus: AppMenuItem[],
    routePath: string,
    routeFullPath = routePath,
    parents: AppMenuItem[] = []
): AppMenuItem[] => {
    const allowBaseMatch = !routeFullPath.includes('?')

    for (const menu of menus) {
        const currentPath = [...parents, menu]
        const menuPath = menu.path || ''
        const menuRoutePath = menuPath.split('?')[0]

        // 带 query 的菜单必须完整匹配；无 query 的基础页才允许路径兜底。
        if (
            menuPath === routeFullPath
            || (allowBaseMatch && !menuPath.includes('?') && menuRoutePath === routePath)
        ) {
            return currentPath
        }

        const matchedPath = findMenuPathByRoute(menu.children || [], routePath, routeFullPath, currentPath)

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

    return menu.path
}

// 菜单层级分块：一级侧栏、二级折叠、三级顶部栏和功能下拉分别派生。
const firstMenus = computed(() => {
    return menuItems.value.filter((item) => item.menu_type !== 2)
})

const activeFirstMenu = computed(() => {
    return firstMenus.value.find((item) => menuKey(item) === selectedFirstId.value)
})

const secondMenus = computed(() => {
    return childrenOf(activeFirstMenu.value)
})

const activeSecondMenu = computed(() => {
    return secondMenus.value.find((item) => menuKey(item) === selectedSecondId.value)
})

const thirdMenus = computed(() => {
    return childrenOf(activeSecondMenu.value)
})

const activeThirdMenu = computed(() => {
    return thirdMenus.value.find((item) => menuKey(item) === selectedThirdId.value)
})

const firstReachableMenu = (menu?: AppMenuItem): AppMenuItem | undefined => {
    // 分组菜单本身没有 path 时，落到它的第一个可访问子页面。
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

const expandFirstMenu = (id: string) => {
    // 左侧菜单采用手风琴模式，同一时间只展开并聚焦一个一级菜单。
    expandedFirstIds.value = id ? [id] : []
}

const toggleFirstMenu = (id: string) => {
    if (expandedFirstIds.value.includes(id)) {
        expandedFirstIds.value = []
        return
    }

    expandFirstMenu(id)
}

const isFirstExpanded = (id: string) => {
    return expandedFirstIds.value.includes(id)
}

const resetThirdSelection = () => {
    selectedThirdId.value = thirdMenus.value[0] ? menuKey(thirdMenus.value[0]) : ''
    selectedFunctionTitle.value = ''
}

const resetSecondSelection = () => {
    selectedSecondId.value = secondMenus.value[0] ? menuKey(secondMenus.value[0]) : ''
    resetThirdSelection()
}

const syncSelectionByCurrentRoute = () => {
    // 刷新页面或复制标签进入时，根据当前 URL 还原菜单焦点。
    const exactMatchedPath = findMenuPathByRoute(
        menuItems.value,
        router.currentRoute.value.path,
        router.currentRoute.value.fullPath
    )
    const matchedPath = exactMatchedPath.length
        ? exactMatchedPath
        : findMenuPathByRoute(menuItems.value, router.currentRoute.value.path)

    if (matchedPath.length) {
        selectedFirstId.value = matchedPath[0] ? menuKey(matchedPath[0]) : ''
        selectedSecondId.value = matchedPath[1] ? menuKey(matchedPath[1]) : ''
        selectedThirdId.value = matchedPath[2] ? menuKey(matchedPath[2]) : ''
        selectedFunctionTitle.value = matchedPath[3]?.title || ''
    }

    if (!selectedFirstId.value && firstMenus.value[0]) {
        selectedFirstId.value = menuKey(firstMenus.value[0])
    }

    if (selectedFirstId.value) {
        expandFirstMenu(selectedFirstId.value)
    }

    if (
        secondMenus.value.length
        && !secondMenus.value.some((item) => menuKey(item) === selectedSecondId.value)
    ) {
        resetSecondSelection()
    }

    if (
        thirdMenus.value.length
        && !thirdMenus.value.some((item) => menuKey(item) === selectedThirdId.value)
    ) {
        resetThirdSelection()
    }
}

const navigateMenu = (menu?: AppMenuItem) => {
    const targetPath = menuTargetPath(menu)

    // 重复点击当前菜单不重复 push，避免浏览器历史记录堆叠。
    if (targetPath && router.currentRoute.value.fullPath !== targetPath) {
        router.push(targetPath)
    }
}

const handleFirstSelect = (item: AppMenuItem) => {
    const id = menuKey(item)
    const wasCurrentFirstMenu = selectedFirstId.value === id
    selectedFirstId.value = id
    selectedFunctionTitle.value = ''

    if (childrenOf(item).length) {
        // 一级菜单有子项时只折叠/展开，并跳到当前分组下第一个可达页面。
        if (wasCurrentFirstMenu) {
            toggleFirstMenu(id)
        } else {
            expandFirstMenu(id)
        }

        resetSecondSelection()
        navigateMenu(firstReachableMenu(activeThirdMenu.value || activeSecondMenu.value || activeFirstMenu.value))
        return
    }

    selectedSecondId.value = ''
    selectedThirdId.value = ''
    navigateMenu(item)
}

const handleSecondSelect = (parent: AppMenuItem, item: AppMenuItem) => {
    selectedFirstId.value = menuKey(parent)
    expandFirstMenu(menuKey(parent))
    selectedSecondId.value = menuKey(item)
    resetThirdSelection()
    navigateMenu(firstReachableMenu(activeThirdMenu.value || activeSecondMenu.value))
}

const handleThirdSelect = (item: AppMenuItem) => {
    // 三级菜单可能只是功能组，实际路径由它自己或第一个子功能提供。
    const id = menuKey(item)
    selectedThirdId.value = id
    selectedFunctionTitle.value = ''
    navigateMenu(firstReachableMenu(item))
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
    // 菜单加载分块：通过请求序号防止切换账号后旧请求覆盖新角色菜单。
    const requestId = ++menuLoadRequestId
    const requestRole = role.value
    const requestUsername = username.value

    const acceptCurrentMenuRequest = () => {
        // 角色和用户名都一致才接收结果，解决复制标签切换账号后的菜单错乱。
        return (
            requestId === menuLoadRequestId
            && requestRole === role.value
            && requestUsername === username.value
        )
    }

    if (!menuItems.value.length) {
        applyImmediateMenus(requestRole)
    } else {
        menuLoaded.value = true
    }

    try {
        const res = await getUserMenus()

        if (!acceptCurrentMenuRequest()) {
            return
        }

        if (res.data.code === 200 && res.data.data?.length) {
            menuItems.value = buildDisplayMenusByRole(visibleMenus(res.data.data), requestRole)
            return
        }

        // 后端菜单还没配置时，使用本地菜单，并根据角色过滤
        menuItems.value = buildFallbackMenusForRole(requestRole)
    } catch (error: unknown) {
        if (!acceptCurrentMenuRequest()) {
            return
        }

        const status = getErrorStatus(error)

        if (status === 401 || status === 403) {
            menuItems.value = []
            return
        }

        // 后端菜单接口异常时，使用本地兜底菜单
        menuItems.value = buildFallbackMenusForRole(requestRole)
    } finally {
        if (acceptCurrentMenuRequest()) {
            menuLoaded.value = true
            syncSelectionByCurrentRoute()
        }
    }
}

const loadNotificationMessages = async () => {
    // 顶部消息角标复用消息中心数据，保证入口数字和列表来源一致。
    const requestId = ++messageLoadRequestId
    const requestRole = role.value
    const requestUsername = username.value

    if (!messageCenterRows.value.length) {
        messageCenterRows.value = getImmediateMessageRows(requestRole)
    }

    const rows = await loadMessageCenterRows(requestRole)

    if (
        requestId !== messageLoadRequestId
        || requestRole !== role.value
        || requestUsername !== username.value
    ) {
        // 旧消息请求返回时直接丢弃，避免显示上一个账号的未读数。
        return
    }

    messageCenterRows.value = rows
}

const loadCommunities = async () => {
    // 顶部小区下拉分块：后端可用时展示真实小区，失败时保留默认演示项。
    try {
        const res = await getCommunityList({ page_size: 20 })
        const rows = extractListRows<CommunityRow>(res.data.data)
        const options = rows
            .map((item) => ({
                id: item.id == null ? '' : String(item.id),
                name: item.name || item.community_name || '未命名小区',
            }))
            .filter((item) => item.id && item.name)

        if (options.length) {
            communityOptions.value = options
        }
    } catch {
        communityOptions.value = communityOptions.value.length
            ? communityOptions.value
            : [{ id: 'default', name: '幸福里小区' }]
    }

    if (!communityOptions.value.some((item) => item.id === selectedCommunityId.value)) {
        selectedCommunityId.value = communityOptions.value[0]?.id || 'default'
        localStorage.setItem('selectedCommunityId', selectedCommunityId.value)
    }
}

const handleCommunityCommand = (id: string) => {
    // 先记录当前选择，其他页面后续需要按小区过滤时可监听这个事件。
    selectedCommunityId.value = id
    localStorage.setItem('selectedCommunityId', id)
    window.dispatchEvent(new CustomEvent('property-management-community-changed', {
        detail: {
            id,
            name: selectedCommunityName.value,
        },
    }))
}

const reloadMenusForCurrentRole = () => {
    // 角色切换后清空旧选中态，再重新加载当前角色菜单。
    selectedFirstId.value = ''
    selectedSecondId.value = ''
    selectedThirdId.value = ''
    selectedFunctionTitle.value = ''
    expandedFirstIds.value = []
    applyImmediateMenus(role.value)
    loadMenus()
}

const refreshLayoutAuthState = () => {
    // 登录态刷新分块：监听全局登录事件，实时同步顶部用户名和菜单权限。
    const nextUsername = getStoredUsername()
    const nextRole = getStoredRole()
    const roleChanged = nextRole !== role.value
    const usernameChanged = nextUsername !== username.value
    const authIdentityChanged = roleChanged || usernameChanged

    username.value = nextUsername
    role.value = nextRole

    if (authIdentityChanged) {
        // 复制标签、切换账号或同角色换用户时，先清空旧菜单和旧消息，避免短暂显示上一会话内容。
        messageCenterRows.value = []
        reloadMenusForCurrentRole()
        loadNotificationMessages()
    }
}

const handleLogout = async () => {
    // 退出登录分块：后端退出失败也清理本地状态，保证能回到登录页。
    const refresh = getStoredRefresh()

    try {
        await logoutApi(refresh)
    } finally {
        clearAuthState()
    }

    router.push('/login')
}

const handleUserCommand = (command: string) => {
    if (command === 'logout') {
        handleLogout()
    }
}

const goRoleMessages = () => {
    // 铃铛是角色消息唯一入口，避免侧边栏再放重复菜单。
    router.push('/message/center')
}

useRealtimeRefresh(
    async () => {
        await loadNotificationMessages()
    },
    {
        scope: 'messages',
        intervalMs: 15000,
        events: MESSAGE_FEEDBACK_EVENTS,
        storageKeys: MESSAGE_FEEDBACK_STORAGE_KEYS,
    },
)

useRealtimeRefresh(
    async () => {
        await loadMenus()
    },
    {
        scope: 'menus',
        immediate: false,
        refreshWhenVisible: false,
        refreshOnWindowFocus: false,
    },
)

onMounted(() => {
    window.addEventListener(AUTH_STATE_CHANGED_EVENT, refreshLayoutAuthState)
    loadMenus()
    loadCommunities()
})

onBeforeUnmount(() => {
    window.removeEventListener(AUTH_STATE_CHANGED_EVENT, refreshLayoutAuthState)
})

watch(
    () => router.currentRoute.value.fullPath,
    () => {
        if (menuLoaded.value) {
            // 页面内跳转、浏览器前进后退后，同步一/二/三级菜单和功能下拉选中态。
            syncSelectionByCurrentRoute()
        }
    }
)
</script>

<template>
    <div class="layout-container">
        <aside class="second-sidebar">
            <div class="logo">
                <el-icon><HomeFilled /></el-icon>
                <span>{{ appMenuTitle }}</span>
            </div>

            <div class="sidebar-menu">
                <section v-for="item in firstMenus" :key="item.id" class="sidebar-group">
                    <button
                        type="button"
                        class="first-menu-item"
                        :class="{
                            active: selectedFirstId === menuKey(item),
                            expanded: isFirstExpanded(menuKey(item)),
                        }"
                        @click="handleFirstSelect(item)"
                    >
                        <span class="menu-label">
                            <el-icon><component :is="resolveMenuIcon(item)" /></el-icon>
                            <span>{{ item.title }}</span>
                        </span>
                        <span v-if="childrenOf(item).length" class="menu-arrow">
                            <el-icon>
                                <component :is="isFirstExpanded(menuKey(item)) ? ArrowDown : ArrowRight" />
                            </el-icon>
                        </span>
                    </button>

                    <div
                        v-if="childrenOf(item).length && isFirstExpanded(menuKey(item))"
                        class="second-menu-list"
                    >
                        <button
                            v-for="child in childrenOf(item)"
                            :key="child.id"
                            type="button"
                            class="second-menu-item"
                            :class="{ active: selectedSecondId === menuKey(child) }"
                            @click.stop="handleSecondSelect(item, child)"
                        >
                            <span>{{ child.title }}</span>
                            <el-icon v-if="childrenOf(child).length"><ArrowRight /></el-icon>
                        </button>
                    </div>
                </section>
            </div>

            <el-empty
                v-if="menuLoaded && firstMenus.length === 0"
                class="menu-empty"
                description="暂无可访问菜单"
                :image-size="72"
            />
        </aside>

        <main class="layout-main">
            <header class="layout-header">
                <el-dropdown
                    trigger="click"
                    popper-class="community-select-popper"
                    @command="handleCommunityCommand"
                >
                    <button type="button" class="community-select">
                        <el-icon><OfficeBuilding /></el-icon>
                        <span>{{ selectedCommunityName }}</span>
                        <el-icon class="community-arrow"><ArrowDown /></el-icon>
                    </button>
                    <template #dropdown>
                        <el-dropdown-menu>
                            <el-dropdown-item
                                v-for="item in communityOptions"
                                :key="item.id"
                                :command="item.id"
                            >
                                {{ item.name }}
                            </el-dropdown-item>
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>

                <div class="global-search">
                    <el-icon><Search /></el-icon>
                    <input
                        :placeholder="searchPlaceholder"
                        type="text"
                        readonly
                    >
                </div>

                <div class="header-user">
                    <button
                        type="button"
                        class="notification-button"
                        aria-label="查看角色消息"
                        @click="goRoleMessages"
                    >
                        <el-badge
                            :value="notificationCount"
                            :max="99"
                            :hidden="notificationCount === 0"
                            class="notification-badge"
                        >
                            <el-icon class="notification-icon"><Bell /></el-icon>
                        </el-badge>
                    </button>
                    <span class="role-pill">{{ roleTitle }}</span>
                    <el-dropdown
                        trigger="click"
                        popper-class="user-dropdown-popper"
                        @command="handleUserCommand"
                    >
                        <span class="avatar-chip">
                            <span class="avatar-circle">{{ usernameInitial }}</span>
                            <span>{{ username }}</span>
                            <el-icon><ArrowDown /></el-icon>
                        </span>
                        <template #dropdown>
                            <el-dropdown-menu>
                                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                            </el-dropdown-menu>
                        </template>
                    </el-dropdown>
                </div>
            </header>

            <div v-if="thirdMenus.length" class="third-bar">
                <el-dropdown
                    v-for="item in thirdMenus"
                    :key="item.id"
                    trigger="click"
                    @command="handleFunctionSelect"
                >
                    <template #default>
                        <el-button
                            :type="selectedThirdId === menuKey(item) ? 'primary' : 'default'"
                            @click="handleThirdSelect(item)"
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
    min-width: 1180px;
    height: 100vh;
    color: var(--text-primary);
    background: var(--surface-page);
    font-family: var(--font-family-base);
    font-size: 14px;
    line-height: 1.5;
    letter-spacing: 0;
}

.second-sidebar {
    position: relative;
    width: 230px;
    flex: 0 0 230px;
    display: flex;
    flex-direction: column;
    background: var(--surface-card);
    border-right: 1px solid var(--border-color);
    z-index: 20;
}

.logo {
    height: 66px;
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0 20px;
    color: var(--brand-primary);
    font-size: 20px;
    font-weight: 700;
    line-height: 28px;
    border-bottom: 1px solid var(--border-color);
    white-space: nowrap;
}

.logo .el-icon {
    color: var(--brand-primary);
    font-size: 26px;
}

.sidebar-menu {
    flex: 1;
    min-height: 0;
    padding: 20px 12px 14px;
    overflow-y: auto;
}

.sidebar-group {
    position: relative;
}

.sidebar-group + .sidebar-group {
    margin-top: 6px;
}

.first-menu-item {
    width: 100%;
    border: 0;
    border-radius: 6px;
    background: transparent;
    color: var(--text-primary);
    cursor: pointer;
    text-align: left;
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-height: 44px;
    padding: 0 12px;
    font-size: 14px;
    font-weight: 500;
    line-height: 22px;
}

.menu-label {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    min-width: 0;
}

.menu-label .el-icon {
    color: var(--text-muted);
    font-size: 18px;
}

.menu-arrow {
    display: inline-flex;
    color: #98a2b3;
    font-size: 13px;
}

.first-menu-item:hover {
    color: var(--brand-primary);
    background: var(--brand-primary-subtle);
}

.first-menu-item:hover .el-icon,
.first-menu-item:hover .menu-arrow {
    color: var(--brand-primary);
}

.first-menu-item.expanded:not(.active) {
    color: var(--brand-primary);
    background: var(--brand-primary-subtle);
}

.first-menu-item.active {
    color: #ffffff;
    background: linear-gradient(135deg, var(--brand-primary), var(--brand-primary-hover));
    box-shadow: 0 8px 18px rgba(15, 118, 110, 0.18);
    font-weight: 600;
    line-height: 22px;
}

.first-menu-item.active .el-icon,
.first-menu-item.active .menu-arrow {
    color: #ffffff;
}

.second-menu-list {
    display: flex;
    flex-direction: column;
    gap: 4px;
    margin: 4px 0 6px 16px;
    padding: 6px 0 6px 10px;
    border-left: 2px solid var(--brand-primary-soft);
}

.second-menu-item {
    width: 100%;
    min-height: 36px;
    padding: 0 10px;
    border: 0;
    border-radius: 5px;
    background: var(--brand-primary-subtle);
    color: var(--text-primary);
    cursor: pointer;
    text-align: left;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    font-size: 14px;
    font-weight: 500;
    line-height: 22px;
}

.second-menu-item:hover {
    color: var(--brand-primary);
    background: var(--brand-primary-soft);
    font-weight: 600;
}

.second-menu-item.active {
    color: var(--brand-primary);
    background: var(--brand-primary-soft);
    box-shadow: inset 3px 0 0 var(--brand-primary);
    font-weight: 600;
}

.second-menu-item.active .el-icon {
    color: var(--brand-primary);
}

.menu-empty {
    padding: 24px 8px;
}

.layout-main {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
}

.layout-header {
    height: 66px;
    display: grid;
    grid-template-columns: minmax(170px, 220px) minmax(220px, 1fr) max-content;
    align-items: center;
    column-gap: clamp(14px, 2vw, 28px);
    padding: 0 clamp(18px, 2vw, 28px);
    background: var(--surface-card);
    border-bottom: 1px solid var(--border-color);
}

.community-select {
    display: flex;
    align-items: center;
    gap: 10px;
    width: 180px;
    min-height: 38px;
    justify-self: start;
    padding: 0 12px;
    border: 1px solid #dfe5ef;
    border-radius: 6px;
    color: var(--text-subtle);
    background: var(--surface-card);
    cursor: pointer;
    font-size: 14px;
    font-weight: 400;
    line-height: 22px;
    text-align: left;
    transition: border-color 0.2s ease, color 0.2s ease;
}

.community-select .el-icon:first-child {
    color: var(--text-muted);
}

.community-select:hover,
.community-select:focus-visible {
    border-color: var(--brand-primary);
    color: var(--brand-primary);
    outline: none;
}

.community-select:hover .el-icon,
.community-select:focus-visible .el-icon {
    color: var(--brand-primary);
}

.community-arrow {
    margin-left: auto;
    font-size: 13px;
}

:global(.community-select-popper .el-dropdown-menu__item) {
    color: var(--text-subtle);
    font-size: 14px;
    font-weight: 500;
}

:global(.community-select-popper .el-dropdown-menu__item:hover),
:global(.community-select-popper .el-dropdown-menu__item:focus) {
    color: var(--brand-primary);
    background: var(--brand-primary-soft);
}

.global-search {
    display: flex;
    align-items: center;
    width: 100%;
    max-width: 560px;
    min-width: 0;
    min-height: 38px;
    justify-self: center;
    padding: 0 14px;
    border: 1px solid #dfe5ef;
    border-radius: 6px;
    background: var(--surface-card);
}

.global-search .el-icon {
    margin-right: 8px;
    color: #98a2b3;
}

.global-search input {
    flex: 1;
    min-width: 0;
    border: 0;
    outline: 0;
    color: var(--text-subtle);
    background: transparent;
    cursor: default;
    font-size: 14px;
    font-weight: 400;
    line-height: 22px;
}

.header-user {
    display: flex;
    align-items: center;
    gap: clamp(10px, 1.4vw, 14px);
    justify-self: end;
    min-width: max-content;
    white-space: nowrap;
    position: relative;
    z-index: 1;
}

.notification-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    padding: 0;
    border: 0;
    border-radius: 8px;
    background: transparent;
    cursor: pointer;
    transition: background 0.2s ease;
}

.notification-button:hover,
.notification-button:focus-visible {
    background: var(--brand-primary-subtle);
    outline: none;
}

.notification-button:hover .notification-icon,
.notification-button:focus-visible .notification-icon {
    color: var(--brand-primary);
}

.notification-icon {
    color: var(--text-primary);
    font-size: 22px;
    transition: color 0.2s ease;
}

.role-pill {
    min-width: 78px;
    padding: 9px 18px;
    border-radius: 18px;
    color: var(--brand-primary);
    background: var(--brand-primary-soft);
    text-align: center;
    font-size: 14px;
    font-weight: 600;
    line-height: 22px;
}

.avatar-chip {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: var(--text-subtle);
    cursor: pointer;
    font-size: 14px;
    font-weight: 400;
    line-height: 22px;
    transition: color 0.2s ease;
    user-select: none;
}

.avatar-chip:hover {
    color: var(--brand-primary);
}

.avatar-circle {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 34px;
    height: 34px;
    border-radius: 50%;
    color: #ffffff;
    background: #2563eb;
    font-weight: 700;
}

:global(.user-dropdown-popper .el-dropdown-menu__item) {
    cursor: pointer;
    color: var(--text-subtle);
    font-size: 14px;
    font-weight: 600;
}

:global(.user-dropdown-popper .el-dropdown-menu__item:hover),
:global(.user-dropdown-popper .el-dropdown-menu__item:focus) {
    color: var(--brand-primary);
    background: var(--brand-primary-soft);
}

.third-bar {
    display: flex;
    align-items: center;
    gap: 10px;
    min-height: 48px;
    padding: 12px 28px 8px;
    background: transparent;
    overflow-x: auto;
}

.third-bar :deep(.el-button) {
    border-radius: 6px;
}

.dropdown-icon {
    margin-left: 6px;
}

.selected-function {
    flex: 0 0 auto;
    margin-left: 8px;
    color: var(--text-muted);
    font-size: 14px;
    font-weight: 400;
    line-height: 22px;
}

.layout-content {
    flex: 1;
    min-width: 0;
    padding: 20px 28px 28px;
    overflow-y: auto;
}

.layout-content :deep(.el-card) {
    border: 1px solid var(--border-color);
    border-radius: 8px;
    color: var(--text-primary);
    box-shadow: 0 8px 20px rgba(16, 24, 40, 0.04);
}

.layout-content :deep(.el-card__header) {
    color: var(--text-heading);
    font-size: 15px;
    font-weight: 600;
    line-height: 22px;
    padding: 22px 24px;
}

.layout-content :deep(.el-card__body) {
    padding: 24px;
}

.layout-content :deep(.el-button) {
    min-height: 40px;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 600;
    line-height: 20px;
}

.layout-content :deep(.el-button--primary) {
    border-color: var(--brand-primary);
    background: var(--brand-primary);
}

.layout-content :deep(.el-button--primary:hover),
.layout-content :deep(.el-button--primary:focus) {
    border-color: var(--brand-primary-hover);
    background: var(--brand-primary-hover);
}

.layout-content :deep(.el-button--primary.is-link) {
    color: var(--brand-primary);
    background: transparent;
}

.layout-content :deep(.el-button--warning) {
    border-color: var(--warning-primary);
    background: var(--warning-primary);
}

.layout-content :deep(.el-input__wrapper),
.layout-content :deep(.el-select__wrapper) {
    border-radius: 6px;
    box-shadow: 0 0 0 1px #dfe5ef inset;
}

.layout-content :deep(.el-input),
.layout-content :deep(.el-select),
.layout-content :deep(.el-date-editor.el-input) {
    --el-input-height: 40px;
}

.layout-content :deep(.el-table) {
    overflow: hidden;
    border-radius: 6px;
    color: var(--text-primary);
    font-size: 14px;
    line-height: 22px;
}

.layout-content :deep(.el-table th.el-table__cell) {
    padding: 16px 0;
    color: var(--text-subtle);
    background: var(--surface-muted);
    font-size: 13px;
    font-weight: 600;
    line-height: 20px;
}

.layout-content :deep(.el-table td.el-table__cell) {
    padding: 16px 0;
    color: var(--text-primary);
    font-size: 14px;
    font-weight: 400;
    line-height: 22px;
}

.layout-content :deep(.el-table .cell) {
    display: flex;
    align-items: center;
    min-height: 24px;
}

.layout-content :deep(.card-header),
.layout-content :deep(.notice-header) {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    min-height: 28px;
}

.layout-content :deep(.list-toolbar),
.layout-content :deep(.filter-form) {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
    margin-bottom: 24px;
}

.layout-content :deep(.filter-form) {
    row-gap: 16px;
}

.layout-content :deep(.filter-form .el-date-editor.el-input) {
    width: 190px;
}

.layout-content :deep(.el-form-item) {
    align-items: center;
    margin-right: 0;
    margin-bottom: 22px;
}

.layout-content :deep(.el-form-item:last-child) {
    margin-bottom: 0;
}

.layout-content :deep(.filter-form .el-form-item),
.layout-content :deep(.list-toolbar .el-form-item),
.layout-content :deep(.el-form--inline .el-form-item) {
    margin-bottom: 0;
}

.layout-content :deep(.el-form-item__label) {
    display: inline-flex;
    align-items: center;
    justify-content: flex-end;
    min-height: 40px;
    color: var(--text-subtle);
    font-size: 14px;
    font-weight: 500;
    line-height: 22px;
}

.layout-content :deep(.el-form-item__content) {
    display: flex;
    align-items: center;
    min-height: 40px;
    line-height: 22px;
}

.layout-content :deep(.el-form-item:has(.el-textarea) .el-form-item__label) {
    align-items: flex-start;
    padding-top: 9px;
}

.layout-content :deep(.el-form-item:has(.el-textarea) .el-form-item__content) {
    align-items: flex-start;
}

.layout-content :deep(.el-radio-group) {
    display: inline-flex;
    align-items: center;
    min-height: 40px;
}

.layout-content :deep(.el-radio-button__inner) {
    display: inline-flex;
    align-items: center;
    min-height: 40px;
    padding: 0 18px;
    font-size: 14px;
    font-weight: 600;
}

.layout-content :deep(.el-upload) {
    display: inline-flex;
    align-items: center;
}

.layout-content :deep(.el-tag) {
    border-radius: 5px;
    font-size: 12px;
    font-weight: 500;
    line-height: 18px;
}
</style>
