import request from '@/utils/request'
import type { ApiResponse, LikeParams, FavoriteParams } from '@/types/api'

/**
 * Like a content item
 */
export function like(data: LikeParams): Promise<ApiResponse<{ like_count: number; is_liked: boolean }>> {
  return request.post('/likes/', data).then((res) => res.data)
}

/**
 * Unlike a content item
 */
export function unlike(data: LikeParams): Promise<ApiResponse<{ like_count: number; is_liked: boolean }>> {
  return request.delete('/likes/', { data }).then((res) => res.data)
}

/**
 * Check like status
 */
export function getLikeStatus(params: LikeParams): Promise<ApiResponse<{ is_liked: boolean; like_count: number }>> {
  return request.get('/likes/status/', { params }).then((res) => res.data)
}

/**
 * Favorite a content item
 */
export function favorite(data: FavoriteParams): Promise<ApiResponse<{ favorite_count: number; is_favorited: boolean }>> {
  return request.post('/favorites/', data).then((res) => res.data)
}

/**
 * Unfavorite a content item
 */
export function unfavorite(data: FavoriteParams): Promise<ApiResponse<{ favorite_count: number; is_favorited: boolean }>> {
  return request.delete('/favorites/', { data }).then((res) => res.data)
}

/**
 * Get my liked items
 */
export function getMyLikes(params?: { page?: number; page_size?: number }): Promise<ApiResponse<{
  list: Array<{ id: number; content_type: number; object_id: number; content: any; created_at: string }>
  pagination: any
}>> {
  return request.get('/likes/my/', { params }).then((res) => res.data)
}

/**
 * Get my favorites
 */
export function getMyFavorites(params?: {
  content_type?: number
  page?: number
  page_size?: number
}): Promise<ApiResponse<{
  list: Array<{ id: number; content_type: number; object_id: number; content: any; folder_name: string; created_at: string }>
  pagination: any
}>> {
  return request.get('/favorites/', { params }).then((res) => res.data)
}
