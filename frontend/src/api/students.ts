import { api } from './client'

export interface Student {
  id: number
  user_id: number
  student_number: string
  date_of_birth: string | null
  gender: string | null
  address: string | null
  emergency_contact: string | null
  department: string | null
  year_of_study: string | null
  created_at: string
}

export interface StudentCreate {
  username: string
  email: string
  full_name: string
  password: string
  phone?: string
  student_number: string
  date_of_birth?: string
  gender?: string
  address?: string
  emergency_contact?: string
  department?: string
  year_of_study?: string
}

export const studentsApi = {
  list: () => api.get<Student[]>('/students').then(r => r.data),
  get: (id: number) => api.get<Student>(`/students/${id}`).then(r => r.data),
  me: () => api.get<Student>('/students/me').then(r => r.data),
  create: (data: StudentCreate) => api.post<Student>('/students', data).then(r => r.data),
  update: (id: number, data: Partial<Student>) => api.put<Student>(`/students/${id}`, data).then(r => r.data),
  delete: (id: number) => api.delete(`/students/${id}`),
}
