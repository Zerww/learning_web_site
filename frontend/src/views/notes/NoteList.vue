<template>
  <div class="page-container">
    <h1 class="section-title">学习笔记</h1>

    <div v-if="loading" class="loading-center">
      <el-skeleton :rows="5" animated />
    </div>

    <div v-else>
      <el-tree :data="noteTree" :props="treeProps" node-key="id" default-expand-all>
        <template #default="{ node, data }">
          <router-link :to="`/notes/${data.id}`" custom v-slot="{ navigate }">
          <el-card class="note-card" shadow="hover" @click="navigate">
            <div class="note-info">
              <span class="note-title">{{ data.title }}</span>
              <span class="note-stage">{{ stageLabel(data.learning_stage) }}</span>
              <el-progress :percentage="data.progress" :width="80" type="circle" :stroke-width="6" />
            </div>
          </el-card>
          </router-link>
        </template>
      </el-tree>

      <el-empty v-if="noteList.length === 0" description="暂无笔记" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getNotes } from '@/api/notes'
import type { Note } from '@/types/api'

const noteList = ref<Note[]>([])
const loading = ref(true)

const treeProps = { children: 'children', label: 'title' }

const noteTree = computed(() => buildTree(noteList.value))

onMounted(async () => {
  try {
    const res = await getNotes({ page_size: 50 } as any)
    if (res.data) noteList.value = res.data.list
  } catch { /* ignore */ }
  loading.value = false
})

function stageLabel(stage: number): string {
  return { 1: '入门', 2: '进阶', 3: '精通' }[stage] || '未知'
}

function buildTree(notes: Note[]): any[] {
  const map = new Map<number, any>()
  const roots: any[] = []

  notes.forEach((n) => {
    map.set(n.id, { ...n, children: [] })
  })

  notes.forEach((n) => {
    const node = map.get(n.id)
    if (n.category?.parent) {
      const parent = map.get(n.category.parent)
      if (parent) parent.children.push(node)
      else roots.push(node)
    } else {
      roots.push(node)
    }
  })

  return roots
}
</script>

<style scoped>
.note-card {
  margin-bottom: 10px;
  cursor: pointer;
  &:hover { border-color: var(--primary-color); }
}

.note-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.note-title {
  flex: 1;
  font-size: 15px;
  font-weight: 500;
}

.note-stage {
  font-size: 12px;
  color: #909399;
}

.loading-center {
  padding: 40px 0;
}
</style>
