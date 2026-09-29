import { api } from './client'

export interface Allocation {
  id: number
  student_id: number
  hostel_id: number
  room_id: number
  bed_id: number
  application_id: number | null
  allocation_date: string
  check_in_date: string | null
  check_out_date: string | null
  status: string
  notes: string | null
  created_at: string
}

export interface AllocationCreate {
  student_id: number
  hostel_id: number
  room_id: number
  bed_id: number
  application_id?: number
  allocation_date: string
  check_in_date?: string
  notes?: string
}

export const allocationsApi = {
  list: (params?: { student_id?: number; status?: string }) =>
    api.get<Allocation[]>('/allocations', { params }).then(r => r.data),
  get: (id: number) => api.get<Allocation>(`/allocations/${id}`).then(r => r.data),
  create: (data: AllocationCreate) => api.post<Allocation>('/allocations', data).then(r => r.data),
  checkout: (id: number, checkOutDate: string) =>
    api.post<Allocation>(`/allocations/${id}/checkout`, { check_out_date: checkOutDate }).then(r => r.data),
  transfer: (id: number, newRoomId: number, newBedId: number, transferDate: string, notes?: string) =>
    api.post<Allocation>(`/allocations/${id}/transfer`, {
      new_room_id: newRoomId,
      new_bed_id: newBedId,
      transfer_date: transferDate,
      notes,
    }).then(r => r.data),
}
