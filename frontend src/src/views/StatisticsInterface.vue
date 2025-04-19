<script setup>
  import {ref, onMounted, onUnmounted, defineProps} from 'vue'
  import dayjs from 'dayjs'
  import {
    Calendar, Download, Finished, Sunset,
    Upload, WindPower, ChatDotSquare, Clock, Odometer, Position,
    Monitor, Cpu, DataBoard, DataLine
  } from '@element-plus/icons-vue'
  import MessageCard from "@/components/utils/MessageCard.vue";

  const timeToNextDay = ref(dayjs().add(1, 'day').startOf('day'))
  const statisticsData = ref({})
  const visits = parseInt(localStorage.getItem('visits')) + 1;
  const currentRunningTime = ref(null)
  const displayTime = ref("")
  const interval = ref(null)

  const cpuUsage = ref(0)
  const gpuUsage = ref(0)
  const memoryUsage = ref(0)
  const diskUsage = ref(0)
  const dynamicSpan = ref(4)
  const props = defineProps({
    isDark: {
      type: Boolean,
      required: true
    },
    windowsHeight: {
      type: Number,
      required: true
    },
    windowsWidth: {
      type: Number,
      required: true
    }
  })

  const colors = [
    { color: '#67C23A', percentage: 20 },  // 绿色
    { color: '#5DB8FF', percentage: 40 },  // 蓝色
    { color: '#E6A23C', percentage: 60 },  // 黄色
    { color: '#F56C6C', percentage: 80 },  // 红色
    { color: '#F56C6C', percentage: 100 }, // 深红色
  ]
  const alt_colors = [
    { color: '#67C23A', percentage: 20 },  // 绿色
    { color: '#5DB8FF', percentage: 40 },  // 蓝色
    { color: '#E6A23C', percentage: 60 },  // 黄色
    { color: '#F56C6C', percentage: 80 },  // 红色
    { color: '#F56C6C', percentage: 100 }, // 深红色
  ]
  const formatTimestamp = (timestamp) => {
    var date = new Date(timestamp);

    var year = date.getFullYear() - 1970;
    var month = date.getMonth();
    var day = date.getDate() - 1;
    var hour = date.getHours();
    var minute = date.getMinutes();
    var second = date.getSeconds();

    let timeStr = day + "天 " + String(hour).padStart(2,'0')
        + "时" + String(minute).padStart(2,'0') + "分" + String(second).padStart(2,'0') + "秒";

    if(year === 0 && month === 0){
      return timeStr
    }
    else if(year === 0){
      return month + "月 " + timeStr
    }
    else{
      return year + "年 " + month + "月 " + timeStr
    }
  }

  const assembleUseage = (data) => {
    cpuUsage.value = data.cpu_usage
    gpuUsage.value = data.gpu_usage
    memoryUsage.value = data.memory_usage
    diskUsage.value = data.disk_usage
  }

  const get_useage = () => {
    fetch('/api/get_useAge/')
        .then(response => {
          return response.json()
        })
        .then((data) => {
          assembleUseage(data)
        })
        .catch(e => console.log("Oops, error", e))
  }

  const currentPercentage = ref(0)
  const assembleStatistics = (data) => {
    statisticsData.value = data[0].fields
    statisticsData.value['modelNum'] = data[0].modelNum
    statisticsData.value['turbineNum'] = data[0].turbineNum
    statisticsData.value['dataNum'] = data[0].dataNum
    statisticsData.value['taskNum'] = data[0].taskNum
    statisticsData.value['guestbookNum'] = data[0].guestbookNum
    console.log(statisticsData.value)
    currentRunningTime.value = new Date(statisticsData.value.statistics_time * 1000)
    displayTime.value = formatTimestamp(currentRunningTime.value)

    interval.value = setInterval(() => {
      currentRunningTime.value = currentRunningTime.value + 500;
      displayTime.value = formatTimestamp(currentRunningTime.value)

      let currentTime = dayjs()
      let pastTime = dayjs().startOf('day')
      let timeDiff = currentTime.diff(pastTime)
      currentPercentage.value = ((1 - timeDiff / 86400000 ) * 100).toFixed(2)

      get_useage()

    }, 500)
  }

  onMounted(() => {
    fetch('/api/get_statistics/')
        .then(response => {
          return response.json()
        })
        .then((data) => {
          assembleStatistics(data)
        })
        .catch(e => console.log("Oops, error", e))
    get_useage()
  })

  onUnmounted(() => {
    clearInterval(interval.value)
  })
