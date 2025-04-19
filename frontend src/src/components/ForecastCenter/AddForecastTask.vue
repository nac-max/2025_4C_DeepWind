<script setup>
import {defineProps,defineEmits, reactive, ref, onMounted} from "vue";
import UploadTurbineData from "@/components/ForecastCenter/UploadTurbineData.vue";
import {ElMessage, ElNotification} from "element-plus";

const formLabelWidth = '100px'
const addTurbineData = ref(false)
const taskForm = reactive({
  turbine_id: "",
  model_id:"",
  forecast_data:[],
  task_comment:"",
  date_range: {},
  startTime: {},
  endTime: {},
})

const props = defineProps({
  turbine_id : {
    type: String||Number,
  },
  model_id : {
    type: String||Number,
  },
})

const emit = defineEmits(['closeDialog', 'refreshTaskList'])
const dateRangeDict = ref({})
const timeRangeDict = ref({})
// 获取风机信息
const turbines = ref([])
const turbineModelList = ref([])

const assembleTurbine = (data) => {
  turbines.value = []
  let turbineModel = "1";
  for (turbineModel in data) {
    let turbine = {};
    turbine["turbine_name"] = data[turbineModel].fields.turbine_name;
    turbine["turbine_id"] = data[turbineModel].pk
    turbine["turbine_comment"] = data[turbineModel].fields.turbine_comment;
    turbine["status"] = data[turbineModel].fields.turbine_status;
    turbine["delete_visible"] = false;
    turbines.value.push(turbine);
  }
}

const getTurbine = () => {
  fetch('/api/get_turbine/')
      .then(response => {
        return response.json()
      })
      .then((data) => {
        assembleTurbine(data)
      })
      .catch(e => console.log("Oops, error", e))
}
/** **************** **/


/** 当对话框打开或关闭时，分别获取风机、清空表单 **/
const handleClose = () => {
  refreshForm()
  emit("closeDialog")
}

const handleOpen = () => {
  getTurbine()
  if(props.turbine_id !== undefined) {
    taskForm.turbine_id = props.turbine_id
    getTurbineModel(props.turbine_id)
    getForecastData(null, props.turbine_id, "forecast")
    if(props.model_id !== undefined) {
      taskForm.model_id = props.model_id
    }
  }

}
/** **************** **/


/** 从预测数据列表中删除预测数据 **/
const removeData = (data_id) => {
  let formData = new FormData();
  formData.append('data_id', data_id);
  fetch('/api/delete_data/', {
    method: 'POST',
    body: formData
  }).then(response => response.json())
      .then(data => {
        if (data.status === "success")
          ElNotification({
                title: '成功',
                message: '数据删除成功',
                type: 'success',
              }
          );
        getForecastData(null, taskForm.turbine_id, "train");
        emit('removeData');
      })
}
/** **************** **/

/** 以下函数当在输入框中确定风机号会进行调用，分别获取风机预测模型信息和风机预测数据信息 **/
/*** 获取风机预测模型信息 ***/
const assembleModel = (data) => {
  turbineModelList.value = []
  for(let index in data) {
    let forecastModel = {};
    forecastModel = data[index].fields;
    forecastModel["model_id"] = data[index].pk;
    forecastModel["delete_visible"] = false;
    turbineModelList.value.push(forecastModel);
  }
}
const getTurbineModel = (turbine_id) => {
  fetch(`/api/get_forecastModel/?turbine_id=${turbine_id}&model_id=all`, {
  }).then((response) => {
    return response.json()
  }).then((data) => {
    assembleModel(data)
  }).catch((e) => {
    console.log("Oops, error", e)
  })
}
/*** **************** ***/

const dateToString = (date) => {
  return date.getFullYear() + "-" + (date.getMonth() + 1).toString().padStart(2, '0') + "-" + date.getDate().toString().padStart(2, '0')
}

