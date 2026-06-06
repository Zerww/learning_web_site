import request from '@/utils/request'
import type { ApiResponse, HomeData } from '@/types/api'

/**
 * Get home page data
 */
export function getHomeData(): Promise<ApiResponse<HomeData>> {
  return request.get('/home').then((res) => res.data)
}
