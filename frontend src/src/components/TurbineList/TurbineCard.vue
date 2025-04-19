<template>
  <div class="turbine-card-container">
    <el-empty 
      v-if="props.turbines.length===0" 
      description="暂无数据"
      :image-size="120"
      class="empty-state" 
    />
    <el-card 
      v-for="turbine in props.turbines" 
      :key="turbine.turbine_id"
      class="box-card" 
      :class="{'dark-mode': props.isDark, 'active-card': realtimeForecast[turbine.turbine_id]}"
      shadow="hover"
    >
      <template #header>
        <div class="card-header">
          <div class="turbine-info">
            <div class="turbine-icon">
              <img
                src="../../assets/static/img/turbine_icon.png"
                class="turbine-image"
              />
            </div>
            <div class="turbine-title">
              <div class="turbine-name">
                <el-icon><WindPower /></el-icon>
                <span>{{turbine.turbine_name}}</span>
              </div>
              <div class="turbine-id">ID: {{turbine.turbine_id}}</div>
            </div>
          </div>
          <div class="action-buttons">
            <el-button
              size="small"
              type="primary"
              class="forecast-button"
              @click="addForecastTask=true; currentTurbine=turbine.turbine_id"
              :icon="Document"
            >
              下达预测任务
            </el-button>
            <el-popover 
              :visible="turbine.delete_visible" 
              placement="top" 
              :width="240"
              transition="el-zoom-in-top"
            >
              <div class="delete-confirm">
                <div class="delete-icon">
                  <el-icon><Warning /></el-icon>
                </div>
                <p class="delete-title">确定删除风机？</p>
                <p class="delete-desc">风机的所有数据及模型将被清除。</p>
                <div class="delete-actions">
                  <el-button size="small" @click="turbine.delete_visible = false">取消</el-button>
                  <el-button 
                    size="small" 
                    type="danger" 
                    @click="removeTurbine(turbine.turbine_id); turbine.delete_visible = false"
                  >
                    确定
                  </el-button>
                </div>
              </div>
              <template #reference>
                <el-button 
                  size="small" 
                  class="delete-button"
                  @click="turbine.delete_visible = true"
                  :icon="Delete"
                >
                  删除风机
                </el-button>
              </template>
            </el-popover>
          </div>
        </div>
      </template>
      
      <div class="turbine-details">
        <div class="detail-row">
          <div class="detail-item">
            <span class="detail-label">风机号：</span>
            <span class="detail-value">{{turbine.turbine_id}}</span>
          </div>
          <div class="detail-divider"></div>
          
          <div class="detail-item">
            <span class="detail-label">风机备注：</span>
            <span class="detail-value">{{turbine.turbine_comment}}</span>
          </div>
          <div class="detail-divider"></div>
          
          <div class="detail-item">
            <span class="detail-label">风机状态：</span>
            <el-tag class="status-tag" type="success" effect="light">正常</el-tag>
          </div>
          <div class="detail-divider"></div>
          
          <div class="detail-item">
            <span class="detail-label">风机模型：</span>
            <div class="model-tags">
              <template v-if="turbine.turbine_id in turbineModelDict">
                <ModelTypeTag
                  v-if="turbineModelDict[turbine.turbine_id]['MLP']"
                  model-type="MLP"
                  :model-status="turbineModelDict[turbine.turbine_id]['MLP']['model_status']"
                />
                <ModelTypeTag
                  v-if="turbineModelDict[turbine.turbine_id]['GCN+LSTM']"
                  model-type="GCN+LSTM"
                  :model-status="turbineModelDict[turbine.turbine_id]['GCN+LSTM']['model_status']"
                />
                <ModelTypeTag
                  v-if="turbineModelDict[turbine.turbine_id]['GCN+LSTM+MLP']"
                  model-type="GCN+LSTM+MLP"
                  :model-status="turbineModelDict[turbine.turbine_id]['GCN+LSTM+MLP']['model_status']"
                />
              </template>
              <template v-else>
                <span class="no-model">暂无模型</span>
              </template>
            </div>
          </div>
        </div>
      </div>
      
      <div class="realtime-section">
        <div class="realtime-divider">
          <el-popover
            trigger="hover"
            title="实时功率预测"
            width="280"
            placement="top"
            transition="el-zoom-in-top"
            popper-class="realtime-popover"
          >
            <template #reference>
              <div class="realtime-switch-wrapper">
                <el-switch
                  v-model="realtimeForecast[turbine.turbine_id]"
                  :is-loading="realtimeChangeLoading[turbine.turbine_id]"
                  inline-prompt
                  :before-change="()=>{
                    realtimeChangeLoading[turbine.turbine_id]= false
                    if(turbine.turbine_id in turbineModelDict){
                      realtimeChangeLoading[turbine.turbine_id]= true
                      if(turbineModelDict[turbine.turbine_id]['MLP']['model_status'] === '准备就绪') {
                        realtimeChangeLoading[turbine.turbine_id]= false
                        return true
                      }
                      else {
                        ElMessage({
                          message: '该风机无训练完成的MLP模型，无法开启实时预测',
                          type: 'warning'
                        });
                        realtimeChangeLoading[turbine.turbine_id]= false
                        return false
                      }
                    }
                    ElMessage({
                        message: '该风机无训练完成的MLP模型，无法开启实时预测',
                        type: 'warning'
                      });
                    realtimeChangeLoading[turbine.turbine_id]= false
                    return false
                  }"
                  active-text="24小时实时功率预测"
                  inactive-text="关闭实时预测"
                  class="realtime-switch"
                />
              </div>
            </template>
            <div class="popover-content">
              <p class="popover-description">在当前时间点，根据未来24小时的天气预报数据，预测风机功率。</p>
              <div class="popover-requirement">
                <span>该功能需要风机具有</span>
                <ModelTypeTag
                  v-if="turbine.turbine_id in turbineModelDict && 'MLP' in turbineModelDict[turbine.turbine_id]"
                  model-type="MLP"
                  :model-status="turbineModelDict[turbine.turbine_id]['MLP']['model_status']"
                />
                <ModelTypeTag
                  v-else
                  model-type="MLP"
                  model-status="未添加"
                />
                <span>模型</span>
              </div>
            </div>
          </el-popover>
        </div>
        
        <div 
          class="chart-container" 
          v-if="realtimeForecast[turbine.turbine_id]"
          :class="{'chart-active': realtimeForecast[turbine.turbine_id]}"
        >
          <ChartVisualize
            :is-dark="props.isDark"
            :turbine-id="turbine.turbine_id"
          />
        </div>
      </div>
    </el-card>
  </div>
  
  <AddForecastTask
    v-model="addForecastTask"
    :turbine_id="currentTurbine"
    @closeDialog="addForecastTask = false"
  />
