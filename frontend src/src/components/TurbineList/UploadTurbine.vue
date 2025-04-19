<script setup>

import {CollectionTag, Memo, Postcard, UploadFilled} from "@element-plus/icons-vue";
import {reactive, ref, defineEmits} from "vue";
import {ElMessageBox} from "element-plus";

const emit = defineEmits(['closeDialog', 'uploadSuccess'])

const turbineForm = reactive({
  turbine_name: '',
  turbine_id: '',
  turbine_comment: '',
  model_type: [],
  model_type_string: '',
})

const data_form = ref(null)
const uploadData = ref({
  data_type: "train",
  turbine_id: "id",
  data_comment: ""
})

const turbine = ref(null)
const fileList = ref([])
const uploadFileUrl = ref("/api/upload_data/")

const formLabelWidth = '72px'

const beforeRemove = (file, fileList) => {
  return ElMessageBox.confirm(
      `取消上传 ${file.name} ?`
  ).then(
      () => {
        return true
      },
      () => {
        return false
      }
  )
}

const uploadTurbine = () => {
  uploadData.value.turbine_id = turbineForm.turbine_id;
  data_form.value.submit();

  let modelType = '';
  for (modelType in turbineForm.model_type) {
    turbineForm.model_type_string += turbineForm.model_type[modelType] + ',';
  }

  let formData = new FormData();
  formData.append('turbine_id', turbineForm.turbine_id);
  formData.append('turbine_name', turbineForm.turbine_name);
  formData.append('turbine_comment', turbineForm.turbine_comment);
  formData.append('model_type', turbineForm.model_type_string);

  fetch("/api/add_turbine/", {
    method: 'POST',
    body: formData
  }).then((response) => {
    return response.json()
  }).then((data) => {
    if (data.status === "success")
     emit('uploadSuccess')
  }).catch((e) => {
    console.log("Oops, error", e)
  })

  fileList.value = [];
  turbineForm.turbine_id = '';
  turbineForm.turbine_name = '';
  turbineForm.turbine_comment = '';
  turbineForm.model_type = [];
  turbineForm.model_type_string = '';
}
</script>

<template>
  <el-dialog 
    title="风机信息" 
    width="560px"
    :close-on-click-modal="false"
    destroy-on-close
    class="turbine-upload-dialog"
  >
    <div class="dialog-header">
      <div class="header-icon">
        <el-icon><UploadFilled /></el-icon>
      </div>
      <h3 class="header-title">添加新风机</h3>
      <p class="header-desc">请填写风机信息并上传训练数据</p>
    </div>
    
    <el-form :model="turbineForm" ref="turbine" class="turbine-form">
      <el-form-item label="风机名称" :label-width="formLabelWidth">
        <el-input
          v-model="turbineForm.turbine_name"
          placeholder="请输入风机名称"
          autocomplete="off"
          class="custom-input">
          <template #append>
            <el-icon><Postcard /></el-icon>
          </template>
        </el-input>
      </el-form-item>
      
      <el-form-item label="风机号" :label-width="formLabelWidth">
        <el-input 
          v-model="turbineForm.turbine_id" 
          placeholder="请输入风机ID"
          autocomplete="off"
          class="custom-input">
          <template #append>
            <el-icon><CollectionTag /></el-icon>
          </template>
        </el-input>
      </el-form-item>
      
      <el-form-item label="风机备注" :label-width="formLabelWidth">
        <el-input 
          v-model="turbineForm.turbine_comment" 
          placeholder="请输入备注信息（选填）"
          autocomplete="off"
          class="custom-input">
          <template #append>
            <el-icon><Memo /></el-icon>
          </template>
        </el-input>
      </el-form-item>
      
      <el-form-item label="模型类型" :label-width="formLabelWidth">
        <el-select
            v-model="turbineForm.model_type"
            collapse-tags
            multiple
            placeholder="请选择预测模型"
            collapse-tags-tooltip
            class="model-select"
        >
          <el-option
              key="MLP"
              label="仅需未来天气数据 (MLP)"
              value="MLP"
          />
          <el-option
              key="GCN+LSTM"
              label="仅需风机前24小时的历史数据 (GCN+LSTM)"
              value="GCN+LSTM"
          />
          <el-option
              key="GCN+LSTM+MLP"
              label="同时使用历史数据和未来天气数据 (GCN+LSTM+MLP)"
              value="GCN+LSTM+MLP"
          />
        </el-select>
      </el-form-item>
      
      <el-form-item label="训练数据" :label-width="formLabelWidth" class="upload-item">
        <el-upload
            ref="data_form"
            drag
            multiple
            method="POST"
            :data="uploadData"
            :action="uploadFileUrl"
            :before-remove="beforeRemove"
            v-model:file-list="fileList"
            :auto-upload="false"
            class="custom-upload"
        >
          <div class="upload-content">
            <el-icon class="upload-icon"><upload-filled /></el-icon>
            <div class="upload-text">
              拖动或<em>点击上传</em>
            </div>
            <div class="upload-tip">
              请上传含有风机数据的csv、xlxs文件
            </div>
          </div>
        </el-upload>
      </el-form-item>
    </el-form>
    
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="$emit('closeDialog')" class="cancel-button">取消</el-button>
        <el-button type="primary" @click="uploadTurbine" class="submit-button">
          <el-icon class="submit-icon"><UploadFilled /></el-icon>
          上传风机
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>
.turbine-upload-dialog :deep(.el-dialog__header) {
  margin-right: 0;
  text-align: center;
  padding: 0;
}

