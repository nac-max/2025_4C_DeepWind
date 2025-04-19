<script setup>
import {defineProps, ref} from "vue";
import {Document, Menu, Grid, Cpu, DataAnalysis, WindPower} from "@element-plus/icons-vue";

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

const isCollapse = ref(false);
const activeIndex = ref('1');
</script>

<template>
  <div class="guide-container" :class="{ 'dark-mode': isDark }">
    <div class="menu-wrapper">
      <div class="menu-header" v-if="!isCollapse">
        <el-icon size="20"><Document /></el-icon>
        <h3 class="menu-title">系统文档</h3>
        <div class="decoration-line"></div>
      </div>
      
      <el-menu
        :default-active="activeIndex"
        :collapse="isCollapse"
        class="guide-menu"
        @select="(index) => { activeIndex = index; $emit('changeGuides', index) }"
      >
        <el-menu-item index="1" class="menu-item">
          <el-icon><WindPower /></el-icon>
          <template #title>
            <span class="item-text">风机列表</span>
          </template>
        </el-menu-item>

        <el-menu-item index="2" class="menu-item">
          <el-icon><Menu /></el-icon>
          <template #title>
            <span class="item-text">风机模型</span>
          </template>
        </el-menu-item>
        
        <el-menu-item index="3" class="menu-item">
          <el-icon><Grid /></el-icon>
          <template #title>
            <span class="item-text">数据中心</span>
          </template>
        </el-menu-item>
        
        <el-menu-item index="4" class="menu-item">
          <el-icon><DataAnalysis /></el-icon>
          <template #title>
            <span class="item-text">预测中心</span>
          </template>
        </el-menu-item>
        
        <el-menu-item index="5" class="menu-item">
          <el-icon><Cpu /></el-icon>
          <template #title>
            <span class="item-text">统计界面</span>
          </template>
        </el-menu-item>
      </el-menu>
    </div>
  </div>
</template>


<style scoped>
/* 基础变量 */
:root {
  --primary-color: #4557e5;
  --primary-hover: #3a4cd9;
  --secondary-color: #2d96e8;
  --text-primary: #1a202c;
  --text-secondary: #4a5568;
  --bg-light: #f8faff;
  --bg-dark: #1a1e2e;
  --menu-width: 200px;
  --menu-collapsed-width: 64px;
  --transition-speed: 0.3s;
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.06);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* 容器样式 */
.guide-container {
  height: 100%;
  position: relative;
  transition: all var(--transition-speed) ease;
}

.menu-wrapper {
  height: 100%;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-md);
  border-radius: 12px;
  transition: all var(--transition-speed) ease;
}

/* 菜单头部 */
.menu-header {
  display: flex;
  align-items: center;
  padding: 20px 16px 12px;
  position: relative;
}

.menu-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 0 12px;
  color: var(--primary-color);
  letter-spacing: 0.5px;
}

.decoration-line {
  position: absolute;
  bottom: 0;
  left: 16px;
  right: 16px;
  height: 1px;
  background: linear-gradient(90deg, 
    rgba(69, 87, 229, 0.1), 
    rgba(45, 150, 232, 0.6), 
    rgba(69, 87, 229, 0.1)
  );
}

/* 菜单样式 */
.guide-menu {
  border-right: none !important;
  width: var(--menu-width);
  transition: width var(--transition-speed) ease;
}

.guide-menu.el-menu--collapse {
  width: var(--menu-collapsed-width);
}

.menu-item {
  margin: 8px 0;
  border-radius: 8px;
  transition: all var(--transition-speed) ease !important;
}

.menu-item:hover, .menu-item.is-active {
  background: linear-gradient(
    45deg,
    rgba(69, 87, 229, 0.08), 
    rgba(45, 150, 232, 0.08)
  ) !important;
}

.menu-item.is-active {
  position: relative;
}

.menu-item.is-active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 60%;
  background: linear-gradient(180deg, var(--primary-color), var(--secondary-color));
  border-radius: 0 4px 4px 0;
}

.item-text {
  font-size: 14px;
  font-weight: 500;
  transition: all var(--transition-speed) ease;
  letter-spacing: 0.3px;
}

.menu-item.is-active .item-text {
  font-weight: 600;
  color: var(--primary-color) !important;
}

/* 亮暗模式适配 */
.dark-mode .menu-wrapper {
  background-color: var(--bg-dark);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.dark-mode .menu-title {
  color: rgba(255, 255, 255, 0.9);
}

.dark-mode .decoration-line {
  background: linear-gradient(90deg, 
    rgba(69, 87, 229, 0.1), 
    rgba(45, 150, 232, 0.5), 
    rgba(69, 87, 229, 0.1)
  );
}

.dark-mode .menu-item:hover, .dark-mode .menu-item.is-active {
  background: linear-gradient(
    45deg,
    rgba(69, 87, 229, 0.15), 
    rgba(45, 150, 232, 0.15)
  ) !important;
}

.dark-mode .item-text {
  color: rgba(255, 255, 255, 0.8);
}

.dark-mode .menu-item.is-active .item-text {
  color: rgba(255, 255, 255, 0.95) !important;
}
</style>