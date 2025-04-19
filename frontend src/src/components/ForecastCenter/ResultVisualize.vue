<script setup>
import {defineProps, ref, computed} from 'vue'
import * as echarts from 'echarts';
import {ElLoading} from "element-plus";

const props = defineProps({
  forecastTask: {
    type: Object,
    required: true
  },
  isDark: {
    type: Boolean,
    required: true
  }
})

// 主题颜色计算属性
const themeColors = computed(() => ({
  mainBg: props.isDark ? 'rgba(30, 41, 59, 0.95)' : 'rgba(255, 255, 255, 0.95)',
  cardBg: props.isDark ? 'rgba(30, 41, 59, 0.5)' : 'rgba(255, 255, 255, 0.5)',
  title: props.isDark ? '#e5e7eb' : '#1e293b',
  text: props.isDark ? '#94a3b8' : '#64748b',
  highlight: props.isDark ? '#60a5fa' : '#3b82f6',
  divider: props.isDark ? 'rgba(148, 163, 184, 0.2)' : 'rgba(203, 213, 225, 0.5)',
  border: props.isDark ? 'rgba(71, 85, 105, 0.3)' : 'rgba(226, 232, 240, 0.5)',
  shadowColor: props.isDark ? 'rgba(0, 0, 0, 0.2)' : 'rgba(0, 0, 0, 0.1)'
}))

const dataContent = ref({})

const startTime = ref('')
const endTime = ref('')
const startRange = ref('')
const endRange = ref('')

const timeRange = ref([])
const chartContainer = ref(null)
const chartOption = ref({})

