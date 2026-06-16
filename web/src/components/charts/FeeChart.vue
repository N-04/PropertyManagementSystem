<!-- 文件说明：费用统计图表，在首页按角色展示已缴费和未缴费金额。 -->
<script setup lang="ts">
import * as echarts from 'echarts'
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'

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

const moneyText = (value: number) => `¥ ${Number(value || 0).toFixed(2)}`

const renderChart = () => {
    if (!chartRef.value) {
        return
    }

    if (!chart) {
        chart = echarts.init(chartRef.value)
    }

    const paid = Number(props.dashboardData.fee_paid || 0)
    const unpaid = Number(props.dashboardData.fee_unpaid || 0)

    chart.setOption({
        title: {
            text: '费用统计',
            subtext: `总额 ${moneyText(props.dashboardData.fee_total)}`,
            left: 'center',
        },
        tooltip: {
            trigger: 'item',
            formatter: (params: any) => `${params.name}: ${moneyText(params.value)} (${params.percent}%)`,
        },
        legend: {
            bottom: '0%',
        },
        series: [
            {
                type: 'pie',
                radius: '58%',
                label: {
                    show: true,
                    formatter: (params: any) => `${params.name}\n${moneyText(params.value)}`,
                },
                data: [
                    {
                        value: paid,
                        name: '已缴费金额',
                    },
                    {
                        value: unpaid,
                        name: '未缴费金额',
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

watch(() => props.dashboardData, renderChart, { deep: true })

onBeforeUnmount(() => {
    window.removeEventListener('resize', resizeChart)
    chart?.dispose()
    chart = null
})
</script>

<template>
    <div ref="chartRef" class="chart-container" />
</template>

<style scoped>
.chart-container {
    height: 400px;
}
</style>
