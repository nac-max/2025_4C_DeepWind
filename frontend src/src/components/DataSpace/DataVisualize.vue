<script setup>
import {defineProps, ref, onMounted, computed} from 'vue'
import * as echarts from 'echarts';
import {ElLoading} from "element-plus";
import RelationChart from "@/components/visualize/RelationChart.vue";

const props = defineProps({
      dataInfo: {
        type: Object,
        required: true
      },
      isDark: {
        type: Boolean,
        required: true
      }
    }
)
const isloading = ref(true)
const dataContent = ref({})
const targetData = ref({})

const startTime = ref('')
const endTime = ref('')
const startRange = ref('')
const endRange = ref('')
const timeRange = ref([])

const requireRefresh = ref(false)
const currentChart = ref(null)
const chartContainer = ref(null)
const chartOption = ref({})

const tableColumns = ref([])
const tableData = ref([])
const tableWidth = ref(window.innerWidth * 0.84)
const tableHeight = ref(640)

// 计算属性用于主题色
const themeColor = computed(() => props.isDark ? '#1f2937' : '#f5f9ff')
const textColor = computed(() => props.isDark ? '#e2e8f0' : '#334155')
const borderColor = computed(() => props.isDark ? '#374151' : '#e2e8f0')
const primaryColor = computed(() => props.isDark ? '#3b82f6' : '#3b82f6')

const resizeTable = () => {
  let widowWidth = window.innerWidth
  tableWidth.value = widowWidth * 0.84
}

const disabledDate = (time) => {
  return time.getTime() < new Date(startTime.value).getTime() || time.getTime() > new Date(endTime.value).getTime()
}

const handleTimeRangeChange = (value) => {
  if (value === null) {
    return
  }
  startRange.value = value[0]
  endRange.value = value[1]
  refreshChart()
}

const getDataContent = () => {
  const loading = ElLoading.service({
    lock: true,
    text: '准备数据中...',
    background: 'rgba(0, 0, 0, 0.7)'
  })
  fetch(`/api/get_dataContent/?data_id=${props.dataInfo.data_id}`)
      .then(response => response.json())
      .then(data => {
        dataContent.value = JSON.parse(data);

        for (let key in dataContent.value) {
          dataContent.value[key] = Object.values(dataContent.value[key])
          if(key === 'TurbID' || key === 'DATATIME'){
            continue
          }
          dataContent.value[key].map((item, index) => {
            return dataContent.value[key][index] = parseFloat(item.toFixed(2))
          })
        }

        startTime.value = dataContent.value.DATATIME[0]
        endTime.value = dataContent.value.DATATIME[dataContent.value.DATATIME.length - 1]

        startRange.value = new Date(dataContent.value.DATATIME[0])
        endRange.value = new Date(new Date(startTime.value).getTime() + 86400000 * 7)

        timeRange.value = [startRange.value, endRange.value]

        initialChart()

        refreshChart()
      }).then(() => {
    loading.close();
  })
}
var chart
const chartResizeHandler = () => {
  if(chart){
    chart.resize();
    chart.setOption(chartOption.value)
  }
}
const tableResizeHandler = () => {
  resizeTable()
}
const initialChart = () => {
  if (props.isDark){
    chart = echarts.init(chartContainer.value, 'dark');
  }
  else{
    chart = echarts.init(chartContainer.value);
  }

  window.addEventListener('resize', chartResizeHandler);
  window.addEventListener('resize', tableResizeHandler);
}

const convertToTableData = (data) => {
  let tableData = []

  for(let i = 0; i < data.DATATIME.length; i++){
    let dataObject = {}
    for (let key in data) {
      dataObject[key] = data[key][i]
    }
    dataObject["id"] = i
    dataObject["parentId"] = null
    tableData.push(dataObject)
  }
  return tableData
}