.turbine-upload-dialog :deep(.el-dialog__headerbtn) {
  top: 16px;
  right: 16px;
  width: 32px;
  height: 32px;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 50%;
  z-index: 10;
}

.turbine-upload-dialog :deep(.el-dialog__body) {
  padding: 0 24px 24px;
}

.dialog-header {
  background: linear-gradient(135deg, var(--el-color-primary-light-7), var(--el-color-primary-light-9));
  padding: 24px;
  border-radius: 8px 8px 0 0;
  text-align: center;
  margin-bottom: 24px;
  position: relative;
}

.header-icon {
  background: var(--el-color-primary);
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  font-size: 24px;
  color: white;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.2);
}

.header-title {
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 8px;
  color: var(--el-text-color-primary);
}

.header-desc {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  margin: 0;
}

.turbine-form {
  padding: 0 12px;
}

.turbine-form :deep(.el-form-item) {
  margin-bottom: 24px;
}

.turbine-form :deep(.el-form-item__label) {
  font-weight: 500;
  color: var(--el-text-color-primary);
}

.custom-input {
  border-radius: 8px;
  overflow: hidden;
}

.custom-input :deep(.el-input__wrapper) {
  box-shadow: 0 0 0 1px var(--el-border-color) inset;
}

.custom-input:hover :deep(.el-input__wrapper) {
  box-shadow: 0 0 0 1px var(--el-color-primary-light-5) inset;
}

.model-select {
  width: 100%;
  border-radius: 8px;
}

.model-select :deep(.el-input__wrapper) {
  box-shadow: 0 0 0 1px var(--el-border-color) inset;
}

.model-select:hover :deep(.el-input__wrapper) {
  box-shadow: 0 0 0 1px var(--el-color-primary-light-5) inset;
}

.upload-item {
  margin-bottom: 0 !important;
}

.custom-upload {
  width: 100%;
}

.custom-upload :deep(.el-upload-dragger) {
  width: 100%;
  border-radius: 8px;
  border: 2px dashed var(--el-border-color);
  background: rgba(64, 158, 255, 0.02);
  transition: all 0.3s;
}

.custom-upload :deep(.el-upload-dragger:hover) {
  border-color: var(--el-color-primary);
  background: rgba(64, 158, 255, 0.05);
}

.upload-content {
  padding: 24px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.upload-icon {
  font-size: 40px;
  color: var(--el-color-primary);
  margin-bottom: 16px;
}

.upload-text {
  margin-bottom: 8px;
  color: var(--el-text-color-primary);
}

.upload-text em {
  font-style: normal;
  color: var(--el-color-primary);
  font-weight: 500;
}

.upload-tip {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.dialog-footer {
  padding-top: 24px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.cancel-button {
  border-radius: 8px;
}

.submit-button {
  border-radius: 8px;
  background: linear-gradient(135deg, var(--el-color-primary), var(--el-color-primary-light-3));
  border: none;
  padding: 8px 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.2);
}

.submit-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(64, 158, 255, 0.3);
}

.submit-icon {
  font-size: 16px;
}
</style>