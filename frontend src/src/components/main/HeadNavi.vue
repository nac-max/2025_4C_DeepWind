<template>
  <div class="head-navi-wrapper">
    <el-menu
      :default-active="activeIndex"
      mode="horizontal"
      class="head-navi-menu"
    >
      <div class="navi-left">
        <el-popover
          placement="bottom-start"
          :width="240"
          trigger="hover"
          popper-class="theme-switch-popover"
        >
          <template #reference>
            <div class="logo-container">
              <img
                class="logo-icon"
                src="../../assets/static/img/newIcon.png"
                alt="Logo"
              />
              <div class="logo-glow"></div>
            </div>
          </template>
          <div class="theme-switch-content">
            <div class="theme-switch-header">
              <el-icon><Setting /></el-icon>
              <span>主题设置</span>
            </div>
            <div class="theme-switch-body">
              <span class="theme-text">深色模式</span>
              <el-switch
                v-model="isDark"
                @change="$emit('changeTheme', isDark)"
                class="theme-switch"
                inline-prompt
                :active-icon="MoonNight"
                :inactive-icon="Sunset"
              />
            </div>
          </div>
        </el-popover>
        
        <div class="proverb-container" v-if="!isCollapse">
          <p class="proverb" ref="proverb">
            风起云算·智风 (DeepWind) 系统
          </p>
          <div class="proverb-decoration"></div>
        </div>
      </div>

      <div class="navi-right">
        <el-menu-item 
          index="1" 
          @click="$emit('changePage', '1')"
          class="navi-item"
        >
          <el-icon><DataLine /></el-icon>
          <span>预测系统</span>
        </el-menu-item>
        
        <el-menu-item 
          index="2" 
          @click="$emit('changePage', '2')"
          class="navi-item"
        >
          <el-icon><Document /></el-icon>
          <span>使用指南</span>
        </el-menu-item>
        
        <el-menu-item
          index="3"
          class="navi-item ai-item"
          @mouseenter="dynamicClass = 'is-loading'"
          @mouseleave="dynamicClass = ''"
          @click="$emit('changePage', '3')"
        >
          <div class="custom-icon-container" :class="dynamicClass">
            <img src="../../assets/static/img/deepwind-icon.png" alt="DeepWind Icon" class="custom-icon" />
          </div>
          <span> DeepWind助手 </span>
          <div class="ai-glow"></div>
        </el-menu-item>
        
        <el-menu-item 
          index="4" 
          @click="$emit('changePage', '4')"
          class="navi-item"
        >
          <el-icon><InfoFilled /></el-icon>
          <span>关于我们</span>
        </el-menu-item>
      </div>
    </el-menu>
  </div>
</template>

<script setup>
import { ref, onMounted, defineEmits } from 'vue'
import { useDark } from '@vueuse/core'
import { 
  MoonNight, 
  Star, 
  Sunset,
  Setting,
  DataLine,
  Document,
  InfoFilled
} from "@element-plus/icons-vue"

const activeIndex = ref('1')
const proverb = ref(null)
const isDark = useDark()
const isCollapse = ref(true)
const dynamicClass = ref('')
const emits = defineEmits(['changePage', 'changeTheme'])

onMounted(() => {
  if(isDark.value) {
    isDark.value = false
  }
  if (window.innerWidth < 620) {
    if(proverb.value){
      proverb.value.style.fontSize = '0px'
    }
  }
  else {
    if(proverb.value) {
      proverb.value.style.fontSize = '18px'
    }
    isCollapse.value = false
  }
  emits('changeTheme', isDark.value)
  window.addEventListener('resize', () => {
    if (window.innerWidth < 620) {
      if(proverb.value){
        proverb.value.style.fontSize = '0px'
      }
    }
    else {
      if(proverb.value) {
        proverb.value.style.fontSize = '18px'
      }
      isCollapse.value = false
    }
  })
})
</script>

<style scoped>
.head-navi-wrapper {
  position: relative;
  z-index: 10;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.head-navi-menu {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 64px;
  padding: 0 24px;
  background: transparent !important;
  border-bottom: none !important;
}

.navi-left {
  display: flex;
  align-items: center;
  gap: 24px;
}

.logo-container {
  position: relative;
  width: 40px;
  height: 40px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logo-icon {
  width: 100%;
  height: 100%;
  object-fit: contain;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
  transition: all 0.3s ease;
}

.logo-glow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, rgba(89, 104, 244, 0.1) 0%, transparent 70%);
  opacity: 0;
  transition: all 0.3s ease;
}

.logo-container:hover .logo-glow {
  opacity: 1;
}

.logo-container:hover .logo-icon {
  transform: scale(1.05);
}

.proverb-container {
  position: relative;
  padding: 0 16px;
}

.proverb {
  font-size: 16px;
  color: var(--el-text-color-primary);
  text-shadow: 0 0 8px rgba(255, 255, 255, 0.5);
  transition: all 0.3s ease;
  margin: 0;
  font-weight: 500;
}

.proverb-decoration {
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--el-color-primary), transparent);
  opacity: 0;
  transition: all 0.3s ease;
}

.proverb-container:hover .proverb-decoration {
  opacity: 1;
}

.navi-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.navi-item {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 40px;
  padding: 0 16px;
  border-radius: 8px;
  transition: all 0.3s ease;
  color: var(--el-text-color-regular);
}

.navi-item:hover {
  background: rgba(89, 104, 244, 0.1);
  color: var(--el-color-primary);
}

.navi-item.is-active {
  background: rgba(89, 104, 244, 0.1);
  color: var(--el-color-primary);
  font-weight: 500;
}

.ai-item {
  position: relative;
  color: #5968f4 !important;
}

.ai-glow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, rgba(89, 104, 244, 0.1) 0%, transparent 70%);
  opacity: 0;
  transition: all 0.3s ease;
  border-radius: 8px;
}

.ai-item:hover .ai-glow {
  opacity: 1;
}

.ai-icon {
  transition: all 0.3s ease;
}

.ai-icon.is-loading {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

:deep(.theme-switch-popover) {
  border-radius: 12px !important;
  border: 1px solid rgba(0, 0, 0, 0.05) !important;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1) !important;
  padding: 16px !important;
}

.theme-switch-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.theme-switch-header {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--el-text-color-primary);
  font-weight: 500;
}

.theme-switch-body {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.theme-text {
  color: var(--el-text-color-regular);
  font-size: 14px;
}

.theme-switch {
  --el-switch-on-color: #5968f4;
}

@media (max-width: 768px) {
  .head-navi-menu {
    padding: 0 16px;
  }
  
  .navi-item {
    padding: 0 12px;
  }
  
  .navi-item span {
    display: none;
  }
  
  .navi-item .el-icon {
    margin: 0;
  }
}

.custom-icon-container {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.custom-icon-container.is-loading {
  animation: spin 1s linear infinite;
}

.custom-icon {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
</style>