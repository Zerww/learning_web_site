<template>
  <div class="admin-shell">
    <!-- Mobile header -->
    <header class="admin-mobile-header">
      <button class="menu-toggle" @click="sidebarOpen = !sidebarOpen">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
      </button>
      <span class="mobile-title">管理后台</span>
      <div style="width:22px"></div>
    </header>

    <!-- Sidebar overlay -->
    <div v-if="sidebarOpen" class="sidebar-overlay" @click="sidebarOpen = false"></div>

    <!-- Sidebar -->
    <aside class="admin-sidebar" :class="{ open: sidebarOpen }">
      <div class="sidebar-brand">
        <router-link to="/" class="brand-link">
          <span class="brand-mark">✦</span>
          <span class="brand-text">学习成果</span>
        </router-link>
        <span class="brand-badge">管理</span>
      </div>

      <nav class="sidebar-nav">
        <router-link to="/admin" class="nav-item" @click="sidebarOpen = false">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
          <span>概览</span>
        </router-link>
        <router-link to="/admin/projects" class="nav-item" @click="sidebarOpen = false">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
          <span>项目管理</span>
        </router-link>
        <router-link to="/admin/articles" class="nav-item" @click="sidebarOpen = false">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
          <span>文章管理</span>
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <router-link to="/" class="nav-item back-link">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
          <span>返回前台</span>
        </router-link>
        <button class="nav-item" @click="themeToggle">
          <svg v-if="!store.isDark" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
          <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
          <span>{{ store.isDark ? '亮色' : '暗色' }}</span>
        </button>
        <button class="nav-item logout-btn" @click="handleLogout">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
          <span>退出</span>
        </button>
      </div>
    </aside>

    <!-- Main content -->
    <div class="admin-main">
      <div class="admin-content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores/app'

const router = useRouter()
const store = useAppStore()
const sidebarOpen = ref(false)

function themeToggle() {
  store.toggleTheme()
  sidebarOpen.value = false
}

function handleLogout() {
  store.clearUser()
  router.push('/auth/login')
}
</script>

<style scoped>
.admin-shell {
  min-height: 100vh;
  display: flex;
  background: var(--bg-warm);
}

/* ============ Sidebar ============ */
.admin-sidebar {
  width: 240px;
  min-height: 100vh;
  background: var(--stone-900);
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 300;
  transition: transform 0.3s ease;
}

.sidebar-brand {
  padding: 24px 20px 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}

.brand-link {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: #fff;
}

.brand-mark { font-size: 18px; color: var(--accent); }
.brand-text { font-size: 16px; font-weight: 700; letter-spacing: -0.03em; }
.brand-badge {
  font-size: 11px;
  font-weight: 600;
  color: var(--accent);
  background: rgba(245,158,11,0.15);
  padding: 2px 8px;
  border-radius: 5px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Nav */
.sidebar-nav {
  flex: 1;
  padding: 12px 10px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  border-radius: 10px;
  color: rgba(255,255,255,0.6);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  font-family: 'DM Sans', sans-serif;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
  text-align: left;
}

.nav-item:hover {
  background: rgba(255,255,255,0.06);
  color: rgba(255,255,255,0.9);
}

.nav-item.router-link-active {
  background: rgba(245,158,11,0.15);
  color: var(--accent);
}

.logout-btn:hover { color: #EF4444; }

.sidebar-footer {
  padding: 12px 10px;
  border-top: 1px solid rgba(255,255,255,0.06);
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.back-link { color: rgba(255,255,255,0.4); }

/* ============ Main Area ============ */
.admin-main {
  flex: 1;
  margin-left: 240px;
  min-height: 100vh;
}

.admin-content {
  padding: 28px;
}

/* ============ Mobile ============ */
.admin-mobile-header {
  display: none;
  position: sticky;
  top: 0;
  z-index: 200;
  background: var(--bg-warm);
  border-bottom: 1px solid var(--stone-200);
  padding: 12px 16px;
  align-items: center;
  justify-content: space-between;
}

.menu-toggle {
  background: none;
  border: none;
  color: var(--text-primary);
  cursor: pointer;
  padding: 4px;
}

.mobile-title {
  font-weight: 600;
  font-size: 15px;
}

.sidebar-overlay {
  display: none;
}

@media (max-width: 768px) {
  .admin-sidebar { transform: translateX(-100%); }
  .admin-sidebar.open { transform: translateX(0); }
  .admin-main { margin-left: 0; }
  .admin-mobile-header { display: flex; }
  .sidebar-overlay {
    display: block;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.4);
    z-index: 299;
  }
}
</style>
