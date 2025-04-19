<template>
  <el-empty v-if="props.dataList.length===0"
            description="暂无数据"
            class="empty-container">
    <template #image>
      <el-icon class="empty-icon"><WindPower /></el-icon>
    </template>
  </el-empty>
  <transition-group name="card-fade">
    <template v-for="turbineData in dataList" :key="turbineData.name">
      <el-card v-if="turbineData.data_type !== 'result'"
               class="box-card"
               :class="{ 'dark-card': props.isDark }">
        <div class="card-badge" :class="{'train-badge': turbineData.data_type === 'train', 'forecast-badge': turbineData.data_type === 'forecast'}"></div>
        <template #header>
          <div class="card-header">
            <div class="card-title">
              <el-icon class="icon-document"><Document /></el-icon>
              <span class="data-name">{{ turbineData.data_name }}</span>
              <el-divider direction="vertical" class="divider"/>
              <span class="text-item">所属风机：<span class="highlight-text">{{ turbineData.turbine_id }}</span></span>
              <el-divider direction="vertical" class="divider"/>
              <span class="text-item" v-if="turbineData.data_type === 'train'">
                数据类型：<el-tag effect="dark" type="success" class="custom-tag">训练数据</el-tag>
              </span>
              <span class="text-item" v-if="turbineData.data_type === 'forecast'">
                数据类型：<el-tag effect="dark" class="custom-tag">预测数据</el-tag>
              </span>
              <span class="text-item" v-if="turbineData.data_type === 'result'">
                数据类型：<el-tag effect="dark" class="ml-2 custom-tag" type="success">预测结果</el-tag>
              </span>
            </div>
            <div class="button-group">
              <div class="custom-btn visualize-btn" @click="currentData = turbineData; dataVisualize = true;">
                <div class="btn-content">
                  <span class="btn-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16">
                      <path fill="currentColor" d="M4 4h4v4H4V4zm0 6h4v4H4v-4zm0 6h4v4H4v-4zm6-12h4v4h-4V4zm0 6h4v4h-4v-4zm0 6h4v4h-4v-4zm6-12h4v4h-4V4zm0 6h4v4h-4v-4zm0 6h4v4h-4v-4z"/>
                    </svg>
                  </span>
                  <span class="btn-label">数据可视化</span>
                </div>
                <div class="btn-shine"></div>
              </div>
              <el-popover :visible="turbineData.delete_visible"
                          placement="top"
                          :width="220"
                          popper-class="delete-popover">
                <div class="delete-confirm">
                  <el-icon class="warning-icon"><Warning /></el-icon>
                  <p class="confirm-title">确定删除数据？</p>
                  <p class="confirm-subtitle">警告：操作不可逆</p>
                  <div class="confirm-buttons">
                    <el-button size="small"
                               class="cancel-btn"
                               @click="turbineData.delete_visible = false">取消</el-button>
                    <el-button size="small"
                               type="danger"
                               class="confirm-btn"
                               @click="removeData(turbineData.data_id); turbineData.delete_visible = false">
                      确定
                    </el-button>
                  </div>
                </div>
                <template #reference>
                  <div class="custom-btn delete-btn" @click="turbineData.delete_visible = true">
                    <div class="btn-content">
                      <span class="btn-icon">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16">
                          <path fill="currentColor" d="M7 4V2h10v2h5v2h-2v15a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V6H2V4h5zM6 6v14h12V6H6zm3 3h2v8H9V9zm4 0h2v8h-2V9z"/>
                        </svg>
                      </span>
                      <span class="btn-label">删除数据</span>
                    </div>
                    <div class="btn-shine"></div>
                  </div>
                </template>
              </el-popover>
            </div>
          </div>
        </template>
        <div class="card-content">
          <div class="info-section">
            <div class="info-item">
              <div class="info-icon-container">
                <el-icon class="info-icon"><Calendar /></el-icon>
              </div>
              <div class="info-text">
                <span class="info-label">上传时间</span>
                <span class="info-value">{{ turbineData.data_uploadTime }}</span>
              </div>
            </div>
            <div class="info-item">
              <div class="info-icon-container">
                <el-icon class="info-icon"><Timer /></el-icon>
              </div>
              <div class="info-text">
                <span class="info-label">起始时间</span>
                <span class="info-value">{{ turbineData.data_startTime }}</span>
              </div>
            </div>
            <div class="info-item">
              <div class="info-icon-container">
                <el-icon class="info-icon"><Timer /></el-icon>
              </div>
              <div class="info-text">
                <span class="info-label">结束时间</span>
                <span class="info-value">{{ turbineData.data_endTime }}</span>
              </div>
            </div>
            <div class="info-item">
              <div class="info-icon-container">
                <el-icon class="info-icon"><Files /></el-icon>
              </div>
              <div class="info-text">
                <span class="info-label">文件大小</span>
                <span class="info-value">{{ turbineData.data_size }}</span>
              </div>
            </div>
          </div>
          <div class="action-section">
            <div class="custom-btn download-btn" @click="downloadData(turbineData.data_id, turbineData.data_name)">
              <div class="btn-content">
                <span class="btn-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16">
                    <path fill="currentColor" d="M12 15.575a1 1 0 0 1-.706-.291l-4.287-4.193a1 1 0 0 1 1.395-1.436L12 13.179l3.598-3.524a1 1 0 1 1 1.395 1.436l-4.287 4.193a1 1 0 0 1-.706.291zM12 16c.5 0 1-.4 1-1V4c0-.6-.5-1-1-1s-1 .4-1 1v11c0 .6.5 1 1 1zm10 4v1c0 .6-.4 1-1 1H3c-.6 0-1-.4-1-1v-1c0-.6.4-1 1-1h18c.6 0 1 .4 1 1z"/>
                  </svg>
                </span>
                <span class="btn-label">下载数据</span>
              </div>
              <div class="btn-shine"></div>
            </div>
          </div>
        </div>
      </el-card>
    </template>
  </transition-group>
  <DataVisualize
      v-model="dataVisualize"
      :dataInfo="currentData"
      :isDark="props.isDark"
  />