const refreshChart = () =>{
  tableColumns.value = []

  for(let key in dataContent.value){
    targetData.value[key] = []
    if (key === 'DATATIME'){
      tableColumns.value.push({
        title: key,
        dataKey: key,
        key: key,
        width: 160,
      })
    }
    else{
      tableColumns.value.push({
        title: key,
        dataKey: key,
        key: key,
        width: 150,
      })
    }
  }

  let index = 0
  for (let i = 0; i < dataContent.value.DATATIME.length; i++) {
    if (new Date(dataContent.value.DATATIME[i]) >= startRange.value) {
      index = i
      break
    }
  }
  for (let i = index; i < dataContent.value.DATATIME.length; i++) {
    for(let key in dataContent.value){
      targetData.value[key].push(dataContent.value[key][i])
    }
    if (new Date(dataContent.value.DATATIME[i]) > endRange.value) {
      break
    }
  }
  chartOption.value = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      textStyle: {
        align: 'left'
      },
      axisPointer: {
        type: 'line',
        lineStyle: {
          color: primaryColor.value,
          width: 1,
          type: 'dashed'
        }
      },
      backgroundColor: props.isDark ? 'rgba(30, 30, 30, 0.9)' : 'rgba(255, 255, 255, 0.9)',
      borderColor: borderColor.value,
      borderWidth: 1,
      extraCssText: 'box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); backdrop-filter: blur(8px)'
    },
    toolbox: {
      show: true,
      right: 20,
      feature: {
        restore: {
          title: '重置'
        },
        saveAsImage: {
          title: '保存为图片'
        }
      },
      iconStyle: {
        borderColor: primaryColor.value
      }
    },
    dataZoom: [
      {
        type: 'inside',
        start: 0,
        end: 100,
        fillerColor: props.isDark ? 'rgba(59, 130, 246, 0.2)' : 'rgba(59, 130, 246, 0.1)'
      },
      {
        start: 0,
        end: 100,
        handleSize: '90%',
        handleStyle: {
          color: primaryColor.value,
          borderColor: primaryColor.value
        },
        borderColor: borderColor.value,
        fillerColor: props.isDark ? 'rgba(59, 130, 246, 0.2)' : 'rgba(59, 130, 246, 0.1)'
      }
    ],
    grid: {
      left: '3%',
      right: '5%',
      bottom: '15%',
      top: '15%',
      containLabel: true
    },
    legend: {
      type: 'scroll',
      orient: 'horizontal',
      top: 0,
      textStyle: {
        color: textColor.value
      },
      pageIconColor: primaryColor.value,
      pageTextStyle: {
        color: textColor.value
      },
      data: []
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: [],
      axisLine: {
        lineStyle: {
          color: borderColor.value
        }
      },
      axisLabel: {
        color: textColor.value,
        formatter: function(value) {
          return value.split(' ')[0] + '\n' + (value.split(' ')[1] || '');
        }
      },
      splitLine: {
        show: true,
        lineStyle: {
          color: props.isDark ? 'rgba(75, 85, 99, 0.2)' : 'rgba(229, 231, 235, 0.6)',
          type: 'dashed'
        }
      }
    },
    yAxis: {
      type: 'value',
      axisLine: {
        lineStyle: {
          color: borderColor.value
        }
      },
      axisLabel: {
        color: textColor.value
      },
      splitLine: {
        lineStyle: {
          color: props.isDark ? 'rgba(75, 85, 99, 0.2)' : 'rgba(229, 231, 235, 0.6)',
          type: 'dashed'
        }
      }
    },
    series: []
  }

  const colors = [
    '#3b82f6', '#10b981', '#f97316', '#8b5cf6', '#ec4899', 
    '#06b6d4', '#f59e0b', '#6366f1', '#ef4444', '#84cc16'
  ];

  let colorIndex = 0;
  for (let key in targetData.value) {
    if (key === 'DATATIME'){
      chartOption.value.xAxis.data = targetData.value[key]
    }
    else{
      chartOption.value.series.push({
        name: key,
        type: 'line',
        symbol: 'emptyCircle',
        symbolSize: 5,
        showSymbol: false,
        data: targetData.value[key],
        lineStyle: {
          width: 2,
          shadowColor: 'rgba(0, 0, 0, 0.2)',
          shadowBlur: 5,
          shadowOffsetY: 5,
          cap: 'round'
        },
        itemStyle: {
          color: colors[colorIndex % colors.length]
        },
        emphasis: {
          focus: 'series',
          itemStyle: {
            borderWidth: 2
          }
        },
        smooth: true
      });
      chartOption.value.legend.data.push(key);
      colorIndex++;
    }
  }
  chart.setOption(chartOption.value);
  tableData.value = convertToTableData(targetData.value);
}

