<template>
  <div class="gallery-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>🖼️ 优秀设计作品展示</span>
          <div class="header-actions">
            <el-select v-model="filterStyle" placeholder="按风格筛选" clearable @change="loadWorks" style="width: 150px; margin-right: 10px;">
              <el-option label="全部风格" value="" />
              <el-option
                v-for="style in styles"
                :key="style"
                :label="styleLabel(style)"
                :value="style"
              />
            </el-select>
            <el-select v-model="filterRoomType" placeholder="按房间类型" clearable @change="loadWorks" style="width: 120px;">
              <el-option label="全部房间" value="" />
              <el-option
                v-for="room in roomTypes"
                :key="room"
                :label="room"
                :value="room"
              />
            </el-select>
          </div>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索作品名称或描述..."
          clearable
          @keyup.enter="searchWorks"
          style="width: 400px;"
        >
          <template #append>
            <el-button @click="searchWorks">
              <el-icon><Search /></el-icon>
            </el-button>
          </template>
        </el-input>
      </div>

      <!-- 作品网格 -->
      <el-row :gutter="20" v-loading="loading">
        <el-col 
          :xs="24" 
          :sm="12" 
          :md="8" 
          :lg="6"
          v-for="work in works" 
          :key="work.id"
        >
          <el-card shadow="hover" class="work-card">
            <el-image 
              :src="work.image_url" 
              fit="cover"
              class="work-image"
              :preview-src-list="[work.image_url]"
            >
              <template #placeholder>
                <div class="image-placeholder">加载中...</div>
              </template>
            </el-image>
            <div class="work-info">
              <h4>{{ work.title }}</h4>
              <div class="tags">
                <el-tag size="small" :type="getStyleType(work.style)">{{ styleLabel(work.style) }}</el-tag>
                <el-tag size="small" v-if="work.room_type">{{ work.room_type }}</el-tag>
              </div>
              <p class="description" v-if="work.description">{{ work.description }}</p>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 空状态 -->
      <el-empty v-if="!loading && works.length === 0" description="暂无作品数据" />

      <!-- 分页 -->
      <div class="pagination" v-if="works.length > 0">
        <el-pagination
          layout="total, prev, pager, next"
          :total="total"
          :page-size="pageSize"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { worksApi, baseApi } from '@/api'

const works = ref([])
const styles = ref([])
const roomTypes = ref([])
const loading = ref(false)
const filterStyle = ref('')
const filterRoomType = ref('')
const searchKeyword = ref('')
const total = ref(0)
const pageSize = ref(12)

const styleLabels = {
  modern: '现代风格',
  minimalist: '极简风格',
  industrial: '工业风格',
  scandinavian: '北欧风格',
  traditional: '传统风格',
  bohemian: '波西米亚风格',
  contemporary: '当代风格',
  rustic: '乡村风格'
}

const styleLabel = (style) => styleLabels[style] || style

const getStyleType = (style) => {
  const types = {
    modern: 'primary',
    minimalist: 'success',
    industrial: 'warning',
    scandinavian: 'info',
    traditional: '',
    bohemian: 'danger',
    contemporary: 'primary',
    rustic: 'warning'
  }
  return types[style] || ''
}

onMounted(() => {
  loadBaseData()
  loadWorks()
})

const loadBaseData = async () => {
  try {
    const [stylesRes, roomsRes] = await Promise.all([
      baseApi.getStyles(),
      baseApi.getRoomTypes()
    ])
    styles.value = stylesRes.data
    roomTypes.value = roomsRes.data
  } catch (error) {
    console.error('加载基础数据失败:', error)
  }
}

const loadWorks = async () => {
  loading.value = true
  try {
    const res = await worksApi.getList(filterStyle.value || null, filterRoomType.value || null)
    works.value = res.data
    total.value = res.data.length
  } catch (error) {
    console.error('加载作品失败:', error)
  } finally {
    loading.value = false
  }
}

const searchWorks = async () => {
  if (!searchKeyword.value.trim()) {
    loadWorks()
    return
  }
  loading.value = true
  try {
    const res = await worksApi.search(searchKeyword.value, filterStyle.value || null)
    works.value = res.data
    total.value = res.data.length
  } catch (error) {
    console.error('搜索失败:', error)
  } finally {
    loading.value = false
  }
}

const handlePageChange = (page) => {
  // 实际项目中实现分页逻辑
  console.log('页码:', page)
}
</script>

<style scoped>
.gallery-container {
  max-width: 1400px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.search-bar {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
}

.work-card {
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.work-card:hover {
  transform: translateY(-5px);
}

.work-image {
  width: 100%;
  height: 220px;
  border-radius: 4px;
}

.image-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 220px;
  background: #f5f7fa;
  color: #909399;
}

.work-info {
  padding: 15px 0 0;
}

.work-info h4 {
  margin: 0 0 10px;
  font-size: 16px;
  color: #303133;
}

.tags {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
}

.description {
  margin: 0;
  font-size: 13px;
  color: #909399;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.pagination {
  margin-top: 20px;
  text-align: center;
}
</style>
