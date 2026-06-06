<template>
  <div class="auth-page">
    <div class="ambient-bg">
      <div class="ambient-shape s1"></div>
      <div class="ambient-shape s2"></div>
    </div>

    <div class="auth-container fade-up">
      <router-link to="/" class="auth-back">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
        返回首页
      </router-link>

      <div class="glass-card auth-card">
        <div class="auth-header">
          <span class="auth-icon">✦</span>
          <h1>登录</h1>
          <p>欢迎回来</p>
        </div>

        <form class="auth-form" @submit.prevent="handleLogin">
          <div class="field-group">
            <label class="field-label">用户名</label>
            <div class="field-input-wrap">
              <svg class="field-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="5"/><path d="M20 21a8 8 0 1 0-16 0"/></svg>
              <input v-model="form.username" type="text" class="field-input" placeholder="输入用户名" autocomplete="username" />
              <span class="input-underline"></span>
            </div>
          </div>

          <div class="field-group">
            <label class="field-label">密码</label>
            <div class="field-input-wrap">
              <svg class="field-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              <input v-model="form.password" type="password" class="field-input" placeholder="输入密码" autocomplete="current-password" />
              <span class="input-underline"></span>
            </div>
          </div>

          <button type="submit" class="auth-submit" :disabled="loading">
            {{ loading ? '登录中…' : '登录' }}
          </button>
        </form>

        <p class="auth-footer">
          还没有账号？<router-link to="/auth/register">注册</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login } from '@/api/auth'
import { useAppStore } from '@/stores/app'

const router = useRouter()
const route = useRoute()
const store = useAppStore()
const loading = ref(false)

const form = reactive({ username: '', password: '' })

async function handleLogin() {
  if (!form.username || !form.password) { ElMessage.warning('请填写用户名和密码'); return }
  loading.value = true
  try {
    const res = await login(form)
    if (res.data) {
      localStorage.setItem('access_token', res.data.access_token)
      localStorage.setItem('refresh_token', res.data.refresh_token)
      store.setUser(res.data.user)
      ElMessage.success('登录成功')
      router.push((route.query.redirect as string) || '/')
    }
  } catch { /* handled by interceptor */ }
  loading.value = false
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh; display: flex; align-items: center; justify-content: center;
  background: var(--bg-warm); position: relative; overflow: hidden; padding: 20px;
}
.ambient-bg { position: fixed; inset: 0; pointer-events: none; }
.ambient-shape {
  position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.3;
}
.s1 { width: 400px; height: 400px; background: radial-gradient(circle, #FDE68A, #F59E0B); top: -100px; left: -100px; animation: float 12s ease infinite; }
.s2 { width: 350px; height: 350px; background: radial-gradient(circle, #FED7AA, #EA580C); bottom: -80px; right: -80px; animation: float 15s ease infinite reverse; }
@keyframes float { 0%,100% { transform: translate(0,0) scale(1); } 50% { transform: translate(30px,-30px) scale(1.05); } }

.auth-container { position: relative; z-index: 1; width: 100%; max-width: 400px; }
.auth-back {
  display: inline-flex; align-items: center; gap: 6px;
  color: var(--text-muted); font-size: 14px; text-decoration: none; margin-bottom: 16px; transition: color 0.2s;
}
.auth-back:hover { color: var(--accent-dark); }

.auth-card { padding: 36px; }
.auth-header { text-align: center; margin-bottom: 28px; }
.auth-icon { font-size: 28px; color: var(--accent); display: block; margin-bottom: 8px; }
.auth-header h1 { font-size: 24px; font-weight: 700; color: var(--text-primary); letter-spacing: -0.03em; margin-bottom: 4px; }
.auth-header p { font-size: 15px; color: var(--text-muted); }

.auth-form { display: flex; flex-direction: column; gap: 20px; }
.field-group { display: flex; flex-direction: column; gap: 6px; }
.field-label { font-size: 13px; font-weight: 600; color: var(--stone-500); text-transform: uppercase; letter-spacing: 0.04em; }
.field-input-wrap { position: relative; display: flex; align-items: center; }
.field-icon { position: absolute; left: 16px; color: var(--stone-400); pointer-events: none; z-index: 1; }
.field-input {
  width: 100%; padding: 14px 16px 14px 46px;
  background: var(--bg-warm); border: 2px solid var(--stone-200); border-radius: 12px;
  font-family: 'DM Sans', sans-serif; font-size: 15px; color: var(--text-primary);
  outline: none; transition: border-color 0.3s, box-shadow 0.3s;
}
.field-input:focus { border-color: var(--accent); box-shadow: 0 0 0 4px rgba(245,158,11,0.08); }
.input-underline {
  position: absolute; bottom: 0; left: 0; width: 0; height: 2px;
  background: linear-gradient(90deg, var(--accent), var(--accent-dark));
  transition: width 0.4s ease; border-radius: 1px;
}
.field-input:focus ~ .input-underline { width: 100%; }

.auth-submit {
  width: 100%; padding: 16px;
  background: linear-gradient(135deg, var(--accent), var(--accent-dark));
  border: none; border-radius: 12px; color: #fff;
  font-family: 'DM Sans', sans-serif; font-size: 16px; font-weight: 600;
  cursor: pointer; transition: all 0.25s ease; margin-top: 4px;
}
.auth-submit:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 8px 24px rgba(245,158,11,0.3); }
.auth-submit:disabled { opacity: 0.7; cursor: wait; }

.auth-footer { text-align: center; margin-top: 20px; font-size: 14px; color: var(--text-muted); }
.auth-footer a { color: var(--accent); font-weight: 600; }
</style>
