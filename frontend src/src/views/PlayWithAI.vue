<script setup>
  import {ref,onMounted,onUnmounted} from "vue";
  import {Close, Promotion, Refresh, Search, Star} from "@element-plus/icons-vue";
  const isCollapse = ref(false)
  const message = ref('')
  const showDialog = ref(false)
  const dynamicHeight = ref('540px')
  const dynamicMargin = ref('128px')
  const dynamicRows = ref('1')
  const pending = ref(false)
  const pendingRows = ref(1)
  const drawerRef = ref(null)
  const carouselItem = [
    {
      title: "让AI帮助你快速入门",
      input: "我应该如何使用风起云算·智风 DeepWind 系统？"
    },
    {
      title: "让AI聆听你的奇思妙想",
      input: "如果风电预测系统加上储能优化算法，度电成本能降低多少？"
    },
    {
      title: "让AI解锁新能源洞察",
      input: "如何通过风电预测优化区域电网的运行？"
    },
    {
      title: "让AI绘制未来能源蓝图",
      input: "如何基于风电预测设计智慧城市能源调度方案？"
    }
  ]

  const messageHistory = ref([])
  const dynamicDrawerWidth = ref('64%')
  const dynamicDrawerMargin = ref('18%')

  const resizeHandler = () => {
    let heightRatio = window.innerHeight/1024
    let widthRatio = window.innerWidth/2048

    if(window.innerWidth < 620) {
      isCollapse.value = true
      dynamicDrawerWidth.value = '100%'
      dynamicDrawerMargin.value = '0px'
      dynamicRows.value = '4'
      dynamicMargin.value = '0px'
      dynamicHeight.value = heightRatio * 576 + 'px'
    }
    else{
      isCollapse.value = false
      dynamicRows.value = '4'
      dynamicDrawerWidth.value = '64%'
      dynamicDrawerMargin.value = '18%'
      dynamicHeight.value = heightRatio * 576 + 'px'
      dynamicMargin.value = widthRatio * 96 + 'px'
    }
  }
  const helloGPT = () => {
    if(message.value === ''){
      return
    }

    messageHistory.value.push(
        {role: 'user', content: message.value}
    )

    let formData = new FormData()
    let messageHistory_string = JSON.stringify(messageHistory.value )
    formData.append('messageHistory', messageHistory_string)

    pending.value = true
    pendingRows.value = (message.value.length / 12).toFixed(0)
    if(pendingRows.value < 1){
      pendingRows.value = 1
    }
    message.value = ''

    fetch("/api/hello_gpt/", {
      method:'POST',
      body:formData,
    }).then(response => response.json())
    .then(data => {
      pending.value = false;
      messageHistory.value.push(data.message);
    })
  }
  const initialDialog = () => {
    messageHistory.value = []
    pending.value = true
    setTimeout(()=>{
      messageHistory.value.push({role: "assistant", content: "你好！我是DeepWind AI助手，我该怎样帮助你？"})
      pending.value = false
    }, 720)
  }

  onMounted(() => {
    resizeHandler()
    window.addEventListener('resize', resizeHandler)
  })
  onUnmounted(() => {
    window.removeEventListener('resize', resizeHandler)
  })

</script>

