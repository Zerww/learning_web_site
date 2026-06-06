import request from '@/utils/request'
import type {
  ApiResponse,
  PaginatedData,
  Project,
  ProjectDetail,
  ProjectCreate,
} from '@/types/api'

/**
 * Get project list
 */
export function getProjects(params?: {
  page?: number
  page_size?: number
  category_id?: number
  status?: number
  is_featured?: number
  search?: string
  tags?: string
  ordering?: string
}): Promise<ApiResponse<PaginatedData<Project>>> {
  return request.get('/projects', { params }).then((res) => res.data)
}

/**
 * Get project detail
 */
export function getProjectDetail(id: number): Promise<ApiResponse<ProjectDetail>> {
  return request.get(`/projects/${id}`).then((res) => res.data)
}

/**
 * Create project (admin)
 */
export function createProject(data: ProjectCreate): Promise<ApiResponse<{ id: number; title: string; slug: string }>> {
  return request.post('/projects', data).then((res) => res.data)
}

/**
 * Update project (admin)
 */
export function updateProject(id: number, data: Partial<ProjectCreate>): Promise<ApiResponse> {
  return request.put(`/projects/${id}`, data).then((res) => res.data)
}

/**
 * Delete project (admin)
 */
export function deleteProject(id: number): Promise<ApiResponse> {
  return request.delete(`/projects/${id}`).then((res) => res.data)
}