</template>

<style scoped>
:root {
  --primary-gradient: linear-gradient(135deg, #4d83fb, #3655b3);
  --success-gradient: linear-gradient(135deg, #67c23a, #409d2c);
}

.empty-container {
  margin: 80px 0;
  opacity: 0.8;
}

.empty-icon {
  font-size: 80px;
  color: var(--el-color-primary);
  opacity: 0.6;
  margin-bottom: 20px;
}

/* 卡片动画 */
.card-fade-enter-active,
.card-fade-leave-active {
  transition: all 0.5s ease;
}

.card-fade-enter-from,
.card-fade-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

.box-card {
  margin-bottom: 32px;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.07);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  border: none;
  overflow: hidden;
  position: relative;
  background-image: linear-gradient(to right, rgba(240, 245, 255, 0.5), rgba(255, 255, 255, 0.8));
}

.box-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 15px 35px rgba(32, 107, 228, 0.1);
}

.card-badge {
  position: absolute;
  top: 0;
  right: 0;
  width: 80px;
  height: 80px;
  overflow: hidden;
  pointer-events: none;
}

.card-badge::before {
  content: '';
  position: absolute;
  top: -10px;
  right: -10px;
  width: 40px;
  height: 40px;
  transform: rotate(45deg);
}

.train-badge::before {
  background: var(--success-gradient);
  box-shadow: 0 0 10px rgba(103, 194, 58, 0.5);
}

.forecast-badge::before {
  background: var(--primary-gradient);
  box-shadow: 0 0 10px rgba(64, 158, 255, 0.5);
}

.dark-card {
  background-image: linear-gradient(to right, rgba(30, 30, 40, 0.95), rgba(25, 25, 35, 0.9));
  color: #e1e1e1;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.dark-card:hover {
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.35);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0;
  position: relative;
}

.card-title {
  display: flex;
  align-items: center;
  font-size: 15px;
  flex-wrap: wrap;
}

.icon-document {
  margin-right: 10px;
  font-size: 20px;
  color: var(--el-color-primary);
  background-color: rgba(64, 158, 255, 0.1);
  padding: 8px;
  border-radius: 8px;
}

.data-name {
  font-weight: 600;
  margin-right: 10px;
  color: var(--el-color-primary);
  font-size: 16px;
  letter-spacing: 0.5px;
}

.divider {
  margin: 0 12px;
  height: 16px;
}

.text-item {
  display: flex;
  align-items: center;
  white-space: nowrap;
  margin-right: 12px;
  padding: 4px 0;
}

.highlight-text {
  font-weight: 600;
  margin-left: 4px;
  color: var(--el-color-success);
}

.custom-tag {
  margin-left: 4px;
  font-weight: 500;
  border-radius: 6px;
  padding: 0 10px;
  height: 24px;
  line-height: 24px;
}

.button-group {
  display: flex;
  gap: 8px;
}

.custom-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0 14px;
  height: 32px;
  min-width: 80px;
  border-radius: 6px;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  color: white;
  font-size: 13px;
  font-weight: 500;
  user-select: none;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
}

.visualize-btn {
  background-image: linear-gradient(135deg, rgba(77, 131, 251, 0.95), rgba(54, 85, 179, 0.95));
  border: 1px solid rgba(77, 131, 251, 0.2);
}

.download-btn {
  background-image: linear-gradient(135deg, rgba(103, 194, 58, 0.95), rgba(64, 157, 44, 0.95));
  border: 1px solid rgba(103, 194, 58, 0.2);
}

.delete-btn {
  background-image: linear-gradient(135deg, rgba(245, 108, 108, 0.95), rgba(212, 59, 59, 0.95));
  border: 1px solid rgba(245, 108, 108, 0.2);
}

