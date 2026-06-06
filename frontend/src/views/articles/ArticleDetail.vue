<template>
  <div class="page-wrap-narrow">
    <div class="back-row fade-up">
      <BackButton to="/articles" label="所有文章" />
    </div>

    <div v-if="loading" class="loading-wrap fade-up-1">
      <div class="skeleton-pulse" style="height:32px; width:70%; margin-bottom:12px"></div>
      <div class="skeleton-pulse" style="height:16px; width:50%; margin-bottom:28px"></div>
      <div class="skeleton-pulse" style="height:500px"></div>
    </div>

    <article v-else-if="article" class="glass-card article-card fade-up-1">
      <h1 class="article-title">{{ article.title }}</h1>

      <div class="article-meta">
        <span>{{ article.author?.nickname }}</span>
        <span class="dot">·</span>
        <span>{{ article.published_at?.slice(0,10) }}</span>
        <span class="dot">·</span>
        <span>{{ article.reading_time }} 分钟</span>
        <span class="dot">·</span>
        <span>{{ article.word_count }} 字</span>
      </div>

      <div class="article-tags">
        <span v-for="t in article.tags" :key="t.id" class="tag-pill">{{ t.name }}</span>
      </div>

      <div class="markdown-content" v-html="renderedContent" />

      <!-- Navigation -->
      <nav class="article-nav">
        <router-link v-if="article.prev_article" :to="`/articles/${article.prev_article.id}`" class="nav-link prev">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
          <span class="nav-text">{{ article.prev_article.title }}</span>
        </router-link>
        <span v-else />
        <router-link v-if="article.next_article" :to="`/articles/${article.next_article.id}`" class="nav-link next">
          <span class="nav-text">{{ article.next_article.title }}</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 12h14M12 5l7 7-7 7"/></svg>
        </router-link>
      </nav>

      <!-- Actions -->
      <div class="article-actions">
        <button :class="['action-btn', { active: isLiked }]" @click="toggleLike">
          <svg width="18" height="18" viewBox="0 0 24 24" :fill="isLiked ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3H14zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"/></svg>
          {{ article.like_count }}
        </button>
        <button :class="['action-btn', { active: isFavorited }]" @click="toggleFavorite">
          <svg width="18" height="18" viewBox="0 0 24 24" :fill="isFavorited ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
          {{ article.favorite_count }}
        </button>
      </div>
    </article>

    <aside v-if="article?.related_articles?.length" class="glass-card related-card fade-up-2">
      <h3 class="related-title">相关文章</h3>
      <div class="related-list">
        <router-link v-for="ra in article.related_articles" :key="ra.id" :to="`/articles/${ra.id}`" class="related-item">
          <span>{{ ra.title }}</span>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m9 18 6-6-6-6"/></svg>
        </router-link>
      </div>
    </aside>

    <div v-else-if="!loading" class="error-wrap fade-up-1">
      <span class="error-icon">◎</span>
      <p>文章不存在或已删除</p>
      <BackButton to="/articles" label="返回文章列表" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { marked } from 'marked'
import BackButton from '@/components/common/BackButton.vue'
import { getArticleDetail } from '@/api/articles'
import { like, unlike, favorite, unfavorite } from '@/api/interactions'
import type { ArticleDetail } from '@/types/api'

const route = useRoute()
const article = ref<ArticleDetail | null>(null)
const loading = ref(true)
const isLiked = ref(false)
const isFavorited = ref(false)

const renderedContent = computed(() => {
  if (!article.value?.content) return ''
  return marked(article.value.content, { async: false }) as string
})

onMounted(async () => {
  const id = Number(route.params.id)
  if (!id) { loading.value = false; return }
  try {
    const res = await getArticleDetail(id)
    if (res.data) {
      article.value = res.data
      isLiked.value = res.data.is_liked
      isFavorited.value = res.data.is_favorited
    }
  } catch { /* ignore */ }
  loading.value = false
})

