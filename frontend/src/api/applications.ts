import { api } from './client'

export interface Application {
  id: number
  student_id: number
  preferred_hostel_id: number | null
  preferred_room_type: string | null
  status: string
  remarks: string | null
  reviewed_by: number | null
  reviewed_at: string | null
  created_at: string
}

export interface ApplicationCreate {
  preferred_hostel_id?: number
  preferred_room_type?: string
}

export const applicationsApi = {
  list: (params?: { student_id?: number; status?: string }) =>
    api.get<Application[]>('/applications', { params }).then(r => r.data),
  get: (id: number) => api.get<Application>(`/applications/${id}`).then(r => r.data),
  create: (data: ApplicationCreate) => api.post<Application>('/applications', data).then(r => r.data),
  review: (id: number, status: string, remarks?: string) =>
    api.put<Application>(`/applications/${id}/review`, { status, remarks }).then(r => r.data),
}
