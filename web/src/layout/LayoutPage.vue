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
    UserFilled,
    Van,
} from '@element-plus/icons-vue'
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
const selectedFirstId = ref('')
const selectedSecondId = ref('')
const selectedThirdId = ref('')
const selectedFunctionTitle = ref('')
const expandedFirstIds = ref<string[]>([])
const noticeMessages = ref<string[]>([])
const roleMessages = ref<string[]>([])
const parkingFeedbackMessages = ref<string[]>([])
const repairEvaluationFeedbackMessages = ref<string[]>([])
const serviceRatingFeedbackMessages = ref<string[]>([])
const PARKING_FEEDBACK_EVENT = 'property-management-parking-feedback'
const PARKING_FEEDBACK_STORAGE_KEY = 'parkingPurchaseFeedback'
const REPAIR_EVALUATION_FEEDBACK_EVENT = 'property-management-repair-evaluation-feedback'
const REPAIR_EVALUATION_FEEDBACK_STORAGE_KEY = 'repairEvaluationFeedback'
const SERVICE_RATING_FEEDBACK_EVENT = 'property-management-service-rating-feedback'
const SERVICE_RATING_FEEDBACK_STORAGE_KEY = 'serviceRatingFeedback'

const roleTitleMap: Record<string, string> = {
    admin: '物业管理员',
    super_admin: '超级管理员',
    property_admin: '物业管理员',
    finance_staff: '财务人员',
    finance: '财务人员',
    customer_service: '客服人员',
    service: '客服人员',
    repair_staff: '维修员',
    repairer: '维修员',
    repair: '维修员',
    owner: '业主',
}