async function toggleLike() {
  if (!article.value) return
  try {
    if (isLiked.value) {
      const res = await unlike({ content_type: 1, object_id: article.value.id })
      isLiked.value = false
      article.value.like_count = res.data?.like_count ?? article.value.like_count - 1
    } else {
      const res = await like({ content_type: 1, object_id: article.value.id })
      isLiked.value = true
      article.value.like_count = res.data?.like_count ?? article.value.like_count + 1
    }
  } catch { /* ignore */ }
}

async function toggleFavorite() {
  if (!article.value) return
  try {
    if (isFavorited.value) {
      const res = await unfavorite({ content_type: 1, object_id: article.value.id })
      isFavorited.value = false
      article.value.favorite_count = res.data?.favorite_count ?? article.value.favorite_count - 1
    } else {
      const res = await favorite({ content_type: 1, object_id: article.value.id })
      isFavorited.value = true
      article.value.favorite_count = res.data?.favorite_count ?? article.value.favorite_count + 1
    }
  } catch { /* ignore */ }
}
</script>

<style scoped>
.back-row { margin-bottom: 20px; }
.loading-wrap { padding: 20px 0; display: flex; flex-direction: column; gap: 10px; }
.article-card { padding: 36px; }
.article-title {
  font-size: 30px; font-weight: 700; letter-spacing: -0.03em;
  margin-bottom: 12px; line-height: 1.3; color: var(--text-primary);
}
.article-meta {
  display: flex; align-items: center; gap: 6px; flex-wrap: wrap;
  font-size: 14px; color: var(--text-muted); margin-bottom: 16px;
}
.dot { opacity: 0.3; }
.article-tags { display: flex; gap: 6px; margin-bottom: 24px; flex-wrap: wrap; }
.tag-pill {
  padding: 4px 12px; border-radius: 6px; font-size: 13px; font-weight: 500;
  background: var(--accent-light); color: var(--accent-dark);
}
.article-nav {
  display: flex; justify-content: space-between; margin-top: 36px;
  padding-top: 20px; border-top: 1px solid var(--stone-200); gap: 16px;
}
.nav-link {
  display: flex; align-items: center; gap: 8px;
  text-decoration: none; color: var(--accent-dark); font-size: 14px; font-weight: 500;
  max-width: 45%; transition: opacity 0.2s;
}
.nav-link:hover { opacity: 0.7; }
.nav-text { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.nav-link.prev { text-align: left; }
.nav-link.next { text-align: right; }
.article-actions {
  display: flex; gap: 10px; margin-top: 24px;
  padding-top: 20px; border-top: 1px solid var(--stone-200);
}
.action-btn {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 10px 18px; border: 1.5px solid var(--stone-200); border-radius: 10px;
  background: transparent; color: var(--text-secondary);
  font-family: 'DM Sans', sans-serif; font-size: 14px; font-weight: 500; cursor: pointer;
  transition: all 0.2s ease;
}
.action-btn:hover { border-color: var(--accent); color: var(--accent-dark); }
.action-btn.active { border-color: var(--accent); color: var(--accent-dark); background: rgba(245,158,11,0.06); }

.related-card { margin-top: 20px; padding: 24px; }
.related-title { font-size: 16px; font-weight: 600; margin-bottom: 12px; }
.related-list { display: flex; flex-direction: column; gap: 4px; }
.related-item {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 12px; border-radius: 8px; color: var(--text-primary);
  text-decoration: none; font-size: 14px; transition: background 0.2s;
}
.related-item:hover { background: rgba(245,158,11,0.06); }

.error-wrap { text-align: center; padding: 60px 0; }
.error-icon { font-size: 40px; color: var(--stone-300); display: block; margin-bottom: 12px; }
.error-wrap p { color: var(--text-muted); margin-bottom: 20px; }

@media (max-width: 600px) {
  .article-card { padding: 24px; }
  .article-title { font-size: 24px; }
}
</style>