</script>

<template>
  <div class="statistics-container" :class="{ 'dark-mode': isDark }">
    <div class="statistics-header">
      <div class="title-wrapper">
        <el-text class="title">统计界面</el-text>
        <div class="title-decoration"></div>
      </div>
      <div class="subtitle">系统实时数据监控中心</div>
    </div>

    <!-- 基础统计数据 -->
    <div class="basic-stats-grid">
      <div class="statistics-card">
        <div class="card-icon">
          <el-icon><Position /></el-icon>
        </div>
        <el-statistic :value="visits" class="statistic-item">
          <template #title>
            <div class="statistic-label">系统访问次数</div>
          </template>
        </el-statistic>
      </div>

      <div class="statistics-card">
        <div class="card-icon">
          <el-icon><Upload /></el-icon>
        </div>
        <el-statistic :value="statisticsData.statistics_upload" class="statistic-item">
          <template #title>
            <div class="statistic-label">数据上传总数</div>
          </template>
        </el-statistic>
      </div>

      <div class="statistics-card">
        <div class="card-icon">
          <el-icon><Download /></el-icon>
        </div>
        <el-statistic :value="statisticsData.statistics_download" class="statistic-item">
          <template #title>
            <div class="statistic-label">数据下载总次数</div>
          </template>
        </el-statistic>
      </div>

      <div class="statistics-card">
        <div class="card-icon">
          <el-icon><WindPower /></el-icon>
        </div>
        <el-statistic :value="statisticsData.statistics_uploadTurbine" class="statistic-item">
          <template #title>
            <div class="statistic-label">风机上传总数</div>
          </template>
        </el-statistic>
      </div>
    </div>

    <!-- 高级统计数据 -->
    <div class="advanced-stats-grid">
      <div class="statistics-card">
        <div class="card-icon">
          <el-icon><Odometer /></el-icon>
        </div>
        <el-statistic :value="statisticsData.statistics_train" class="statistic-item">
          <template #title>
            <div class="statistic-label">训练模型总数</div>
          </template>
        </el-statistic>
      </div>

      <div class="statistics-card">
        <div class="card-icon">
          <el-icon><Finished /></el-icon>
        </div>
        <el-statistic :value="statisticsData.statistics_upload" class="statistic-item">
          <template #title>
            <div class="statistic-label">预测任务下达数</div>
          </template>
        </el-statistic>
      </div>
    </div>

    <!-- 时间统计区域 -->
    <div class="time-section">
      <div class="time-card">
        <div class="time-icon">
          <el-icon><Clock /></el-icon>
        </div>
        <el-statistic :value="displayTime" class="time-statistic">
          <template #title>
            <div class="time-label">系统运行总时长</div>
          </template>
        </el-statistic>
      </div>

      <div class="time-card">
        <div class="time-icon">
          <el-icon><Sunset /></el-icon>
        </div>
        <el-countdown format="HH:mm:ss" :value="timeToNextDay" class="time-statistic">
          <template #title>
            <div class="time-label">今天剩余时间</div>
          </template>
        </el-countdown>
        <div class="countdown-footer">{{ dayjs().format('YYYY-MM-DD') }}</div>
      </div>
    </div>

    <!-- 系统资源监控区域 -->
    <div class="resource-section">
      <div class="section-header">
        <h3 class="section-title">系统资源监控</h3>
        <div class="section-divider"></div>
      </div>

      <template v-if="windowsWidth > 1186">
        <div class="resource-grid">
          <!-- 内存使用率 -->
          <div class="resource-card">
            <div class="resource-icon">
              <el-icon><DataBoard /></el-icon>
            </div>
            <div class="resource-content">
              <el-progress
                type="dashboard"
                :percentage="memoryUsage"
                :color="alt_colors"
                :width="120"
                :stroke-width="12"
                class="resource-progress"
              >
                <template #default="{ percentage }">
                  <span class="percentage-value" :data-percentage="memoryUsage < 60 ? 'low' : memoryUsage < 80 ? 'medium' : 'high'">{{ percentage }}%</span>
                  <span class="percentage-label">RAM占用率</span>
                </template>
              </el-progress>
              <div class="resource-details">
                <div class="detail-item">
                  <span class="detail-label">已用内存</span>
                  <span class="detail-value">{{ ((memoryUsage / 100) * 16).toFixed(1) }}GB</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">总内存</span>
                  <span class="detail-value">16GB</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 磁盘使用率 -->
          <div class="resource-card">
            <div class="resource-icon">
              <el-icon><DataLine /></el-icon>
            </div>
            <div class="resource-content">
              <el-progress
                type="dashboard"
                :percentage="diskUsage"
                :color="alt_colors"
                :width="120"
                :stroke-width="12"
                class="resource-progress"
              >
                <template #default="{ percentage }">
                  <span class="percentage-value" :data-percentage="diskUsage < 60 ? 'low' : diskUsage < 80 ? 'medium' : 'high'">{{ percentage }}%</span>
                  <span class="percentage-label">ROM占用率</span>
                </template>
              </el-progress>
              <div class="resource-details">
                <div class="detail-item">
                  <span class="detail-label">已用空间</span>
                  <span class="detail-value">{{ ((diskUsage / 100) * 500).toFixed(1) }}GB</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">总空间</span>
                  <span class="detail-value">500GB</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 今日进度 -->
          <div class="resource-card">
            <div class="resource-icon">
              <el-icon><Calendar /></el-icon>
            </div>
            <div class="resource-content">
              <el-progress
                type="dashboard"
                :percentage="currentPercentage"
                :color="colors"
                :width="120"
                :stroke-width="12"
                class="resource-progress"
              >
                <template #default="{ percentage }">
                  <span class="percentage-value" :data-percentage="currentPercentage < 60 ? 'low' : currentPercentage < 80 ? 'medium' : 'high'">{{ percentage }}%</span>
                  <span class="percentage-label">今日</span>
                </template>
              </el-progress>
              <div class="resource-details">
                <div class="detail-item">
                  <span class="detail-label">已过时间</span>
                  <span class="detail-value">{{ (100 - currentPercentage).toFixed(1) }}%</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">剩余时间</span>
                  <span class="detail-value">{{ currentPercentage }}%</span>
                </div>
              </div>
            </div>
          </div>

          <!-- CPU使用率 -->
          <div class="resource-card">
            <div class="resource-icon">
              <el-icon><Cpu /></el-icon>
            </div>
            <div class="resource-content">
              <el-progress
                type="dashboard"
                :percentage="cpuUsage"
                :color="alt_colors"
                :width="120"
                :stroke-width="12"
                class="resource-progress"
              >
                <template #default="{ percentage }">
                  <span class="percentage-value" :data-percentage="cpuUsage < 60 ? 'low' : cpuUsage < 80 ? 'medium' : 'high'">{{ percentage }}%</span>
                  <span class="percentage-label">系统CPU占用率</span>
                </template>
              </el-progress>
              <div class="resource-details">
                <div class="detail-item">
                  <span class="detail-label">核心温度</span>
                  <span class="detail-value">{{ (cpuUsage * 0.8 + 30).toFixed(1) }}°C</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">频率</span>
                  <span class="detail-value">3.2GHz</span>
                </div>
              </div>
            </div>
          </div>

          <!-- GPU使用率 -->
          <div class="resource-card">
            <div class="resource-icon">
              <el-icon><Monitor /></el-icon>
            </div>
            <div class="resource-content">
              <el-progress
                type="dashboard"
                :percentage="gpuUsage"
                :color="alt_colors"
                :width="120"
                :stroke-width="12"
                class="resource-progress"
              >
                <template #default="{ percentage }">
                  <span class="percentage-value" :data-percentage="gpuUsage < 60 ? 'low' : gpuUsage < 80 ? 'medium' : 'high'">{{ percentage }}%</span>
                  <span class="percentage-label">GPU占用率</span>
                </template>
              </el-progress>
              <div class="resource-details">
                <div class="detail-item">
                  <span class="detail-label">显存使用</span>
                  <span class="detail-value">{{ ((gpuUsage / 100) * 8).toFixed(1) }}GB</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">总显存</span>
                  <span class="detail-value">8GB</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
      <template v-else>
        <div class="resource-grid-mobile">
          <!-- 移动端布局 - CPU使用率 -->
          <div class="resource-card">
            <div class="resource-icon">
              <el-icon><Cpu /></el-icon>
            </div>
            <el-progress
              type="dashboard"
              :percentage="cpuUsage"
              :color="alt_colors"
              :width="100"
              :stroke-width="10"
              class="resource-progress"
            >
              <template #default="{ percentage }">
                <span class="percentage-value" :data-percentage="cpuUsage < 60 ? 'low' : cpuUsage < 80 ? 'medium' : 'high'">{{ percentage }}%</span>
                <span class="percentage-label">CPU占用率</span>
              </template>
            </el-progress>
            <div class="detail-mobile">
              <span>核心温度: {{ ((cpuUsage / 100) * 80 + 30).toFixed(1) }}°C</span>
            </div>
          </div>

          <!-- 移动端布局 - GPU使用率 -->
          <div class="resource-card">
            <div class="resource-icon">
              <el-icon><Monitor /></el-icon>
            </div>
            <el-progress
              type="dashboard"
              :percentage="gpuUsage"
              :color="alt_colors"
              :width="100"
              :stroke-width="10"
              class="resource-progress"
            >
              <template #default="{ percentage }">
                <span class="percentage-value" :data-percentage="gpuUsage < 60 ? 'low' : gpuUsage < 80 ? 'medium' : 'high'">{{ percentage }}%</span>
                <span class="percentage-label">GPU占用率</span>
              </template>
            </el-progress>
            <div class="detail-mobile">
              <span>显存使用: {{ ((gpuUsage / 100) * 8).toFixed(1) }}GB/8GB</span>
            </div>
          </div>

          <!-- 移动端布局 - 内存使用率 -->
          <div class="resource-card">
            <div class="resource-icon">
              <el-icon><DataBoard /></el-icon>
            </div>
            <el-progress
              type="dashboard"
              :percentage="memoryUsage"
              :color="alt_colors"
              :width="100"
              :stroke-width="10"
              class="resource-progress"
            >
              <template #default="{ percentage }">
                <span class="percentage-value" :data-percentage="memoryUsage < 60 ? 'low' : memoryUsage < 80 ? 'medium' : 'high'">{{ percentage }}%</span>
                <span class="percentage-label">RAM占用率</span>
              </template>
            </el-progress>
            <div class="detail-mobile">
              <span>内存使用: {{ ((memoryUsage / 100) * 16).toFixed(1) }}GB/16GB</span>
            </div>
          </div>

          <!-- 移动端布局 - 今日进度 -->
          <div class="resource-card">
            <div class="resource-icon">
              <el-icon><Calendar /></el-icon>
            </div>
            <el-progress
              type="dashboard"
              :percentage="currentPercentage"
              :color="colors"
              :width="100"
              :stroke-width="10"
              class="resource-progress"
            >
              <template #default="{ percentage }">
                <span class="percentage-value" :data-percentage="currentPercentage < 60 ? 'low' : currentPercentage < 80 ? 'medium' : 'high'">{{ percentage }}%</span>
                <span class="percentage-label">今日</span>
              </template>
            </el-progress>
            <div class="detail-mobile">
              <span>剩余: {{ currentPercentage }}%</span>
            </div>
          </div>

          <!-- 移动端布局 - 磁盘使用率 -->
          <div class="resource-card">
            <div class="resource-icon">
              <el-icon><DataLine /></el-icon>
            </div>
            <el-progress
              type="dashboard"
              :percentage="diskUsage"
              :color="alt_colors"
              :width="100"
              :stroke-width="10"
              class="resource-progress"
            >
              <template #default="{ percentage }">
                <span class="percentage-value" :data-percentage="diskUsage < 60 ? 'low' : diskUsage < 80 ? 'medium' : 'high'">{{ percentage }}%</span>
                <span class="percentage-label">ROM占用率</span>
              </template>
            </el-progress>
            <div class="detail-mobile">
              <span>存储空间: {{ ((diskUsage / 100) * 500).toFixed(1) }}GB/500GB</span>
            </div>
          </div>
        </div>
      </template>
    </div>

    <MessageCard />
  </div>