</template>

<style scoped>
.turbine-card-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.box-card {
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.05);
  margin-bottom: 24px;
  background: linear-gradient(145deg, var(--el-bg-color), var(--el-bg-color-overlay));
  position: relative;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.box-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #9254de, #409EFF, #67C23A, #E6A23C);
  opacity: 0.8;
  animation: gradient 3.5s ease infinite;
  background-size: 300% 300%;
}

.box-card::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
  pointer-events: none;
}

.box-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.dark-mode {
  background: linear-gradient(145deg, var(--el-bg-color-overlay), var(--el-bg-color));
  border: 1px solid rgba(255, 255, 255, 0.05);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.dark-mode:hover {
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.25);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}

.turbine-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.turbine-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(64, 158, 255, 0.1), rgba(64, 158, 255, 0.2));
  border-radius: 12px;
  padding: 10px;
  height: 48px;
  width: 48px;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.1);
  animation: subtlePulse 3.5s ease-in-out infinite;
  backdrop-filter: blur(5px);
}

.turbine-image {
  height: 32px;
  transition: all 0.3s ease;
}

.box-card:hover .turbine-image {
  transform: rotate(15deg);
}

.turbine-title {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.turbine-name {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  background: linear-gradient(90deg, var(--el-text-color-primary), var(--el-color-primary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.turbine-id {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  opacity: 0.8;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.forecast-button {
  border-radius: 8px;
  transition: all 0.3s ease;
  background: linear-gradient(135deg, var(--el-color-primary), var(--el-color-primary-light-3));
  border: none;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.2);
}

.forecast-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(64, 158, 255, 0.3);
}

.delete-button {
  border-radius: 8px;
  transition: all 0.3s ease;
  background: linear-gradient(135deg, var(--el-color-danger), var(--el-color-danger-light-3));
  border: none;
  box-shadow: 0 4px 12px rgba(245, 108, 108, 0.2);
}

.delete-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(245, 108, 108, 0.3);
}

.delete-confirm {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 0;
}

.delete-icon {
  font-size: 24px;
  color: var(--el-color-danger);
  margin-bottom: 8px;
}

.delete-title {
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--el-text-color-primary);
}

.delete-desc {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  margin-bottom: 16px;
  text-align: center;
}

.delete-actions {
  display: flex;
  justify-content: flex-end;
  width: 100%;
  gap: 8px;
}

.turbine-details {
  padding: 16px 0;
}

.detail-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.detail-item {
  display: flex;
  align-items: center;
  margin-right: 0;
}

.detail-label {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  white-space: nowrap;
}

.detail-value {
  font-size: 14px;
  color: var(--el-text-color-primary);
}

.status-tag {
  height: 24px;
  border-radius: 4px;
  padding: 0 10px;
  background: rgba(103, 194, 58, 0.15);
  border: 1px solid var(--el-color-success);
  color: var(--el-color-success);
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(103, 194, 58, 0.1);
  backdrop-filter: blur(5px);
}

.detail-divider {
  width: 1px;
  height: 20px;
  background: linear-gradient(to bottom, transparent, var(--el-border-color-lighter), transparent);
  margin: 0 12px;
}

.model-tags {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
}

.no-model {
  font-size: 13px;
  color: var(--el-text-color-secondary);
  font-style: italic;
}

.realtime-section {
  margin-top: 8px;
}

.realtime-divider {
  text-align: center;
  margin: 16px 0;
  position: relative;
}

.realtime-divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background-color: var(--el-border-color-light);
  z-index: 0;
}

