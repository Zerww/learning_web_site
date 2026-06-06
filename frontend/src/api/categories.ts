import request from '@/utils/request'
import type { ApiResponse, Category } from '@/types/api'

/**
 * Get category list
 */
export function getCategories(params?: {
  type?: number
  parent_id?: number
}): Promise<ApiResponse<{ list: Category[] }>> {
  return request.get('/categories', { params }).then((res) => res.data)
}
