export type Role = 'ADMIN' | 'STAFF' | 'STUDENT'

export interface User {
  id: number
  username: string
  email: string
  full_name: string
  role: Role
  is_active: boolean
  created_at: string
}

export interface AuthTokens {
  access_token: string
  token_type: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  size: number
  pages: number
}

export interface ApiErrorShape {
  code: string
  message: string
  details?: unknown
}

export interface PaginationParams {
  page?: number
  size?: number
  search?: string
  sort_by?: string
  sort_order?: 'asc' | 'desc'
}
