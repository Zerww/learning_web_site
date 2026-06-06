<template>
  <div class="page-container home-page">
    <!-- Hero Section -->
    <section class="hero-section card">
      <div class="hero-content">
        <el-avatar :size="100" :src="homeData?.profile.avatar || undefined" class="hero-avatar">
          {{ homeData?.profile.nickname.charAt(0) || 'M' }}
        </el-avatar>
        <h1 class="hero-name">{{ homeData?.profile.nickname || '欢迎来到我的学习空间' }}</h1>
        <p class="hero-bio">{{ homeData?.profile.bio || '记录学习历程，展示项目作品，分享技术知识' }}</p>

        <!-- Skills -->
        <div class="skill-tags">
          <el-tag
            v-for="skill in homeData?.profile.skills || []"
            :key="skill"
            type="primary"
            effect="plain"
            class="skill-tag"
          >
            {{ skill }}
          </el-tag>
        </div>

        <!-- Statistics -->
        <div class="stat-row">
          <div class="stat-item">
            <span class="stat-value">{{ homeData?.statistics.article_count || 0 }}</span>
            <span class="stat-label">文章</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ homeData?.statistics.project_count || 0 }}</span>
            <span class="stat-label">项目</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ formatViews(homeData?.statistics.total_views || 0) }}</span>
            <span class="stat-label">访问量</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ homeData?.statistics.total_likes || 0 }}</span>
            <span class="stat-label">获赞</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Featured Projects -->
    <section v-if="homeData?.featured_projects?.length" class="section">
      <h2 class="section-title">推荐项目</h2>
      <el-row :gutter="20">
        <el-col v-for="project in homeData?.featured_projects" :key="project.id" :xs="24" :sm="12" :md="8">
          <router-link :to="`/projects/${project.id}`" custom v-slot="{ navigate }">
            <el-card class="content-card" shadow="hover" @click="navigate">
              <div v-if="project.cover_image" class="card-image">
                <img :src="project.cover_image" :alt="project.title" />
              </div>
              <div class="card-body">
                <h3>{{ project.title }}</h3>
              </div>
            </el-card>
          </router-link>
        </el-col>
      </el-row>
    </section>

    <!-- Latest Articles -->
    <section v-if="homeData?.latest_articles?.length" class="section">
      <h2 class="section-title">最新文章</h2>
      <el-timeline>
        <el-timeline-item
          v-for="article in homeData?.latest_articles"
          :key="article.id"
          :timestamp="article.published_at"
          placement="top"
        >
          <router-link :to="`/articles/${article.id}`" custom v-slot="{ navigate }">
            <el-card shadow="hover" @click="navigate">
              <h3>{{ article.title }}</h3>
            </el-card>
          </router-link>
        </el-timeline-item>
      </el-timeline>
    </section>

    <!-- Popular Tags -->
    <section v-if="homeData?.popular_tags?.length" class="section">
      <h2 class="section-title">热门标签</h2>
      <div class="tag-cloud">
        <router-link
          v-for="tag in homeData?.popular_tags"
          :key="tag.id"
          :to="{ name: 'Articles', query: { tags: tag.id } }"
          custom
          v-slot="{ navigate }"
        >
          <el-tag
            :class="['cloud-tag', `tag-size-${getTagSize(tag.usage_count)}`]"
            type="primary"
            effect="plain"
            @click="navigate"
          >
            {{ tag.name }}
          </el-tag>
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getHomeData } from '@/api/home'
import type { HomeData } from '@/types/api'

const homeData = ref<HomeData | null>(null)
const maxUsage = ref(1)

onMounted(async () => {
  try {
    const res = await getHomeData()
    if (res.data) {
      homeData.value = res.data
      maxUsage.value = Math.max(
        ...(res.data.popular_tags?.map((t) => t.usage_count) || [1]),
      )
    }
  } catch {
    // Handle error silently
  }
})

function formatViews(count: number): string {
  if (count >= 10000) return (count / 10000).toFixed(1) + 'w'
  if (count >= 1000) return (count / 1000).toFixed(1) + 'k'
  return String(count)
}

function getTagSize(count: number): string {
  const ratio = count / maxUsage.value
  if (ratio > 0.8) return 'lg'
  if (ratio > 0.5) return 'md'
  return 'sm'
}
</script>

<style scoped>
.home-page {
  padding-top: 20px;
}

.hero-section {
  text-align: center;
  padding: 40px 20px;
  margin-bottom: 30px;
}

.hero-avatar {
  margin-bottom: 16px;
  border: 3px solid var(--primary-color);
}

.hero-name {
  font-size: 28px;
  margin-bottom: 12px;
}

.hero-bio {
  color: #909399;
  font-size: 16px;
  margin-bottom: 20px;
}

.skill-tags {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 24px;
}

.skill-tag {
  font-size: 14px;
}

.stat-row {
  display: flex;
  justify-content: center;
  gap: 40px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--primary-color);
}

.stat-label {
  font-size: 13px;
  color: #909399;
  margin-top: 4px;
}

.section {
  margin-bottom: 30px;
}

.content-card {
  margin-bottom: 20px;
  cursor: pointer;
}

.card-image {
  width: 100%;
  height: 160px;
  overflow: hidden;
  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.card-body {
  padding: 8px 0;
  h3 {
    font-size: 16px;
    font-weight: 500;
  }
}

.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
  padding: 10px 0;
}

.cloud-tag {
  cursor: pointer;
  transition: transform 0.2s;
  &:hover {
    transform: scale(1.1);
  }
}

.tag-size-lg { font-size: 18px; }
.tag-size-md { font-size: 14px; }
.tag-size-sm { font-size: 12px; }
</style>
