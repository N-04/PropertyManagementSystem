<!-- 文件说明：封装可复用前端组件。 -->
<script setup lang="ts">
// 引入 ECharts
import * as echarts from 'echarts'

// Vue生命周期
import { onMounted, ref } from 'vue'

// Dashboard接口
import { getDashboard } from '@/api/dashboard'

// 图表DOM对象
const chartRef = ref()

// 页面加载完成执行
onMounted(async () => {
    // 获取Dashboard统计数据
    const res = await getDashboard()

    // 后端返回数据
    const data = res.data.data

    // 初始化图表
    const chart = echarts.init(chartRef.value)

    // 设置图表配置
    chart.setOption({
        // 标题
        title: {
            text: '房屋统计',
            left: 'center',
        },

        // 鼠标提示
        tooltip: {
            trigger: 'item',
        },

        // 图例
        legend: {
            bottom: '0%',
        },

        // 柱状图数据
        series: [
            {
                // 图表类型
                type: 'bar',
                // 数据来源
                data: [data.house_count, data.owner_count, data.parking_count, data.repair_count],
            },
        ],
        xAxis: {
            type: 'category',

            data: ['房屋', '业主', '车位', '报修'],
        },
        yAxis: {
            type: 'value',
        },
    })
})
</script>

<template>
    <!-- 图表容器 -->
    <div ref="chartRef" style="height: 400px" />
</template>
