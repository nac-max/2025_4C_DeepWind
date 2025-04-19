<script setup>
import {ref, onMounted} from 'vue'
import {Calendar, Document, User} from "@element-plus/icons-vue";
import {ElNotification} from "element-plus";

const addGuestbook = ref(false)
const guestbookList = ref([])
const guestbookForm = ref({
  guest_name: '',
  guest_comment: ''
})

const submitGuestbook = () => {
  let formData = new FormData()

  formData.append('guest_name', guestbookForm.value.guest_name)
  formData.append('guest_comment', guestbookForm.value.guest_comment)

  fetch("/api/add_guestbook/", {
    method: 'POST',
    body: formData
  }).then(response => response.json())
      .then(data => {
        if (data.status === "success"){
          ElNotification({
            title: '成功',
            message: '留言成功 ;)',
            type: 'success',
          });
          getGuestbook()
        }
      })
      .catch(e => console.log("Oops, error", e))

}
const assembleMessage = (data) => {
  guestbookList.value = []
  for (let index in data) {
    let message = {}
    message = data[index].fields
    message.id = data[index].pk
    guestbookList.value.push(message)
  }
}
const getGuestbook = () => {
  fetch('/api/get_guestbook/')
      .then(response => {
        return response.json()
      })
      .then((data) => {
        assembleMessage(data)
      })
      .catch(e => console.log("Oops, error", e))
}

onMounted(() => {
  getGuestbook()
  }
)
</script>

<template>
  <div class="message-board-container">
    <div class="board-header">
      <h2 class="board-title">留言板</h2>
      <div class="board-decoration"></div>
      <p class="board-subtitle">分享您的想法和建议</p>
      
      <el-button
        class="add-message-btn"
        @click="addGuestbook = true"
        type="primary"
      >
        <el-icon><Document /></el-icon>
        <span>添加留言</span>
      </el-button>
    </div>
    
    <transition-group name="message-list" tag="div" class="messages-container">
      <el-empty
        v-if="guestbookList.length===0"
        description="暂无留言"
        :image-size="120"
        class="empty-state"
      >
        <template #description>
          <p class="empty-description">还没有留言，成为第一个留言的人吧！</p>
        </template>
      </el-empty>
      
      <div 
        v-for="guestbook in guestbookList"
        :key="guestbook.id"
        class="message-card-wrapper"
      >
        <el-card class="message-card" shadow="hover">
          <div class="card-content">
            <div class="user-info">
              <div class="avatar-container">
                <img
                  src="../../assets/static/img/turbine_icon.png"
                  alt="User Avatar"
                  class="user-avatar"
                />
                <div class="avatar-glow"></div>
              </div>
              <div class="user-details">
                <h3 class="user-name">{{ guestbook.guest_name }}</h3>
                <p class="message-time">
                  <el-icon><Calendar /></el-icon>
                  {{ guestbook.guest_time }}
                </p>
              </div>
            </div>
            
            <div class="message-content">
              <p class="message-text">{{ guestbook.guest_comment }}</p>
            </div>
          </div>
        </el-card>
      </div>
    </transition-group>
  </div>
  
  <el-drawer
    v-model="addGuestbook"
    title="留下您的足迹"
    direction="rtl"
    size="420px"
    :destroy-on-close="false"
    :modal="true"
    :show-close="true"
    :with-header="true"
    append-to-body
  >
    <el-form class="message-form" label-position="top">
      <el-form-item label="您的名字">
        <el-input 
          v-model="guestbookForm.guest_name"
          placeholder="请输入您的名字"
          clearable
        >
          <template #prefix>
            <el-icon><User /></el-icon>
          </template>
        </el-input>
      </el-form-item>
      
      <el-form-item label="留言内容">
        <el-input 
          v-model="guestbookForm.guest_comment"
          type="textarea"
          placeholder="分享您的想法、感受或建议..."
          :rows="6"
          resize="none"
        />
      </el-form-item>
      
      <div class="form-actions">
        <el-button 
          @click="addGuestbook = false"
        >
          取消
        </el-button>
        
        <el-button 
          type="primary"
          @click="submitGuestbook(); addGuestbook = false;"
          :disabled="!guestbookForm.guest_name || !guestbookForm.guest_comment"
        >
          <el-icon><Document /></el-icon>
          提交留言
        </el-button>
      </div>
    </el-form>
  </el-drawer>
