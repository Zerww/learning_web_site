<template>
  <div class="app-shell">
    <!-- Header -->
    <header class="main-header">
      <div class="header-inner">
        <router-link to="/" class="brand">
          <span class="brand-mark">✦</span>
          <span class="brand-text">学习成果</span>
        </router-link>

        <nav class="nav-desktop">
          <router-link to="/" class="nav-link" :class="{ active: $route.path === '/' }">首页</router-link>
          <router-link to="/projects" class="nav-link">项目</router-link>
          <router-link to="/articles" class="nav-link">文章</router-link>
          <router-link to="/notes" class="nav-link">笔记</router-link>
          <router-link to="/about" class="nav-link">关于</router-link>
        </nav>

        <div class="header-actions">
          <button class="icon-btn search-btn" @click="doSearch" title="搜索">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>
            </svg>
          </button>

          <button class="icon-btn theme-btn" @click="store.toggleTheme()" :title="store.isDark ? '亮色模式' : '暗色模式'">
            <svg v-if="!store.isDark" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
            </svg>
            <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
            </svg>
          </button>

          <template v-if="store.user">
            <div class="user-menu" @click.stop="showUserMenu = !showUserMenu" @keydown.escape="showUserMenu = false">
              <div class="user-avatar">
                {{ store.user.nickname?.charAt(0) || store.user.username.charAt(0) }}
              </div>
              <svg v-if="showUserMenu" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="m18 15-6-6-6 6"/></svg>
              <svg v-else width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="m6 9 6 6 6-6"/></svg>
              <transition name="dropdown">
                <div v-if="showUserMenu" class="dropdown-menu">
                  <router-link to="/profile" class="dropdown-item" @click="showUserMenu = false">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="5"/><path d="M20 21a8 8 0 1 0-16 0"/></svg>
                    个人信息
                  </router-link>
                  <router-link v-if="store.isAdmin()" to="/admin" class="dropdown-item" @click="showUserMenu = false">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                    管理后台
                  </router-link>
                  <hr class="dropdown-divider" />
                  <button class="dropdown-item" @click="handleLogout">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
                    退出登录
                  </button>
                </div>
              </transition>
            </div>
          </template>
          <template v-else>
            <router-link to="/auth/login" class="btn-primary-sm">登录</router-link>
          </template>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main-area">
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="main-footer">
      <div class="footer-inner">
        <span class="footer-mark">✦</span>
        <p>{{ new Date().getFullYear() }} 学习成果展示 · 用代码记录成长</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { useAppStore } from '@/stores/app'
import { logout } from '@/api/auth'

const router = useRouter()
const store = useAppStore()
const showUserMenu = ref(false)
const userMenuRef = ref<HTMLElement | null>(null)

// Click outside to close user menu
function onClickOutside(e: MouseEvent) {
  if (showUserMenu.value) {
    showUserMenu.value = false
  }
}
onMounted(() => document.addEventListener('click', onClickOutside))
onUnmounted(() => document.removeEventListener('click', onClickOutside))

function doSearch() {
  router.push({ name: 'Search' })
}

async function handleLogout() {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示')
    await logout()
  } catch { /* ignore */ }
  store.clearUser()
  router.push('/')
}
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg-warm);
}

/* ============ Header ============ */
.main-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255, 248, 240, 0.88);
  backdrop-filter: blur(24px) saturate(1.4);
  -webkit-backdrop-filter: blur(24px) saturate(1.4);
  border-bottom: 1px solid rgba(245, 158, 11, 0.08);
  padding: 0 20px;
}

.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  height: 64px;
  gap: 32px;
}

/* Brand */
.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  flex-shrink: 0;
}

.brand-mark {
  font-size: 20px;
  color: var(--accent);
}

.brand-text {
  font-size: 19px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.03em;
}

/* Nav */
.nav-desktop {
  display: flex;
  gap: 4px;
  flex: 1;
}

.nav-link {
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  text-decoration: none;
  transition: all 0.2s ease;
}

.nav-link:hover {
  color: var(--accent-dark);
  background: rgba(245,158,11,0.06);
}

.nav-link.active {
  color: var(--accent-dark);
  background: rgba(245,158,11,0.08);
}

/* Actions */
.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.icon-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 10px;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.icon-btn:hover {
  background: rgba(245,158,11,0.08);
  color: var(--accent-dark);
}

.btn-primary-sm {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 18px;
  background: linear-gradient(135deg, var(--accent), var(--accent-dark));
  border: none;
  border-radius: 10px;
  color: #ffffff;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.25s ease;
}

.btn-primary-sm:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(245,158,11,0.3);
}

/* User avatar */
.user-menu {
  position: relative;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px 4px 4px;
  border-radius: 10px;
  transition: background 0.2s;
  color: var(--text-secondary);
}

.user-menu:hover {
  background: rgba(245,158,11,0.06);
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent), var(--accent-dark));
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
}

/* Dropdown */
.dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 180px;
  background: #fff;
  border: 1px solid var(--stone-200);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.08);
  padding: 6px;
  z-index: 200;
  animation: dropIn 0.2s ease;
}

@keyframes dropIn {
  from { opacity: 0; transform: translateY(-6px); }
  to { opacity: 1; transform: translateY(0); }
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 10px 14px;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: var(--stone-700);
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.15s ease;
}

.dropdown-item:hover {
  background: rgba(245,158,11,0.08);
  color: var(--accent-dark);
}

.dropdown-divider {
  border: none;
  border-top: 1px solid var(--stone-100);
  margin: 4px 8px;
}

.dropdown-enter-active, .dropdown-leave-active {
  transition: opacity 0.2s, transform 0.2s;
}
.dropdown-enter-from, .dropdown-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

/* ============ Main ============ */
.main-area {
  flex: 1;
}

/* ============ Footer ============ */
.main-footer {
  background: var(--stone-900);
  color: var(--stone-400);
  padding: 24px 20px;
  text-align: center;
}

.footer-inner {
  max-width: 1200px;
  margin: 0 auto;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.footer-mark {
  color: var(--accent);
  font-size: 14px;
}

.footer-inner p {
  margin: 0;
}

/* ============ Responsive ============ */
@media (max-width: 700px) {
  .nav-desktop { display: none; }
  .header-inner { gap: 12px; }
}
</style>
