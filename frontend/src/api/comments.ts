import request from '@/utils/request'
import type { ApiResponse, PaginatedData, Comment, CommentCreate } from '@/types/api'

/**
 * Get comment list for a content object
 */
export function getComments(params: {
  content_type: number
  object_id: number
  page?: number
  page_size?: number
}): Promise<ApiResponse<PaginatedData<Comment>>> {
  return request.get('/comments', { params }).then((res) => res.data)
}

/**
 * Create a comment
 */
export function createComment(data: CommentCreate): Promise<ApiResponse<{ id: number; content: string; status: number }>> {
  return request.post('/comments', data).then((res) => res.data)
}

/**
 * Delete a comment
 */
export function deleteComment(id: number): Promise<ApiResponse> {
  return request.delete(`/comments/${id}`).then((res) => res.data)
}
