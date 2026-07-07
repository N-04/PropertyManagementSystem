<!-- 文件说明：费用统计图表，在首页按角色展示已缴费和未缴费金额。 -->
<script setup lang="ts">
import * as echarts from 'echarts'
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'

type DashboardData = {
    fee_total: number
    fee_paid: number
    fee_unpaid: number
}

const props = defineProps<{
    dashboardData: DashboardData
}>()

const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

const PAID_COLOR = '#4f6fea'
const UNPAID_COLOR = '#00a896'
const EMPTY_COLOR = '#eef4f7'

const moneyText = (value: number) => `¥ ${Number(value || 0).toFixed(2)}`

const percentText = (value: number, total: number) => {
    if (!total) {
        return '0%'
    }

    return `${((value / total) * 100).toFixed(1)}%`
}

const safePercent = (value: number, total: number) => {
    if (!total) {
        return 0
    }

    return Number(((value / total) * 100).toFixed(1))
}

// 图表数据分块：所有比例都基于后端实时金额计算，避免 UI 原型数据写死。
const paidAmount = computed(() => Number(props.dashboardData.fee_paid || 0))
const unpaidAmount = computed(() => Number(props.dashboardData.fee_unpaid || 0))
const totalAmount = computed(() => Number(props.dashboardData.fee_total || 0) || paidAmount.value + unpaidAmount.value)
const paidRate = computed(() => percentText(paidAmount.value, totalAmount.value))
const legendRows = computed(() => [
    {
        name: '已缴费金额',
        value: paidAmount.value,
        color: PAID_COLOR,
        percent: safePercent(paidAmount.value, totalAmount.value),
        percentLabel: percentText(paidAmount.value, totalAmount.value),
    },
    {
        name: '未缴费金额',
        value: unpaidAmount.value,
        color: UNPAID_COLOR,
        percent: safePercent(unpaidAmount.value, totalAmount.value),
        percentLabel: percentText(unpaidAmount.value, totalAmount.value),
    },
])

type PieTooltipParams = {
    name?: string
    value?: number | string
    percent?: number
}

const renderChart = () => {
    if (!chartRef.value) {
        return
    }

    if (!chart) {
        chart = echarts.init(chartRef.value)
    }

    const total = totalAmount.value
    const hasData = total > 0

    // 渲染配置分块：环形图只负责视觉占比，完整金额和百分比交给右侧图例承载。
    chart.setOption({
        tooltip: {
            show: hasData,
            trigger: 'item',
            borderWidth: 0,
            padding: [8, 12],
            formatter: (params: unknown) => {
                const item = params as PieTooltipParams
                const value = Number(item.value || 0)
                const percent = typeof item.percent === 'number' ? item.percent.toFixed(1) : percentText(value, total)

                return `${item.name || ''}: ${moneyText(value)} (${percent}%)`
            },
        },
        color: [PAID_COLOR, UNPAID_COLOR],
        series: [
            {
                type: 'pie',
                radius: ['58%', '82%'],
                center: ['50%', '50%'],
                minAngle: 3,
                avoidLabelOverlap: true,
                itemStyle: {
                    borderColor: '#fff',
                    borderRadius: 8,
                    borderWidth: 4,
                },
                label: {
                    show: false,
                },
                labelLine: {
                    show: false,
                },
                data: hasData ? [
                    {
                        value: paidAmount.value,
                        name: '已缴费金额',
                    },
                    {
                        value: unpaidAmount.value,
                        name: '未缴费金额',
                    },
                ] : [
                    {
                        value: 1,
                        name: '暂无数据',
                        itemStyle: {
                            color: EMPTY_COLOR,
                        },
                    },
                ],
            },
        ],
    })
}

const resizeChart = () => {
    chart?.resize()
}

onMounted(() => {
    nextTick(renderChart)
    window.addEventListener('resize', resizeChart)
})

watch(() => props.dashboardData, () => nextTick(renderChart), { deep: true })

onBeforeUnmount(() => {
    window.removeEventListener('resize', resizeChart)
    chart?.dispose()
    chart = null
})
</script>

