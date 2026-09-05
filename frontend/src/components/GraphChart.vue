<template>
  <div ref="chartContainer" style="width: 100%; height: 100%;"></div>
</template>

<script setup>
import {ref, onMounted, watch} from 'vue'
import * as echarts from 'echarts'

const props = defineProps(['data'])
const chartContainer = ref(null)
let chart = null

onMounted(() => {
  chart = echarts.init(chartContainer.value)

  watch(() => props.data, (newData) => {
    if (!newData || !newData.nodes || !newData.links) {
      console.warn('图谱数据无效', newData)
      return
    }

    // 节点去重（按 id）
    const uniqueNodes = []
    const seenIds = new Set()
    newData.nodes.forEach(node => {
      if (!node.id) return
      if (seenIds.has(node.id)) return
      seenIds.add(node.id)
      uniqueNodes.push(node)
    })

    // 过滤有效 links
    const validLinks = newData.links.filter(link =>
        seenIds.has(link.source) && seenIds.has(link.target)
    )

    // 建立节点索引映射
    const nodeIndexMap = {}
    uniqueNodes.forEach((node, idx) => {
      nodeIndexMap[node.id] = idx
    })

    const links = validLinks
        .filter(link => nodeIndexMap[link.source] !== undefined && nodeIndexMap[link.target] !== undefined)
        .map(link => ({
          source: nodeIndexMap[link.source],
          target: nodeIndexMap[link.target],
          label: link.label,
          lineStyle: {color: '#c0b298', width: 1.5, curveness: 0.1}
        }))

    // 节点大小根据类别动态调整（防止大节点遮挡）
    const getSymbolSize = (category) => {
      switch (category) {
        case 'Constitution':
          return 50
        case 'TherapyProcess':
          return 40
        case 'HealthKnowledge':
          return 35
        case 'Acupoint':
          return 25
        case 'Food':
          return 22
        case 'Exercise':
          return 22
        default:
          return 20
      }
    }

    const option = {
      tooltip: {
        trigger: 'item', formatter: (params) => { /* 保持原有 tooltip 逻辑 */
        }
      },
      series: [{
        type: 'graph',
        layout: 'force',
        force: {
          initIterations: 300,      // 初始迭代次数，越多布局越稳定
          repulsion: 500,           // 节点斥力，值越大节点间距越大
          edgeLength: 80,           // 边长，值越小连线越短
          gravity: 0.1,             // 重力，使节点向中心靠拢
          friction: 0.1,            // 摩擦力
          layoutAnimation: true     // 布局动画
        },
        roam: true,                 // 允许缩放/平移
        draggable: true,            // 允许拖拽节点
        data: uniqueNodes.map(n => ({
          ...n,
          symbolSize: getSymbolSize(n.category),
          label: {show: true, position: 'right', fontSize: 10, offset: [5, 0]},
          itemStyle: {
            color: n.category === 'Constitution' ? '#8b3a3a' :
                n.category === 'Acupoint' ? '#b8860b' :
                    n.category === 'Food' ? '#556b2f' :
                        n.category === 'Exercise' ? '#4682b4' :
                            n.category === 'TherapyProcess' ? '#2e8b57' :
                                n.category === 'HealthKnowledge' ? '#4682b4' : '#c0b298'
          }
        })),
        links: links,
        lineStyle: {color: '#c0b298', width: 1.5, curveness: 0.1, opacity: 0.6},
        edgeSymbol: ['none', 'arrow'],
        edgeSymbolSize: [0, 8],
        label: {show: true, position: 'right', fontSize: 10, offset: [5, 0]},
        emphasis: {scale: true}
      }]
    }

    chart.setOption(option, true)
  }, {immediate: true})
})
</script>