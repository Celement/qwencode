<template>
  <div class="app-container">
    <el-container>
      <!-- 侧边栏导航 -->
      <el-aside width="220px" class="sidebar">
        <div class="logo">
          <el-icon><House /></el-icon>
          <span>AI 室内设计室</span>
        </div>
        <el-menu :default-active="activeMenu" router background-color="#304156" text-color="#bfcbd9" active-text-color="#409EFF">
          <el-menu-item index="/">
            <el-icon><HomeFilled /></el-icon>
            <span>首页</span>
          </el-menu-item>
          <el-menu-item index="/text-to-image">
            <el-icon><EditPen /></el-icon>
            <span>文生图</span>
          </el-menu-item>
          <el-menu-item index="/image-to-image">
            <el-icon><Picture /></el-icon>
            <span>图生图</span>
          </el-menu-item>
          <el-menu-item index="/gallery">
            <el-icon><Gallery /></el-icon>
            <span>作品展示</span>
          </el-menu-item>
          <el-menu-item index="/knowledge">
            <el-icon><Reading /></el-icon>
            <span>知识库</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 主内容区 -->
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const activeMenu = computed(() => route.path)
</script>

<style scoped>
.app-container {
  height: 100vh;
}

.el-container {
  height: 100%;
}

.sidebar {
  background-color: #304156;
  overflow-x: hidden;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 60px;
  color: #fff;
  font-size: 20px;
  font-weight: bold;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo .el-icon {
  margin-right: 10px;
  font-size: 28px;
}

.el-main {
  background-color: #f0f2f5;
  padding: 20px;
}
</style>