/*** 获取风机预测数据信息 ***/
const forecastDataList = ref([])
const assembleData = (data) => {
  forecastDataList.value = []
  for(let index in data) {
    let dataModel = {};
    dataModel = data[index].fields;
    dataModel["data_id"] = data[index].pk;
    dataModel["delete_visible"] = false;

    let start_time = dataModel["data_startTime"]
    let end_time = dataModel["data_endTime"]

    let tmpStartTime = new Date(end_time)
    tmpStartTime =  tmpStartTime.getTime() - (1 * 24 * 60 * 60 * 1000);
    tmpStartTime = new Date(tmpStartTime)
    tmpStartTime = dateToString(tmpStartTime)

    taskForm.date_range[dataModel['data_id']] =
        [tmpStartTime, end_time.slice(0,end_time.indexOf(' '))]

    dateRangeDict.value[dataModel['data_id']] =
        [start_time.slice(0,start_time.indexOf(' ')),
          end_time.slice(0,end_time.indexOf(' '))]

    start_time = new Date(start_time)
    end_time = new Date(end_time)

    taskForm.startTime[dataModel['data_id']] = "05:00"
    taskForm.endTime[dataModel['data_id']] =
        end_time.getHours().toString().padStart(2, '0') + ":" + end_time.getMinutes().toString().padStart(2, '0')
    timeRangeDict.value[dataModel['data_id']] =
        [start_time.getHours().toString().padStart(2, '0') + ":" + start_time.getMinutes().toString().padStart(2, '0'),
        end_time.getHours().toString().padStart(2, '0') + ":" + end_time.getMinutes().toString().padStart(2, '0'),]


    disabledDate_Fun_Dict.value[dataModel['data_id']] = (time) => {
      return !(time.getTime() >= start_time.getTime() &&
          time.getTime() <= end_time.getTime() &&
          time.getMinutes() % 15 === 0 && time.getSeconds() === 0);

    }
    forecastDataList.value.push(dataModel);
  }
}
const getForecastData = (event, turbine_id="all", data_type="forecast") => {
  fetch(`/api/get_turbineData/?turbine_id=${turbine_id}&data_type=${data_type}`, {
  }).then((response) => {
    return response.json()
  }).then((data) => {
    assembleData(data)
  }).catch((e) => {
    console.log("Oops, error", e)
  })
}
const handleTurbineChange = (val) => {
  getTurbineModel(val)
  getForecastData(null, val, "forecast")
}
const handleCurrentChange = (val) => {
  taskForm.forecast_data = val
}
/*** **************** ***/
/** **************** **/


/** 上传风机表单至后端 **/
const uploadTaskForm = () => {
  // 检查表单
  if(taskForm.turbine_id === ""){
    ElMessage({
      message: '请选择预测风机',
      type: 'error',
    })
    return
  }
  if(taskForm.model_id === ""){
    ElMessage({
      message: '请选择预测模型',
      type: 'error',
    })
    return
  }
  if(taskForm.forecast_data.length === 0){
    ElMessage({
      message: '请选择预测数据',
      type: 'error',
    })
    return
  }
  // 上传表单
  let formData = new FormData();
  formData.append('turbine_id', taskForm.turbine_id);
  formData.append('model_id', taskForm.model_id);
  formData.append('task_comment', taskForm.task_comment);
  let index = 0;
  for (;index < taskForm.forecast_data.length - 1; index++) {

    let data_id = taskForm.forecast_data[index]['data_id']

    formData.set('data_id', data_id)

    let startTime = new Date(taskForm.date_range[data_id][0])
    let endTime = new Date(taskForm.date_range[data_id][1])

    startTime = startTime.getFullYear() + "-" + (startTime.getMonth()+1).toString().padStart(2, '0') + "-" +
        startTime.getDate().toString().padStart(2, '0') + " " + taskForm.startTime[data_id]+":00"
    endTime = endTime.getFullYear() + "-" + (endTime.getMonth()+1).toString().padStart(2, '0') + "-" +
        endTime.getDate().toString().padStart(2, '0') + " " + taskForm.endTime[data_id]+":00"

    formData.set('task_startTime', startTime);
    formData.set('task_endTime', endTime);

    fetch('/api/add_forecastTask/', {
      method: 'POST',
      body: formData
    })

  }
  let data_id = taskForm.forecast_data[index]['data_id']

  formData.set('data_id', data_id)

  let startTime = new Date(taskForm.date_range[data_id][0])
  let endTime = new Date(taskForm.date_range[data_id][1])

  startTime = startTime.getFullYear() + "-" + (startTime.getMonth()+1).toString().padStart(2, '0') + "-" +
      startTime.getDate().toString().padStart(2, '0') + " " + taskForm.startTime[data_id]+":00"
  endTime = endTime.getFullYear() + "-" + (endTime.getMonth()+1).toString().padStart(2, '0') + "-" +
      endTime.getDate().toString().padStart(2, '0') + " " + taskForm.endTime[data_id]+":00"

  formData.set('task_startTime', startTime);
  formData.set('task_endTime', endTime);

  fetch('/api/add_forecastTask/', {
    method: 'POST',
    body: formData
  }).then(response => response.json())
      .then(data => {
        if (data.status === "success"){
          ElNotification({
                title: '成功',
                message: '任务添加成功',
                type: 'success'
              }
          );
        }
        refreshForm()
        emit('refreshTaskList')
        emit('closeDialog')
      })
}

/** **************** **/


/** 判断日期是被禁用的函数组 **/
const disabledDate_Fun_Dict = ref({})
/** **************** **/
const refreshForm = () =>{
  taskForm.turbine_id = ""
  taskForm.model_id = ""
  taskForm.forecast_data = []
  taskForm.task_comment = ""
  taskForm.date_range = {}
  taskForm.startTime = {}
  taskForm.endTime = {}
  dateRangeDict.value = {}
  timeRangeDict.value = {}
  turbineModelList.value = []
  forecastDataList.value = []
}
</script>