<template>
  <div class="ai-assistant-container">
    <!-- 背景装饰元素 -->
    <div class="bg-decoration">
      <div class="bg-circle circle-1"></div>
      <div class="bg-circle circle-2"></div>
      <div class="bg-circle circle-3"></div>
    </div>
    
    <!-- 主内容区 -->
    <div class="content-wrapper">
      <header class="app-header">
        <div class="logo-wrapper">
          <img src="../assets/static/img/deepwind-icon.png" alt="DeepWind" class="logo-icon" />
          <h1 class="app-title">DeepWind <span>AI助手</span></h1>
        </div>
      </header>
      
      <!-- 交互展示区 -->
      <div class="interactive-section">
        <div class="feature-showcase">
          <div class="feature-header">
            <h2 class="section-title">AI 助手使用场景</h2>
            <p class="section-subtitle">探索智风系统的无限可能</p>
          </div>
          
          <el-carousel
            class="feature-carousel"
            height="180px"
            arrow="never"
            indicator-position="none"
            direction="vertical"
            interval="3000"
          >
            <el-carousel-item v-for="(item, index) in carouselItem" :key="index" class="carousel-item">
              <div class="feature-card">
                <div class="feature-card-content">
                  <span class="feature-icon"><el-icon><Star /></el-icon></span>
                  <h3 class="feature-title">{{ item.title }}</h3>
                  <div class="feature-sample">
                    <p class="sample-text">"{{ item.input }}"</p>
                  </div>
                </div>
              </div>
            </el-carousel-item>
          </el-carousel>
          
          <div class="cta-container">
            <el-button class="cta-button" @click="showDialog = true">
              <span class="btn-inner">开始探索</span>
              <span class="btn-shine"></span>
            </el-button>
          </div>
        </div>
        
        <!-- 预览区 -->
        <div class="preview-container">
          <div class="chat-preview">
            <div class="preview-header">
              <img src="../assets/static/img/deepwind-icon.png" alt="DeepWind" class="preview-logo" />
              <span class="preview-title"> AI 实时对话预览</span>
            </div>
            
            <div class="preview-chat">
              <div class="chat-message ai-message">
                <div class="message-avatar">
                  <img src="../assets/static/img/deepwind-icon.png" alt="Assistant" />
                </div>
                <div class="message-content ai-content">
                  <p>你好！我是DeepWind AI助手，我该怎样帮助你？</p>
                </div>
              </div>
              
              <div class="chat-message user-message">
                <div class="message-content user-content">
                  <p>我应该如何使用风起云算·智风 DeepWind 系统？</p>
                </div>
                <div class="message-avatar">
                  <img src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" alt="User" />
                </div>
              </div>
              
              <div class="chat-message ai-message">
                <div class="message-avatar">
                  <img src="../assets/static/img/deepwind-icon.png" alt="Assistant" />
                  <div class="pulse-animation"></div>
                </div>
                <div class="message-content ai-content typing-content">
                  <el-skeleton animated :rows="2" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- AI对话抽屉 -->
    <el-drawer
      v-model="showDialog"
      direction="rtl"
      size="80%"
      :show-close="true"
      :with-header="false"
      class="chat-drawer"
      @open="()=>{ if(messageHistory.length === 0){ initialDialog() } }"
      ref="drawerRef"
    >
      <div class="chat-interface">
        <div class="chat-header">
          <div class="chat-header-left">
            <img src="../assets/static/img/deepwind-icon.png" alt="DeepWind" class="chat-logo" />
            <h2 class="chat-title">DeepWind 智能助手</h2>
          </div>
          <div class="chat-header-right">
            <el-button circle class="header-btn" @click="drawerRef.close">
              <el-icon><Close /></el-icon>
            </el-button>
          </div>
        </div>
        
        <div class="chat-messages" :style="{height: dynamicHeight}">
          <el-scrollbar>
            <div class="messages-wrapper">
              <div 
                v-for="(message,index) in messageHistory" 
                :key="index"
                :class="['chat-message', message.role === 'assistant' ? 'ai-message' : 'user-message']"
              >
                <template v-if="message.role === 'assistant'">
                  <div class="message-avatar">
                    <img src="../assets/static/img/deepwind-icon.png" alt="Assistant" />
                  </div>
                  <div class="message-content ai-content">
                    <p>{{ message.content }}</p>
                  </div>
                </template>
                
                <template v-else>
                  <div class="message-content user-content">
                    <p>{{ message.content }}</p>
                  </div>
                  <div class="message-avatar">
                    <img src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" alt="User" />
                  </div>
                </template>
              </div>
              
              <div v-if="pending" class="chat-message ai-message">
                <div class="message-avatar">
                  <img src="../assets/static/img/deepwind-icon.png" alt="Assistant" />
                  <div class="pulse-animation"></div>
                </div>
                <div class="message-content ai-content typing-content">
                  <el-skeleton animated :rows="pendingRows" />
                </div>
              </div>
            </div>
          </el-scrollbar>
        </div>
        
        <div class="chat-input-area">
          <div class="input-container">
            <el-input
              v-model="message"
              type="textarea"
              :rows="dynamicRows"
              maxlength="1024"
              show-word-limit
              class="chat-input"
              @keyup.enter="message=message.slice(0,-1);helloGPT();"
              placeholder="输入你的问题或想法..."
            />
            
            <div class="input-actions">
              <el-button circle class="action-btn clear-btn" @click="message='';initialDialog()">
                <el-icon><Refresh /></el-icon>
              </el-button>
              
              <el-button circle class="action-btn send-btn" @click="helloGPT" :disabled="!message">
                <el-icon><Promotion /></el-icon>
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<style scoped>
/* 全局样式变量 */
:root {
  --primary-color: #4557e5;
  --primary-gradient: linear-gradient(135deg, #4557e5, #2d96e8);
  --secondary-color: #2d96e8;
  --bg-color: #f8faff;
  --card-bg: rgba(255, 255, 255, 0.95);
  --text-primary: #1a202c;
  --text-secondary: #4a5568;
  --shadow-sm: 0 4px 12px rgba(0, 0, 0, 0.06);
  --shadow-md: 0 8px 24px rgba(0, 0, 0, 0.09);
  --shadow-lg: 0 15px 35px rgba(0, 0, 0, 0.12);
  --border-radius-sm: 8px;
  --border-radius-md: 16px;
  --border-radius-lg: 24px;
  --transition: all 0.3s ease;
}

/* 主容器样式 */
.ai-assistant-container {
  position: relative;
  width: 100%;
  min-height: 100vh;
  overflow: hidden;
  background-color: var(--bg-color);
  padding: 40px 0;
}

/* 背景装饰 */
.bg-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
}

