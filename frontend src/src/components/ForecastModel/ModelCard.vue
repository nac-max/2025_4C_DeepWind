<script setup>
import {CircleCheck, Loading, Warning, WarningFilled, WindPower, Plus, Delete, DataLine} from "@element-plus/icons-vue";
import {defineProps, ref, onMounted} from "vue";
import UploadModel from "@/components/ForecastModel/UploadModel.vue";
import AddForecastTask from "@/components/ForecastCenter/AddForecastTask.vue";
import {ElNotification} from "element-plus";

const props = defineProps(
    {
      turbines: {
        type: Array,
        required: true
      }
    }
)

const addModel = ref(false)
const turbine_now = ref("")
const turbineModelDict = ref({})

const currentTurbine = ref("")
const currentModel = ref("")
const addForecastTask = ref(false)

const assembleModel = (data) => {
  for(let index in data) {
    let forecastModel = {};
    forecastModel = data[index].fields;
    forecastModel["model_id"] = data[index].pk;
    forecastModel["delete_visible"] = false;
    if(forecastModel.turbine_id in turbineModelDict.value){
      turbineModelDict.value[forecastModel.turbine_id].push(forecastModel)
    }else{
      turbineModelDict.value[forecastModel.turbine_id] = [forecastModel]
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
const deleteModel = (event, turbine_id, model_id) => {
  let formData = new FormData();
  formData.append("model_id", model_id);
  fetch('/api/delete_forecastModel/', {
    method: 'POST',
    body: formData
  }).then((response) => {
    return response.json()
  }).then((data) => {
    if (data.status === "success") {
      ElNotification({
        title: '成功',
        message: '模型删除成功',
        type: 'success'
      });
    } else {
      ElNotification({
        title: '失败',
        message: '模型删除失败',
        type: 'error'
      });
    }
    turbineModelDict.value[turbine_id] = []
    getForecastModel(null, turbine_id, "all")
  }).catch((e) => {
    console.log("Oops, error", e)
  })
}
const updateTurbineModel = (turbine_id, model_id) => {
  fetch(`/api/get_forecastModel/?turbine_id=${turbine_id}&model_id=${model_id}`, {
  }).then((response) => {
    return response.json()
  }).then((data) => {
    for(let index in data) {
      for(let turbineModel in turbineModelDict.value[turbine_id]){
        if(turbineModelDict.value[turbine_id][turbineModel].model_id === data[index].pk){
          turbineModelDict.value[turbine_id][turbineModel]["model_status"] = data[index].fields["model_status"]
        }
      }
    }
  }).catch((e) => {
    console.log("Oops, error", e)
  })
}

const trainModel = (event, turbine_id, model_id) =>{
  let formData = new FormData();
  formData.append("model_id", model_id);

  let intervalId = setInterval(updateTurbineModel, 2000, turbine_id, model_id)

  fetch('/api/train_forecastModel/', {
    method: 'POST',
    body: formData
  }).then((response) => {
    return response.json()
  }).then((data) => {
    if (data.status === "success") {
      ElNotification({
        title: '成功',
        message: '模型训练完成',
        type: 'success'
      });
    } else {
      ElNotification({
        title: '失败',
        message: '模型训练失败',
        type: 'error'
      });
    }
    clearInterval(intervalId)
    updateModel(null, turbine_id)
  }).catch((e) => {
    console.log("Oops, error", e)
  })
}

const updateModel = (event, turbine_id) => {
  turbineModelDict.value[turbine_id] = []
  getForecastModel(null, turbine_id, "all")
}

onMounted(() => {
  getForecastModel(null, "all")
})

const trainDataList = ref([])
const modelData = ref([])

const assembleData = (data) => {
  trainDataList.value = []
  for(let index in data) {
    let dataModel = {};
    dataModel = data[index].fields;
    dataModel["data_id"] = data[index].pk;
    dataModel["delete_visible"] = false;
    trainDataList.value.push(dataModel);
  }
}
const getTrainData = (event, turbine_id="all", data_type="train") => {
  fetch(`/api/get_turbineData/?turbine_id=${turbine_id}&data_type=${data_type}`, {
  }).then((response) => {
    return response.json()
  }).then((data) => {
    assembleData(data)
  }).catch((e) => {
    console.log("Oops, error", e)
  })
}
const handleChange = (val) => {
  modelData.value = val;
  console.log(modelData.value)
}
const selectAndTrain = (turbine_id, model_id)=>{
  let formData = new FormData();

  let model_data_string = ""
  for(let index in modelData.value){
    model_data_string += modelData.value[index].data_id + ","
  }

  formData.append("model_data", model_data_string);
  formData.append("model_id", model_id);

  fetch(`/api/alter_forecastModel/`, {
    method: 'POST',
    body: formData
  }).then((response) => {
    return response.json()
  }).then((data) => {
    if (data.status === "success") {
      trainModel(null, turbine_id, model_id)
    }
  }).catch((e) => {
    console.log("Oops, error", e)
  })
}

</script>

<template>
  <el-card
      class="box-card"
      v-for="turbine in props.turbines"
      :key="turbine.turbine_id">
    <template #header>
      <div class="card-header">
        <div class="turbine-info">
          <div class="turbine-icon">
            <el-icon><WindPower /></el-icon>
          </div>
          <div class="turbine-details">
            <span class="turbine-name">{{turbine.turbine_name}}</span>
            <el-tag type="info" size="small" class="turbine-id-tag">
              风机号：{{turbine.turbine_id}}
            </el-tag>
          </div>
        </div>
        <div class="action-area">
          <el-button
              size="small"
              type="primary"
              class="add-model-btn"
              @click="
              turbine_now=turbine.turbine_id;
              addModel=true;
              "
          >
            <el-icon class="mr-5"><Plus /></el-icon>
            添加预测模型
          </el-button>
        </div>
      </div>
    </template>
    <div class="card-content">
      <div class="desc">
        <span class="turbine-name">{{ turbine.turbine_name }}</span>

      </div>

      <template v-if="turbineModelDict[turbine.turbine_id] && turbineModelDict[turbine.turbine_id].length > 0">
        <div class="model-list">
          <el-table
              :data="turbineModelDict[turbine.turbine_id]"
              :border="false"
              :stripe="true"
              :header-cell-style="{
                backgroundColor: 'var(--el-color-primary-light-9)',
                color: 'var(--el-color-primary)',
                fontWeight: 'bold'
              }"
              class="model-table"
          >
            <el-table-column label="模型类型" min-width="120">
              <template #default="scope">
                <el-popover
                    v-if="scope.row.model_type === 'MLP'"
                    placement="top-start"
                    title="MLP模型"
                    :width="240"
                    trigger="hover"
                    popper-class="model-popover"
                >
                  <template #reference>
                    <div class="model-type-cell">
                      <el-tag type="info" effect="plain">{{ scope.row.model_type }}</el-tag>
                    </div>
                  </template>
                </el-popover>
                <el-popover
                    v-if="scope.row.model_type === 'GCN+LSTM'"
                    placement="top-start"
                    title="GCN+LSTM模型"
                    :width="240"
                    trigger="hover"
                    popper-class="model-popover"
                >
                  <template #reference>
                    <div class="model-type-cell">
                      <el-tag type="success" effect="plain">{{ scope.row.model_type }}</el-tag>
                    </div>
                  </template>
                </el-popover>
                <el-popover
                    v-if="scope.row.model_type === 'GCN+LSTM+MLP'"
                    placement="top-start"
                    title="GCN+LSTM+MLP模型"
                    :width="240"
                    trigger="hover"
                    popper-class="model-popover"
                >
                  <template #reference>
                    <div class="model-type-cell">
                      <el-tag type="primary" effect="plain">{{ scope.row.model_type }}</el-tag>
                    </div>
                  </template>
                </el-popover>
              </template>
            </el-table-column>
            
            <el-table-column label="模型大小" min-width="100">
              <template #default="scope">
                <div class="model-size-cell">
                  <span>{{ scope.row.model_size }}</span>
                </div>
              </template>
            </el-table-column>
            
            <el-table-column label="模型状态" min-width="140">
              <template #default="scope">
                <div class="model-status-cell">
                  <el-tag
                      v-if="scope.row.model_status === '待训练'"
                      type="warning"
                      effect="dark"
                      class="status-tag"
                  >
                    <el-icon class="mr-5"><Warning /></el-icon>
                    {{ scope.row.model_status }}
                  </el-tag>
                  <el-tag
                      v-else-if="scope.row.model_status === '准备就绪'"
                      type="success"
                      effect="dark"
                      class="status-tag"
                  >
                    <el-icon class="mr-5"><CircleCheck /></el-icon>
                    {{ scope.row.model_status }}
                  </el-tag>
                  <el-tag
                      v-else-if="scope.row.model_status === '未选择数据'"
                      type="warning"
                      effect="dark"
                      class="status-tag"
                  >
                    <el-icon class="mr-5"><Warning /></el-icon>
                    {{ scope.row.model_status }}
                  </el-tag>
                  <el-tag 
                      v-else
                      type="primary"
                      effect="dark"
                      class="status-tag training-status"
                  >
                    <el-icon class="mr-5 is-loading"><Loading /></el-icon>
                    {{ scope.row.model_status }}
                  </el-tag>
                </div>
              </template>
            </el-table-column>
            
            <el-table-column label="模型备注" min-width="180" show-overflow-tooltip>
              <template #default="scope">
                <div class="model-comment-cell">
                  {{ scope.row.model_comment || '无备注' }}
                </div>
              </template>
            </el-table-column>
            
            <el-table-column label="训练时间" min-width="180">
              <template #default="scope">
                <div class="model-time-cell">
                  {{ scope.row.model_trainTime || '尚未训练' }}
                </div>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <div class="operation-area">
                  <div v-if="scope.row.model_status.slice(0,3) === '训练中'" class="training-progress">
                    <div class="progress-info">训练进度</div>
                    <el-progress 
                      :percentage="parseInt(scope.row.model_status.slice(scope.row.model_status.indexOf('...')+3,
                      scope.row.model_status.indexOf('%')))" 
                      :stroke-width="8"
                      status=""
                      :show-text="true"
                      :format="format => `${format}%`"
                      class="progress-bar"
                    />
                  </div>
                  <template v-else>
                    <div class="button-group">
                      <el-button
                          v-if="scope.row.model_status === '准备就绪'"
                          size="small"
                          type="primary"
                          @click="
                          currentTurbine = scope.row.turbine_id;
                          currentModel = scope.row.model_id;
                          addForecastTask = true;"
                          class="predict-btn"
                      >预测</el-button>
                      <template v-else>
                        <el-button
                            v-if="scope.row.model_status === '待训练'"
                            size="small"
                            type="primary"
                            @click="trainModel(null, scope.row.turbine_id, scope.row.model_id)"
                            class="train-btn"
                        >训练
                        </el-button>
                        <el-popover
                            v-else
                            placement="left"
                            :width="450"
                            trigger="click"
                            class="data-popover"
                        >
                          <template #reference>
                            <el-button
                                size="small"
                                type="primary"
                                @click="getTrainData(null, scope.row.turbine_id, 'train')"
                                class="train-btn"
                            >训练
                            </el-button>
                          </template>
                          <template #default>
                            <div class="data-selection">
                              <div class="selection-header">选择训练数据</div>
                              <el-table
                                  :data="trainDataList"
                                  :default-sort="{ prop: 'date_uploadTime', order: 'descending' }"
                                  highlight-current-row
                                  style="width: 100%;"
                                  max-height="300px"
                                  @selection-change="handleChange"
                                  class="selection-table"
                                  :header-cell-style="{
                                    backgroundColor: 'var(--el-color-primary-light-9)', 
                                    color: 'var(--el-color-primary)',
                                    fontSize: '12px'
                                  }"
                              >
                                <el-table-column type="selection" width="40" />
                                <el-table-column property="data_name" label="数据名称" width="120" show-overflow-tooltip></el-table-column>
                                <el-table-column property="data_comment" label="数据备注" width="120" show-overflow-tooltip></el-table-column>
                                <el-table-column property="data_startTime" label="起始时间" width="140" show-overflow-tooltip></el-table-column>
                                <el-table-column property="data_endTime" label="结束时间" width="140" show-overflow-tooltip></el-table-column>
                                <el-table-column property="data_size" label="数据大小" width="90" show-overflow-tooltip/>
                                <el-table-column property="data_uploadTime" label="上传时间" width="140" sortable show-overflow-tooltip></el-table-column>
                              </el-table>
                              <div class="selection-footer">
                                <el-button
                                    type="primary"
                                    size="small"
                                    :disabled="modelData.length === 0"
                                    @click="selectAndTrain(scope.row.turbine_id, scope.row.model_id)"
                                    class="start-train-btn"
                                >开始训练</el-button>
                              </div>
                            </div>
                          </template>
                        </el-popover>
                      </template>
                      <el-popconfirm
                          title="您确定删除此模型? "
                          :icon="WarningFilled"
                          confirm-button-text="确认"
                          cancel-button-text="取消"
                          confirm-button-type="danger"
                          @confirm="deleteModel(null,scope.row.turbine_id, scope.row.model_id)"
                          width="220"
                      >
                        <template #reference>
                          <el-button
                              size="small"
                              type="danger"
                              class="delete-btn"
                          ><el-icon><Delete /></el-icon></el-button>
                        </template>
                      </el-popconfirm>
                    </div>
                  </template>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </template>
      <template v-else>
        <div class="empty-state">
          <el-icon class="empty-icon" :size="48"><DataLine /></el-icon>
          <h3 style="margin-top: 16px; color: var(--el-color-primary); font-size: 18px;">暂无预测模型</h3>
          <p style="margin: 12px 0 24px; color: #909399; font-size: 14px;">该风机尚未添加任何预测模型</p>
          <div @click="turbine_now=turbine.turbine_id; addModel=true;" class="add-empty-btn">
            <span class="btn-shine"></span>
            <el-icon><Plus /></el-icon>
            添加预测模型
          </div>
        </div>
      </template>
    </div>
  </el-card>
  <UploadModel
      v-model="addModel"
      :turbine_id="turbine_now"
      @closeDialog="addModel=false"
      @uploadSuccess="updateModel(null, turbine_now)"
  />
  <AddForecastTask
      v-model="addForecastTask"
      :turbine_id="currentTurbine"
      :model_id="currentModel"
      @closeDialog="addForecastTask=false"
  />