const refreshChart_1 = () => {
  chart.dispose()
  chart = echarts.init(chartContainer.value, props.isDark ? 'dark' : null);
  isloading.value = true
  chartOption.value = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      textStyle: {
        align: 'left'
      },
      axisPointer: {
        type: 'cross',
        lineStyle: {
          color: primaryColor.value,
          width: 1,
          type: 'dashed'
        }
      },
      backgroundColor: props.isDark ? 'rgba(30, 30, 30, 0.9)' : 'rgba(255, 255, 255, 0.9)',
      borderColor: borderColor.value,
      borderWidth: 1,
      extraCssText: 'box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); backdrop-filter: blur(8px)'
    },
    toolbox: {
      show: true,
      right: 20,
      feature: {
        restore: {
          title: '重置'
        },
        saveAsImage: {
          title: '保存为图片'
        }
      },
      iconStyle: {
        borderColor: primaryColor.value
      }
    },
    grid: {
      left: '3%',
      right: '5%',
      bottom: '15%',
      top: '15%',
      containLabel: true
    },
    legend: {
      type: 'scroll',
      orient: 'horizontal',
      top: 0,
      textStyle: {
        color: textColor.value
      },
      pageIconColor: primaryColor.value,
      pageTextStyle: {
        color: textColor.value
      },
      data: []
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: [],
      axisLine: {
        lineStyle: {
          color: borderColor.value
        }
      },
      axisLabel: {
        color: textColor.value,
        formatter: function(value) {
          return value.split(' ')[0] + '\n' + (value.split(' ')[1] || '');
        }
      },
      splitLine: {
        show: true,
        lineStyle: {
          color: props.isDark ? 'rgba(75, 85, 99, 0.2)' : 'rgba(229, 231, 235, 0.6)',
          type: 'dashed'
        }
      }
    },
    yAxis: [],
    series: []
  }

  const colors = [
    '#3b82f6', '#10b981', '#f97316', '#8b5cf6', '#ec4899', 
    '#06b6d4', '#f59e0b', '#6366f1', '#ef4444', '#84cc16'
  ];

  let colorIndex = 0;
  for (let key in targetData.value) {
    if (key === 'DATATIME'){
      chartOption.value.xAxis.data = targetData.value[key]
    }
    else{
      chartOption.value.series.push({
        name: key,
        type: 'line',
        symbol: 'emptyCircle',
        symbolSize: 5,
        showSymbol: false,
        data: targetData.value[key],
        lineStyle: {
          width: 2,
          shadowColor: 'rgba(0, 0, 0, 0.2)',
          shadowBlur: 5,
          shadowOffsetY: 5
        },
        itemStyle: {
          color: colors[colorIndex % colors.length]
        },
        emphasis: {
          focus: 'series',
          itemStyle: {
            borderWidth: 2
          }
        },
        smooth: true
      });
      chartOption.value.yAxis.push(
          {
            type: 'value',
            name: key,
            nameTextStyle: {
              color: colors[colorIndex % colors.length],
              fontWeight: 'bold'
            },
            axisLine: {
              lineStyle: {
                color: borderColor.value
              }
            },
            axisLabel: {
              color: textColor.value
            },
            splitLine: {
              lineStyle: {
                color: props.isDark ? 'rgba(75, 85, 99, 0.2)' : 'rgba(229, 231, 235, 0.6)',
                type: 'dashed'
              }
            }
          }
      )
      chartOption.value.legend.data.push(key);
      colorIndex++;
    }
  }
  isloading.value = false
  chart.setOption(chartOption.value);
}

const handleTabClick = () => {
  if (currentChart.value === 1){
    refreshChart()
  }
  else{
    refreshChart_1()
  }
}

