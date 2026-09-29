import { api } from './client'

export interface Hostel {
  id: number
  name: string
  code: string
  address: string | null
  contact_number: string | null
  description: string | null
  status: string
  created_at: string
}

export interface Building {
  id: number
  hostel_id: number
  name: string
  code: string
  description: string | null
  status: string
  created_at: string
}

export interface Floor {
  id: number
  building_id: number
  name: string
  floor_number: number
  description: string | null
  status: string
  created_at: string
}

export interface Room {
  id: number
  floor_id: number
  room_number: string
  room_type: string
  capacity: number
  status: string
  rent: number | null
  description: string | null
  created_at: string
}

export interface Bed {
  id: number
  room_id: number
  bed_number: string
  status: string
  description: string | null
  created_at: string
}

export const hostelsApi = {
  list: () => api.get<Hostel[]>('/hostels').then(r => r.data),
  get: (id: number) => api.get<Hostel>(`/hostels/${id}`).then(r => r.data),
  create: (data: Partial<Hostel>) => api.post<Hostel>('/hostels', data).then(r => r.data),
  update: (id: number, data: Partial<Hostel>) => api.put<Hostel>(`/hostels/${id}`, data).then(r => r.data),
  delete: (id: number) => api.delete(`/hostels/${id}`),
}

export const buildingsApi = {
  list: (hostelId?: number) => api.get<Building[]>('/buildings', { params: { hostel_id: hostelId } }).then(r => r.data),
  get: (id: number) => api.get<Building>(`/buildings/${id}`).then(r => r.data),
  create: (data: Partial<Building>) => api.post<Building>('/buildings', data).then(r => r.data),
  update: (id: number, data: Partial<Building>) => api.put<Building>(`/buildings/${id}`, data).then(r => r.data),
  delete: (id: number) => api.delete(`/buildings/${id}`),
}

export const floorsApi = {
  list: (buildingId?: number) => api.get<Floor[]>('/floors', { params: { building_id: buildingId } }).then(r => r.data),
  get: (id: number) => api.get<Floor>(`/floors/${id}`).then(r => r.data),
  create: (data: Partial<Floor>) => api.post<Floor>('/floors', data).then(r => r.data),
  update: (id: number, data: Partial<Floor>) => api.put<Floor>(`/floors/${id}`, data).then(r => r.data),
  delete: (id: number) => api.delete(`/floors/${id}`),
}

export const roomsApi = {
  list: (floorId?: number, status?: string) => api.get<Room[]>('/rooms', { params: { floor_id: floorId, status } }).then(r => r.data),
  get: (id: number) => api.get<Room>(`/rooms/${id}`).then(r => r.data),
  create: (data: Partial<Room>) => api.post<Room>('/rooms', data).then(r => r.data),
  update: (id: number, data: Partial<Room>) => api.put<Room>(`/rooms/${id}`, data).then(r => r.data),
  delete: (id: number) => api.delete(`/rooms/${id}`),
}

export const bedsApi = {
  list: (roomId?: number, status?: string) => api.get<Bed[]>('/beds', { params: { room_id: roomId, status } }).then(r => r.data),
  get: (id: number) => api.get<Bed>(`/beds/${id}`).then(r => r.data),
  create: (data: Partial<Bed>) => api.post<Bed>('/beds', data).then(r => r.data),
  update: (id: number, data: Partial<Bed>) => api.put<Bed>(`/beds/${id}`, data).then(r => r.data),
  delete: (id: number) => api.delete(`/beds/${id}`),
}
