<template>
  <div class="page-wrap-narrow">
    <div class="back-row fade-up">
      <BackButton to="/" label="首页" />
    </div>

    <div class="glass-card search-card fade-up-1">
      <div class="search-bar">
        <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
        <input
          v-model="keyword"
          placeholder="搜索文章、项目、笔记..."
          class="search-input"
          @keyup.enter="doSearch"
        />
      </div>

      <div v-if="searched" class="result-stats">共找到 {{ result?.total || 0 }} 条结果</div>

      <div v-if="loading" class="loading-wrap">
        <div class="skeleton-pulse" style="height:60px"></div>
        <div class="skeleton-pulse" style="height:60px"></div>
      </div>

      <template v-else-if="result?.total">
        <div v-if="result.results.articles?.count" class="result-section fade-up-2">
          <h3 class="result-type-title">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
            文章 ({{ result.results.articles.count }})
          </h3>
          <button v-for="item in result.results.articles.list" :key="'a'+item.id" class="result-item" @click="router.push(`/articles/${item.id}`)">
            <span class="ri-title">{{ item.title }}</span>
            <span class="ri-desc">{{ item.summary }}</span>
          </button>
        </div>

        <div v-if="result.results.projects?.count" class="result-section fade-up-3">
          <h3 class="result-type-title">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
            项目 ({{ result.results.projects.count }})
          </h3>
          <button v-for="item in result.results.projects.list" :key="'p'+item.id" class="result-item" @click="router.push(`/projects/${item.id}`)">
            <span class="ri-title">{{ item.title }}</span>
            <span class="ri-desc">{{ item.description }}</span>
          </button>
        </div>
      </template>

      <div v-else-if="searched" class="empty-state">
        <span class="empty-icon">🔍</span>
        <p>未找到相关内容<br/>试试其他关键词</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import BackButton from '@/components/common/BackButton.vue'
import { search } from '@/api/search'
import type { SearchResult } from '@/types/api'

const route = useRoute()
const router = useRouter()
const keyword = ref('')
const result = ref<SearchResult | null>(null)
const loading = ref(false)
const searched = ref(false)

onMounted(() => {
  const kw = route.query.keyword as string
  if (kw) { keyword.value = kw; doSearch() }
})

async function doSearch() {
  if (!keyword.value.trim()) return
  loading.value = true
  searched.value = true
  try {
    const res = await search({ keyword: keyword.value })
    if (res.data) result.value = res.data
  } catch { /* ignore */ }
  loading.value = false
}
</script>

<style scoped>
.back-row { margin-bottom: 20px; }
.search-card { padding: 28px; }

.search-bar {
  display: flex; align-items: center; gap: 12px;
  padding: 4px 16px; border: 2px solid var(--stone-200);
  border-radius: 14px; transition: border-color 0.3s;
}
.search-bar:focus-within { border-color: var(--accent); }
.search-icon { color: var(--text-muted); flex-shrink: 0; }
.search-input {
  flex: 1; border: none; outline: none; background: transparent;
  font-family: 'DM Sans', sans-serif; font-size: 16px; padding: 14px 0;
  color: var(--text-primary);
}
.search-input::placeholder { color: var(--stone-300); }

.result-stats { font-size: 14px; color: var(--text-muted); margin: 16px 0; }
.loading-wrap { display: flex; flex-direction: column; gap: 10px; margin-top: 16px; }

.result-section { margin-top: 24px; }
.result-type-title {
  display: flex; align-items: center; gap: 8px;
  font-size: 15px; font-weight: 600; color: var(--text-secondary);
  margin-bottom: 10px;
}
.result-item {
  display: block; width: 100%; text-align: left;
  padding: 14px 16px; margin-bottom: 6px;
  border: 1px solid var(--stone-200); border-radius: 10px;
  background: transparent; cursor: pointer;
  font-family: 'DM Sans', sans-serif;
  transition: all 0.2s ease;
}
.result-item:hover { border-color: var(--accent); background: rgba(245,158,11,0.04); }
.ri-title { display: block; font-size: 15px; font-weight: 500; color: var(--text-primary); }
.ri-desc { display: block; font-size: 13px; color: var(--text-muted); margin-top: 4px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

.empty-state { text-align: center; padding: 40px 0; }
.empty-icon { font-size: 36px; display: block; margin-bottom: 12px; }
.empty-state p { color: var(--text-muted); font-size: 15px; line-height: 1.6; }
</style>
