<template>
  <button class="back-btn" @click="handleBack" :title="tooltip">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M19 12H5M12 19l-7-7 7-7"/>
    </svg>
    <span v-if="label" class="back-label">{{ label }}</span>
  </button>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const props = withDefaults(defineProps<{
  to?: string
  label?: string
  tooltip?: string
}>(), {
  tooltip: '返回',
})

const router = useRouter()

function handleBack() {
  if (props.to) {
    router.push(props.to)
  } else {
    router.back()
  }
}
</script>

<style scoped>
.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px 8px 10px;
  background: var(--bg-card);
  border: 1px solid rgba(245,158,11,0.12);
  border-radius: 10px;
  color: var(--stone-500);
  cursor: pointer;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.25s ease;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.back-btn:hover {
  color: var(--accent-dark);
  border-color: rgba(245,158,11,0.25);
  background: rgba(245,158,11,0.04);
  transform: translateX(-2px);
}

.back-btn:active {
  transform: translateX(0);
}

.back-label {
  line-height: 1;
}
</style>