</template>

<style scoped>
.statistics-container {
  padding: 30px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(249, 250, 252, 0.9));
  backdrop-filter: blur(15px);
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

.dark-mode {
  background: linear-gradient(135deg, rgba(40, 44, 52, 0.95), rgba(30, 34, 42, 0.9));
}

.statistics-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(circle at 25% 25%, rgba(64, 158, 255, 0.1) 1px, transparent 1px),
    radial-gradient(circle at 75% 75%, rgba(64, 158, 255, 0.05) 1px, transparent 1px);
  background-size: 40px 40px;
  opacity: 0.6;
  z-index: -1;
}

.statistics-container::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(64, 158, 255, 0.03), transparent);
  z-index: -1;
}

.statistics-header {
  margin-bottom: 40px;
  position: relative;
}

.statistics-header::after {
  content: '';
  position: absolute;
  bottom: -15px;
  left: 0;
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, var(--el-color-primary), transparent 80%);
}

.title-wrapper {
  position: relative;
  display: inline-block;
  margin-bottom: 10px;
}

.title {
  font-size: 32px;
  font-weight: 700;
  background: linear-gradient(135deg, var(--el-color-primary), var(--el-color-primary-light-3));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: 1.5px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.title-decoration {
  position: absolute;
  bottom: -6px;
  left: 0;
  width: 60%;
  height: 3px;
  background: linear-gradient(90deg, var(--el-color-primary), transparent 80%);
  border-radius: 3px;
  box-shadow: 0 2px 4px rgba(64, 158, 255, 0.2);
}

.subtitle {
  font-size: 16px;
  color: var(--el-text-color-secondary);
  margin-left: 4px;
  letter-spacing: 0.5px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.basic-stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 30px;
  margin-bottom: 40px;
}

.advanced-stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 30px;
  margin-bottom: 40px;
}