.bg-circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.15;
}

.circle-1 {
  top: -10%;
  right: -10%;
  width: 40vw;
  height: 40vw;
  background: linear-gradient(45deg, #4557e5, #2d96e8);
}

.circle-2 {
  bottom: -20%;
  left: -10%;
  width: 60vw;
  height: 60vw;
  background: linear-gradient(45deg, #2d96e8, #53b0ff);
}

.circle-3 {
  top: 40%;
  left: 30%;
  width: 30vw;
  height: 30vw;
  background: linear-gradient(45deg, #53b0ff, #4557e5);
  opacity: 0.05;
}

/* 内容包装 */
.content-wrapper {
  position: relative;
  z-index: 1;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
}

/* 应用头部 */
.app-header {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 40px;
}

.logo-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 48px;
  height: 48px;
  object-fit: contain;
}

.app-title {
  font-size: 32px;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(135deg, #4557e5, #2d96e8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 2px 8px rgba(89, 104, 244, 0.2);
  letter-spacing: 0.5px;
}

.app-title span {
  font-weight: 400;
  opacity: 0.8;
}

/* 交互区域 */
.interactive-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  margin-top: 20px;
}

/* 特性展示 */
.feature-showcase {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.feature-header {
  text-align: center;
  margin-bottom: 32px;
}

.section-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 8px 0;
  background: linear-gradient(135deg, #4557e5, #2d96e8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: 0.3px;
}

.section-subtitle {
  font-size: 16px;
  color: var(--text-secondary);
  margin: 0;
  font-weight: 500;
}

.feature-carousel {
  width: 100%;
  max-width: 480px;
  border-radius: var(--border-radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  margin-bottom: 40px;
}

.carousel-item {
  height: 100%;
}

.feature-card {
  height: 100%;
  background: var(--card-bg);
  backdrop-filter: blur(10px);
  border-radius: var(--border-radius-lg);
  overflow: hidden;
  padding: 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  border: 1px solid rgba(89, 104, 244, 0.1);
}

.feature-card-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.feature-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--primary-gradient);
  margin-bottom: 16px;
  color: white;
  font-size: 24px;
  box-shadow: 0 8px 16px rgba(89, 104, 244, 0.3);
}

.feature-title {
  font-size: 20px;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 16px 0;
}

.feature-sample {
  background: rgba(89, 104, 244, 0.05);
  padding: 16px;
  border-radius: var(--border-radius-md);
  width: 100%;
  text-align: center;
}

.sample-text {
  font-size: 15px;
  color: #334155;
  font-style: italic;
  margin: 0;
  font-weight: 500;
}

.cta-container {
  margin-top: 20px;
}

.cta-button {
  position: relative;
  width: 180px;
  height: 54px;
  font-size: 18px;
  font-weight: 600;
  color: white;
  background: linear-gradient(135deg, #4557e5, #2d96e8);
  border: none;
  border-radius: var(--border-radius-md);
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(89, 104, 244, 0.4);
  transition: var(--transition);
  letter-spacing: 0.5px;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.cta-button:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(89, 104, 244, 0.5);
  background: linear-gradient(135deg, #3a4cd9, #1a89e0);
}

.btn-inner {
  position: relative;
  z-index: 2;
}

.btn-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 300%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  transition: var(--transition);
}

.cta-button:hover .btn-shine {
  left: 100%;
  transition: 0.8s ease;
}

/* 预览容器 */
.preview-container {
  padding-top: 20px;
}

.chat-preview {
  background: var(--card-bg);
  backdrop-filter: blur(10px);
  border-radius: var(--border-radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-lg);
  border: 1px solid rgba(89, 104, 244, 0.1);
  height: 560px;
  display: flex;
  flex-direction: column;
}

.preview-header {
  display: flex;
  align-items: center;
  padding: 16px 24px;
  background: rgba(89, 104, 244, 0.03);
  border-bottom: 1px solid rgba(89, 104, 244, 0.1);
}

.preview-logo {
  width: 32px;
  height: 32px;
  margin-right: 12px;
}

.preview-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  background: linear-gradient(135deg, #4557e5, #2d96e8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: 0.2px;
}

.preview-chat {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 聊天消息样式 */
.chat-message {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  animation: fadeInUp 0.5s ease;
  max-width: 90%;
}

.ai-message {
  align-self: flex-start;
}

.user-message {
  flex-direction: row-reverse;
  align-self: flex-end;
}

.message-avatar {
  position: relative;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  border: 2px solid white;
  box-shadow: var(--shadow-sm);
}

.message-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.message-content {
  padding: 16px;
  border-radius: var(--border-radius-md);
  position: relative;
  max-width: calc(100% - 60px);
  box-shadow: var(--shadow-sm);
}

.ai-content {
  background: rgba(89, 104, 244, 0.05);
  border-top-left-radius: 0;
  color: var(--text-primary);
}

.ai-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: -12px;
  width: 12px;
  height: 12px;
  background: rgba(89, 104, 244, 0.05);
  clip-path: polygon(100% 0, 0 0, 100% 100%);
}

.user-content {
  background: linear-gradient(135deg, #4557e5, #2d96e8);
  border-top-right-radius: 0;
  color: white;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.user-content::before {
  content: '';
  position: absolute;
  top: 0;
  right: -12px;
  width: 12px;
  height: 12px;
  background: #2d96e8;
  clip-path: polygon(0 0, 0 100%, 100% 0);
}

.message-content p {
  margin: 0;
  line-height: 1.6;
  font-size: 15px;
  letter-spacing: 0.2px;
}

.typing-content {
  min-width: 240px;
}

.pulse-animation {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(
    circle at center,
    rgba(89, 104, 244, 0.4) 0%,
    transparent 70%
  );
  border-radius: 50%;
  animation: pulse 1.5s infinite ease-in-out;
}

@keyframes pulse {
  0% { opacity: 0; transform: scale(0.8); }
  50% { opacity: 0.8; transform: scale(1.2); }
  100% { opacity: 0; transform: scale(0.8); }
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 聊天抽屉样式 */
.chat-drawer {
  --el-drawer-bg-color: transparent;
  --el-drawer-padding-primary: 0;
}

.chat-interface {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: var(--card-bg);
  backdrop-filter: blur(10px);
  border-radius: 24px 0 0 24px;
  overflow: hidden;
  box-shadow: var(--shadow-lg);
  border-left: 1px solid rgba(89, 104, 244, 0.1);
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  background: rgba(89, 104, 244, 0.03);
  border-bottom: 1px solid rgba(89, 104, 244, 0.08);
}

.chat-header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.chat-logo {
  width: 32px;
  height: 32px;
}

.chat-title {
  font-size: 20px;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(135deg, #4557e5, #2d96e8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: 0.3px;
}

.header-btn {
  width: 36px;
  height: 36px;
  color: var(--text-secondary);
  border: none;
  background: rgba(89, 104, 244, 0.08);
  transition: var(--transition);
}

.header-btn:hover {
  background: rgba(89, 104, 244, 0.15);
  color: var(--primary-color);
}

.chat-messages {
  flex: 1;
  overflow: hidden;
  padding: 0 24px;
}

.messages-wrapper {
  padding: 24px 0;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.chat-input-area {
  padding: 24px;
  border-top: 1px solid rgba(89, 104, 244, 0.08);
  background: rgba(255, 255, 255, 0.5);
}

.input-container {
  position: relative;
}

.chat-input {
  width: 100%;
  resize: none;
  border-radius: var(--border-radius-md);
  border: 1px solid rgba(89, 104, 244, 0.2);
  transition: var(--transition);
  padding-right: 100px;
  font-size: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.chat-input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(89, 104, 244, 0.2);
}

.input-actions {
  position: absolute;
  right: 8px;
  bottom: 8px;
  display: flex;
  gap: 8px;
}

.action-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
  font-size: 18px;
}

.clear-btn {
  background: rgba(100, 116, 139, 0.1);
  color: var(--text-secondary);
  border: none;
}

.clear-btn:hover {
  background: rgba(100, 116, 139, 0.2);
  transform: rotate(180deg);
}

.send-btn {
  background: linear-gradient(135deg, #4557e5, #2d96e8);
  color: white;
  border: none;
  box-shadow: 0 4px 12px rgba(69, 87, 229, 0.4);
}

.send-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(69, 87, 229, 0.5);
  background: linear-gradient(135deg, #3a4cd9, #1a89e0);
}

.send-btn:disabled {
  background: linear-gradient(135deg, #9ca3e0, #8ebce9);
  opacity: 0.6;
}

/* 响应式调整 */
@media screen and (max-width: 1024px) {
  .interactive-section {
    grid-template-columns: 1fr;
    gap: 40px;
  }
  
  .feature-showcase {
    order: 1;
  }
  
  .preview-container {
    order: 2;
  }
  
  .chat-preview {
    max-height: 500px;
  }
}

@media screen and (max-width: 768px) {
  .content-wrapper {
    padding: 0 16px;
  }
  
  .app-title {
    font-size: 28px;
  }
  
  .section-title {
    font-size: 24px;
  }
  
  .feature-carousel {
    max-width: 100%;
  }
}

@media screen and (max-width: 480px) {
  .app-header {
    margin-bottom: 24px;
  }
  
  .logo-icon {
    width: 40px;
    height: 40px;
  }
  
  .app-title {
    font-size: 24px;
  }
  
  .feature-title {
    font-size: 18px;
  }
  
  .sample-text {
    font-size: 14px;
  }
  
  .cta-button {
    width: 160px;
    height: 48px;
    font-size: 16px;
  }
}
</style>