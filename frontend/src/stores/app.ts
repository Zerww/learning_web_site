import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { UserInfo } from '@/types/api'
import { getCurrentUser } from '@/api/auth'

export const useAppStore = defineStore('app', () => {
  const user = ref<UserInfo | null>(null)
  const isDark = ref(false)

  /** Initialize user from localStorage */
  function initUser() {
    const stored = localStorage.getItem('user_info')
    if (stored) {
      try {
        user.value = JSON.parse(stored)
      } catch {
        localStorage.removeItem('user_info')
      }
    }
  }

  /** Fetch latest user info from API */
  async function fetchUser() {
    try {
      const res = await getCurrentUser()
      if (res.data) {
        user.value = {
          id: res.data.id,
          username: res.data.username,
          nickname: res.data.nickname,
          avatar: res.data.avatar,
          role: res.data.role,
        }
        localStorage.setItem('user_info', JSON.stringify(user.value))
      }
    } catch {
      // Not logged in
    }
  }

  /** Set user after login */
  function setUser(userInfo: UserInfo) {
    user.value = userInfo
    localStorage.setItem('user_info', JSON.stringify(userInfo))
  }

  /** Clear user on logout */
  function clearUser() {
    user.value = null
    localStorage.removeItem('user_info')
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  /** Check if current user is admin */
  const isAdmin = () => user.value?.role === 1

  /** Toggle dark/light theme */
  function toggleTheme() {
    isDark.value = !isDark.value
    document.documentElement.classList.toggle('dark', isDark.value)
  }

  /** Initialize theme from system preference */
  function initTheme() {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    isDark.value = prefersDark
    document.documentElement.classList.toggle('dark', isDark.value)
  }

  initUser()
  initTheme()

  return {
    user,
    isDark,
    setUser,
    clearUser,
    fetchUser,
    isAdmin,
    toggleTheme,
  }
})
