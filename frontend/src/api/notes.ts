import request from '@/utils/request'
import type { ApiResponse, PaginatedData, Note, NoteDetail } from '@/types/api'

/**
 * Get note list
 */
export function getNotes(params?: {
  page?: number
  page_size?: number
  category_id?: number
  learning_stage?: number
  parent_id?: number
  search?: string
  ordering?: string
}): Promise<ApiResponse<PaginatedData<Note>>> {
  return request.get('/notes', { params }).then((res) => res.data)
}

/**
 * Get note detail
 */
export function getNoteDetail(id: number): Promise<ApiResponse<NoteDetail>> {
  return request.get(`/notes/${id}`).then((res) => res.data)
}