const tableColumns = ref([])
const tableData = ref([])
const tableWidth = ref(window.innerWidth * 0.84)
const tableHeight = ref(640)


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
    text: '准备中...^ ^',
  })
  fetch(`/api/get_dataContent/?data_id=${props.forecastTask.result_id}`)
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
    chart = echarts.init(chartContainer.value,'dark' );
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
  let targetData = {}
  tableColumns.value = []

  for(let key in dataContent.value){
    targetData[key] = []
    if(key === 'TurbID' || key === 'ROUND(A.POWER,0)'){
      continue
    }
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
      targetData[key].push(dataContent.value[key][i])
    }
    if (new Date(dataContent.value.DATATIME[i]) > endRange.value) {
      break
    }
  }
  
  // 计算每个系列的最大值和最小值
  const seriesMaxMin = {};
  for (let key in targetData) {
    if(key !== 'DATATIME' && key !== 'TurbID' && key !== 'ROUND(A.POWER,0)'){
      const data = targetData[key];
      seriesMaxMin[key] = {
        max: Math.max(...data),
        min: Math.min(...data),
        maxIndex: data.indexOf(Math.max(...data)),
        minIndex: data.indexOf(Math.min(...data))
      };
    }
  }
  
  // 生成渐变色数组
  const gradientColors = [
    ['#36D1DC', '#5B86E5'], // 蓝色渐变
    ['#FF9A8B', '#FF6A88'], // 红色渐变
    ['#8BC6EC', '#9599E2'], // 紫色渐变
    ['#FCCF31', '#F55555'], // 黄橙渐变
    ['#43E97B', '#38F9D7'], // 绿色渐变
    ['#FA709A', '#FEE140']  // 粉色渐变
  ];
  
  chartOption.value = {
    backgroundColor: props.isDark ? 'rgba(30, 41, 59, 0.6)' : 'rgba(255, 255, 255, 0.6)',
    title: {
      text: '预测数据可视化',
      left: 'center',
      textStyle: {
        fontWeight: 'bold',
        color: props.isDark ? '#e5e7eb' : '#1e293b',
        fontSize: 18
      }
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: props.isDark ? 'rgba(30, 41, 59, 0.9)' : 'rgba(255, 255, 255, 0.9)',
      borderColor: props.isDark ? 'rgba(71, 85, 105, 0.3)' : 'rgba(226, 232, 240, 0.8)',
      textStyle: {
        color: props.isDark ? '#e5e7eb' : '#1e293b',
        fontSize: 13
      },
      formatter: function(params) {
        let result = `<div style="font-weight:bold;margin-bottom:5px;">${params[0].axisValue}</div>`;
        params.forEach((param, index) => {
          const colorStyle = props.isDark ? 
            `background:linear-gradient(to right, ${gradientColors[index % gradientColors.length][0]}, ${gradientColors[index % gradientColors.length][1]});-webkit-background-clip:text;-webkit-text-fill-color:transparent;` : 
            `color:${param.color}`;
          result += `<div style="display:flex;align-items:center;margin:5px 0;">
            <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:${param.color};margin-right:8px;"></span>
            <span style="font-weight:bold;${colorStyle}">${param.seriesName}:</span>
            <span style="margin-left:5px;font-weight:bold;">${param.value}</span>
          </div>`;
        });
        return result;
      },
      axisPointer: {
        type: 'line',
        lineStyle: {
          color: props.isDark ? 'rgba(148, 163, 184, 0.5)' : 'rgba(100, 116, 139, 0.2)',
          width: 1,
          type: 'dashed'
        }
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '8%',
      top: '70px',
      containLabel: true
    },
    toolbox: {
      show: true,
      right: 20,
      feature: {
        dataZoom: {
          yAxisIndex: 'none',
          icon: {
            zoom: 'path://M0,13.5h26.9 M13.5,26.9V0 M32.1,13.5H58V58H13.5 V32.1',
            back: 'path://M22,1.4L9.9,13.5l12.3,12.3 M10.3,13.5H54.9v44.6 H10.3v-12.6'
          },
          title: {
            zoom: '区域缩放',
            back: '还原缩放'
          }
        },
        restore: {
          title: '还原'
        },
        saveAsImage: {
          title: '保存为图片'
        }
      }
    },
    dataZoom: [
      {
        type: 'inside',
        start: 0,
        end: 100,
        minValueSpan: 3600 * 24 * 1000 * 3, // 最小为3天数据
      },
      {
        start: 0,
        end: 100,
        height: 20,
        bottom: 10,
        borderColor: props.isDark ? 'rgba(71, 85, 105, 0.3)' : 'rgba(226, 232, 240, 0.8)',
        fillerColor: props.isDark ? 'rgba(59, 130, 246, 0.2)' : 'rgba(59, 130, 246, 0.1)',
        textStyle: {
          color: props.isDark ? '#94a3b8' : '#64748b'
        },
        handleStyle: {
          color: props.isDark ? '#60a5fa' : '#3b82f6',
          borderColor: props.isDark ? '#60a5fa' : '#3b82f6'
        },
        moveHandleStyle: {
          color: props.isDark ? '#60a5fa' : '#3b82f6'
        },
        selectedDataBackground: {
          lineStyle: {
            color: props.isDark ? '#60a5fa' : '#3b82f6'
          },
          areaStyle: {
            color: props.isDark ? 'rgba(59, 130, 246, 0.2)' : 'rgba(59, 130, 246, 0.1)'
          }
        }
      }
    ],
    legend: {
      data: [],
      top: 30,
      type: 'scroll',
      padding: [5, 20],
      itemGap: 20,
      textStyle: {
        color: props.isDark ? '#94a3b8' : '#64748b',
        fontSize: 12
      },
      icon: 'roundRect',
      itemWidth: 12,
      itemHeight: 12,
      pageTextStyle: {
        color: props.isDark ? '#94a3b8' : '#64748b'
      }
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: [],
      axisLine: {
        lineStyle: {
          color: props.isDark ? 'rgba(148, 163, 184, 0.2)' : 'rgba(203, 213, 225, 0.5)'
        }
      },
      axisTick: {
        show: false
      },
      axisLabel: {
        color: props.isDark ? '#94a3b8' : '#64748b',
        fontSize: 12,
        formatter: function(value) {
          const date = new Date(value);
          return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`;
        }
      },
      splitLine: {
        show: true,
        lineStyle: {
          color: props.isDark ? 'rgba(148, 163, 184, 0.1)' : 'rgba(203, 213, 225, 0.3)',
          type: 'dashed'
        }
      }
    },
    yAxis: {
      type: 'value',
      axisLine: {
        lineStyle: {
          color: props.isDark ? 'rgba(148, 163, 184, 0.2)' : 'rgba(203, 213, 225, 0.5)'
        }
      },
      axisTick: {
        show: false
      },
      axisLabel: {
        color: props.isDark ? '#94a3b8' : '#64748b',
        fontSize: 12
      },
      splitLine: {
        lineStyle: {
          color: props.isDark ? 'rgba(148, 163, 184, 0.1)' : 'rgba(203, 213, 225, 0.3)',
          type: 'dashed'
        }
      }
    },
    series: []
  }

  let colorIndex = 0;
  for (let key in targetData) {
    if(key === 'TurbID' || key === 'ROUND(A.POWER,0)'){
      continue
    }
    if (key === 'DATATIME'){
      chartOption.value.xAxis.data = targetData[key]
    }
    else{
      // 获取当前系列的最大值和最小值
      const maxValue = seriesMaxMin[key].max;
      const minValue = seriesMaxMin[key].min;
      const maxIndex = seriesMaxMin[key].maxIndex;
      const minIndex = seriesMaxMin[key].minIndex;
      
      // 创建渐变色
      const currentGradient = gradientColors[colorIndex % gradientColors.length];
      
      chartOption.value.series.push({
        name: key,
        type: 'line',
        symbol: 'emptyCircle',
        symbolSize: 6,
        showSymbol: false,
        data: targetData[key],
        lineStyle: {
          width: 3,
          shadowColor: 'rgba(0, 0, 0, 0.2)',
          shadowBlur: 10,
          shadowOffsetY: 5,
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [{
              offset: 0, 
              color: currentGradient[0]
            }, {
              offset: 1, 
              color: currentGradient[1]
            }]
          }
        },
        itemStyle: {
          color: function(params) {
            return new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
              offset: 0,
              color: currentGradient[0]
            }, {
              offset: 1,
              color: currentGradient[1]
            }]);
          },
          borderColor: '#fff',
          borderWidth: 1
        },
        emphasis: {
          scale: true,
          focus: 'series',
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(0, 0, 0, 0.3)'
          }
        },
        smooth: true,
        areaStyle: {
          opacity: 0.2,
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: currentGradient[0]
            },
            {
              offset: 1,
              color: 'rgba(255, 255, 255, 0.1)'
            }
          ])
        },
        markPoint: {
          symbolSize: 45,
          data: [
            {
              type: 'max', 
              name: '最大值',
              itemStyle: {
                color: currentGradient[0],
                shadowBlur: 10,
                shadowColor: 'rgba(0, 0, 0, 0.3)'
              },
              label: {
                fontSize: 12,
                color: '#fff',
                formatter: `{c}`
              }
            },
            {
              type: 'min', 
              name: '最小值',
              itemStyle: {
                color: currentGradient[1],
                shadowBlur: 10,
                shadowColor: 'rgba(0, 0, 0, 0.3)'
              },
              label: {
                fontSize: 12,
                color: '#fff',
                formatter: `{c}`
              }
            }
          ]
        }
      })
      chartOption.value.legend.data.push(key)
      colorIndex++;
    }
  }
  chart.setOption(chartOption.value);
  tableData.value = convertToTableData(targetData)
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
      class="visualization-drawer"
  >
    <div class="drawer-content">
      <div class="header-section">
        <div class="title-wrapper">
          <h3 class="main-title">预测任务详情</h3>
          <div class="title-decoration"></div>
        </div>
        
        <div class="task-info-grid">
          <div class="task-info-card">
            <div class="task-info-icon">
              <el-icon><WindPower /></el-icon>
            </div>
            <div class="task-info-content">
              <div class="task-info-label">预测风机</div>
              <div class="task-info-value">{{forecastTask.turbine_id}}</div>
            </div>
          </div>
          
          <div class="task-info-card">
            <div class="task-info-icon">
              <el-icon><DataLine /></el-icon>
            </div>
            <div class="task-info-content">
              <div class="task-info-label">预测数据</div>
              <div class="task-info-value">{{forecastTask.data_name}}</div>
            </div>
          </div>
          
          <div class="task-info-card">
            <div class="task-info-icon">
              <el-icon><Odometer /></el-icon>
            </div>
            <div class="task-info-content">
              <div class="task-info-label">模型类型</div>
              <div class="task-info-value">{{forecastTask.model_type}}</div>
            </div>
          </div>
          
          <div class="task-info-card">
            <div class="task-info-icon">
              <el-icon><Check /></el-icon>
            </div>
            <div class="task-info-content">
              <div class="task-info-label">完成时间</div>
              <div class="task-info-value">{{forecastTask.task_finishTime}}</div>
            </div>
          </div>
          
          <div class="task-info-card">
            <div class="task-info-icon">
              <el-icon><VideoPlay /></el-icon>
            </div>
            <div class="task-info-content">
              <div class="task-info-label">起始时间</div>
              <div class="task-info-value">{{forecastTask.task_startTime}}</div>
            </div>
          </div>
          
          <div class="task-info-card">
            <div class="task-info-icon">
              <el-icon><VideoPause /></el-icon>
            </div>
            <div class="task-info-content">
              <div class="task-info-label">结束时间</div>
              <div class="task-info-value">{{forecastTask.task_endTime}}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="visualization-section">
        <div class="section-header">
          <h3 class="section-title">数据可视化</h3>
          <div class="section-divider"></div>
        </div>
        <div class="date-picker-container">
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
              class="custom-date-picker"
          />
        </div>
        <div class="chart-container">
          <div ref="chartContainer" class="echarts-container"></div>
        </div>
      </div>

      <div class="table-section">
        <div class="section-header">
          <h3 class="section-title">数据表格</h3>
          <div class="section-divider"></div>
        </div>
        <div class="table-container">
          <el-table-v2
              :columns="tableColumns"
              :data="tableData"
              :width="tableWidth"
              :height="tableHeight"
              fixed
              class="custom-table"
          />
        </div>
      </div>
    </div>
  </el-drawer>
</template>

<style scoped>
.visualization-drawer {
  --el-drawer-bg-color: var(--el-bg-color);
  --el-drawer-padding: 0;
}

.drawer-content {
  padding: 24px;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 24px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(249, 250, 252, 0.9));
  backdrop-filter: blur(15px);
}

.header-section {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.04), 0 2px 5px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(235, 238, 245, 0.8);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.header-section:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.05), 0 5px 15px rgba(0, 0, 0, 0.03);
}

.title-wrapper {
  position: relative;
  margin-bottom: 24px;
}

.main-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin: 0;
  background: linear-gradient(135deg, var(--el-color-primary), var(--el-color-primary-light-3));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.title-decoration {
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, var(--el-color-primary), var(--el-color-primary-light-5));
  border-radius: 3px;
  box-shadow: 0 2px 4px rgba(64, 158, 255, 0.2);
}

.task-info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
  margin-top: 24px;
}

.task-info-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(235, 238, 245, 0.8);
  transition: all 0.3s ease;
}

.task-info-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  background: rgba(255, 255, 255, 0.9);
}

.task-info-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--el-color-primary-light-5), var(--el-color-primary));
  color: white;
  font-size: 24px;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.2);
  transition: all 0.3s ease;
}

.task-info-card:hover .task-info-icon {
  transform: rotate(5deg) scale(1.1);
}

.task-info-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex-grow: 1;
}

.task-info-label {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  margin-bottom: 4px;
}

.task-info-value {
  font-size: 16px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 为每个卡片设置不同的渐变色 */
.task-info-card:nth-child(1) .task-info-icon {
  background: linear-gradient(135deg, #36D1DC, #5B86E5);
}

.task-info-card:nth-child(2) .task-info-icon {
  background: linear-gradient(135deg, #FF9A8B, #FF6A88);
}

.task-info-card:nth-child(3) .task-info-icon {
  background: linear-gradient(135deg, #8BC6EC, #9599E2);
}

.task-info-card:nth-child(4) .task-info-icon {
  background: linear-gradient(135deg, #FCCF31, #F55555);
}

.task-info-card:nth-child(5) .task-info-icon {
  background: linear-gradient(135deg, #43E97B, #38F9D7);
}

.task-info-card:nth-child(6) .task-info-icon {
  background: linear-gradient(135deg, #FA709A, #FEE140);
}

.visualization-section,
.table-section {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.04), 0 2px 5px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(235, 238, 245, 0.8);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.visualization-section:hover,
.table-section:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.05), 0 5px 15px rgba(0, 0, 0, 0.03);
}

.section-header {
  margin-bottom: 24px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin: 0 0 12px 0;
  display: flex;
  align-items: center;
}

.section-title::before {
  content: '';
  display: inline-block;
  width: 4px;
  height: 18px;
  background: var(--el-color-primary);
  border-radius: 2px;
  margin-right: 10px;
}

.section-divider {
  height: 1px;
  width: 100%;
  background: linear-gradient(90deg, var(--el-color-primary), transparent 80%);
}

.date-picker-container {
  margin-bottom: 24px;
}

.custom-date-picker {
  width: 100%;
}

.chart-container {
  height: 450px;
  margin-bottom: 24px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  padding: 16px;
  box-shadow: inset 0 1px 5px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  border: 1px solid rgba(235, 238, 245, 0.8);
  position: relative;
  overflow: hidden;
}

.chart-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, 
    #36D1DC, #5B86E5, 
    #FF9A8B, #FF6A88, 
    #8BC6EC, #9599E2);
  opacity: 0.7;
  border-radius: 12px 12px 0 0;
}

.chart-container:hover {
  box-shadow: inset 0 1px 10px rgba(0, 0, 0, 0.08);
}

.echarts-container {
  width: 100%;
  height: 100%;
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.table-container {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  padding: 16px;
  box-shadow: inset 0 1px 5px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(235, 238, 245, 0.8);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.table-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, 
    #8BC6EC, #9599E2, 
    #43E97B, #38F9D7,
    #FCCF31, #F55555);
  opacity: 0.7;
  border-radius: 12px 12px 0 0;
}

.table-container:hover {
  box-shadow: inset 0 1px 10px rgba(0, 0, 0, 0.08);
}

.custom-table {
  --el-table-border-color: rgba(235, 238, 245, 0.8);
  --el-table-header-bg-color: rgba(64, 158, 255, 0.05);
  --el-table-row-hover-bg-color: rgba(64, 158, 255, 0.05);
}

:deep(.el-table-v2__header-cell) {
  background: rgba(64, 158, 255, 0.05);
  font-weight: 600;
  color: var(--el-text-color-primary);
  text-align: center;
  position: relative;
}

:deep(.el-table-v2__header-cell::after) {
  content: '';
  position: absolute;
  bottom: 0;
  left: 10%;
  width: 80%;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(64, 158, 255, 0.2), transparent);
}

:deep(.el-table-v2__row) {
  transition: all 0.3s ease;
}

:deep(.el-table-v2__row:hover) {
  background: rgba(64, 158, 255, 0.05);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

:deep(.el-date-editor) {
  --el-input-bg-color: rgba(255, 255, 255, 0.8);
  --el-input-border-color: rgba(235, 238, 245, 0.8);
  transition: all 0.3s ease;
}

:deep(.el-date-editor:hover) {
  --el-input-border-color: var(--el-color-primary-light-5);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

:deep(.el-date-editor:focus) {
  --el-input-border-color: var(--el-color-primary);
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
  transform: translateY(-1px);
}
</style>