<template>
  <el-dialog 
    title="添加预测任务" 
    @open="handleOpen" 
    width="720px"
    class="forecast-task-dialog"
    destroy-on-close>
    <div class="dialog-content">
      <el-form :model="taskForm" label-position="top">
        <div class="form-section">
          <h3 class="section-title">基本信息</h3>
          <div class="form-grid">
            <el-form-item label="预测风机" class="form-item">
              <el-select
                v-model="taskForm.turbine_id"
                collapse-tags
                collapse-tags-tooltip
                placeholder="请选择预测风机"
                class="custom-select"
                @change="handleTurbineChange">
                <el-option
                  v-for="turbine in turbines"
                  :key="turbine.turbine_id"
                  :value="turbine.turbine_id"
                  :label="turbine.turbine_id" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="预测模型" class="form-item">
              <el-select
                v-model="taskForm.model_id"
                placeholder="请选择预测模型"
                class="custom-select">
                <el-popover
                  v-for="turbineModel in turbineModelList"
                  :key="turbineModel.model_id"
                  placement="top-start"
                  title="模型信息"
                  :width="240"
                  trigger="hover"
                  popper-class="model-popover">
                  <template #reference>
                    <el-option
                      :label="turbineModel.model_type"
                      :value="turbineModel.model_id"
                      :disabled="turbineModel.model_status !== '准备就绪'"
                      class="model-option" />
                  </template>
                  <div class="model-info">
                    <div class="info-item">
                      <span class="info-label">模型备注:</span>
                      <span class="info-value">{{turbineModel.model_comment}}</span>
                    </div>
                    <div class="info-item">
                      <span class="info-label">训练时间:</span>
                      <span class="info-value">{{turbineModel.model_trainTime}}</span>
                    </div>
                  </div>
                </el-popover>
              </el-select>
            </el-form-item>
          </div>
          
          <el-form-item label="任务备注" class="form-item full-width">
            <el-input
              v-model="taskForm.task_comment"
              placeholder="请输入任务备注"
              class="custom-input" />
          </el-form-item>
        </div>
        
        <div class="form-section">
          <div class="section-header">
            <h3 class="section-title">预测数据</h3>
            <el-button
              type="primary"
              size="small"
              class="upload-btn"
              @click="addTurbineData = true">
              <i class="el-icon-upload"></i>
              上传新数据
            </el-button>
          </div>
          
          <el-table
            ref="TableRef"
            :data="forecastDataList"
            :default-sort="{ prop: 'date_uploadTime', order: 'descending' }"
            highlight-current-row
            class="custom-table"
            @selection-change="handleCurrentChange">
            <el-table-column type="selection" width="55" />
            <el-table-column property="data_name" label="数据名称"></el-table-column>
            <el-table-column property="data_comment" label="数据备注"></el-table-column>
            <el-table-column property="data_startTime" label="起始时间"></el-table-column>
            <el-table-column property="data_endTime" label="结束时间"></el-table-column>
            <el-table-column property="data_size" label="数据大小" width="120" />
            <el-table-column property="data_uploadTime" label="上传时间" sortable></el-table-column>
            <el-table-column label="操作">
              <template #default="scope">
                <el-popover 
                  :visible="scope.row.delete_visible" 
                  placement="top" 
                  :width="180"
                  popper-class="delete-popover">
                  <div class="delete-confirm">
                    <div class="delete-title">
                      <i class="el-icon-warning"></i> 确定删除数据？
                    </div>
                    <div class="delete-warning">警告：操作不可逆</div>
                    <div class="delete-actions">
                      <el-button size="small" @click="scope.row.delete_visible = false">取消</el-button>
                      <el-button 
                        size="small" 
                        type="danger" 
                        @click="removeData(scope.row.data_id); scope.row.delete_visible = false">
                        确定
                      </el-button>
                    </div>
                  </div>
                  <template #reference>
                    <el-button 
                      @click="scope.row.delete_visible = true" 
                      type="danger"
                      size="small"
                      class="delete-btn">
                      删除
                    </el-button>
                  </template>
                </el-popover>
              </template>
            </el-table-column>
          </el-table>
        </div>
        
        <div v-if="taskForm.forecast_data.length > 0" class="form-section">
          <h3 class="section-title">预测配置</h3>
          <div v-for="item in taskForm.forecast_data" :key="item['data_id']" class="data-config-item">
            <div class="data-header">
              <div class="data-title">{{ item['data_name'] }}</div>
            </div>
            
            <div class="data-config-grid">
              <el-form-item label="预测区间" class="form-item">
                <el-date-picker
                  v-model="taskForm.date_range[item['data_id']]"
                  type="daterange"
                  range-separator="至"
                  start-placeholder="起始日期"
                  clearable
                  unlink-panels
                  :default-value="taskForm.date_range[item['data_id']][1]"
                  :disabled-date="disabledDate_Fun_Dict[item['data_id']]"
                  end-placeholder="结束日期"
                  class="custom-date-picker" />
              </el-form-item>
              
              <el-form-item label="起止时间" class="form-item">
                <div class="time-selector">
                  <el-time-select
                    start="00:00"
                    end="23:45"
                    v-model="taskForm.startTime[item['data_id']]"
                    placeholder="起始时间"
                    clearable
                    step="00:15"
                    class="time-input" />
                    
                  <div class="time-separator">至</div>
                  
                  <el-time-select
                    start="00:00"
                    end="23:45"
                    v-model="taskForm.endTime[item['data_id']]"
                    placeholder="结束时间"
                    step="00:15"
                    clearable
                    class="time-input" />
                </div>
              </el-form-item>
            </div>
          </div>
        </div>
      </el-form>
    </div>
    
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose" class="cancel-btn">取消</el-button>
        <el-button type="primary" @click="uploadTaskForm" class="confirm-btn">添加任务</el-button>
      </div>
    </template>
    
    <UploadTurbineData 
      v-model="addTurbineData"
      :turbine_id="taskForm.turbine_id"
      @closeDialog="addTurbineData = false"
      @uploadSuccess="addTurbineData = false; getForecastData(null, taskForm.turbine_id, 'forecast')" />
  </el-dialog>