</template>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.box-card {
  margin-bottom: 32px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  overflow: hidden;
}

.box-card:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.turbine-info {
  display: flex;
  align-items: center;
}

.turbine-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  margin-right: 12px;
  background-color: rgba(64, 158, 255, 0.1);
  border-radius: 50%;
  color: var(--el-color-primary);
}

.turbine-details {
  display: flex;
  flex-direction: column;
}

.turbine-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin-bottom: 4px;
}

.turbine-id-tag {
  margin-top: 2px;
  border-radius: 4px;
}

.action-area {
  display: flex;
  align-items: center;
}

.add-model-btn {
  margin-left: auto;
  display: flex;
  align-items: center;
  background: linear-gradient(to right, var(--el-color-primary), var(--el-color-primary-light-3));
  border: none;
  border-radius: 6px;
  color: white;
  padding: 8px 16px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.add-model-btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.2);
}

.mr-5 {
  margin-right: 5px;
}

/* 卡片内容样式 */
.card-content {
  padding: 12px;
}

.model-table {
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 0;
}

.model-table :deep(th.el-table__cell) {
  font-size: 14px;
  padding: 10px 0;
}

.model-table :deep(.el-table__row) {
  transition: all 0.2s ease;
}

.model-table :deep(.el-table__row:hover) {
  background-color: var(--el-color-primary-light-9);
}

