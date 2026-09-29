import { api } from './client'

export interface DashboardStats {
  total_students: number
  total_staff: number
  total_hostels: number
  total_rooms: number
  total_beds: number
  occupied_beds: number
  available_beds: number
  pending_applications: number
  pending_payments: number
  active_complaints: number
  pending_maintenance: number
  monthly_revenue: number
  monthly_expenses: number
}

export const reportsApi = {
  dashboard: () => api.get<DashboardStats>('/reports/dashboard').then(r => r.data),
  occupancy: () => api.get<unknown[]>('/reports/occupancy').then(r => r.data),
  students: () => api.get<unknown[]>('/reports/students').then(r => r.data),
  payments: () => api.get<unknown[]>('/reports/payments').then(r => r.data),
  outstandingFees: () => api.get<unknown[]>('/reports/outstanding-fees').then(r => r.data),
}
