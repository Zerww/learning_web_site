<template>
  <div class="page-wrap-narrow">
    <!-- Back button -->
    <div class="back-row fade-up">
      <BackButton to="/projects" label="所有项目" />
    </div>

    <div v-if="loading" class="loading-wrap fade-up-1">
      <div class="skeleton-pulse" style="height:32px; width:60%; margin-bottom:16px"></div>
      <div class="skeleton-pulse" style="height:16px; width:40%; margin-bottom:32px"></div>
      <div class="skeleton-pulse" style="height:400px"></div>
    </div>

    <div v-else-if="project" class="detail-layout fade-up-1">
      <article class="glass-card detail-card">
        <h1 class="detail-title">{{ project.title }}</h1>

        <div class="detail-meta">
          <span class="meta-item">{{ project.author?.nickname }}</span>
          <span class="meta-dot">·</span>
          <span class="meta-item">{{ project.published_at?.slice(0,10) }}</span>
          <span class="meta-dot">·</span>
          <span class="meta-item">{{ difficultyLabel }}</span>
        </div>

        <!-- Tags -->
        <div class="detail-tags">
          <span v-for="t in project.tags" :key="t.id" class="tag-badge" :style="{ background: t.color + '18', color: t.color }">
            {{ t.name }}
          </span>
          <span v-for="t in project.tech_stack" :key="t" class="tag-badge tech-tag">{{ t }}</span>
        </div>

        <!-- Cover -->
        <div v-if="project.cover_image" class="detail-cover">
          <img :src="project.cover_image" :alt="project.title" />
        </div>

        <!-- Content -->
        <div class="markdown-content" v-html="renderedContent" />

        <!-- Links -->
        <div class="detail-links">
          <a v-if="project.github_url" :href="project.github_url" target="_blank" class="link-btn">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>
            GitHub
          </a>
          <a v-if="project.demo_url" :href="project.demo_url" target="_blank" class="link-btn primary">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
            在线演示
          </a>
        </div>

        <!-- Actions -->
        <div class="detail-actions">
          <button :class="['action-btn', { active: isLiked }]" @click="toggleLike">
            <svg width="18" height="18" viewBox="0 0 24 24" :fill="isLiked ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3H14zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"/></svg>
            {{ project.like_count }}
          </button>
          <button :class="['action-btn', { active: isFavorited }]" @click="toggleFavorite">
            <svg width="18" height="18" viewBox="0 0 24 24" :fill="isFavorited ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            {{ project.favorite_count }}
          </button>
        </div>
      </article>

      <!-- Related -->
      <aside v-if="project.related_projects?.length" class="glass-card related-card fade-up-2">
        <h3 class="related-title">相关项目</h3>
        <div class="related-list">
          <router-link v-for="rp in project.related_projects" :key="rp.id" :to="`/projects/${rp.id}`" class="related-item">
            <span class="related-name">{{ rp.title }}</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m9 18 6-6-6-6"/></svg>
          </router-link>
        </div>
      </aside>
    </div>

    <div v-else class="error-wrap fade-up-1">
      <span class="error-icon">◎</span>
      <p>项目不存在或已删除</p>
      <BackButton to="/projects" label="返回项目列表" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { marked } from 'marked'
import BackButton from '@/components/common/BackButton.vue'
import { getProjectDetail } from '@/api/projects'
import { like, unlike, favorite, unfavorite } from '@/api/interactions'
import type { ProjectDetail } from '@/types/api'

const route = useRoute()
const project = ref<ProjectDetail | null>(null)
const loading = ref(true)
const isLiked = ref(false)
const isFavorited = ref(false)

const renderedContent = computed(() => {
  if (!project.value?.content) return ''
  return marked(project.value.content, { async: false }) as string
})

const difficultyLabel = computed(() => {
  const map: Record<number, string> = { 1: '入门', 2: '中级', 3: '高级' }
  return map[project.value?.difficulty || 0] || '未知'
})