const handleClose = () => {
  window.removeEventListener('resize', chartResizeHandler);
  window.removeEventListener('resize', tableResizeHandler);
  if(chart){
    chart.dispose()
  }
}

</script>

<template>
  <el-drawer
      direction="rtl"
      size="90%"
      @open="getDataContent"
      @close="handleClose"
      :with-header="false"
      :destroy-on-close="true"
      :modal-class="props.isDark ? 'dark-drawer-mask' : 'light-drawer-mask'"
      :class="props.isDark ? 'dark-drawer' : 'light-drawer'"
  >
    <div class="drawer-content">
      <div class="drawer-header">
        <h2 class="drawer-title">
          <el-icon><DataAnalysis /></el-icon>
          数据可视化分析
        </h2>
        <div class="drawer-subtitle">{{ dataInfo.data_name }}</div>
      </div>
      
      <div class="section data-info-section">
        <div class="section-header">
          <h3>数据详情</h3>
          <div class="section-divider"></div>
        </div>
        
        <div class="data-info-grid">
          <div class="data-info-item">
            <div class="info-label">所属风机</div>
            <div class="info-value">{{ dataInfo.turbine_id }}</div>
          </div>
          <div class="data-info-item">
            <div class="info-label">数据类型</div>
            <div class="info-value">
              <el-tag :type="dataInfo.data_type === 'train' ? 'success' : 'primary'" effect="dark" size="small" round>
                {{ dataInfo.data_type === 'train' ? '训练数据' : '预测数据' }}
              </el-tag>
            </div>
          </div>
          <div class="data-info-item">
            <div class="info-label">起始时间</div>
            <div class="info-value">{{ dataInfo.data_startTime }}</div>
          </div>
          <div class="data-info-item">
            <div class="info-label">结束时间</div>
            <div class="info-value">{{ dataInfo.data_endTime }}</div>
          </div>
          <div class="data-info-item">
            <div class="info-label">数据大小</div>
            <div class="info-value">{{ dataInfo.data_size }}</div>
          </div>
          <div class="data-info-item">
            <div class="info-label">上传时间</div>
            <div class="info-value">{{ dataInfo.data_uploadTime }}</div>
          </div>
        </div>
        
        <div v-if="dataInfo.data_comment" class="data-comment">
          <div class="info-label">数据备注</div>
          <div class="info-value comment-text">{{ dataInfo.data_comment }}</div>
        </div>
      </div>
      
      <div class="section chart-section">
        <div class="section-header">
          <h3>数据可视化</h3>
          <div class="section-divider"></div>
    </div>
        
        <div class="time-range-selector">
    <el-date-picker
        v-model="timeRange"
        type="datetimerange"
        range-separator="至"
        unlink-panels
        :default-value="[new Date(startTime), new Date(endTime)]"
        @change="handleTimeRangeChange"
        start-placeholder="起始日期"
        end-placeholder="截止日期"
        :disabled-date="disabledDate"
              class="date-picker"
    />
        </div>
        
        <div class="chart-container">
    <el-tabs
        v-model="currentChart"
        type="border-card"
        @tab-click="handleTabClick"
              class="chart-tabs"
    >
            <el-tab-pane label="折线图" name="0">
      </el-tab-pane>
            <el-tab-pane label="关系折线图" name="1">
      </el-tab-pane>
            <div ref="chartContainer" class="echarts-container"></div>
          </el-tabs>
        </div>
      </div>
      
      <div class="section table-section">
        <div class="section-header">
          <h3>数据表格</h3>
          <div class="section-divider"></div>
        </div>
        
        <div class="table-container">
    <el-table-v2
        :columns="tableColumns"
        :data="tableData"
        :width="tableWidth"
        :height="tableHeight"
        fixed
              class="data-table"
              :theme="props.isDark ? 'dark' : 'light'"
    />
        </div>
      </div>
    </div>
  </el-drawer>
</template>

