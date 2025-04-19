<template>
  <div class="aside-wrapper" :class="{'is-collapsed': isCollapse}">
    <el-menu
        default-active="1-1"
        :collapse="isCollapse"
        class="aside-menu"
        background-color="transparent"
        text-color="var(--el-text-color-regular)"
        active-text-color="var(--el-color-primary)"
    >
      <div class="menu-header" v-if="!isCollapse">
        <div class="header-content">
          <span class="header-icon-bg">
            <el-icon class="header-icon"><Setting /></el-icon>
          </span>
          <h3 class="header-title">功能导航</h3>
        </div>
        <el-divider class="header-divider" />
      </div>
      
      <el-sub-menu index="1" class="nav-sub-menu" popper-class="nav-submenu-popper">
        <template #title>
          <div class="menu-item-content">
            <span class="icon-container">
              <el-icon class="menu-icon"><Location /></el-icon>
            </span>
            <span class="menu-text">风机管理</span>
          </div>
        </template>
        <el-menu-item-group class="menu-group">
          <el-menu-item 
            index="1-1" 
            @click="$emit('changeIndex', '1-1')"
            class="menu-item"
          >
            <div class="submenu-item-content">
              <span class="dot-indicator"></span>
              <span class="item-text">风机列表</span>
            </div>
          </el-menu-item>
          <el-menu-item 
            index="1-2" 
            @click="$emit('changeIndex', '1-2')"
            class="menu-item"
          >
            <div class="submenu-item-content">
              <span class="dot-indicator"></span>
              <span class="item-text">风机模型</span>
            </div>
          </el-menu-item>
        </el-menu-item-group>
      </el-sub-menu>
      
      <el-menu-item 
        index="2" 
        @click="$emit('changeIndex', '2')"
        class="menu-item"
      >
        <div class="menu-item-content">
          <span class="icon-container">
            <el-icon class="menu-icon"><IconMenu /></el-icon>
          </span>
          <span class="menu-text">数据空间</span>
        </div>
      </el-menu-item>
      
      <el-menu-item 
        index="3" 
        @click="$emit('changeIndex', '3')"
        class="menu-item"
      >
        <div class="menu-item-content">
          <span class="icon-container">
            <el-icon class="menu-icon"><Document /></el-icon>
          </span>
          <span class="menu-text">预测中心</span>
        </div>
      </el-menu-item>
      
      <el-menu-item 
        index="4" 
        @click="$emit('changeIndex', '4')"
        class="menu-item"
      >
        <div class="menu-item-content">
          <span class="icon-container">
            <el-icon class="menu-icon"><Setting /></el-icon>
          </span>
          <span class="menu-text">统计界面</span>
        </div>
      </el-menu-item>
    </el-menu>
    
    <div class="nav-footer" v-if="!isCollapse">
      <div class="footer-content">
        <div class="footer-icon">
          <el-icon><Setting /></el-icon>
        </div>
        <div class="footer-text">v1.0.0</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted} from 'vue'
import {
  Document,
  Menu as IconMenu,
  Location,
  Setting,
} from '@element-plus/icons-vue'

const title = ref(null)
const isCollapse = ref(true)

onMounted(() => {
  isCollapse.value = window.innerWidth < 768;
  window.addEventListener('resize', () => {
    isCollapse.value = window.innerWidth < 768;
  })
})
</script>

<style scoped>
.aside-wrapper {
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: white;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.05);
  position: relative;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  width: 235px;
  border-right: 1px solid var(--el-border-color-light);
}

.aside-wrapper::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(to bottom, var(--el-color-primary), var(--el-color-primary-light-5), var(--el-color-success));
  background-size: 100% 200%;
  opacity: 0.8;
  animation: gradient-flow 8s ease infinite;
}

@keyframes gradient-flow {
  0% {
    background-position: 0% 0%;
  }
  50% {
    background-position: 0% 100%;
  }
  100% {
    background-position: 0% 0%;
  }
}

.is-collapsed {
  width: 72px;
}

.aside-menu {
  flex: 1;
  border-right: none;
  background-color: transparent;
  transition: all 0.3s ease;
}

.menu-header {
  padding: 18px 16px 10px;
  margin-top: 10px;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 14px;
}

.header-icon-bg {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border-radius: 8px;
  background: rgba(64, 158, 255, 0.1);
}

.header-icon {
  font-size: 18px;
  color: var(--el-color-primary);
}

.header-title {
  font-size: 15px;
  font-weight: 500;
  margin: 0;
  color: var(--el-text-color-secondary);
  text-transform: uppercase;
  letter-spacing: 1.5px;
}

