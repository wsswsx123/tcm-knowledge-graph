// ECharts 按需引入：项目只用到 雷达图(radar) + 关系图(graph)，
// 通过 echarts/core 注册所需组件，避免整包打入（体积约减小 60%+）。
import * as echarts from 'echarts/core'
import { RadarChart, GraphChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

echarts.use([
  RadarChart,
  GraphChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  CanvasRenderer,
])

export default echarts
