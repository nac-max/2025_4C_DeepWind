<script setup>
import {defineProps, defineEmits, ref} from "vue";
import {CircleCheckFilled, Postcard} from "@element-plus/icons-vue";
import {ElNotification} from "element-plus";
import ResultVisualize from "@/components/ForecastCenter/ResultVisualize.vue";
import ModelTypeTag from "@/components/utils/ModelTypeTag.vue";

const props = defineProps({
  forecast_task_dict: {
    type: Object,
    required: true
  },
  isDark: {
    type: Boolean,
    required: true
  }
})

const emits = defineEmits(['refreshForecastTaskList',
'startForecastTask',])

/** 删除任务 **/
const removeTask = (event, task_id) => {
  let formData = new FormData();
  formData.append('task_id', task_id);
  fetch('/api/delete_forecastTask/', {
    method: 'POST',
    body: formData
  }).then(response => response.json())
      .then(data => {
        if (data.status === "success")
          ElNotification({
                title: '成功',
                message: '预测任务删除成功',
                type: 'success',
              }
          );
        emits('refreshForecastTaskList')
      })
}
/** ******* **/


/** 下载数据 **/
const downloadData = (data_id, data_name) => {
  let formData = new FormData();
  formData.append('data_id', data_id);
  fetch('/api/download_data/', {
    method: 'POST',
    body: formData
  }).then(response => {
    return response.blob()})
      .then(blob => {
        // 创建一个新的Blob对象并创建一个URL来指向它
        const url = window.URL.createObjectURL(blob);

        // 创建一个<a>标签并设置相关属性
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', data_name); // 设置下载的文件名（替换为实际的文件名）

        // 添加<a>标签到文档中，并触发点击事件以下载文件
        document.body.appendChild(link);
        link.click();

        // 清理创建的URL对象
        window.URL.revokeObjectURL(url);
        setTimeout(() => {ElNotification({
          title: '成功',
          message: '开始下载数据',
          type: 'success',
        })}, 400);
      })
      .catch(error => {
        ElNotification({
          title: '失败',
          message: '数据下载失败',
          type: 'error',
        });
      });
}
/** ******* **/


/** 下载结果 **/
const handleDownloadResult = (task_status, result_id, data_name) => {
  if (task_status === '任务完成'){
    if (data_name.includes('in'))
      data_name = data_name.replace('in', 'out')
    else
      data_name = data_name.slice(0, data_name.indexOf('.csv')) + 'out.csv'
    downloadData(result_id, `${data_name}`)
  }
  else {
    ElNotification({
      title: '失败',
      message: '预测任务尚未完成',
      type: 'error',
    })
  }
}
/** ******* **/

/** 可视化结果 **/
const resultVisualize = ref(false)
const currentTask = ref({})
</script>

