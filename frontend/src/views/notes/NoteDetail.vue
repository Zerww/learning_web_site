<template>
  <div class="page-wrap-narrow">
    <div class="back-row fade-up">
      <BackButton to="/notes" label="所有笔记" />
    </div>

    <div v-if="loading" class="loading-wrap fade-up-1">
      <div class="skeleton-pulse" style="height:28px; width:50%; margin-bottom:12px"></div>
      <div class="skeleton-pulse" style="height:400px"></div>
    </div>

    <div v-else-if="note" class="glass-card note-card fade-up-1">
      <div class="note-header">
        <h1 class="note-title">{{ note.title }}</h1>
        <div class="note-progress-bar">
          <div class="progress-fill" :style="{ width: note.progress + '%' }"></div>
        </div>
        <div class="note-meta">
          <span>{{ stageLabel(note.learning_stage) }}</span>
          <span class="dot">·</span>
          <span>进度 {{ note.progress }}%</span>
          <span class="dot">·</span>
          <span>{{ note.view_count }} 次浏览</span>
        </div>
      </div>

      <div class="markdown-content" v-html="renderedContent" />
    </div>

    <aside v-if="note?.children?.length" class="glass-card children-card fade-up-2">
      <h3 class="children-title">子笔记</h3>
      <div class="children-list">
        <router-link v-for="c in note.children" :key="c.id" :to="`/notes/${c.id}`" class="child-item">
          <span class="child-name">{{ c.title }}</span>
          <div class="child-progress">
            <div class="child-progress-fill" :style="{ width: c.progress + '%' }"></div>
          </div>
        </router-link>
      </div>
    </aside>

    <div v-else-if="!loading" class="error-wrap fade-up-1">
      <span class="error-icon">◎</span>
      <p>笔记不存在</p>
      <BackButton to="/notes" label="返回笔记列表" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { marked } from 'marked'
import BackButton from '@/components/common/BackButton.vue'
import { getNoteDetail } from '@/api/notes'
import type { NoteDetail } from '@/types/api'

const route = useRoute()
const note = ref<NoteDetail | null>(null)
const loading = ref(true)

const renderedContent = computed(() => {
  if (!note.value?.content) return ''
  return marked(note.value.content, { async: false }) as string
})

function stageLabel(stage: number): string {
  return { 1: '入门', 2: '进阶', 3: '精通' }[stage] || '未知'
}

onMounted(async () => {
  const id = Number(route.params.id)
  if (!id) { loading.value = false; return }
  try {
    const res = await getNoteDetail(id)
    if (res.data) note.value = res.data
  } catch { /* ignore */ }
  loading.value = false
})
</script>

<style scoped>
.back-row { margin-bottom: 20px; }
.loading-wrap { padding: 20px 0; display: flex; flex-direction: column; gap: 10px; }
.note-card { padding: 36px; }
.note-header { margin-bottom: 28px; }
.note-title {
  font-size: 28px; font-weight: 700; letter-spacing: -0.03em;
  margin-bottom: 16px; color: var(--text-primary);
}
.note-progress-bar {
  height: 4px; background: var(--stone-200); border-radius: 2px; margin-bottom: 10px; overflow: hidden;
}
.progress-fill {
  height: 100%; background: linear-gradient(90deg, var(--accent), var(--accent-dark));
  border-radius: 2px; transition: width 0.5s ease;
}
.note-meta {
  display: flex; align-items: center; gap: 6px;
  font-size: 14px; color: var(--text-muted);
}
.dot { opacity: 0.3; }

.children-card { margin-top: 20px; padding: 24px; }
.children-title { font-size: 16px; font-weight: 600; margin-bottom: 16px; }
.children-list { display: flex; flex-direction: column; gap: 12px; }
.child-item {
  display: flex; flex-direction: column; gap: 6px;
  padding: 14px 16px; border-radius: 10px;
  background: var(--bg-warm); text-decoration: none;
  transition: background 0.2s;
}
.child-item:hover { background: rgba(245,158,11,0.06); }
.child-name { font-size: 15px; font-weight: 500; color: var(--text-primary); }
.child-progress { height: 3px; background: var(--stone-200); border-radius: 2px; overflow: hidden; }
.child-progress-fill { height: 100%; background: var(--accent); border-radius: 2px; }

.error-wrap { text-align: center; padding: 60px 0; }
.error-icon { font-size: 40px; color: var(--stone-300); display: block; margin-bottom: 12px; }
.error-wrap p { color: var(--text-muted); margin-bottom: 20px; }

@media (max-width: 600px) {
  .note-card { padding: 24px; }
  .note-title { font-size: 22px; }
}
</style>
