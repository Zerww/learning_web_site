import request from '@/utils/request'
import type { ApiResponse, Tag } from '@/types/api'

/**
 * Get tag list
 */
export function getTags(params?: {
  type?: number
  ordering?: string
}): Promise<ApiResponse<{ list: Tag[] }>> {
  return request.get('/tags', { params }).then((res) => res.data)
}