onMounted(async () => {
  const id = Number(route.params.id)
  if (!id) { loading.value = false; return }
  try {
    const res = await getProjectDetail(id)
    if (res.data) {
      project.value = res.data
      isLiked.value = res.data.is_liked
      isFavorited.value = res.data.is_favorited
    }
  } catch { /* ignore */ }
  loading.value = false
})

async function toggleLike() {
  if (!project.value) return
  try {
    if (isLiked.value) {
      const res = await unlike({ content_type: 2, object_id: project.value.id })
      isLiked.value = false
      project.value.like_count = res.data?.like_count ?? project.value.like_count - 1
    } else {
      const res = await like({ content_type: 2, object_id: project.value.id })
      isLiked.value = true
      project.value.like_count = res.data?.like_count ?? project.value.like_count + 1
    }
  } catch { /* ignore */ }
}

async function toggleFavorite() {
  if (!project.value) return
  try {
    if (isFavorited.value) {
      const res = await unfavorite({ content_type: 2, object_id: project.value.id })
      isFavorited.value = false
      project.value.favorite_count = res.data?.favorite_count ?? project.value.favorite_count - 1
    } else {
      const res = await favorite({ content_type: 2, object_id: project.value.id })
      isFavorited.value = true
      project.value.favorite_count = res.data?.favorite_count ?? project.value.favorite_count + 1
    }
  } catch { /* ignore */ }
}
</script>

<style scoped>
.back-row { margin-bottom: 20px; }

.loading-wrap { padding: 20px 0; display: flex; flex-direction: column; gap: 12px; }

.detail-layout { display: flex; flex-direction: column; gap: 24px; }

.detail-card { padding: 36px; }

.detail-title {
  font-size: 30px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.03em;
  margin-bottom: 12px;
  line-height: 1.3;
}

.detail-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--text-muted);
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.meta-dot { opacity: 0.3; }

.detail-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 24px;
}

.tag-badge {
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
}

.tech-tag {
  background: var(--stone-100);
  color: var(--stone-500);
}

.detail-cover {
  margin-bottom: 28px;
  img { width: 100%; border-radius: 12px; }
}

.detail-links {
  display: flex;
  gap: 10px;
  margin-top: 28px;
  flex-wrap: wrap;
}

.link-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  font-family: 'DM Sans', sans-serif;
  text-decoration: none;
  border: 1.5px solid var(--stone-200);
  color: var(--text-secondary);
  transition: all 0.2s ease;
}

.link-btn:hover {
  border-color: var(--stone-300);
  color: var(--text-primary);
}

.link-btn.primary {
  background: linear-gradient(135deg, var(--accent), var(--accent-dark));
  border-color: transparent;
  color: #fff;
}

.link-btn.primary:hover {
  box-shadow: 0 4px 16px rgba(245,158,11,0.3);
  transform: translateY(-1px);
}

.detail-actions {
  display: flex;
  gap: 10px;
  margin-top: 28px;
  padding-top: 24px;
  border-top: 1px solid var(--stone-200);
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 18px;
  border: 1.5px solid var(--stone-200);
  border-radius: 10px;
  background: transparent;
  color: var(--text-secondary);
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn:hover { border-color: var(--accent); color: var(--accent-dark); }
.action-btn.active { border-color: var(--accent); color: var(--accent-dark); background: rgba(245,158,11,0.06); }

/* Related */
.related-card { padding: 24px; }
.related-title { font-size: 16px; font-weight: 600; margin-bottom: 12px; }
.related-list { display: flex; flex-direction: column; gap: 4px; }
.related-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  border-radius: 8px;
  color: var(--text-primary);
  text-decoration: none;
  font-size: 14px;
  transition: background 0.2s;
}
.related-item:hover { background: rgba(245,158,11,0.06); }
.related-name { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

/* Error */
.error-wrap { text-align: center; padding: 60px 0; }
.error-icon { font-size: 40px; color: var(--stone-300); display: block; margin-bottom: 12px; }
.error-wrap p { color: var(--text-muted); margin-bottom: 20px; }

@media (max-width: 600px) {
  .detail-card { padding: 24px; }
  .detail-title { font-size: 24px; }
}
</style>