.statistics-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.04), 0 2px 5px rgba(0, 0, 0, 0.05);
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  border: 1px solid rgba(235, 238, 245, 0.8);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  backdrop-filter: blur(5px);
}

.statistics-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, var(--el-color-primary), var(--el-color-primary-light-5));
  border-radius: 4px 4px 0 0;
  transform: translateY(-100%);
  transition: all 0.3s ease;
}

.statistics-card::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(64, 158, 255, 0.05), transparent);
  opacity: 0;
  transition: all 0.3s ease;
}

.statistics-card:hover {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.08), 0 5px 15px rgba(0, 0, 0, 0.05);
}

.statistics-card:hover::before {
  transform: translateY(0);
}

.statistics-card:hover::after {
  opacity: 1;
}

.card-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  border-radius: 12px;
  margin-bottom: 16px;
  background: linear-gradient(135deg, rgba(64, 158, 255, 0.15), rgba(64, 158, 255, 0.05));
  color: var(--el-color-primary);
  font-size: 24px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.1);
}

.statistics-card:hover .card-icon {
  transform: scale(1.1);
  box-shadow: 0 0 20px rgba(64, 158, 255, 0.2);
}

.statistic-item {
  text-align: center;
  width: 100%;
}

.statistic-label {
  font-size: 15px;
  font-weight: 500;
  color: var(--el-text-color-regular);
  margin-bottom: 8px;
  text-align: center;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.time-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 30px;
  margin-bottom: 40px;
}