/* 单元格样式 */
.model-type-cell,
.model-size-cell,
.model-status-cell,
.model-comment-cell,
.model-time-cell {
  display: flex;
  align-items: center;
  padding: 4px 0;
}

.status-tag {
  display: flex;
  align-items: center;
  padding: 2px 8px;
  border-radius: 4px;
}

/* Popover样式 */
.model-popover {
  max-width: 240px;
  border-radius: 8px;
  overflow: hidden;
}

/* 操作区域样式 */
.operation-area {
  display: flex;
  align-items: center;
  justify-content: center;
}

.training-progress {
  width: 100%;
  background-color: rgba(240, 245, 250, 0.8);
  padding: 10px 14px;
  border-radius: 10px;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(238, 242, 246, 0.95);
  backdrop-filter: blur(5px);
  animation: appearScale 0.4s ease-out;
}

@keyframes appearScale {
  0% {
    opacity: 0;
    transform: scale(0.95);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

.progress-info {
  font-size: 13px;
  font-weight: 600;
  color: var(--el-color-primary);
  margin-bottom: 8px;
  display: flex;
  align-items: center;
}

.progress-info::before {
  content: '';
  display: inline-block;
  width: 8px;
  height: 8px;
  background-color: var(--el-color-success);
  border-radius: 50%;
  margin-right: 8px;
  animation: blink 1.5s infinite;
}

@keyframes blink {
  0% { opacity: 0.4; }
  50% { opacity: 1; }
  100% { opacity: 0.4; }
}

.progress-bar {
  margin-top: 3px;
  position: relative;
}

.progress-bar :deep(.el-progress-bar__inner) {
  background: linear-gradient(to right, var(--el-color-success-light-3), var(--el-color-success));
  transition: width 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
  position: relative;
  overflow: hidden;
}

.progress-bar :deep(.el-progress-bar__inner)::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  animation: shimmer 1.5s infinite;
}

.progress-bar:after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 12px;
  box-shadow: 0 0 8px var(--el-color-success-light-5);
  animation: pulse 2s infinite;
  z-index: -1;
}

