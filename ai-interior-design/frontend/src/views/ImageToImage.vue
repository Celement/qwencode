<template>
  <div class="image-to-image-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>🖼️ 图生图 - 基于参考图生成新设计</span>
        </div>
      </template>

      <el-row :gutter="20">
        <!-- 左侧表单 -->
        <el-col :span="12">
          <el-form :model="form" label-width="100px" label-position="top">
            <el-form-item label="上传参考图" required>
              <el-upload
                ref="uploadRef"
                class="upload-demo"
                drag
                action="#"
                :auto-upload="false"
                :on-change="handleFileChange"
                :limit="1"
                accept="image/*"
              >
                <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
                <div class="el-upload__text">
                  拖拽文件到此处或<em>点击上传</em>
                </div>
              </el-upload>
            </el-form-item>

            <el-form-item label="预览参考图" v-if="previewUrl">
              <el-image
                :src="previewUrl"
                fit="contain"
                class="preview-image"
              />
            </el-form-item>

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

            <el-form-item label="修改描述" required>
              <el-input
                v-model="form.prompt"
                type="textarea"
                :rows="4"
                placeholder="描述您想要如何修改这张图片，例如：将客厅改为现代简约风格，增加大窗户，使用浅色墙面..."
              />
            </el-form-item>

            <el-form-item label="重绘强度">
              <el-slider v-model="form.strength" :min="0.1" :max="1" :step="0.1" show-input />
              <div class="slider-tip">
                <span>低 (保留更多原图)</span>
                <span>高 (更多创意变化)</span>
              </div>
            </el-form-item>

            <el-form-item>
              <el-button 
                type="primary" 
                size="large" 
                @click="generateImage"
                :loading="generating"
                :disabled="!selectedFile"
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
          </el-card>
        </el-col>

        <!-- 右侧结果展示 -->
        <el-col :span="12">
          <div class="result-area">
            <div v-if="!generatedResult" class="empty-result">
              <el-empty description="生成的图片将显示在这里" />
            </div>
            <div v-else class="result-content">
              <h4>生成结果</h4>
              <el-image
                :src="generatedResult.image_url"
                fit="contain"
                class="generated-image"
              />
              <div class="result-info">
                <p><strong>使用提示词:</strong></p>
                <p class="prompt-text">{{ generatedResult.prompt_used }}</p>
                <p><strong>参考图:</strong> {{ generatedResult.reference_image }}</p>
                <p><strong>生成类型:</strong> {{ generatedResult.generation_type }}</p>
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

const uploadRef = ref(null)
const selectedFile = ref(null)
const previewUrl = ref('')

const form = reactive({
  style: 'modern',
  prompt: '',
  strength: 0.7
})

const styles = ref([])
const generating = ref(false)
const generatedResult = ref(null)
const knowledgePrompts = ref([])

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
    const stylesRes = await baseApi.getStyles()
    styles.value = stylesRes.data
    loadKnowledgePrompts()
  } catch (error) {
    console.error('加载数据失败:', error)
  }
})

const handleFileChange = (file) => {
  selectedFile.value = file.raw
  previewUrl.value = URL.createObjectURL(file.raw)
}

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
  if (!selectedFile.value) {
    ElMessage.warning('请先上传参考图')
    return
  }
  if (!form.prompt.trim()) {
    ElMessage.warning('请输入修改描述')
    return
  }

  generating.value = true
  try {
    const formData = new FormData()
    formData.append('image', selectedFile.value)
    formData.append('prompt', form.prompt)
    formData.append('style', form.style)
    formData.append('strength', form.strength.toString())

    const res = await generateApi.imageToImage(formData)
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
    link.download = `interior_design_img2img_${Date.now()}.png`
    link.click()
    ElMessage.success('下载已开始')
  }
}
</script>

<style scoped>
.image-to-image-container {
  max-width: 1400px;
  margin: 0 auto;
}

.card-header {
  font-size: 18px;
  font-weight: bold;
}

.preview-image {
  width: 100%;
  max-height: 300px;
  border-radius: 8px;
}

.slider-tip {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
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

.result-content h4 {
  margin: 0 0 15px;
  color: #303133;
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