.header-divider {
  margin: 0;
  border-color: var(--el-border-color-light);
}

.nav-sub-menu {
  margin: 4px 0;
}

.menu-item-content {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 4px 0;
}

.icon-container {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: rgba(64, 158, 255, 0.08);
  transition: all 0.3s ease;
}

.menu-icon {
  font-size: 18px;
  color: var(--el-text-color-primary);
  transition: all 0.3s ease;
}

.menu-text {
  font-size: 14px;
  font-weight: 500;
  color: var(--el-text-color-primary);
  transition: all 0.3s ease;
}

.menu-group {
  padding: 4px 0;
  background: rgba(64, 158, 255, 0.03);
  border-radius: 8px;
  margin: 0 8px;
}

.menu-item {
  height: 44px;
  line-height: 44px;
  margin: 5px 8px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.submenu-item-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.dot-indicator {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--el-border-color);
  transition: all 0.3s ease;
}

.menu-item:hover {
  background: rgba(64, 158, 255, 0.05);
}

.menu-item:hover .icon-container {
  background: rgba(64, 158, 255, 0.12);
}

.menu-item:hover .menu-icon,
.menu-item:hover .menu-text {
  color: var(--el-color-primary);
}

.menu-item.is-active {
  background: rgba(64, 158, 255, 0.1);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.1);
}

.menu-item.is-active .icon-container {
  background: var(--el-color-primary);
}

.menu-item.is-active .menu-icon {
  color: white;
  transform: scale(1.1);
}

.menu-item.is-active .menu-text {
  color: var(--el-color-primary);
  font-weight: 600;
}

.menu-item.is-active .dot-indicator {
  background: var(--el-color-primary);
  box-shadow: 0 0 8px var(--el-color-primary);
}

.item-text {
  font-size: 13px;
  color: var(--el-text-color-regular);
  transition: all 0.3s ease;
}

.nav-footer {
  padding: 16px;
  border-top: 1px solid var(--el-border-color-light);
  margin-top: auto;
}

.footer-content {
  display: flex;
  align-items: center;
  gap: 10px;
}

.footer-icon {
  font-size: 16px;
  color: var(--el-text-color-secondary);
}

.footer-text {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

/* 自定义菜单样式 */
:deep(.el-menu--collapse) {
  width: 80px;
}

:deep(.el-menu) {
  --el-menu-hover-bg-color: transparent;
  --el-menu-bg-color: transparent;
}

:deep(.el-menu-item),
:deep(.el-sub-menu__title) {
  height: 44px;
  line-height: 44px;
  color: var(--el-text-color-primary);
  margin: 5px 8px;
  border-radius: 8px;
}

:deep(.el-sub-menu__title:hover),
:deep(.el-menu-item:hover) {
  background-color: rgba(64, 158, 255, 0.05);
}

:deep(.el-sub-menu__title) {
  padding-left: 16px !important;
}

:deep(.el-menu-item.is-active) {
  color: var(--el-color-primary);
}

:deep(.el-sub-menu.is-active .el-sub-menu__title) {
  color: var(--el-color-primary);
}

:deep(.el-menu--collapse .el-sub-menu__title) {
  padding: 0 16px !important;
}

:deep(.el-sub-menu__icon-arrow) {
  color: var(--el-text-color-secondary);
}

:deep(.el-menu--collapse) .menu-item-content {
  justify-content: center;
}

/* 折叠状态下的图标容器调整 */
.is-collapsed .icon-container {
  margin: 0 auto;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .aside-wrapper {
    width: 210px;
  }
  
  .is-collapsed {
    width: 65px;
  }
  
  .menu-item {
    height: 40px;
    line-height: 40px;
  }
  
  :deep(.el-menu-item),
  :deep(.el-sub-menu__title) {
    height: 40px;
    line-height: 40px;
  }
}

/* 自定义子菜单弹出样式 */
:global(.nav-submenu-popper) {
  border-radius: 12px !important;
  background: white !important;
  border: 1px solid var(--el-border-color-light) !important;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08) !important;
}

:global(.nav-submenu-popper .el-menu) {
  background: transparent !important;
}

:global(.nav-submenu-popper .el-menu-item) {
  color: var(--el-text-color-primary) !important;
}

:global(.nav-submenu-popper .el-menu-item.is-active) {
  color: var(--el-color-primary) !important;
  background: rgba(64, 158, 255, 0.1) !important;
}

:global(.nav-submenu-popper .el-menu-item:hover) {
  background: rgba(64, 158, 255, 0.05) !important;
}
</style>