</template>

<style scoped>
.forecast-task-dialog :deep(.el-dialog__body) {
  padding: 0 24px;
}

.forecast-task-dialog :deep(.el-dialog__header) {
  padding: 20px 24px;
  margin: 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.forecast-task-dialog :deep(.el-dialog__title) {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.forecast-task-dialog :deep(.el-dialog__footer) {
  padding: 16px 24px;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
}

.dialog-content {
  padding: 16px 0;
  max-height: 65vh;
  overflow-y: auto;
}

.form-section {
  margin-bottom: 24px;
  padding: 20px;
  background-color: #f9fafb;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 16px 0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-item {
  margin-bottom: 16px;
}

.full-width {
  grid-column: span 2;
}

.custom-select,
.custom-input,
.custom-date-picker {
  width: 100%;
  border-radius: 6px;
}

.custom-select :deep(.el-input__wrapper),
.custom-input :deep(.el-input__wrapper),
.custom-date-picker :deep(.el-input__wrapper) {
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06);
  border-radius: 6px;
}

.custom-table {
  margin-top: 8px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.custom-table :deep(.el-table__header-wrapper th) {
  background-color: #f5f7fa;
  color: #606266;
  font-weight: 600;
}

.data-config-item {
  background-color: white;
  border-radius: 6px;
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.data-config-item:last-child {
  margin-bottom: 0;
}

.data-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px dashed rgba(0, 0, 0, 0.1);
}

.data-title {
  font-weight: 600;
  color: #409EFF;
  font-size: 15px;
}

.data-config-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.time-selector {
  display: flex;
  align-items: center;
}

.time-input {
  width: 45%;
}

.time-separator {
  margin: 0 12px;
  color: #909399;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.cancel-btn {
  border-radius: 6px;
}

.confirm-btn {
  border-radius: 6px;
  padding: 9px 20px;
}

.upload-btn {
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.delete-btn {
  padding: 6px 12px;
  border-radius: 4px;
}

.delete-confirm {
  padding: 6px;
}

.delete-title {
  font-weight: 600;
  font-size: 14px;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 6px;
  color: #f56c6c;
}

.delete-warning {
  font-size: 12px;
  color: #909399;
  margin-bottom: 12px;
}

.delete-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.model-info {
  padding: 8px 4px;
}

.info-item {
  margin-bottom: 8px;
  font-size: 13px;
}

.info-label {
  font-weight: 600;
  color: #606266;
  margin-right: 4px;
}

.info-value {
  color: #303133;
}

/* 为按钮添加过渡动画 */
.confirm-btn,
.cancel-btn,
.upload-btn,
.delete-btn {
  transition: all 0.3s ease;
}

.confirm-btn:hover,
.upload-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.2);
}

.delete-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(245, 108, 108, 0.2);
}

/* 添加响应式布局 */
@media (max-width: 768px) {
  .form-grid, 
  .data-config-grid {
    grid-template-columns: 1fr;
  }
  
  .time-selector {
    flex-direction: column;
    align-items: stretch;
  }
  
  .time-input {
    width: 100%;
    margin-bottom: 8px;
  }
  
  .time-separator {
    margin: 8px 0;
    text-align: center;
  }
}
</style>