.time-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.04), 0 2px 5px rgba(0, 0, 0, 0.05);
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  border: 1px solid rgba(235, 238, 245, 0.8);
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  backdrop-filter: blur(5px);
}

.time-card::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(64, 158, 255, 0.05), transparent);
  opacity: 0;
  transition: all 0.3s ease;
}

.time-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.08), 0 5px 15px rgba(0, 0, 0, 0.05);
}

.time-card:hover::after {
  opacity: 1;
}

.time-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, rgba(64, 158, 255, 0.15), rgba(64, 158, 255, 0.05));
  color: var(--el-color-primary);
  border-radius: 50%;
  font-size: 28px;
  margin-bottom: 20px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.1);
}

.time-card:hover .time-icon {
  transform: scale(1.1);
  box-shadow: 0 0 20px rgba(64, 158, 255, 0.2);
}

.time-statistic {
  text-align: center;
  font-size: 24px;
}

.time-label {
  font-size: 16px;
  font-weight: 500;
  color: var(--el-text-color-regular);
  margin-bottom: 10px;
  text-align: center;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.countdown-footer {
  margin-top: 20px;
  text-align: center;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  border-top: 1px dashed rgba(0, 0, 0, 0.08);
  padding-top: 12px;
  width: 100%;
}

.resource-section {
  margin: 40px 0;
}

.section-header {
  margin-bottom: 30px;
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin-bottom: 15px;
  position: relative;
  display: inline-block;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 40px;
  height: 3px;
  background: var(--el-color-primary);
  border-radius: 3px;
  box-shadow: 0 2px 4px rgba(64, 158, 255, 0.2);
}

.section-divider {
  height: 1px;
  width: 100%;
  background: linear-gradient(90deg, rgba(0, 0, 0, 0.05), transparent 80%);
  margin-bottom: 30px;
}

.resource-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 30px;
}