const roleTitle = computed(() => roleTitleMap[role.value] || '用户')
const usernameInitial = computed(() => (username.value || '用').slice(0, 1).toUpperCase())
const notificationCount = computed(() => notificationMessages.value.length)

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
    routeFullPath = routePath,
    parents: AppMenuItem[] = []
): AppMenuItem[] => {
    const allowBaseMatch = !routeFullPath.includes('?')

    for (const menu of menus) {
        const currentPath = [...parents, menu]
        const menuPath = menu.path || ''
        const menuRoutePath = menuPath.split('?')[0]

        if (menuPath === routeFullPath || (allowBaseMatch && menuRoutePath === routePath)) {
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

const canReceiveNotice = computed(() => {
    // 公告接收方只包含管理员和业主；财务/维修只进入公告发布列表。
    return ['owner', 'property_admin', 'admin', 'super_admin'].includes(role.value)
})

const notificationMessages = computed(() => {
    const messages = [
        ...parkingFeedbackMessages.value,
        ...repairEvaluationFeedbackMessages.value,
        ...serviceRatingFeedbackMessages.value,
        ...noticeMessages.value,
        ...roleMessages.value,
    ].filter(Boolean)

    if (messages.length) {
        return messages.slice(0, 8)
    }

    return ['系统运行正常，欢迎使用社区物业管理系统']
})

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

const expandFirstMenu = (id: string) => {
    if (!expandedFirstIds.value.includes(id)) {
        expandedFirstIds.value.push(id)
    }
}

const toggleFirstMenu = (id: string) => {
    if (expandedFirstIds.value.includes(id)) {
        expandedFirstIds.value = expandedFirstIds.value.filter((item) => item !== id)
        return
    }

    expandedFirstIds.value.push(id)
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
        // 通知角标只是提醒入口，接口失败不影响页面主体。
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
        // 通知角标只是提醒入口，接口失败不影响页面主体。
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
        // 通知角标只是提醒入口，接口失败不影响页面主体。
    }

    roleMessages.value = messages
}

const loadNotificationMessages = () => {
    loadNoticeMessages()
    loadRoleMessages()
}

const readParkingFeedbackMessages = () => {
    try {
        const raw = localStorage.getItem(PARKING_FEEDBACK_STORAGE_KEY)
        const item = raw ? JSON.parse(raw) : null

        if (!item?.message) {
            parkingFeedbackMessages.value = []
            return
        }

        parkingFeedbackMessages.value = [`车位反馈：${item.message}`]
    } catch {
        parkingFeedbackMessages.value = []
    }
}

const readRepairEvaluationFeedbackMessages = () => {
    try {
        const raw = localStorage.getItem(REPAIR_EVALUATION_FEEDBACK_STORAGE_KEY)
        const item = raw ? JSON.parse(raw) : null

        if (!item?.message) {
            repairEvaluationFeedbackMessages.value = []
            return
        }

        repairEvaluationFeedbackMessages.value = [`评价反馈：${item.message}`]
    } catch {
        repairEvaluationFeedbackMessages.value = []
    }
}

const readServiceRatingFeedbackMessages = () => {
    try {
        const raw = localStorage.getItem(SERVICE_RATING_FEEDBACK_STORAGE_KEY)
        const item = raw ? JSON.parse(raw) : null

        if (!item?.message) {
            serviceRatingFeedbackMessages.value = []
            return
        }

        serviceRatingFeedbackMessages.value = [`服务反馈：${item.message}`]
    } catch {
        serviceRatingFeedbackMessages.value = []
    }
}

const handleParkingFeedback = () => {
    readParkingFeedbackMessages()
}

const handleRepairEvaluationFeedback = () => {
    readRepairEvaluationFeedbackMessages()
}

const handleServiceRatingFeedback = () => {
    readServiceRatingFeedbackMessages()
}

const handleStorageFeedback = (event: StorageEvent) => {
    if (event.key === PARKING_FEEDBACK_STORAGE_KEY) {
        readParkingFeedbackMessages()
    }

    if (event.key === REPAIR_EVALUATION_FEEDBACK_STORAGE_KEY) {
        readRepairEvaluationFeedbackMessages()
    }

    if (event.key === SERVICE_RATING_FEEDBACK_STORAGE_KEY) {
        readServiceRatingFeedbackMessages()
    }
}

const reloadMenusForCurrentRole = () => {
    selectedFirstId.value = ''
    selectedSecondId.value = ''
    selectedThirdId.value = ''
    selectedFunctionTitle.value = ''
    expandedFirstIds.value = []
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
        loadNotificationMessages()
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
    window.addEventListener(PARKING_FEEDBACK_EVENT, handleParkingFeedback)
    window.addEventListener(REPAIR_EVALUATION_FEEDBACK_EVENT, handleRepairEvaluationFeedback)
    window.addEventListener(SERVICE_RATING_FEEDBACK_EVENT, handleServiceRatingFeedback)
    window.addEventListener('storage', handleStorageFeedback)
    loadMenus()
    readParkingFeedbackMessages()
    readRepairEvaluationFeedbackMessages()
    readServiceRatingFeedbackMessages()
    loadNotificationMessages()
})

onBeforeUnmount(() => {
    window.removeEventListener(AUTH_STATE_CHANGED_EVENT, refreshLayoutAuthState)
    window.removeEventListener(PARKING_FEEDBACK_EVENT, handleParkingFeedback)
    window.removeEventListener(REPAIR_EVALUATION_FEEDBACK_EVENT, handleRepairEvaluationFeedback)
    window.removeEventListener(SERVICE_RATING_FEEDBACK_EVENT, handleServiceRatingFeedback)
    window.removeEventListener('storage', handleStorageFeedback)
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

            <div class="role-switcher">
                <el-icon><UserFilled /></el-icon>
                <span>{{ roleTitle }}</span>
                <el-icon class="role-arrow"><ArrowDown /></el-icon>
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
                <div class="community-select">
                    <el-icon><OfficeBuilding /></el-icon>
                    <span>幸福里小区</span>
                    <el-icon class="community-arrow"><ArrowDown /></el-icon>
                </div>

                <div class="global-search">
                    <el-icon><Search /></el-icon>
                    <input
                        :placeholder="searchPlaceholder"
                        type="text"
                        readonly
                    >
                </div>

                <div class="header-user">
                    <el-badge :value="notificationCount" :max="99" class="notification-badge">
                        <el-icon class="notification-icon"><Bell /></el-icon>
                    </el-badge>
                    <span class="role-pill">{{ roleTitle }}</span>
                    <span class="avatar-chip">
                        <span class="avatar-circle">{{ usernameInitial }}</span>
                        <span>{{ username }}</span>
                        <el-icon><ArrowDown /></el-icon>
                    </span>
                    <el-button link type="primary" @click="handleLogout">退出登录</el-button>
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
    color: #172033;
    background: #f5f7fa;
}

.second-sidebar {
    position: relative;
    width: 230px;
    flex: 0 0 230px;
    background: #ffffff;
    border-right: 1px solid #e4e7ed;
    z-index: 20;
}

.logo {
    height: 66px;
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0 20px;
    font-size: 18px;
    font-weight: 700;
    color: #111827;
    border-bottom: 1px solid #e4e7ed;
    white-space: nowrap;
}

.logo .el-icon {
    color: #00897b;
    font-size: 26px;
}

.role-switcher {
    display: flex;
    align-items: center;
    gap: 10px;
    min-height: 46px;
    margin: 20px 12px 12px;
    padding: 0 14px;
    border-radius: 6px;
    color: #00897b;
    background: #e4f5f2;
    font-size: 16px;
    font-weight: 700;
}

.role-switcher .role-arrow {
    margin-left: auto;
    font-size: 14px;
}

.sidebar-menu {
    height: calc(100vh - 144px);
    padding: 0 12px 14px;
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
    color: #344054;
    cursor: pointer;
    text-align: left;
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-height: 44px;
    padding: 0 12px;
    font-size: 15px;
    font-weight: 600;
}

.menu-label {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    min-width: 0;
}

.menu-label .el-icon {
    color: #667085;
    font-size: 18px;
}

.menu-arrow {
    display: inline-flex;
    color: #98a2b3;
    font-size: 13px;
}

.first-menu-item:hover {
    color: #00897b;
    background: #edf8f6;
}

.first-menu-item:hover .el-icon,
.first-menu-item:hover .menu-arrow {
    color: #00897b;
}

.first-menu-item.expanded:not(.active) {
    color: #006d63;
    background: #f3fbfa;
}

.first-menu-item.active {
    color: #ffffff;
    background: linear-gradient(135deg, #009688, #00796b);
    box-shadow: 0 8px 18px rgba(0, 137, 123, 0.22);
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
    padding: 4px 0 4px 10px;
    border-left: 2px solid #e4f5f2;
}

.second-menu-item {
    width: 100%;
    min-height: 36px;
    padding: 0 10px;
    border: 0;
    border-radius: 5px;
    background: transparent;
    color: #475467;
    cursor: pointer;
    text-align: left;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    font-size: 14px;
}

.second-menu-item:hover,
.second-menu-item.active {
    color: #00897b;
    background: #e4f5f2;
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
    grid-template-columns: 180px minmax(320px, 1fr) auto;
    align-items: center;
    gap: 24px;
    padding: 0 28px;
    background: #ffffff;
    border-bottom: 1px solid #e4e7ed;
}

.community-select {
    display: flex;
    align-items: center;
    gap: 10px;
    min-height: 38px;
    padding: 0 12px;
    border: 1px solid #dfe5ef;
    border-radius: 6px;
    color: #344054;
    background: #ffffff;
    font-size: 14px;
}

.community-select .el-icon:first-child {
    color: #667085;
}

.community-arrow {
    margin-left: auto;
    font-size: 13px;
}

.global-search {
    display: flex;
    align-items: center;
    width: min(430px, 100%);
    min-height: 38px;
    justify-self: center;
    padding: 0 14px;
    border: 1px solid #dfe5ef;
    border-radius: 6px;
    background: #ffffff;
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
    color: #667085;
    background: transparent;
    cursor: default;
}

.header-user {
    display: flex;
    align-items: center;
    gap: 14px;
    white-space: nowrap;
}

.notification-icon {
    color: #344054;
    font-size: 22px;
}

.role-pill {
    min-width: 78px;
    padding: 9px 18px;
    border-radius: 18px;
    color: #00897b;
    background: #d8f3ef;
    text-align: center;
    font-weight: 700;
}

.avatar-chip {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: #172033;
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
    color: #667085;
    font-size: 14px;
}

.layout-content {
    flex: 1;
    min-width: 0;
    padding: 20px 28px 28px;
    overflow-y: auto;
}
</style>
