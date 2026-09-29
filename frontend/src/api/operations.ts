import { api } from './client'

export interface Attendance {
  id: number
  student_id: number
  attendance_date: string
  status: string
  remarks: string | null
  marked_by: number | null
  created_at: string
}

export interface LeaveRequest {
  id: number
  student_id: number
  start_date: string
  end_date: string
  reason: string
  status: string
  reviewed_by: number | null
  reviewed_at: string | null
  remarks: string | null
  created_at: string
}

export interface Complaint {
  id: number
  student_id: number
  title: string
  description: string
  status: string
  resolved_by: number | null
  resolved_at: string | null
  resolution_notes: string | null
  created_at: string
}

export interface MaintenanceRequest {
  id: number
  student_id: number
  room_id: number
  title: string
  description: string
  status: string
  handled_by: number | null
  handled_at: string | null
  resolution_notes: string | null
  created_at: string
}

export const attendanceApi = {
  list: (params?: { student_id?: number; attendance_date?: string }) =>
    api.get<Attendance[]>('/attendance', { params }).then(r => r.data),
  mark: (data: { student_id: number; attendance_date: string; status: string; remarks?: string }) =>
    api.post<Attendance>('/attendance', data).then(r => r.data),
  update: (id: number, data: Partial<Attendance>) => api.put<Attendance>(`/attendance/${id}`, data).then(r => r.data),
}

export const leavesApi = {
  list: (params?: { student_id?: number; status?: string }) =>
    api.get<LeaveRequest[]>('/leaves', { params }).then(r => r.data),
  create: (data: { start_date: string; end_date: string; reason: string }) =>
    api.post<LeaveRequest>('/leaves', data).then(r => r.data),
  review: (id: number, status: string, remarks?: string) =>
    api.put<LeaveRequest>(`/leaves/${id}/review`, { status, remarks }).then(r => r.data),
}

export const complaintsApi = {
  list: (params?: { student_id?: number; status?: string }) =>
    api.get<Complaint[]>('/complaints', { params }).then(r => r.data),
  create: (data: { title: string; description: string }) =>
    api.post<Complaint>('/complaints', data).then(r => r.data),
  update: (id: number, data: Partial<Complaint>) => api.put<Complaint>(`/complaints/${id}`, data).then(r => r.data),
}

export const maintenanceApi = {
  list: (params?: { student_id?: number; status?: string; room_id?: number }) =>
    api.get<MaintenanceRequest[]>('/maintenance', { params }).then(r => r.data),
  create: (data: { room_id: number; title: string; description: string }) =>
    api.post<MaintenanceRequest>('/maintenance', data).then(r => r.data),
  update: (id: number, data: Partial<MaintenanceRequest>) => api.put<MaintenanceRequest>(`/maintenance/${id}`, data).then(r => r.data),
}