<template>
  <el-empty v-if="Object.keys(props.forecast_task_dict).length===0" description="暂无任务" class="empty-container" />
  <div 
    v-for="forecast_task in props.forecast_task_dict"
    :key="forecast_task.task_id"
    class="task-card-container">
    <el-card
        class="task-card"
        :class="{ 'completed-task': forecast_task.task_status === '任务完成' }">
      <template #header>
        <div class="card-header">
          <div class="task-info">
            <div class="turbine-icon">
              <img
                  src="../../assets/static/img/turbine_icon.png"
                  alt="风机图标"
              />
            </div>
            <div class="task-meta">
              <div class="meta-row">
                <span class="meta-label">
                  <el-icon><Postcard /></el-icon>所属风机：
                </span>
                <span class="meta-value">{{forecast_task.turbine_id}}</span>
              </div>
              <div class="meta-row">
                <span class="meta-label">预测数据：</span>
                <span class="meta-value">{{forecast_task.data_name}}</span>
              </div>
              <div class="meta-row">
                <span class="meta-label">预测模型：</span>
                <ModelTypeTag :model-type="forecast_task.model_type"/>
              </div>
            </div>
          </div>
          <div class="task-actions">
            <el-button
                type="primary"
                size="small"
                class="action-btn start-btn"
                @click="$emit('startForecastTask', forecast_task.task_id)"
                v-if="forecast_task.task_status === '待预测'"
            >
              <span class="btn-text">开始预测</span>
            </el-button>
            <el-button
                size="small"
                type="primary"
                class="action-btn visualize-btn"
                v-if="forecast_task.task_status === '任务完成'"
                @click="currentTask = forecast_task;resultVisualize = true"
            >
              <span class="btn-text">数据可视化</span>
            </el-button>
            <el-popover :visible="forecast_task.delete_visible" placement="top" popper-class="delete-popover">
              <div class="delete-confirm">
                <div class="delete-title">确定删除任务？</div>
                <div class="delete-warning">警告：操作不可逆</div>
                <div class="delete-actions">
                  <el-button size="small" @click="forecast_task.delete_visible = false">取消</el-button>
                  <el-button size="small" type="danger" @click="removeTask(null, forecast_task.task_id); forecast_task.delete_visible = false">确定</el-button>
                </div>
              </div>
              <template #reference>
                <el-button
                    size="small"
                    class="action-btn delete-btn"
                    @click="forecast_task.delete_visible = true">删除任务</el-button>
              </template>
            </el-popover>
          </div>
        </div>
      </template>
      <div class="card-content">
        <div class="progress-section">
          <div class="progress-container">
            <el-progress 
              v-if="forecast_task.task_status === '待预测'" 
              type="circle" 
              :percentage="0" 
              :stroke-width="10"
              class="task-progress">
              <template #default>
                <div class="progress-info">
                  <span class="percentage-value">0%</span>
                  <span class="percentage-label">{{forecast_task.task_status}}</span>
                </div>
              </template>
            </el-progress>
            <el-progress 
              v-else-if="forecast_task.task_status === '任务完成'"
              type="circle"
              :percentage="100"
              status="success"
              :stroke-width="10"
              class="task-progress"
            >
              <template #default>
                <div class="progress-info">
                  <el-icon size="36" class="success-icon"><CircleCheckFilled /></el-icon>
                  <span class="percentage-label">完成</span>
                </div>
              </template>
            </el-progress>
            <el-progress 
              v-else 
              type="circle" 
              :percentage="Number(forecast_task.task_status.slice(6, forecast_task.task_status.indexOf('%')))" 
              :stroke-width="10"
              class="task-progress">
              <template #default>
                <div class="progress-info">
                  <span class="percentage-value">{{forecast_task.task_status.slice(6)}}</span>
                  <span class="percentage-label">{{forecast_task.task_status.slice(0, 6)}}</span>
                </div>
              </template>
            </el-progress>
          </div>
        </div>
        
        <div class="details-section">
          <div class="details-container">
            <div class="details-row">
              <div class="detail-item">
                <span class="detail-label">任务备注</span>
                <span class="detail-value">{{forecast_task.task_comment || '无'}}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">任务状态</span>
                <span class="detail-value">
                  <el-tag v-if="forecast_task.task_status === '待预测'" class="status-tag" type="warning">{{forecast_task.task_status}}</el-tag>
                  <el-tag v-else-if="forecast_task.task_status === '任务完成'" class="status-tag" type="success">{{forecast_task.task_status}}</el-tag>
                  <el-tag v-else class="status-tag" type="info">{{forecast_task.task_status}}</el-tag>
                </span>
              </div>
            </div>
            <div class="details-row">
              <div class="detail-item">
                <span class="detail-label">预测起始时间</span>
                <span class="detail-value">{{forecast_task.task_startTime}}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">预测结束时间</span>
                <span class="detail-value">{{forecast_task.task_endTime}}</span>
              </div>
            </div>
            <div class="details-row">
              <div class="detail-item">
                <span class="detail-label">任务完成时间</span>
                <span class="detail-value">{{forecast_task.task_finishTime || '尚未完成'}}</span>
              </div>
            </div>
          </div>
          
          <div class="download-section">
            <el-button 
              size="small"
              type="success"
              class="download-btn"
              @click="downloadData(forecast_task.data_id, forecast_task.data_name)">
              下载预测数据
            </el-button>
            <el-button
              size="small"
              type="success"
              class="download-btn"
              :disabled="forecast_task.task_status !== '任务完成'"
              @click="handleDownloadResult(forecast_task.task_status, forecast_task.result_id, forecast_task.data_name)">
              下载预测结果
            </el-button>
          </div>
        </div>
      </div>
    </el-card>
  </div>
  
  <ResultVisualize
    v-model="resultVisualize"
    :forecast-task="currentTask"
    @closeDialog="resultVisualize = false"
    :is-dark="isDark"
  />
</template>

<style scoped>
/* 全局布局和主题变量 */
:root {
  --primary-color: #409eff;
  --success-color: #67c23a;
  --warning-color: #e6a23c;
  --danger-color: #f56c6c;
  --text-primary: #303133;
  --text-regular: #606266;
  --text-secondary: #909399;
  --border-color: #e4e7ed;
  --border-light: #f2f6fc;
  --card-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  --card-radius: 12px;
  --transition-time: 0.3s;
}

