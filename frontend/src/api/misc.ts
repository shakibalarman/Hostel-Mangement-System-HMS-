import { api } from './client'

export interface Meal {
  id: number
  hostel_id: number
  meal_type: string
  menu: string
  meal_date: string
  is_active: boolean
  created_at: string
}

export interface InventoryItem {
  id: number
  hostel_id: number
  item_name: string
  quantity: number
  unit: string | null
  description: string | null
  status: string
  created_at: string
}

export interface Notice {
  id: number
  title: string
  content: string
  audience: string
  is_active: boolean
  created_by: number | null
  created_at: string
}

export interface Notification {
  id: number
  user_id: number
  title: string
  message: string
  is_read: boolean
  created_at: string
}

export const mealsApi = {
  list: (params?: { hostel_id?: number; meal_type?: string; meal_date?: string }) =>
    api.get<Meal[]>('/meals', { params }).then(r => r.data),
  create: (data: Partial<Meal>) => api.post<Meal>('/meals', data).then(r => r.data),
  update: (id: number, data: Partial<Meal>) => api.put<Meal>(`/meals/${id}`, data).then(r => r.data),
  delete: (id: number) => api.delete(`/meals/${id}`),
}

export const inventoryApi = {
  list: (hostelId?: number) => api.get<InventoryItem[]>('/inventory', { params: { hostel_id: hostelId } }).then(r => r.data),
  create: (data: Partial<InventoryItem>) => api.post<InventoryItem>('/inventory', data).then(r => r.data),
  update: (id: number, data: Partial<InventoryItem>) => api.put<InventoryItem>(`/inventory/${id}`, data).then(r => r.data),
  delete: (id: number) => api.delete(`/inventory/${id}`),
}

export const noticesApi = {
  list: (params?: { audience?: string; is_active?: boolean }) =>
    api.get<Notice[]>('/notices', { params }).then(r => r.data),
  create: (data: Partial<Notice>) => api.post<Notice>('/notices', data).then(r => r.data),
  update: (id: number, data: Partial<Notice>) => api.put<Notice>(`/notices/${id}`, data).then(r => r.data),
  delete: (id: number) => api.delete(`/notices/${id}`),
}

export const notificationsApi = {
  list: () => api.get<Notification[]>('/notifications').then(r => r.data),
  markRead: (id: number) => api.put<Notification>(`/notifications/${id}/read`).then(r => r.data),
  markAllRead: () => api.put<{ marked_read: number }>('/notifications/read-all').then(r => r.data),
}
