import axios, { AxiosError, type AxiosInstance, type InternalAxiosRequestConfig } from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1'

const request: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor - attach token & always use trailing slash (Django APPEND_SLASH)
request.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('access_token')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    // Always add trailing slash to avoid Django 301 redirects that can strip auth headers
    if (config.url && !config.url.endsWith('/') && !config.url.includes('?')) {
      config.url += '/'
    }
    return config
  },
  (error) => Promise.reject(error),
)

// Response interceptor - handle errors
request.interceptors.response.use(
  (response) => response,
  async (error: AxiosError<{ message?: string; errors?: any[] }>) => {
    const status = error.response?.status
    const data = error.response?.data

    if (status === 401) {
      // Try to refresh token
      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken && error.config && !(error.config as any)._retry) {
        (error.config as any)._retry = true
        try {
          const res = await axios.post(`${BASE_URL}/auth/refresh`, {
            refresh_token: refreshToken,
          })
          const newToken = res.data.data.access_token
          localStorage.setItem('access_token', newToken)
          if (error.config.headers) {
            error.config.headers.Authorization = `Bearer ${newToken}`
          }
          return request(error.config)
        } catch {
          // Refresh failed - logout
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          router.push('/auth/login')
          ElMessage.error('登录已过期，请重新登录')
        }
      } else {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        router.push('/auth/login')
        ElMessage.error('请先登录')
      }
    } else if (status === 403) {
      ElMessage.error('权限不足')
    } else if (status === 429) {
      ElMessage.warning('请求过于频繁，请稍后再试')
    } else if (status === 500) {
      ElMessage.error('服务器内部错误')
    } else if (data?.message) {
      ElMessage.error(data.message)
    }

    return Promise.reject(error)
  },
)

export default request