/* 空状态美化 */
.empty-container {
  padding: 32px;
  background: #f9fafc;
  border-radius: var(--card-radius);
  margin-bottom: 24px;
  box-shadow: var(--card-shadow);
}

/* 任务卡片容器 */
.task-card-container {
  margin-bottom: 32px;
  transition: transform var(--transition-time);
}

.task-card-container:hover {
  transform: translateY(-2px);
}

/* 任务卡片 */
.task-card {
  border-radius: var(--card-radius);
  overflow: hidden;
  box-shadow: var(--card-shadow);
  transition: all var(--transition-time);
  background-color: #ffffff;
}

.task-card:deep(.el-card__header) {
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-light);
  background: linear-gradient(to right, #f5f7fa, #ffffff);
}

.task-card:deep(.el-card__body) {
  padding: 0;
}

.completed-task {
  border-left: 4px solid var(--success-color);
}

/* 卡片头部 */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.task-info {
  display: flex;
  gap: 16px;
  align-items: center;
}

.turbine-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 24px;
  overflow: hidden;
  background-color: rgba(64, 158, 255, 0.1);
  padding: 3px;
}

.turbine-icon img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.task-meta {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.meta-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.meta-label {
  color: var(--text-secondary);
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.meta-value {
  color: var(--text-primary);
  font-weight: 500;
  font-size: 14px;
}

.task-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  border-radius: 6px;
  transition: all var(--transition-time);
}

.action-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.start-btn {
  background: linear-gradient(45deg, #409eff, #79bbff);
  border: none;
}

.visualize-btn {
  background: linear-gradient(45deg, #409eff, #53a8ff);
  border: none;
}

.delete-btn {
  opacity: 0.8;
}

.delete-btn:hover {
  opacity: 1;
}

.btn-text {
  font-weight: 500;
}

/* 卡片内容 */
.card-content {
  display: flex;
  background-color: #ffffff;
}

/* 进度部分 */
.progress-section {
  width: 25%;
  padding: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-right: 1px dashed var(--border-color);
}

.progress-container {
  width: 100%;
  display: flex;
  justify-content: center;
}

.task-progress {
  --el-progress-circle-radius: 50px;
}

.progress-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.percentage-value {
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.2;
}

.percentage-label {
  margin-top: 4px;
  font-size: 14px;
  color: var(--text-secondary);
}

.success-icon {
  color: var(--success-color);
  margin-bottom: 4px;
}

/* 详情部分 */
.details-section {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.details-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.details-row {
  display: flex;
  gap: 24px;
}

.detail-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-label {
  font-size: 13px;
  color: var(--text-secondary);
}

.detail-value {
  font-size: 14px;
  color: var(--text-primary);
}

.status-tag {
  font-weight: 500;
}

/* 下载部分 */
.download-section {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.download-btn {
  border-radius: 6px;
  transition: all var(--transition-time);
}

.download-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 删除确认弹窗 */
:deep(.delete-popover) {
  padding: 12px;
  border-radius: 8px;
}

.delete-confirm {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.delete-title {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 14px;
}

.delete-warning {
  color: var(--danger-color);
  font-size: 12px;
  margin-bottom: 8px;
}

.delete-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

/* 深色模式适配 */
:deep(.dark) .task-card {
  background-color: #1f2937;
  border-color: #374151;
}

:deep(.dark) .task-card:deep(.el-card__header) {
  background: linear-gradient(to right, #1a2234, #1f2937);
  border-color: #374151;
}

:deep(.dark) .meta-label,
:deep(.dark) .detail-label {
  color: #9ca3af;
}

:deep(.dark) .meta-value,
:deep(.dark) .detail-value {
  color: #e5e7eb;
}

:deep(.dark) .turbine-icon {
  background-color: rgba(64, 158, 255, 0.2);
}

:deep(.dark) .empty-container {
  background-color: #1f2937;
}

/* 响应式优化 */
@media (max-width: 768px) {
  .card-header {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }
  
  .task-actions {
    justify-content: flex-end;
  }
  
  .card-content {
    flex-direction: column;
  }
  
  .progress-section {
    width: 100%;
    border-right: none;
    border-bottom: 1px dashed var(--border-color);
    padding: 16px;
  }
  
  .details-row {
    flex-direction: column;
    gap: 12px;
  }
}
</style>