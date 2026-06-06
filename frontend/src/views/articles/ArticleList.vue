<template>
  <div class="page-container">
    <h1 class="section-title">技术文章</h1>

    <!-- Filters -->
    <el-card class="filter-bar" shadow="never">
      <el-select v-model="filters.category_id" placeholder="分类筛选" clearable style="width: 140px">
        <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
      </el-select>
    </el-card>

    <div v-if="loading" class="loading-center">
      <el-skeleton :rows="5" animated />
    </div>

    <div v-else>
      <router-link v-for="article in articleList" :key="article.id" :to="`/articles/${article.id}`" custom v-slot="{ navigate }">
        <el-card class="article-card" shadow="hover" @click="navigate">
          <div class="article-body">
            <div class="article-content">
              <h2 class="article-title">{{ article.title }}</h2>
              <p v-if="article.summary" class="article-summary">{{ article.summary }}</p>
              <div class="article-meta">
                <span>{{ article.published_at?.slice(0, 10) }}</span>
                <span>{{ article.category?.name }}</span>
                <span>{{ article.reading_time }} 分钟阅读</span>
                <span><el-icon><View /></el-icon> {{ article.view_count }}</span>
                <span>{{ article.like_count }} 赞</span>
              </div>
              <div class="article-tags">
                <el-tag v-for="tag in article.tags" :key="tag.id" size="small" effect="plain">{{ tag.name }}</el-tag>
              </div>
            </div>
            <div v-if="article.cover_image" class="article-cover">
              <img :src="article.cover_image" :alt="article.title" />
            </div>
          </div>
        </el-card>
      </router-link>

      <el-empty v-if="articleList.length === 0" description="暂无文章" />

      <div v-if="pagination.total > 0" class="pagination-wrap">
        <el-pagination
          v-model:current-page="pagination.page"
          :page-size="pagination.page_size"
          :total="pagination.total"
          layout="prev, pager, next"
          @current-change="loadArticles"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { View } from '@element-plus/icons-vue'
import { getArticles } from '@/api/articles'
import { getCategories } from '@/api/categories'
import type { Article, Category, Pagination } from '@/types/api'

const articleList = ref<Article[]>([])
const categories = ref<Category[]>([])
const loading = ref(false)

const pagination = ref<Pagination>({
  page: 1, page_size: 10, total: 0, total_pages: 0, has_next: false, has_prev: false,
})

const filters = ref<{ category_id?: number }>({})

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
    const res = await getArticles({
      page: pagination.value.page,
      page_size: pagination.value.page_size,
      status: 1,
      ...filters.value,
    })
    if (res.data) {
      articleList.value = res.data.list
      pagination.value = res.data.pagination
    }
  } catch { /* ignore */ }
  loading.value = false
}
</script>

<style scoped>
.filter-bar {
  margin-bottom: 20px;
}

.article-card {
  margin-bottom: 16px;
  cursor: pointer;
}

.article-body {
  display: flex;
  gap: 20px;
}

.article-content {
  flex: 1;
}

.article-title {
  font-size: 18px;
  margin-bottom: 8px;
}

.article-summary {
  font-size: 14px;
  color: #909399;
  margin-bottom: 10px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  font-size: 13px;
  color: #909399;
  margin-bottom: 8px;
  span { display: flex; align-items: center; gap: 4px; }
}

.article-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.article-cover {
  width: 180px;
  min-height: 120px;
  flex-shrink: 0;
  img {
    width: 100%;
    height: 120px;
    object-fit: cover;
    border-radius: 6px;
  }
}

.loading-center {
  padding: 40px 0;
}

.pagination-wrap {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}
</style>
