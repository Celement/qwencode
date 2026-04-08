<template>
  <div class="home-container">
    <el-card class="welcome-card">
      <template #header>
        <div class="card-header">
          <span>🎨 AI Interior Design Studio</span>
        </div>
      </template>
      
      <div class="welcome-content">
        <h1>欢迎使用 AI 室内设计室</h1>
        <p class="subtitle">智能设计 · 创意无限 · 专业品质</p>
        
        <el-row :gutter="20" class="feature-grid">
          <el-col :span="12" v-for="feature in features" :key="feature.title">
            <el-card shadow="hover" class="feature-card">
              <div class="feature-icon">
                <el-icon :size="48"><component :is="feature.icon" /></el-icon>
              </div>
              <h3>{{ feature.title }}</h3>
              <p>{{ feature.description }}</p>
            </el-card>
          </el-col>
        </el-row>

        <div class="action-buttons">
          <el-button type="primary" size="large" @click="$router.push('/text-to-image')">
            <el-icon><EditPen /></el-icon>
            开始文生图
          </el-button>
          <el-button type="success" size="large" @click="$router.push('/image-to-image')">
            <el-icon><Picture /></el-icon>
            开始图生图
          </el-button>
          <el-button type="info" size="large" @click="$router.push('/gallery')">
            <el-icon><Gallery /></el-icon>
            查看作品
          </el-button>
        </div>
      </div>
    </el-card>

    <!-- 优秀案例展示 -->
    <el-card class="showcase-card" style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <span>✨ 优秀设计案例</span>
          <el-button text type="primary" @click="$router.push('/gallery')">查看更多</el-button>
        </div>
      </template>
      
      <el-row :gutter="20">
        <el-col :span="8" v-for="(work, index) in showcaseWorks" :key="index">
          <el-card shadow="hover" class="work-card">
            <el-image 
              :src="work.image" 
              fit="cover"
              class="work-image"
            />
            <div class="work-info">
              <h4>{{ work.title }}</h4>
              <el-tag size="small" :type="work.styleType">{{ work.style }}</el-tag>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { worksApi } from '@/api'

const features = [
  {
    title: '文生图',
    description: '通过文本描述快速生成室内设计效果图，支持多种风格选择',
    icon: 'EditPen'
  },
  {
    title: '图生图',
    description: '上传参考图片，基于现有设计生成新的创意方案',
    icon: 'Picture'
  },
  {
    title: '作品展示',
    description: '浏览公司优秀设计作品，按风格和房间类型分类展示',
    icon: 'Gallery'
  },
  {
    title: '知识库',
    description: '访问精选设计提示词和图稿链接，辅助 AI 生成更优质的设计',
    icon: 'Reading'
  }
]

const showcaseWorks = ref([
  {
    title: '现代简约客厅',
    style: '现代风格',
    styleType: 'primary',
    image: 'https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=400&h=300&fit=crop'
  },
  {
    title: '北欧风卧室',
    style: '北欧风格',
    styleType: 'success',
    image: 'https://images.unsplash.com/photo-1616594039964-40891a90bba8?w=400&h=300&fit=crop'
  },
  {
    title: '工业风书房',
    style: '工业风格',
    styleType: 'warning',
    image: 'https://images.unsplash.com/photo-1507089947368-19c1da9775ae?w=400&h=300&fit=crop'
  }
])
</script>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-content {
  text-align: center;
  padding: 20px 0;
}

.welcome-content h1 {
  font-size: 32px;
  color: #303133;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 18px;
  color: #909399;
  margin-bottom: 40px;
}

.feature-grid {
  margin-bottom: 40px;
}

.feature-card {
  text-align: center;
  padding: 20px;
  height: 100%;
}

.feature-icon {
  color: #409EFF;
  margin-bottom: 15px;
}

.feature-card h3 {
  margin: 10px 0;
  color: #303133;
}

.feature-card p {
  color: #909399;
  line-height: 1.6;
}

.action-buttons {
  margin-top: 30px;
}

.action-buttons .el-button {
  margin: 0 10px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.work-card {
  margin-bottom: 20px;
}

.work-image {
  width: 100%;
  height: 200px;
  border-radius: 4px;
}

.work-info {
  padding: 15px 0 0;
}

.work-info h4 {
  margin: 0 0 10px;
  font-size: 16px;
}
</style>