.custom-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.visualize-btn:hover {
  background-image: linear-gradient(135deg, rgba(90, 143, 255, 0.95), rgba(64, 101, 201, 0.95));
}

.download-btn:hover {
  background-image: linear-gradient(135deg, rgba(116, 207, 71, 0.95), rgba(77, 175, 58, 0.95));
}

.delete-btn:hover {
  background-image: linear-gradient(135deg, rgba(255, 126, 126, 0.95), rgba(224, 76, 76, 0.95));
}

.custom-btn:active {
  transform: translateY(0);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.btn-shine {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 40%;
  background: linear-gradient(to bottom, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0) 100%);
  border-radius: 6px 6px 0 0;
  pointer-events: none;
}

.btn-content {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  width: 100%;
  height: 100%;
}

.btn-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 14px;
  height: 14px;
  filter: drop-shadow(0 1px 1px rgba(0,0,0,0.05));
}

.btn-label {
  display: inline-block;
  white-space: nowrap;
  letter-spacing: 0.3px;
  text-shadow: 0 1px 1px rgba(0,0,0,0.05);
  font-weight: 500;
}

.card-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  position: relative;
}

.info-section {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  text-align: left;
}

.info-item {
  display: flex;
  align-items: center;
  background-color: rgba(240, 245, 255, 0.6);
  padding: 10px 16px;
  border-radius: 10px;
  transition: all 0.2s ease;
}

.dark-card .info-item {
  background-color: rgba(55, 55, 65, 0.5);
}

.info-item:hover {
  background-color: rgba(230, 238, 255, 0.8);
  transform: translateY(-2px);
}

.dark-card .info-item:hover {
  background-color: rgba(60, 60, 70, 0.7);
}

.info-icon-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background-color: rgba(64, 158, 255, 0.1);
  margin-right: 12px;
}

.info-icon {
  color: var(--el-color-primary);
  font-size: 18px;
}

.info-text {
  display: flex;
  flex-direction: column;
}

.info-label {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  margin-bottom: 4px;
}

.info-value {
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.3px;
}

.action-section {
  padding-left: 20px;
}

@media (max-width: 768px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }

  .card-title {
    flex-wrap: wrap;
    gap: 12px;
  }

  .button-group {
    align-self: flex-end;
  }

  .card-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
  }

  .action-section {
    padding-left: 0;
    align-self: flex-end;
  }

  .info-section {
    width: 100%;
  }

  .info-item {
    flex: 1 1 calc(50% - 10px);
    min-width: 220px;
  }
}

/* 确认弹窗样式 */
.delete-confirm {
  text-align: center;
  padding: 16px;
}

.warning-icon {
  color: var(--el-color-danger);
  font-size: 32px;
  margin-bottom: 12px;
}

.confirm-title {
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--el-color-danger);
  font-size: 16px;
}

.confirm-subtitle {
  font-size: 14px;
  opacity: 0.8;
  margin-bottom: 20px;
}

.confirm-buttons {
  display: flex;
  justify-content: center;
  gap: 12px;
}

.cancel-btn, .confirm-btn {
  padding: 8px 20px;
  border-radius: 6px;
}
</style>

<script setup>
import { defineProps, defineEmits, ref } from 'vue';
import { Document, DataAnalysis, Delete, Calendar, Timer, Files, Download, Warning, WindPower } from "@element-plus/icons-vue";
import { ElNotification } from "element-plus";
import DataVisualize from "@/components/DataSpace/DataVisualize.vue";

const props = defineProps({
  dataList: {
    type: Array,
    required: true
  },
  isDark: {
    type: Boolean,
    required: true
  }
});

const emit = defineEmits(['removeData', 'closeDialog']);
const currentData = ref({});
const dataVisualize = ref(false);

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
            message: '风机删除成功',
            type: 'success',
          });
        emit('removeData');
      });
};

const downloadData = (data_id, data_name) => {
  let formData = new FormData();
  formData.append('data_id', data_id);
  fetch('/api/download_data/', {
    method: 'POST',
    body: formData
  }).then(response => {
    return response.blob();
  })
      .then(blob => {
        // 创建一个新的Blob对象并创建一个URL来指向它
        const url = window.URL.createObjectURL(blob);

        // 创建一个<a>标签并设置相关属性
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', data_name);

        // 添加<a>标签到文档中，并触发点击事件以下载文件
        document.body.appendChild(link);
        link.click();

        // 清理创建的URL对象
        window.URL.revokeObjectURL(url);
        setTimeout(() => {
          ElNotification({
            title: '成功',
            message: '开始下载数据',
            type: 'success',
          });
        }, 400);
      })
      .catch(error => {
        ElNotification({
          title: '失败',
          message: '数据下载失败',
          type: 'error',
        });
      });
};
</script>