.realtime-switch-wrapper {
  position: relative;
  z-index: 1;
  display: inline-block;
  background: linear-gradient(135deg, var(--el-bg-color), var(--el-bg-color-overlay));
  padding: 0 16px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid var(--el-border-color-light);
}

.realtime-switch {
  display: flex;
  align-items: center;
}

.popover-content {
  padding: 8px 0;
}

.popover-description {
  margin-bottom: 12px;
  font-size: 14px;
  line-height: 1.5;
  color: var(--el-text-color-primary);
}

.popover-requirement {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-wrap: wrap;
  font-size: 13px;
  color: var(--el-text-color-secondary);
}

.chart-container {
  overflow: hidden;
  margin-top: 16px;
  border-radius: 8px;
  border: 1px solid var(--el-border-color-light);
  background: linear-gradient(145deg, var(--el-bg-color-overlay), var(--el-bg-color));
  transition: max-height 0.5s ease, opacity 0.5s ease;
  max-height: 0;
  opacity: 0;
  backdrop-filter: blur(10px);
}

.chart-active {
  max-height: 500px;
  opacity: 1;
  padding: 16px;
  box-shadow: inset 0 0 20px rgba(64, 158, 255, 0.1);
}

.empty-state {
  padding: 40px 0;
  border-radius: 12px;
  background: linear-gradient(145deg, var(--el-bg-color-overlay), var(--el-bg-color));
  border: 2px dashed var(--el-border-color);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  backdrop-filter: blur(10px);
}

.active-card {
  border-color: var(--el-color-primary-light-7);
  box-shadow: 0 0 30px rgba(64, 158, 255, 0.2);
  animation: subtlePulse 3.5s ease-in-out infinite;
}