@keyframes pulse {
  0% {
    opacity: 0.6;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.02);
  }
  100% {
    opacity: 0.6;
    transform: scale(1);
  }
}

@keyframes shimmer {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

.button-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.predict-btn,
.train-btn {
  border-radius: 6px;
  transition: all 0.2s ease;
}

.predict-btn {
  background: linear-gradient(to right, #13c2c2, #36cfc9);
  border: none;
  color: white;
}

.train-btn {
  background: linear-gradient(to right, var(--el-color-primary), var(--el-color-primary-light-3));
  border: none;
  color: white;
}

.delete-btn {
  border-radius: 6px;
  background: linear-gradient(to right, #ff4d4f, #ff7875);
  border: none;
  color: white;
  padding: 6px 8px;
}

.predict-btn:hover,
.train-btn:hover,
.delete-btn:hover {
  transform: translateY(-1px);
  opacity: 0.9;
}

/* 数据选择区域 */
.data-popover {
  max-width: 450px;
}

.data-selection {
  padding: 10px 0;
}

.selection-header {
  font-size: 15px;
  font-weight: 600;
  color: var(--el-color-primary);
  margin-bottom: 12px;
  padding: 0 10px 10px;
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.selection-table {
  max-height: 300px;
  overflow-y: auto;
}

.selection-footer {
  margin-top: 12px;
  padding: 10px;
  text-align: right;
  border-top: 1px solid var(--el-border-color-lighter);
}

.start-train-btn {
  background: linear-gradient(to right, var(--el-color-primary), var(--el-color-primary-light-3));
  border: none;
  color: white;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.start-train-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  opacity: 0.9;
}

/* 空状态 */
.empty-state {
  padding: 40px 0;
}

.add-empty-btn {
  display: flex;
  align-items: center;
  background: linear-gradient(to right, var(--el-color-primary), var(--el-color-primary-light-3));
  border: none;
  color: white;
  padding: 8px 20px;
  border-radius: 6px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.add-empty-btn:hover {
  transform: translateY(-1px);
  opacity: 0.9;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.2);
}

/* 响应式调整 */
@media (max-width: 992px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .action-area {
    width: 100%;
    justify-content: flex-end;
  }
  
  .model-table {
    overflow-x: auto;
  }
}

.training-status {
  background: linear-gradient(to right, #1890ff, #69c0ff);
  border: none;
  position: relative;
  overflow: hidden;
}

.training-status::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

.progress-bar :deep(.el-progress__text) {
  color: var(--el-color-success);
  font-weight: bold;
  background: -webkit-linear-gradient(120deg, var(--el-color-success), var(--el-color-success-light-3));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-right: 5px;
}

.add-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: 6px;
  background: linear-gradient(to right, var(--el-color-primary), var(--el-color-primary-light-3));
  color: white;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 6px rgba(64, 158, 255, 0.2);
}

.add-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 10px rgba(64, 158, 255, 0.25);
}

.add-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 5px rgba(64, 158, 255, 0.2);
}

.card-content {
  min-height: 300px;
  position: relative;
}

.add-empty-btn {
  position: relative;
  overflow: hidden;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, var(--el-color-primary), var(--el-color-primary-light-3));
  color: white;
  padding: 10px 24px;
  border-radius: 8px;
  font-weight: 500;
  letter-spacing: 0.5px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.25);
  z-index: 1;
}