<style scoped>
/* 全局样式变量 - 更精致的设计系统 */
:root {
  --border-radius-sm: 6px;
  --border-radius: 12px;
  --border-radius-lg: 16px;
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.1);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.08), 0 2px 4px -1px rgba(0, 0, 0, 0.04);
  --shadow-lg: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  --primary-color: #3b82f6;
  --primary-gradient: linear-gradient(135deg, #3b82f6, #2563eb);
  --success-color: #10b981;
  --success-gradient: linear-gradient(135deg, #10b981, #059669);
  --warning-color: #f59e0b;
  --danger-color: #ef4444;
  --transition-normal: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  --transition-bounce: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* 增强暗色主题适配 */
:deep(.dark-drawer-mask) {
  background-color: rgba(0, 0, 0, 0.8) !important;
  backdrop-filter: blur(8px);
}

:deep(.dark-drawer) {
  background-color: #0f172a;
  color: #e2e8f0;
  border-left: 1px solid #1e293b;
}

:deep(.light-drawer-mask) {
  background-color: rgba(255, 255, 255, 0.15) !important;
  backdrop-filter: blur(8px);
}

:deep(.light-drawer) {
  background-color: #f8fafc;
  color: #334155;
  border-left: 1px solid #e2e8f0;
}

/* 升级抽屉内容区域 */
.drawer-content {
  padding: 28px;
  height: 100%;
  overflow-y: auto;
  scrollbar-width: thin;
  background-image: var(--drawer-bg-pattern);
  background-attachment: fixed;
  background-size: cover;
}

.dark-drawer .drawer-content {
  --drawer-bg-pattern: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M54.627 0l.83.828-1.415 1.415L51.8 0h2.827zM5.373 0l-.83.828L5.96 2.243 8.2 0H5.374zM48.97 0l3.657 3.657-1.414 1.414L46.143 0h2.828zM11.03 0L7.372 3.657 8.787 5.07 13.857 0H11.03zm32.284 0L49.8 6.485 48.384 7.9l-7.9-7.9h2.83zM16.686 0L10.2 6.485 11.616 7.9l7.9-7.9h-2.83zm20.97 0l9.315 9.314-1.414 1.414L34.828 0h2.83zM22.344 0L13.03 9.314l1.414 1.414L25.172 0h-2.83zM32 0l12.142 12.142-1.414 1.414L30 .828 17.272 13.556l-1.414-1.414L28 0h4zM.284 0l28 28-1.414 1.414L0 2.544v2.83L25.456 30l-1.414 1.414-28-28L0 0h.284zM0 5.373l25.456 25.455-1.414 1.415L0 8.2v2.83l21.628 21.628-1.414 1.414L0 13.515v2.83l17.8 17.8-1.414 1.414L0 18.688v2.83l14.142 14.14-1.414 1.415L0 23.86v2.828l10.314 10.314-1.414 1.414L0 29.044v2.828L5.657 37.5-1.414 38.914 0 34.23v2.828L1.828 40.8-.414 42.142 0 39.6v2.83l-1.414 1.413 1.414 1.414-1.414 1.414L0 45.058v2.828l-4.242 4.242 1.414 1.414L0 50.23v2.828l-8.07 8.07 1.415 1.414L0 55.402v2.826L-15.1-15.1l1.414-1.414 14.85 14.84v-2.827l-13.435-13.44 1.414-1.413L0 6.7V3.873l-9.9-9.9 1.415-1.415L0 1.7V-1.14l-6.364-6.364 1.415-1.415L0-2.853z' fill='%23334155' fill-opacity='0.02' fill-rule='evenodd'/%3E%3C/svg%3E");
}

.light-drawer .drawer-content {
  --drawer-bg-pattern: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M54.627 0l.83.828-1.415 1.415L51.8 0h2.827zM5.373 0l-.83.828L5.96 2.243 8.2 0H5.374zM48.97 0l3.657 3.657-1.414 1.414L46.143 0h2.828zM11.03 0L7.372 3.657 8.787 5.07 13.857 0H11.03zm32.284 0L49.8 6.485 48.384 7.9l-7.9-7.9h2.83zM16.686 0L10.2 6.485 11.616 7.9l7.9-7.9h-2.83zm20.97 0l9.315 9.314-1.414 1.414L34.828 0h2.83zM22.344 0L13.03 9.314l1.414 1.414L25.172 0h-2.83zM32 0l12.142 12.142-1.414 1.414L30 .828 17.272 13.556l-1.414-1.414L28 0h4zM.284 0l28 28-1.414 1.414L0 2.544v2.83L25.456 30l-1.414 1.414-28-28L0 0h.284zM0 5.373l25.456 25.455-1.414 1.415L0 8.2v2.83l21.628 21.628-1.414 1.414L0 13.515v2.83l17.8 17.8-1.414 1.414L0 18.688v2.83l14.142 14.14-1.414 1.415L0 23.86v2.828l10.314 10.314-1.414 1.414L0 29.044v2.828L5.657 37.5-1.414 38.914 0 34.23v2.828L1.828 40.8-.414 42.142 0 39.6v2.83l-1.414 1.413 1.414 1.414-1.414 1.414L0 45.058v2.828l-4.242 4.242 1.414 1.414L0 50.23v2.828l-8.07 8.07 1.415 1.414L0 55.402v2.826L-15.1-15.1l1.414-1.414 14.85 14.84v-2.827l-13.435-13.44 1.414-1.413L0 6.7V3.873l-9.9-9.9 1.415-1.415L0 1.7V-1.14l-6.364-6.364 1.415-1.415L0-2.853z' fill='%233b82f6' fill-opacity='0.02' fill-rule='evenodd'/%3E%3C/svg%3E");
}

.drawer-content::-webkit-scrollbar {
  width: 4px;
}

.drawer-content::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.3);
  border-radius: 2px;
}

