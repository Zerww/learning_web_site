import request from '@/utils/request'
import type {
  ApiResponse,
  LoginParams,
  LoginResult,
  RegisterParams,
  UserDetail,
} from '@/types/api'

/**
 * User login
 */
export function login(data: LoginParams): Promise<ApiResponse<LoginResult>> {
  return request.post('/auth/login', data).then((res) => res.data)
}

/**
 * User registration
 */
export function register(data: RegisterParams): Promise<ApiResponse<{ user_id: number; username: string }>> {
  return request.post('/auth/register', data).then((res) => res.data)
}

/**
 * Refresh access token
 */
export function refreshToken(refresh_token: string): Promise<ApiResponse<{ access_token: string; expires_in: number }>> {
  return request.post('/auth/refresh', { refresh_token }).then((res) => res.data)
}

/**
 * User logout
 */
export function logout(): Promise<ApiResponse> {
  return request.post('/auth/logout').then((res) => res.data)
}

/**
 * Get current user info
 */
export function getCurrentUser(): Promise<ApiResponse<UserDetail>> {
  return request.get('/auth/me').then((res) => res.data)
}

/**
 * Update user profile
 */
/**
 * Change password
 */
export function changePassword(data: {
  old_password: string
  new_password: string
  new_password_confirm: string
}): Promise<ApiResponse> {
  return request.post('/users/change-password', data).then((res) => res.data)
}

/**
 * Update user profile
 */
export function updateProfile(data: {
  nickname?: string
  avatar?: string
  bio?: string
  github_url?: string
  website_url?: string
}): Promise<ApiResponse> {
  return request.put('/users/profile', data).then((res) => res.data)
}