.add-empty-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(64, 158, 255, 0.35);
}

.add-empty-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.25);
}

.btn-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    to right,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0.4) 50%,
    rgba(255, 255, 255, 0) 100%
  );
  animation: btn-shine 3s infinite;
}

@keyframes btn-shine {
  0% {
    left: -100%;
  }
  20% {
    left: 100%;
  }
  100% {
    left: 100%;
  }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  background: linear-gradient(135deg, rgba(250, 252, 254, 0.7), rgba(245, 247, 250, 0.7));
  border-radius: 12px;
  text-align: center;
  margin: 10px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  border: 2px dashed rgba(64, 158, 255, 0.15);
  overflow: hidden;
  position: relative;
  min-height: 200px;
}

.empty-state::before {
  content: '';
  position: absolute;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(64, 158, 255, 0.05) 0%, transparent 70%);
  animation: pulse 6s infinite cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes pulse {
  0% {
    transform: scale(0.8) rotate(0deg);
    opacity: 0.3;
  }
  50% {
    transform: scale(1.2) rotate(180deg);
    opacity: 0.5;
  }
  100% {
    transform: scale(0.8) rotate(360deg);
    opacity: 0.3;
  }
}

.status-tag {
  display: inline-flex;
  align-items: center;
  padding: 2px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  line-height: 1.6;
  position: relative;
  overflow: hidden;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  border: none !important;
}

:deep(.el-tag.el-tag--warning) {
  background: linear-gradient(to right, #E6A23C, #f0b85d);
  color: white;
}

:deep(.el-tag.el-tag--success) {
  background: linear-gradient(to right, #67C23A, #85ce61);
  color: white;
}

:deep(.el-tag.el-tag--primary) {
  background: linear-gradient(to right, #409EFF, #66b1ff);
  color: white;
}

.predict-btn,
.train-btn,
.delete-btn {
  border-radius: 6px;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.08);
  border: none;
}

.predict-btn {
  background: linear-gradient(to right, #13c2c2, #36cfc9);
  color: white;
}

.train-btn {
  background: linear-gradient(to right, var(--el-color-primary), var(--el-color-primary-light-3));
  color: white;
}

.delete-btn {
  background: linear-gradient(to right, #ff4d4f, #ff7875);
  color: white;
  padding: 6px 8px;
}

.predict-btn:hover,
.train-btn:hover,
.delete-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  opacity: 0.95;
}

.predict-btn:active,
.train-btn:active,
.delete-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.08);
}
</style>