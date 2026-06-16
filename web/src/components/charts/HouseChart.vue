<!-- 文件说明：基础资源统计图表，在管理员首页展示房屋、业主、车位和报修总量。 -->
<script setup lang="ts">
import * as echarts from 'echarts'
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'

type DashboardData = {
    house_count: number
    owner_count: number
    parking_count: number
    repair_count: number
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
            text: '基础资源统计',
            left: 'center',
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow',
            },
        },
        grid: {
            top: 72,
            left: 42,
            right: 24,
            bottom: 42,
        },
        xAxis: {
            type: 'category',
            data: ['房屋', '业主', '车位', '报修'],
        },
        yAxis: {
            type: 'value',
            minInterval: 1,
        },
        series: [
            {
                type: 'bar',
                barMaxWidth: 46,
                label: {
                    show: true,
                    position: 'top',
                    formatter: '{c}',
                },
                data: [
                    Number(props.dashboardData.house_count || 0),
                    Number(props.dashboardData.owner_count || 0),
                    Number(props.dashboardData.parking_count || 0),
                    Number(props.dashboardData.repair_count || 0),
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
