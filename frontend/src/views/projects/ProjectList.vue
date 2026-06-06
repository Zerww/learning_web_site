<template>
  <div class="page-container">
    <h1 class="section-title">项目作品</h1>

    <!-- Filters -->
    <el-card class="filter-bar" shadow="never">
      <el-select v-model="filters.category_id" placeholder="分类筛选" clearable style="width: 140px">
        <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
      </el-select>
      <el-select v-model="filters.difficulty" placeholder="难度" clearable style="width: 120px; margin-left: 12px">
        <el-option label="入门" :value="1" />
        <el-option label="中级" :value="2" />
        <el-option label="高级" :value="3" />
      </el-select>
    </el-card>

    <!-- Project Grid -->
    <div v-if="loading" class="loading-center">
      <el-skeleton :rows="3" animated />
    </div>

    <el-row v-else :gutter="24">
      <el-col v-for="project in projectList" :key="project.id" :xs="24" :sm="12" :md="8">
        <router-link :to="`/projects/${project.id}`" custom v-slot="{ navigate }">
          <el-card class="project-card" shadow="hover" @click="navigate">
            <div v-if="project.cover_image" class="project-cover">
              <img :src="project.cover_image" :alt="project.title" />
            </div>
            <div class="project-info">
              <h3 class="project-title">{{ project.title }}</h3>
              <p class="project-desc">{{ project.description }}</p>
              <div class="project-meta">
                <el-tag v-for="tech in project.tech_stack?.slice(0, 3)" :key="tech" size="small" class="meta-tag">
                  {{ tech }}
                </el-tag>
              </div>
              <div class="project-stats">
                <span><el-icon><View /></el-icon> {{ project.view_count }}</span>
                <span>{{ project.like_count }} 赞</span>
              </div>
            </div>
          </el-card>
        </router-link>
      </el-col>
    </el-row>

    <!-- Empty State -->
    <el-empty v-if="!loading && projectList.length === 0" description="暂无项目" />

    <!-- Pagination -->
    <div v-if="pagination.total > 0" class="pagination-wrap">
      <el-pagination
        v-model:current-page="pagination.page"
        :page-size="pagination.page_size"
        :total="pagination.total"
        layout="prev, pager, next"
        @current-change="loadProjects"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { View } from '@element-plus/icons-vue'
import { getProjects } from '@/api/projects'
import { getCategories } from '@/api/categories'
import type { Project, Category, Pagination } from '@/types/api'

const projectList = ref<Project[]>([])
const categories = ref<Category[]>([])
const loading = ref(false)

const pagination = ref<Pagination>({
  page: 1, page_size: 12, total: 0, total_pages: 0, has_next: false, has_prev: false,
})

const filters = ref<{ category_id?: number; difficulty?: number }>({})

onMounted(async () => {
  try {
    const catRes = await getCategories({ type: 1 })
    categories.value = catRes.data?.list || []
  } catch { /* ignore */ }
  await loadProjects()
})

async function loadProjects() {
  loading.value = true
  try {
    const res = await getProjects({
      page: pagination.value.page,
      page_size: pagination.value.page_size,
      status: 1,
      ...filters.value,
    })
    if (res.data) {
      projectList.value = res.data.list
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

.project-card {
  margin-bottom: 24px;
  cursor: pointer;
}

.project-cover {
  width: 100%;
  height: 180px;
  overflow: hidden;
  border-radius: 8px 8px 0 0;
  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.project-info {
  padding: 4px 0;
}

.project-title {
  font-size: 18px;
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.project-desc {
  font-size: 14px;
  color: #909399;
  margin-bottom: 10px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.project-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 8px;
}

.meta-tag {
  font-size: 12px;
}

.project-stats {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: #909399;
  span { display: flex; align-items: center; gap: 4px; }
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