.drawer-content::-webkit-scrollbar-thumb:hover {
  background-color: rgba(156, 163, 175, 0.5);
}

/* 升级页面标题部分 */
.drawer-header {
  margin-bottom: 36px;
  text-align: center;
  position: relative;
  animation: fadeIn 0.8s ease-out;
}

.drawer-header::after {
  content: '';
  position: absolute;
  bottom: -12px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 3px;
  border-radius: 3px;
  background: var(--primary-gradient);
}

.drawer-title {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  letter-spacing: 0.5px;
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
  animation: float 4s ease-in-out infinite;
}

.drawer-subtitle {
  font-size: 16px;
  opacity: 0.8;
  font-weight: 500;
}

/* 升级区块通用样式 */
.section {
  margin-bottom: 36px;
  padding: 24px;
  border-radius: var(--border-radius-lg);
  transition: var(--transition-normal);
  position: relative;
  overflow: hidden;
  animation: fadeIn 0.6s ease-out;
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), 
              box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.section:nth-child(1) {
  animation-delay: 0.1s;
}

.section:nth-child(2) {
  animation-delay: 0.3s;
}

.section:nth-child(3) {
  animation-delay: 0.5s;
}

.section:hover {
  transform: translateY(-5px);
}

.dark-drawer .section {
  background-color: rgba(30, 41, 59, 0.8);
  box-shadow: var(--shadow-lg);
  border: 1px solid rgba(71, 85, 105, 0.1);
  backdrop-filter: blur(8px);
}

.light-drawer .section {
  background-color: rgba(255, 255, 255, 0.9);
  box-shadow: var(--shadow-md);
  border: 1px solid rgba(226, 232, 240, 0.5);
  backdrop-filter: blur(8px);
}

.section-header {
  display: flex;
  align-items: center;
  margin-bottom: 28px;
  position: relative;
}

.section-header h3 {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
  padding-left: 16px;
  position: relative;
}

.section-header h3::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 20px;
  border-radius: 2px;
  background: var(--primary-gradient);
}

.section-divider {
  flex: 1;
  height: 1px;
  background: linear-gradient(to right, var(--primary-color), transparent);
  margin-left: 16px;
  border-radius: 1px;
  opacity: 0.3;
}

/* 升级数据信息区域 */
.data-info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 24px;
}

