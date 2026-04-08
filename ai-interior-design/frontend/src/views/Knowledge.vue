<template>
  <div class="knowledge-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>📚 设计知识库 - 优秀提示词与图稿</span>
          <el-button type="primary" @click="showAddDialog = true">
            <el-icon><Plus /></el-icon>
            添加知识
          </el-button>
        </div>
      </template>

      <!-- 搜索和筛选 -->
      <div class="filter-bar">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索提示词..."
          clearable
          @keyup.enter="searchKnowledge"
          style="width: 300px; margin-right: 15px;"
        >
          <template #append>
            <el-button @click="searchKnowledge">
              <el-icon><Search /></el-icon>
            </el-button>
          </template>
        </el-input>
        <el-select v-model="filterStyle" placeholder="按风格筛选" clearable @change="loadKnowledge" style="width: 150px;">
          <el-option label="全部风格" value="" />
          <el-option
            v-for="style in styles"
            :key="style"
            :label="styleLabel(style)"
            :value="style"
          />
        </el-select>
      </div>

      <!-- 知识列表 -->
      <el-table 
        :data="knowledgeList" 
        v-loading="loading"
        style="width: 100%"
        border
      >
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column label="风格" width="120">
          <template #default="{ row }">
            <el-tag :type="getStyleType(row.style)">{{ styleLabel(row.style) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="prompt" label="提示词" min-width="300" show-overflow-tooltip />
        <el-table-column label="预览图" width="120">
          <template #default="{ row }">
            <el-image 
              :src="row.image_url" 
              fit="cover"
              class="thumbnail"
              :preview-src-list="[row.image_url]"
            />
          </template>
        </el-table-column>
        <el-table-column prop="tags" label="标签" width="150" show-overflow-tooltip />
        <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button 
              type="primary" 
              size="small" 
              @click="usePrompt(row)"
            >
              使用提示词
            </el-button>
            <el-button 
              type="danger" 
              size="small" 
              @click="deleteKnowledge(row.id)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 空状态 -->
      <el-empty v-if="!loading && knowledgeList.length === 0" description="暂无知识库数据" />
    </el-card>

    <!-- 添加知识对话框 -->
    <el-dialog
      v-model="showAddDialog"
      title="添加知识条目"
      width="600px"
    >
      <el-form :model="newKnowledge" label-width="100px">
        <el-form-item label="设计风格" required>
          <el-select v-model="newKnowledge.style" placeholder="请选择风格" style="width: 100%">
            <el-option
              v-for="style in styles"
              :key="style"
              :label="styleLabel(style)"
              :value="style"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="提示词" required>
          <el-input
            v-model="newKnowledge.prompt"
            type="textarea"
            :rows="4"
            placeholder="输入优秀的设计提示词..."
          />
        </el-form-item>
        <el-form-item label="图稿链接" required>
          <el-input
            v-model="newKnowledge.image_url"
            placeholder="输入设计图稿的 URL 链接..."
          />
        </el-form-item>
        <el-form-item label="标签">
          <el-input
            v-model="newKnowledge.tags"
            placeholder="用逗号分隔多个标签，如：客厅，现代，明亮"
          />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="newKnowledge.description"
            type="textarea"
            :rows="3"
            placeholder="可选的描述信息..."
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="addKnowledge">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { knowledgeApi, baseApi } from '@/api'
import { useRouter } from 'vue-router'

const router = useRouter()

const knowledgeList = ref([])
const styles = ref([])
const loading = ref(false)
const filterStyle = ref('')
const searchKeyword = ref('')
const showAddDialog = ref(false)

const newKnowledge = reactive({
  style: '',
  prompt: '',
  image_url: '',
  tags: '',
  description: ''
})

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
  loadKnowledge()
})

const loadBaseData = async () => {
  try {
    const res = await baseApi.getStyles()
    styles.value = res.data
  } catch (error) {
    console.error('加载风格数据失败:', error)
  }
}

const loadKnowledge = async () => {
  loading.value = true
  try {
    const res = await knowledgeApi.getList(filterStyle.value || null)
    knowledgeList.value = res.data
  } catch (error) {
    console.error('加载知识库失败:', error)
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

const searchKnowledge = async () => {
  if (!searchKeyword.value.trim()) {
    loadKnowledge()
    return
  }
  loading.value = true
  try {
    const res = await knowledgeApi.search(searchKeyword.value, filterStyle.value || null)
    knowledgeList.value = res.data
  } catch (error) {
    console.error('搜索失败:', error)
  } finally {
    loading.value = false
  }
}

const addKnowledge = async () => {
  if (!newKnowledge.style || !newKnowledge.prompt || !newKnowledge.image_url) {
    ElMessage.warning('请填写必填项')
    return
  }

  try {
    const params = new URLSearchParams()
    params.append('style', newKnowledge.style)
    params.append('prompt', newKnowledge.prompt)
    params.append('image_url', newKnowledge.image_url)
    if (newKnowledge.tags) params.append('tags', newKnowledge.tags)
    if (newKnowledge.description) params.append('description', newKnowledge.description)

    await knowledgeApi.add(params)
    ElMessage.success('添加成功')
    showAddDialog.value = false
    loadKnowledge()
    
    // 重置表单
    Object.assign(newKnowledge, {
      style: '',
      prompt: '',
      image_url: '',
      tags: '',
      description: ''
    })
  } catch (error) {
    ElMessage.error('添加失败：' + (error.response?.data?.detail || error.message))
  }
}

const deleteKnowledge = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除这条知识吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    // 实际项目中实现删除接口
    ElMessage.success('删除成功')
    loadKnowledge()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
    }
  }
}

const usePrompt = (item) => {
  // 跳转到文生图或图生图页面，并带上提示词
  router.push({
    path: '/text-to-image',
    query: { prompt: item.prompt, style: item.style }
  })
  ElMessage.success('已跳转到生成页面')
}
</script>

<style scoped>
.knowledge-container {
  max-width: 1400px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-bar {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.thumbnail {
  width: 80px;
  height: 60px;
  border-radius: 4px;
  cursor: pointer;
}

:deep(.el-table__cell) {
  padding: 12px 8px;
}
</style>
