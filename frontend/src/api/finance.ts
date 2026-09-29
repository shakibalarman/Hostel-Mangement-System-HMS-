import { api } from './client'

export interface FeeStructure {
  id: number
  hostel_id: number
  name: string
  fee_type: string
  amount: number
  description: string | null
  is_active: boolean
  created_at: string
}

export interface Payment {
  id: number
  student_id: number
  fee_structure_id: number
  amount: number
  status: string
  payment_method: string | null
  transaction_id: string | null
  payment_date: string | null
  due_date: string | null
  remarks: string | null
  created_at: string
}

export interface Expense {
  id: number
  hostel_id: number
  title: string
  category: string | null
  amount: number
  expense_date: string
  description: string | null
  created_by: number | null
  created_at: string
}

export const feesApi = {
  list: (hostelId?: number) => api.get<FeeStructure[]>('/fees', { params: { hostel_id: hostelId } }).then(r => r.data),
  create: (data: Partial<FeeStructure>) => api.post<FeeStructure>('/fees', data).then(r => r.data),
  update: (id: number, data: Partial<FeeStructure>) => api.put<FeeStructure>(`/fees/${id}`, data).then(r => r.data),
  delete: (id: number) => api.delete(`/fees/${id}`),
}

export const paymentsApi = {
  list: (params?: { student_id?: number; status?: string }) =>
    api.get<Payment[]>('/payments', { params }).then(r => r.data),
  create: (data: Partial<Payment>) => api.post<Payment>('/payments', data).then(r => r.data),
  update: (id: number, data: Partial<Payment>) => api.put<Payment>(`/payments/${id}`, data).then(r => r.data),
}

export const expensesApi = {
  list: (hostelId?: number) => api.get<Expense[]>('/expenses', { params: { hostel_id: hostelId } }).then(r => r.data),
  create: (data: Partial<Expense>) => api.post<Expense>('/expenses', data).then(r => r.data),
  update: (id: number, data: Partial<Expense>) => api.put<Expense>(`/expenses/${id}`, data).then(r => r.data),
  delete: (id: number) => api.delete(`/expenses/${id}`),
}
