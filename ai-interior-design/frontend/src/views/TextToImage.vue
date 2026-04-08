<template>
  <div class="text-to-image-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>📝 文生图 - 文本描述生成室内设计</span>
        </div>
      </template>

      <el-row :gutter="20">
        <!-- 左侧表单 -->
        <el-col :span="12">
          <el-form :model="form" label-width="100px" label-position="top">
            <el-form-item label="设计风格">
              <el-select v-model="form.style" placeholder="请选择风格" style="width: 100%">
                <el-option
                  v-for="style in styles"
                  :key="style"
                  :label="styleLabel(style)"
                  :value="style"
                />
              </el-select>
            </el-form-item>

            <el-form-item label="房间类型">
              <el-select v-model="form.roomType" placeholder="请选择房间类型" style="width: 100%">
                <el-option
                  v-for="room in roomTypes"
                  :key="room"
                  :label="room"
                  :value="room"
                />
              </el-select>
            </el-form-item>

            <el-form-item label="设计描述" required>
              <el-input
                v-model="form.prompt"
                type="textarea"
                :rows="6"
                placeholder="请详细描述您想要的室内设计效果，例如：一个明亮宽敞的现代客厅，有大落地窗，浅色木地板，灰色布艺沙发，简约的茶几，墙上挂着抽象艺术画..."
              />
            </el-form-item>

            <el-form-item label="负面提示词">
              <el-input
                v-model="form.negativePrompt"
                placeholder="不希望出现的内容，例如：模糊、低质量、变形"
              />
            </el-form-item>

            <el-form-item>
              <el-button 
                type="primary" 
                size="large" 
                @click="generateImage"
                :loading="generating"
                style="width: 100%"
              >
                <el-icon><MagicStick /></el-icon>
                {{ generating ? '生成中...' : '开始生成' }}
              </el-button>
            </el-form-item>
          </el-form>

          <!-- 知识库提示词推荐 -->
          <el-card shadow="never" class="knowledge-card">
            <template #header>
              <span>💡 知识库提示词推荐</span>
            </template>
            <el-tag
              v-for="(item, index) in knowledgePrompts"
              :key="index"
              closable
              @close="removePrompt(index)"
              @click="addPrompt(item.prompt)"
              style="margin: 5px;"
            >
              {{ item.prompt.substring(0, 20) }}...
            </el-tag>
            <el-button text type="primary" size="small" @click="loadKnowledgePrompts">
              加载更多
            </el-button>
          </el-card>
        </el-col>

        <!-- 右侧结果展示 -->
        <el-col :span="12">
          <div class="result-area">
            <div v-if="!generatedResult" class="empty-result">
              <el-empty description="生成的图片将显示在这里" />
            </div>
            <div v-else class="result-content">
              <el-image
                :src="generatedResult.image_url"
                fit="contain"
                class="generated-image"
              />
              <div class="result-info">
                <h4>生成信息</h4>
                <p><strong>使用提示词:</strong></p>
                <p class="prompt-text">{{ generatedResult.prompt_used }}</p>
                <p><strong>生成类型:</strong> {{ generatedResult.generation_type }}</p>
                <p><strong>知识库增强:</strong> 
                  <el-tag type="success" size="small">已启用</el-tag>
                </p>
              </div>
              <el-button type="success" @click="downloadImage">
                <el-icon><Download /></el-icon>
                下载图片
              </el-button>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { generateApi, knowledgeApi, baseApi } from '@/api'

const form = reactive({
  style: 'modern',
  roomType: '客厅',
  prompt: '',
  negativePrompt: 'blurry, low quality, distorted'
})

const styles = ref([])
const roomTypes = ref([])
const generating = ref(false)
const generatedResult = ref(null)
const knowledgePrompts = ref([])

// 风格标签映射
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

onMounted(async () => {
  try {
    const [stylesRes, roomsRes] = await Promise.all([
      baseApi.getStyles(),
      baseApi.getRoomTypes()
    ])
    styles.value = stylesRes.data
    roomTypes.value = roomsRes.data
    loadKnowledgePrompts()
  } catch (error) {
    console.error('加载数据失败:', error)
  }
})

const loadKnowledgePrompts = async () => {
  try {
    const res = await knowledgeApi.getList(form.style)
    knowledgePrompts.value = res.data.slice(0, 10)
  } catch (error) {
    console.error('加载知识库失败:', error)
  }
}

const addPrompt = (prompt) => {
  if (form.prompt) {
    form.prompt += ', ' + prompt
  } else {
    form.prompt = prompt
  }
  ElMessage.success('提示词已添加')
}

const removePrompt = (index) => {
  knowledgePrompts.value.splice(index, 1)
}

const generateImage = async () => {
  if (!form.prompt.trim()) {
    ElMessage.warning('请输入设计描述')
    return
  }

  generating.value = true
  try {
    const params = new URLSearchParams()
    params.append('prompt', form.prompt)
    params.append('style', form.style)
    params.append('negative_prompt', form.negativePrompt)

    const res = await generateApi.textToImage(params)
    generatedResult.value = res.data
    ElMessage.success('图片生成成功！')
  } catch (error) {
    ElMessage.error('生成失败：' + (error.response?.data?.detail || error.message))
  } finally {
    generating.value = false
  }
}

const downloadImage = () => {
  if (generatedResult.value?.image_url) {
    const link = document.createElement('a')
    link.href = generatedResult.value.image_url
    link.download = `interior_design_${Date.now()}.png`
    link.click()
    ElMessage.success('下载已开始')
  }
}
</script>

<style scoped>
.text-to-image-container {
  max-width: 1400px;
  margin: 0 auto;
}

.card-header {
  font-size: 18px;
  font-weight: bold;
}

.result-area {
  background: #f5f7fa;
  border-radius: 8px;
  padding: 20px;
  min-height: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-result {
  width: 100%;
}

.result-content {
  width: 100%;
  text-align: center;
}

.generated-image {
  width: 100%;
  max-height: 400px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.result-info {
  text-align: left;
  margin: 20px 0;
  padding: 15px;
  background: #fff;
  border-radius: 8px;
}

.result-info h4 {
  margin: 0 0 10px;
  color: #303133;
}

.result-info p {
  margin: 8px 0;
  color: #606266;
  font-size: 14px;
}

.prompt-text {
  background: #f0f9eb;
  padding: 10px;
  border-radius: 4px;
  color: #67c23a;
}

.knowledge-card {
  margin-top: 20px;
}

.knowledge-card :deep(.el-card__header) {
  padding: 10px 15px;
  font-size: 14px;
}
</style>