.resource-grid-mobile {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 25px;
}

.resource-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  padding: 30px 20px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.04), 0 2px 5px rgba(0, 0, 0, 0.05);
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  border: 1px solid rgba(235, 238, 245, 0.8);
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  backdrop-filter: blur(5px);
  overflow: hidden;
}

.resource-card::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(64, 158, 255, 0.05), transparent);
  opacity: 0;
  transition: all 0.3s ease;
}

.resource-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.08), 0 5px 15px rgba(0, 0, 0, 0.05);
}

.resource-card:hover::after {
  opacity: 1;
}

.resource-icon {
  position: absolute;
  top: 15px;
  left: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: linear-gradient(135deg, rgba(64, 158, 255, 0.15), rgba(64, 158, 255, 0.05));
  color: var(--el-color-primary);
  font-size: 20px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.1);
}

.resource-card:hover .resource-icon {
  transform: scale(1.1);
  box-shadow: 0 0 20px rgba(64, 158, 255, 0.2);
}

.resource-content {
  position: relative;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.resource-details {
  width: 100%;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  padding: 15px;
  background: rgba(64, 158, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(64, 158, 255, 0.15);
  box-shadow: inset 0 1px 5px rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(5px);
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-label {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  font-weight: 500;
}

.detail-value {
  font-size: 16px;
  font-weight: 600;
  color: var(--el-color-primary);
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.05);
}

.resource-progress {
  position: relative;
  filter: drop-shadow(0 0 6px rgba(64, 158, 255, 0.2));
}

.resource-progress::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 150px;
  height: 150px;
  background: radial-gradient(circle, rgba(64, 158, 255, 0.15) 0%, transparent 70%);
  border-radius: 50%;
  z-index: -1;
  animation: pulse 3s ease-in-out infinite;
}

.resource-progress::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 120px;
  height: 120px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  z-index: -1;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08), inset 0 2px 10px rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(5px);
}

@keyframes pulse {
  0% {
    opacity: 0.4;
    transform: translate(-50%, -50%) scale(0.98);
  }
  50% {
    opacity: 0.6;
    transform: translate(-50%, -50%) scale(1.02);
  }
  100% {
    opacity: 0.4;
    transform: translate(-50%, -50%) scale(0.98);
  }
}

.percentage-value {
  display: block;
  margin-top: 16px;
  font-size: 28px;
  font-weight: 600;
  line-height: 1;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  position: relative;
}

.percentage-value[data-percentage="low"] {
  color: #67C23A;
}

.percentage-value[data-percentage="medium"] {
  color: #E6A23C;
}

.percentage-value[data-percentage="high"] {
  color: #F56C6C;
}

.percentage-label {
  display: block;
  margin-top: 10px;
  font-size: 14px;
  font-weight: 500;
  color: var(--el-text-color-secondary);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  position: relative;
}

.resource-card:hover .resource-progress::before {
  animation-duration: 1.5s;
}

@media (max-width: 1186px) {
  .basic-stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .advanced-stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .basic-stats-grid {
    grid-template-columns: 1fr;
  }
  
  .advanced-stats-grid {
    grid-template-columns: 1fr;
  }
  
  .resource-details {
    grid-template-columns: 1fr;
  }
}

.detail-mobile {
  margin-top: 10px;
  text-align: center;
  color: var(--el-text-color-secondary);
  font-size: 12px;
  width: 100%;
}
</style>