/* 添加动画效果 */
@keyframes gradient {
  0% {
    background-position: 0% 50%;
  }
  25% {
    background-position: 50% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  75% {
    background-position: 50% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

@keyframes subtlePulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.02);
  }
  100% {
    transform: scale(1);
  }
}

/* 响应式调整 */
@media (max-width: 768px) {
  .box-card::before {
    height: 3px;
  }
  
  .turbine-icon {
    height: 40px;
    width: 40px;
  }
  
  .turbine-name {
    font-size: 16px;
  }
}
</style>

<script setup>
import {defineProps, defineEmits, ref, onMounted} from 'vue'
import {WindPower, Delete, Document, Warning} from "@element-plus/icons-vue";
import {ElMessage, ElNotification} from "element-plus";
import ModelTypeTag from "@/components/utils/ModelTypeTag.vue";
import AddForecastTask from "@/components/ForecastCenter/AddForecastTask.vue";
import ChartVisualize from "@/components/utils/ChartVisualize.vue";

const currentTurbine = ref("")
const addForecastTask = ref(false)
const emit = defineEmits(['removeTurbine'])
const realtimeForecast = ref({})
const realtimeChangeLoading = ref({})

const props = defineProps(
    {
      turbines: {
        type: Array,
        required: true
      },
      isDark: {
        type: Boolean,
        required: true
      }
    }
)

const checkRealtimeForecast = ref([])

const removeTurbine = (turbine_id) => {
  let formData = new FormData();
  formData.append('turbine_id', turbine_id);
  fetch('/api/delete_turbine/', {
    method: 'POST',
    body: formData
  }).then(response => response.json())
    .then(data => {
        if (data.status === "success")
          ElNotification({
            title: '成功',
            message: '风机删除成功',
            type: 'success',
          });
          emit('removeTurbine');
      })
}

const turbineModelDict = ref({})
const assembleModel = (data) => {
  for(let index in data) {
    let forecastModel = {};
    forecastModel = data[index].fields;
    if (!(forecastModel.turbine_id in turbineModelDict.value))
      turbineModelDict.value[forecastModel.turbine_id] = {};
    if (!(forecastModel.model_type in turbineModelDict.value[forecastModel.turbine_id]))
      turbineModelDict.value[forecastModel.turbine_id][forecastModel.model_type] = {};
    if (turbineModelDict.value[forecastModel.turbine_id][forecastModel.model_type]["model_status"] !== "准备就绪")
      turbineModelDict.value[forecastModel.turbine_id][forecastModel.model_type]["model_status"] = forecastModel.model_status;
  }
  for(let key in turbineModelDict.value){
    if(turbineModelDict.value[key]['MLP']["model_status"] === "准备就绪"){
      realtimeForecast.value[key] = true
    }
    else {
      realtimeForecast.value[key] = false
    }
  }
}
const getForecastModel = (event, turbine_id="all", model_id="all") => {

  fetch(`/api/get_forecastModel/?turbine_id=${turbine_id}&model_id=${model_id}`, {
  }).then((response) => {
    return response.json()
  }).then((data) => {
    assembleModel(data)
  }).catch((e) => {
    console.log("Oops, error", e)
  })
}

onMounted(() => {
  getForecastModel(null, "all")
  for(let index in props.turbines){
    let turbineId = props.turbines[index].turbine_id

    realtimeChangeLoading.value[turbineId] = false
    checkRealtimeForecast.value[turbineId] = () => {
      console.log(turbineModelDict.value[turbineId]['MLP']['model_status'])
      realtimeChangeLoading.value[turbineId ]= true
      if(turbineModelDict.value[turbineId]['MLP']['model_status'] === '准备就绪') {
        realtimeChangeLoading.value[turbineId]= false
        return true
      }
      else {
        ElMessage({
          message: '该风机无训练完成的MLP模型，无法开启实时预测',
          type: 'warning'
        });
        realtimeChangeLoading.value[turbineId]= false
        return false
      }
    }
  }
})
</script>