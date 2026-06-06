import request from '@/utils/request'
import type { ApiResponse, SearchResult } from '@/types/api'

/**
 * Full-text search
 */
export function search(params: {
  keyword: string
  type?: string
  page?: number
  page_size?: number
}): Promise<ApiResponse<SearchResult>> {
  return request.get('/search', { params }).then((res) => res.data)
}
