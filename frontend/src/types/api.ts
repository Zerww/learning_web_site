/* ========== Common API Response Types ========== */

export interface ApiResponse<T = any> {
  code: number
  message: string
  data?: T
  errors?: ApiError[]
}

export interface ApiError {
  field: string
  message: string
}

export interface PaginatedData<T> {
  list: T[]
  pagination: Pagination
}

export interface Pagination {
  page: number
  page_size: number
  total: number
  total_pages: number
  has_next: boolean
  has_prev: boolean
}

/* ========== User Types ========== */

export interface LoginParams {
  username: string
  password: string
}

export interface RegisterParams {
  username: string
  email: string
  password: string
  password_confirm: string
}

export interface LoginResult {
  access_token: string
  refresh_token: string
  expires_in: number
  user: UserInfo
}

export interface UserInfo {
  id: number
  username: string
  nickname: string
  avatar: string | null
  role: number
}

export interface UserDetail extends UserInfo {
  email: string
  bio: string | null
  github_url: string | null
  website_url: string | null
  created_at: string
  last_login_at: string | null
}

export interface UserPublic {
  id: number
  username: string
  nickname: string
  avatar: string | null
  bio: string | null
  github_url: string | null
  website_url: string | null
  article_count: number
  project_count: number
}

export interface UserProfileUpdate {
  nickname?: string
  avatar?: string
  bio?: string
  github_url?: string
  website_url?: string
}

/* ========== Category & Tag Types ========== */

export interface Category {
  id: number
  name: string
  slug: string
  description: string | null
  type: number
  icon: string | null
  sort_order: number
  parent: number | null
  children: Category[]
  count: number
}

export interface Tag {
  id: number
  name: string
  slug: string
  color: string
  type: number
  usage_count: number
}

/* ========== Project Types ========== */

export interface Project {
  id: number
  title: string
  slug: string
  description: string
  cover_image: string | null
  category: Category
  tags: Tag[]
  tech_stack: string[]
  github_url: string | null
  demo_url: string | null
  status: number
  is_featured: boolean
  view_count: number
  like_count: number
  favorite_count: number
  difficulty: number | null
  published_at: string
  author: {
    id: number
    nickname: string
    avatar: string | null
  }
}

export interface ProjectDetail extends Project {
  content: string
  video_url: string | null
  start_date: string | null
  end_date: string | null
  created_at: string
  updated_at: string
  is_liked: boolean
  is_favorited: boolean
  related_projects: Array<{ id: number; title: string; cover_image: string | null }>
}

export interface ProjectCreate {
  title: string
  slug: string
  description: string
  content: string
  cover_image?: string
  category_id: number
  tags?: number[]
  tech_stack?: string[]
  github_url?: string
  demo_url?: string
  video_url?: string
  status: number
  is_featured?: number
  difficulty?: number
  start_date?: string
  end_date?: string
}

/* ========== Article Types ========== */

export interface Article {
  id: number
  title: string
  slug: string
  summary: string | null
  cover_image: string | null
  category: Category
  tags: Tag[]
  reading_time: number
  word_count: number
  status: number
  is_featured: boolean
  is_top: boolean
  view_count: number
  like_count: number
  comment_count: number
  published_at: string
  author: {
    id: number
    nickname: string
    avatar: string | null
  }
}

export interface ArticleDetail extends Article {
  content: string
  allow_comment: boolean
  favorite_count: number
  source_type: number | null
  source_url: string | null
  created_at: string
  updated_at: string
  is_liked: boolean
  is_favorited: boolean
  prev_article: { id: number; title: string; slug: string } | null
  next_article: { id: number; title: string; slug: string } | null
  related_articles: Array<{ id: number; title: string; slug: string }>
}

export interface ArticleCreate {
  title: string
  slug: string
  summary?: string
  content: string
  cover_image?: string
  category_id: number
  tags?: number[]
  status: number
  is_featured?: number
  is_top?: number
  allow_comment?: number
  source_type?: number
  source_url?: string
}

export interface ArticleArchive {
  year: number
  month: number
  count: number
  articles: Array<{ id: number; title: string; published_at: string }>
}

/* ========== Note Types ========== */

export interface Note {
  id: number
  title: string
  slug: string
  category: Category
  learning_stage: number
  progress: number
  difficulty: number | null
  status: number
  view_count: number
  like_count: number
  children_count: number
  created_at: string
}

export interface NoteDetail extends Note {
  content: string
  parent: number | null
  children: Array<{ id: number; title: string; progress: number }>
}

/* ========== Comment Types ========== */

export interface Comment {
  id: number
  content: string
  content_type: number
  object_id: number
  user: {
    id: number
    nickname: string
    avatar: string | null
  }
  replies: Array<{
    id: number
    content: string
    user: { id: number; nickname: string; avatar: string | null }
    reply_to: { id: number; nickname: string } | null
    like_count: number
    status: number
    created_at: string
  }>
  like_count: number
  status: number
  created_at: string
}

export interface CommentCreate {
  content: string
  content_type: number
  object_id: number
  parent_id?: number | null
  reply_to_user_id?: number | null
  nickname?: string
  email?: string
  website?: string
}

/* ========== Interaction Types ========== */

export interface LikeParams {
  content_type: number
  object_id: number
}

export interface FavoriteParams {
  content_type: number
  object_id: number
  folder_name?: string
}

/* ========== Home Types ========== */

export interface HomeData {
  profile: {
    nickname: string
    avatar: string | null
    bio: string
    skills: string[]
    github_url: string | null
    social_links: Record<string, string | null>
  }
  statistics: {
    article_count: number
    project_count: number
    total_views: number
    total_likes: number
  }
  featured_projects: Array<{ id: number; title: string; cover_image: string | null; slug: string }>
  featured_articles: Array<{ id: number; title: string; summary: string | null; slug: string }>
  latest_articles: Array<{ id: number; title: string; slug: string; published_at: string }>
  popular_tags: Array<{ id: number; name: string; usage_count: number }>
}

/* ========== Search Types ========== */

export interface SearchResult {
  keyword: string
  results: {
    articles?: { count: number; list: any[] }
    projects?: { count: number; list: any[] }
    notes?: { count: number; list: any[] }
  }
  total: number
}