</template>

<style scoped>
.message-board-container {
  padding: 32px 0;
  max-width: 1000px;
  margin: 0 auto;
}

.board-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 40px;
  position: relative;
}

.board-title {
  font-size: 28px;
  font-weight: 600;
  color: var(--el-color-primary);
  margin: 0 0 12px 0;
  position: relative;
}

.board-decoration {
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, var(--el-color-primary), var(--el-color-primary-light-5));
  border-radius: 3px;
  margin-bottom: 16px;
}

.board-subtitle {
  font-size: 16px;
  color: var(--el-text-color-secondary);
  margin: 0 0 24px 0;
}

.add-message-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  font-size: 15px;
  font-weight: 500;
  border-radius: 8px;
  transition: all 0.3s ease;
  background: linear-gradient(135deg, var(--el-color-primary), var(--el-color-primary-light-3));
  border: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.add-message-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.messages-container {
  display: grid;
  gap: 24px;
}

.message-card-wrapper {
  transition: all 0.3s ease;
}

.message-card {
  border-radius: 12px;
  border: none;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
}

.message-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.card-content {
  padding: 4px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.avatar-container {
  position: relative;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  overflow: hidden;
  background: linear-gradient(135deg, var(--el-color-primary-light-7), var(--el-color-primary-light-9));
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.user-avatar {
  width: 32px;
  height: 32px;
  object-fit: contain;
  transition: all 0.3s ease;
}

.avatar-glow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, rgba(64, 158, 255, 0.4) 0%, transparent 70%);
  opacity: 0;
  transition: all 0.3s ease;
}

.avatar-container:hover .avatar-glow {
  opacity: 1;
}

.avatar-container:hover .user-avatar {
  transform: scale(1.1);
}

.user-details {
  flex: 1;
}

.user-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin: 0 0 4px 0;
}

.message-time {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--el-text-color-secondary);
  margin: 0;
}

.message-content {
  padding: 16px;
  background: rgba(0, 0, 0, 0.02);
  border-radius: 8px;
  position: relative;
}

.message-content::before {
  content: '';
  position: absolute;
  top: -8px;
  left: 16px;
  width: 16px;
  height: 16px;
  background: rgba(0, 0, 0, 0.02);
  transform: rotate(45deg);
}

.message-text {
  font-size: 15px;
  line-height: 1.6;
  color: var(--el-text-color-primary);
  margin: 0;
  text-align: left;
}

.empty-state {
  padding: 60px 0;
}

.empty-description {
  font-size: 16px;
  color: var(--el-text-color-secondary);
  margin-top: 16px;
}

.message-drawer :deep(.el-drawer__header) {
  margin-bottom: 24px;
  padding: 16px 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.message-drawer :deep(.el-drawer__body) {
  padding: 0 20px 20px 20px;
  height: calc(100% - 70px);
  overflow-y: auto;
}

.message-form {
  width: 100%;
  padding: 0;
}

.message-form :deep(.el-form-item__label) {
  padding: 0 0 8px;
  font-weight: 500;
  color: var(--el-text-color-primary);
}

.message-form :deep(.el-input__wrapper),
.message-form :deep(.el-textarea__wrapper) {
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.1) inset;
  border-radius: 8px;
  padding: 8px 12px;
  transition: all 0.3s ease;
}

.message-form :deep(.el-input__wrapper:hover),
.message-form :deep(.el-textarea__wrapper:hover) {
  box-shadow: 0 0 0 1px var(--el-color-primary-light-5) inset;
}

.message-form :deep(.el-input__wrapper:focus-within),
.message-form :deep(.el-textarea__wrapper:focus-within) {
  box-shadow: 0 0 0 1px var(--el-color-primary) inset;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
  margin-top: 32px;
}

.cancel-btn,
.submit-btn {
  padding: 10px 24px;
  border-radius: 8px;
  font-weight: 500;
}

.submit-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, var(--el-color-primary), var(--el-color-primary-light-3));
  border: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.submit-btn:not(:disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

/* 列表动画效果 */
.message-list-enter-active,
.message-list-leave-active {
  transition: all 0.5s ease;
}

.message-list-enter-from,
.message-list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}
</style>