<template>
    <div class="chart-container">
        <div class="chart-visual" aria-label="费用统计环形图">
            <div ref="chartRef" class="echart-ring" />
            <div class="donut-center">
                <small>到账率</small>
                <strong>{{ paidRate }}</strong>
            </div>
        </div>

        <div class="chart-legend">
            <div v-for="row in legendRows" :key="row.name" class="legend-row" :class="{ 'muted-row': row.value <= 0 }">
                <div class="legend-top">
                    <p>
                        <i :style="`--dot-color: ${row.color}`" />
                        {{ row.name }}
                    </p>
                    <b>{{ moneyText(row.value) }}</b>
                </div>
                <div class="meter">
                    <span :style="`--meter-width: ${row.percent}%; --meter-color: ${row.color}`" />
                </div>
                <em>{{ row.percentLabel }}</em>
            </div>
        </div>

        <div class="chart-summary">
            <strong>总额 {{ moneyText(totalAmount) }}</strong>
            <span>金额与占比独立展示，避免饼图外侧文字截断。</span>
        </div>
    </div>
</template>

<style scoped>
/* 图表布局分块：参考原型的左环形图、右图例、底部摘要三段结构。 */
.chart-container {
    display: grid;
    min-height: 390px;
    overflow: hidden;
    align-content: stretch;
    grid-template-columns: minmax(160px, 0.82fr) minmax(0, 1fr);
    gap: 24px 22px;
}

.chart-visual {
    position: relative;
    display: grid;
    min-width: 0;
    place-items: center;
}

.echart-ring {
    width: min(100%, 248px);
    height: 248px;
}

.donut-center {
    position: absolute;
    top: 50%;
    left: 50%;
    display: grid;
    width: 112px;
    height: 112px;
    border: 1px solid var(--border-soft);
    border-radius: 50%;
    background: #fff;
    box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.8);
    place-items: center;
    align-content: center;
    transform: translate(-50%, -50%);
}

.donut-center small {
    color: var(--text-muted);
    font-size: 13px;
    font-weight: 700;
}

.donut-center strong {
    margin-top: 8px;
    color: #4f6fea;
    font-size: 26px;
    font-weight: 800;
    line-height: 1;
}

/* 图例分块：用进度条展示百分比，替代 ECharts 外侧折线标签。 */
.chart-legend {
    display: grid;
    min-width: 0;
    align-content: center;
    gap: 18px;
}

.legend-row {
    display: grid;
    min-width: 0;
    gap: 8px;
}

.legend-row.muted-row {
    opacity: 0.72;
}

.legend-top {
    display: flex;
    min-width: 0;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
}

.legend-top p {
    display: flex;
    flex: 1 1 auto;
    min-width: 0;
    overflow: hidden;
    align-items: center;
    gap: 10px;
    margin: 0;
    color: var(--text-primary);
    font-size: 15px;
    font-weight: 700;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.legend-top i {
    width: 11px;
    height: 11px;
    flex: 0 0 auto;
    border-radius: 50%;
    background: var(--dot-color);
}

.legend-top b {
    flex: 0 1 auto;
    max-width: min(132px, 48%);
    overflow: hidden;
    color: var(--text-heading);
    font-size: 14px;
    font-weight: 700;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.meter {
    min-width: 0;
    height: 10px;
    overflow: hidden;
    border-radius: 999px;
    background: #eef4f7;
}

.meter span {
    display: block;
    width: max(6px, var(--meter-width));
    height: 100%;
    border-radius: inherit;
    background: var(--meter-color);
}

.legend-row.muted-row .meter span {
    width: 6px;
}

.legend-row em {
    color: var(--text-muted);
    font-size: 13px;
    font-style: normal;
    font-weight: 700;
}

/* 摘要分块：对齐原型卡片底部说明，承接总额和图表含义。 */
.chart-summary {
    grid-column: 1 / -1;
    align-self: end;
    min-width: 0;
    padding: 16px 18px;
    border: 1px solid var(--border-soft);
    border-radius: 8px;
    background: var(--surface-muted);
}

.chart-summary strong,
.chart-summary span {
    display: block;
}

.chart-summary strong {
    color: var(--text-subtle);
    font-size: 15px;
    font-weight: 700;
}

.chart-summary span {
    margin-top: 6px;
    color: var(--text-muted);
    font-size: 13px;
    font-weight: 600;
}

@media (max-width: 1280px) {
    .chart-container {
        grid-template-columns: 1fr;
    }

    .chart-legend {
        align-content: start;
    }
}
</style>
