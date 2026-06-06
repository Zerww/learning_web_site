import request from '@/utils/request'
import type {
  ApiResponse,
  PaginatedData,
  Article,
  ArticleDetail,
  ArticleCreate,
  ArticleArchive,
} from '@/types/api'

/**
 * Get article list
 */
export function getArticles(params?: {
  page?: number
  page_size?: number
  category_id?: number
  status?: number
  is_featured?: number
  is_top?: number
  search?: string
  year?: number
  month?: number
  tags?: string
  ordering?: string
}): Promise<ApiResponse<PaginatedData<Article>>> {
  return request.get('/articles', { params }).then((res) => res.data)
}

/**
 * Get article detail
 */
export function getArticleDetail(id: number): Promise<ApiResponse<ArticleDetail>> {
  return request.get(`/articles/${id}`).then((res) => res.data)
}

/**
 * Create article (admin)
 */
export function createArticle(data: ArticleCreate): Promise<ApiResponse<{ id: number; title: string; slug: string }>> {
  return request.post('/articles', data).then((res) => res.data)
}

/**
 * Update article (admin)
 */
export function updateArticle(id: number, data: Partial<ArticleCreate>): Promise<ApiResponse> {
  return request.put(`/articles/${id}`, data).then((res) => res.data)
}

/**
 * Delete article (admin)
 */
export function deleteArticle(id: number): Promise<ApiResponse> {
  return request.delete(`/articles/${id}`).then((res) => res.data)
}

/**
 * Get article archive
 */
export function getArticleArchive(): Promise<ApiResponse<{ archives: ArticleArchive[] }>> {
  return request.get('/articles/archive').then((res) => res.data)
}
