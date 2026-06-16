<!-- 文件说明：报修统计图表，在首页按角色展示工单状态数量。 -->
<script setup lang="ts">
import * as echarts from 'echarts'
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'

type DashboardData = {
    repair_pending: number
    repair_processing: number
    repair_finished: number
}

const props = defineProps<{
    dashboardData: DashboardData
}>()

const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

const renderChart = () => {
    if (!chartRef.value) {
        return
    }

    if (!chart) {
        chart = echarts.init(chartRef.value)
    }

    chart.setOption({
        title: {
            text: '报修统计',
            left: 'center',
        },
        tooltip: {
            trigger: 'item',
            formatter: '{b}: {c} 单 ({d}%)',
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
                    formatter: '{b}\n{c} 单',
                },
                data: [
                    {
                        value: Number(props.dashboardData.repair_pending || 0),
                        name: '待派单',
                    },
                    {
                        value: Number(props.dashboardData.repair_processing || 0),
                        name: '进行中',
                    },
                    {
                        value: Number(props.dashboardData.repair_finished || 0),
                        name: '已完成',
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