.data-info-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 16px;
  border-radius: var(--border-radius);
  transition: var(--transition-normal);
  animation: fadeIn 0.5s ease-out forwards;
  animation-delay: calc(0.1s * var(--item-index, 1));
  opacity: 0;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.data-info-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.dark-drawer .data-info-item {
  background-color: rgba(15, 23, 42, 0.3);
  border: 1px solid rgba(51, 65, 85, 0.2);
}

.light-drawer .data-info-item {
  background-color: rgba(248, 250, 252, 0.7);
  border: 1px solid rgba(226, 232, 240, 0.8);
}

.info-label {
  font-size: 14px;
  opacity: 0.7;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 0.2px;
  position: relative;
  transition: all 0.3s ease;
}

.info-value:hover {
  transform: scale(1.05);
  color: var(--primary-color);
}

.data-comment {
  margin-top: 16px;
  padding: 20px;
  border-radius: var(--border-radius);
  position: relative;
  overflow: hidden;
}

.dark-drawer .data-comment {
  background-color: rgba(15, 23, 42, 0.3);
  border: 1px solid rgba(51, 65, 85, 0.2);
}

.light-drawer .data-comment {
  background-color: rgba(248, 250, 252, 0.7);
  border: 1px solid rgba(226, 232, 240, 0.8);
}

.comment-text {
  margin-top: 8px;
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-line;
}

/* 升级图表区域 */
.time-range-selector {
  margin-bottom: 24px;
}

.date-picker {
  width: 100%;
}

.date-picker :deep(.el-input__wrapper) {
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.date-picker :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px var(--primary-color) !important;
  transform: translateY(-1px);
}

.date-picker :deep(.el-range-separator) {
  transition: all 0.3s ease;
}

.dark-drawer :deep(.el-input__wrapper),
.dark-drawer :deep(.el-range-input) {
  --el-input-bg-color: rgba(30, 41, 59, 0.8) !important;
  --el-input-border-color: rgba(71, 85, 105, 0.2) !important;
  --el-input-hover-border-color: var(--primary-color) !important;
  --el-input-focus-border-color: var(--primary-color) !important;
  color: #e2e8f0 !important;
}

.chart-container {
  width: 100%;
  border-radius: var(--border-radius);
  overflow: hidden;
}

:deep(.chart-tabs .el-tabs__header) {
  margin-bottom: 0;
  border-radius: var(--border-radius) var(--border-radius) 0 0;
  overflow: hidden;
}

:deep(.chart-tabs .el-tabs__nav) {
  border: none !important;
  border-radius: var(--border-radius) var(--border-radius) 0 0;
}

:deep(.chart-tabs .el-tabs__item) {
  height: 46px;
  line-height: 46px;
  font-weight: 600;
  letter-spacing: 0.3px;
  transition: var(--transition-normal);
  position: relative;
  overflow: hidden;
}

:deep(.chart-tabs .el-tabs__item)::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 3px;
  background: var(--primary-gradient);
  transition: all 0.3s ease;
  transform: translateX(-50%);
  border-radius: 3px 3px 0 0;
}

:deep(.chart-tabs .el-tabs__item):hover::before {
  width: 100%;
}

:deep(.chart-tabs .el-tabs__item.is-active)::before {
  width: 100%;
}

.dark-drawer :deep(.chart-tabs) {
  --el-border-color: #334155;
  --el-fill-color-blank: #1e293b;
  --el-text-color-primary: #e2e8f0;
  border-color: #334155;
}

.echarts-container {
  width: 100%;
  height: 500px;
  margin-bottom: 0;
  border-radius: 0 0 var(--border-radius) var(--border-radius);
  overflow: hidden;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.05);
  transition: all 0.5s ease;
}

/* 升级表格区域 */
.table-container {
  width: 100%;
  overflow: hidden;
  border-radius: var(--border-radius);
}

:deep(.data-table) {
  border-radius: var(--border-radius);
  overflow: hidden;
}

.dark-drawer :deep(.el-table-v2__header-cell) {
  background-color: #1e293b !important;
  color: #e2e8f0 !important;
  font-weight: 600;
}

