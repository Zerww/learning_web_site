<template>
  <div>
    <div class="admin-header-bar">
      <h2 class="section-title" style="margin-bottom: 0">文章管理</h2>
      <el-button type="primary" @click="showDialog = true">新增文章</el-button>
    </div>

    <el-table :data="articles" border stripe v-loading="loading" style="width: 100%">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="title" label="标题" min-width="200" />
      <el-table-column prop="category.name" label="分类" width="100" />
      <el-table-column prop="view_count" label="浏览" width="80" />
      <el-table-column prop="status" label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.status === 1 ? 'success' : 'info'" size="small">
            {{ row.status === 1 ? '已发布' : '草稿' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="published_at" label="发布时间" width="180" />
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="showDialog" title="新增文章" width="600px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="标题" required>
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="摘要">
          <el-input v-model="form.summary" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="内容" required>
          <el-input v-model="form.content" type="textarea" :rows="8" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="form.category_id" placeholder="选择分类" style="width: 100%">
            <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="handleCreate">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getArticles, createArticle, deleteArticle } from '@/api/articles'
import { getCategories } from '@/api/categories'
import type { Article, Category } from '@/types/api'

const articles = ref<Article[]>([])
const categories = ref<Category[]>([])
const loading = ref(false)
const showDialog = ref(false)

const form = ref({
  title: '',
  summary: '',
  content: '',
  category_id: undefined as number | undefined,
  status: 1,
})

onMounted(async () => {
  try {
    const catRes = await getCategories({ type: 2 })
    categories.value = catRes.data?.list || []
  } catch { /* ignore */ }
  await loadArticles()
})

async function loadArticles() {
  loading.value = true
  try {
    const res = await getArticles({ page_size: 50 })
    if (res.data) articles.value = res.data.list
  } catch (err: any) {
    const msg = err?.response?.data?.message || err?.message || '加载失败'
    ElMessage.error(msg)
  }
  loading.value = false
}

function generateSlug(title: string): string {
  // Use timestamp + random as slug for non-ASCII titles
  const ascii = title.replace(/[^\x00-\x7F]/g, '').trim()
  if (ascii.length > 0) {
    return ascii.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '') || 'article-' + Date.now()
  }
  return 'article-' + Date.now()
}

async function handleCreate() {
  try {
    await createArticle({ ...form.value, slug: generateSlug(form.value.title) } as any)
    ElMessage.success('创建成功')
    showDialog.value = false
    form.value = { title: '', summary: '', content: '', category_id: undefined, status: 1 }
    await loadArticles()
  } catch (err: any) {
    const msg = err?.response?.data?.message || err?.message || '创建失败'
    ElMessage.error(msg)
  }
}

async function handleDelete(id: number) {
  try {
    await ElMessageBox.confirm('确定删除该文章？', '提示')
    await deleteArticle(id)
    ElMessage.success('删除成功')
    await loadArticles()
  } catch (err: any) {
    if (err !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}
</script>

<style scoped>
.admin-header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style>
