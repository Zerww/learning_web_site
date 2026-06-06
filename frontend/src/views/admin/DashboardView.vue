<template>
  <div>
    <h2 class="section-title">概览</h2>
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-num">{{ stats.article_count }}</div>
            <div class="stat-desc">文章总数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-num">{{ stats.project_count }}</div>
            <div class="stat-desc">项目总数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-num">{{ stats.total_comments }}</div>
            <div class="stat-desc">评论总数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-num">{{ stats.total_views }}</div>
            <div class="stat-desc">总访问量</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getArticles } from '@/api/articles'
import { getProjects } from '@/api/projects'

const stats = ref({
  article_count: 0,
  project_count: 0,
  total_comments: 0,
  total_views: 0,
})

onMounted(async () => {
  try {
    const [articleRes, projectRes] = await Promise.all([
      getArticles({ page_size: 1, status: 1 }),
      getProjects({ page_size: 1, status: 1 }),
    ])
    stats.value.article_count = articleRes.data?.pagination?.total ?? 0
    stats.value.project_count = projectRes.data?.pagination?.total ?? 0
  } catch { /* ignore */ }
})
</script>

<style scoped>
.stat-card {
  text-align: center;
  padding: 10px 0;
}
.stat-num {
  font-size: 32px;
  font-weight: 700;
  color: var(--primary-color, #409eff);
  line-height: 1.4;
}
.stat-desc {
  font-size: 14px;
  color: var(--text-color, #909399);
  margin-top: 4px;
}
</style>