.light-drawer :deep(.el-table-v2__header-cell) {
  background-color: #f1f5f9 !important;
  color: #334155 !important;
  font-weight: 600;
}

.dark-drawer :deep(.el-table-v2__cell) {
  background-color: #0f172a !important;
  color: #e2e8f0 !important;
  border-bottom: 1px solid #334155 !important;
}

.light-drawer :deep(.el-table-v2__cell) {
  background-color: #ffffff !important;
  color: #334155 !important;
  border-bottom: 1px solid #e2e8f0 !important;
}

/* 响应式处理升级 */
@media (max-width: 768px) {
  .drawer-content {
    padding: 20px;
  }
  
  .data-info-grid {
    grid-template-columns: 1fr;
  }
  
  .section {
    padding: 20px;
  }
  
  .drawer-title {
    font-size: 24px;
  }
  
  .echarts-container {
    height: 360px;
  }
}

@media (min-width: 1440px) {
  .drawer-content {
    padding: 36px;
  }
  
  .section {
    padding: 32px;
  }
  
  .echarts-container {
    height: 600px;
  }
}

/* 精致动画效果 */
@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-8px);
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

/* 全局交互动画应用 */
.drawer-content {
  /* 已有样式保持不变 */
}

.drawer-header {
  animation: fadeIn 0.8s ease-out;
}

.drawer-title .el-icon {
  animation: float 4s ease-in-out infinite;
}

.section {
  animation: fadeIn 0.6s ease-out;
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), 
              box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.section:nth-child(1) {
  animation-delay: 0.1s;
}

.section:nth-child(2) {
  animation-delay: 0.3s;
}

.section:nth-child(3) {
  animation-delay: 0.5s;
}

.section:hover {
  transform: translateY(-5px);
}

/* 数据信息区块动画 */
.data-info-item {
  animation: fadeIn 0.5s ease-out forwards;
  animation-delay: calc(0.1s * var(--item-index, 1));
  opacity: 0;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.data-info-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.info-value {
  position: relative;
  transition: all 0.3s ease;
}

.info-value:hover {
  transform: scale(1.05);
  color: var(--primary-color);
}

/* 图表区域交互 */
:deep(.chart-tabs .el-tabs__item) {
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

:deep(.chart-tabs .el-tabs__item)::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 3px;
  background: var(--primary-gradient);
  transition: all 0.3s ease;
  transform: translateX(-50%);
  border-radius: 3px 3px 0 0;
}

:deep(.chart-tabs .el-tabs__item):hover::before {
  width: 100%;
}

:deep(.chart-tabs .el-tabs__item.is-active)::before {
  width: 100%;
}

.echarts-container {
  transition: all 0.5s ease;
}

/* 数据表格交互效果 */
:deep(.el-table-v2__row) {
  transition: background-color 0.2s ease;
}

:deep(.el-table-v2__row:hover .el-table-v2__cell) {
  background-color: rgba(59, 130, 246, 0.05) !important;
}

/* 为数据信息项设置动画延迟 */
.data-info-grid:deep(.data-info-item:nth-child(1)) { --item-index: 1; }
.data-info-grid:deep(.data-info-item:nth-child(2)) { --item-index: 2; }
.data-info-grid:deep(.data-info-item:nth-child(3)) { --item-index: 3; }
.data-info-grid:deep(.data-info-item:nth-child(4)) { --item-index: 4; }
.data-info-grid:deep(.data-info-item:nth-child(5)) { --item-index: 5; }
.data-info-grid:deep(.data-info-item:nth-child(6)) { --item-index: 6; }

/* 抽屉动画增强 */
:deep(.el-drawer__body) {
  --transform-transition: transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* 加载动画增强 */
:deep(.el-loading-mask) {
  backdrop-filter: blur(5px);
  background-color: rgba(0, 0, 0, 0.6) !important;
}

:deep(.el-loading-spinner) {
  animation: pulse 2s infinite;
}

:deep(.el-loading-text) {
  background: linear-gradient(to right, #3b82f6, #60a5fa, #3b82f6);
  background-size: 200% auto;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  animation: shimmer 2s linear infinite;
}
</style>