import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { createColumnHelper } from '@tanstack/react-table'
import { useState } from 'react'
import { api } from '../../api/client'
import { Card, CardBody, CardHeader } from '../../components/ui/Card'
import { DataTable } from '../../components/ui/DataTable'
import { Badge } from '../../components/ui/Badge'
import { Modal } from '../../components/ui/Modal'
import { Input } from '../../components/ui/Input'
import { Button } from '../../components/ui/Button'

interface Staff {
  id: number
  user_id: number
  staff_number: string
  designation: string | null
  department: string | null
  hire_date: string | null
  created_at: string
  user?: {
    id: number
    username: string
    email: string
    full_name: string
    phone: string | null
    is_active: boolean
  }
}

const columnHelper = createColumnHelper<Staff>()

export function StaffPage() {
  const queryClient = useQueryClient()
  const [showAddModal, setShowAddModal] = useState(false)
  const [showDeleteModal, setShowDeleteModal] = useState(false)
  const [selectedStaff, setSelectedStaff] = useState<Staff | null>(null)
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    full_name: '',
    password: '',
    phone: '',
    staff_number: '',
    designation: '',
  })

  const { data: staff, isLoading } = useQuery({
    queryKey: ['staff'],
    queryFn: () => api.get<Staff[]>('/staff').then(r => r.data),
  })

  const createMutation = useMutation({
    mutationFn: (data: typeof formData) => api.post<Staff>('/staff', data).then(r => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['staff'] })
      setShowAddModal(false)
      setFormData({ username: '', email: '', full_name: '', password: '', phone: '', staff_number: '', designation: '' })
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: number) => api.delete(`/staff/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['staff'] })
      setShowDeleteModal(false)
      setSelectedStaff(null)
    },
  })

  if (isLoading) {
    return <div className="p-8 text-slate-500">Loading staff...</div>
  }

  const columns = [
    columnHelper.accessor('staff_number', { header: 'Staff Number' }),
    columnHelper.accessor('id', { header: 'ID' }),
    columnHelper.display({
      id: 'name',
      header: 'Name',
      cell: (ctx) => ctx.row.original.user?.full_name ?? '-',
    }),
    columnHelper.display({
      id: 'email',
      header: 'Email',
      cell: (ctx) => ctx.row.original.user?.email ?? '-',
    }),
    columnHelper.accessor('designation', { header: 'Designation' }),
    columnHelper.display({
      id: 'status',
      header: 'Status',
      cell: (ctx) => (
        <Badge variant={ctx.row.original.user?.is_active ? 'success' : 'default'}>
          {ctx.row.original.user?.is_active ? 'Active' : 'Inactive'}
        </Badge>
      ),
    }),
    columnHelper.display({
      id: 'actions',
      header: 'Actions',
      cell: (ctx) => (
        <Button
          variant="danger"
          size="sm"
          onClick={() => {
            setSelectedStaff(ctx.row.original)
            setShowDeleteModal(true)
          }}
        >
          Remove
        </Button>
      ),
    }),
  ]

  return (
    <div className="p-8">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">Staff</h1>
          <p className="mt-1 text-sm text-slate-500">Manage staff members</p>
        </div>
        <Button onClick={() => setShowAddModal(true)}>Add Staff</Button>
      </div>

      <Card>
        <CardHeader title="All Staff" subtitle={`${staff?.length ?? 0} members`} />
        <CardBody>
          <DataTable columns={columns} data={staff ?? []} />
        </CardBody>
      </Card>

      <Modal
        open={showAddModal}
        onClose={() => setShowAddModal(false)}
        title="Add New Staff"
        footer={
          <>
            <Button variant="secondary" onClick={() => setShowAddModal(false)}>Cancel</Button>
            <Button onClick={() => createMutation.mutate(formData)} disabled={createMutation.isPending}>
              {createMutation.isPending ? 'Adding...' : 'Add Staff'}
            </Button>
          </>
        }
      >
        <div className="space-y-4">
          <Input
            label="Username"
            value={formData.username}
            onChange={(e) => setFormData({ ...formData, username: e.target.value })}
            required
          />
          <Input
            label="Full Name"
            value={formData.full_name}
            onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
            required
          />
          <Input
            label="Email"
            type="email"
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            required
          />
          <Input
            label="Password"
            type="password"
            value={formData.password}
            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
            required
          />
          <Input
            label="Phone"
            value={formData.phone}
            onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
          />
          <Input
            label="Staff Number"
            value={formData.staff_number}
            onChange={(e) => setFormData({ ...formData, staff_number: e.target.value })}
            required
          />
          <Input
            label="Designation"
            value={formData.designation}
            onChange={(e) => setFormData({ ...formData, designation: e.target.value })}
          />
        </div>
      </Modal>

      <Modal
        open={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        title="Remove Staff"
        footer={
          <>
            <Button variant="secondary" onClick={() => setShowDeleteModal(false)}>Cancel</Button>
            <Button
              variant="danger"
              onClick={() => selectedStaff && deleteMutation.mutate(selectedStaff.id)}
              disabled={deleteMutation.isPending}
            >
              {deleteMutation.isPending ? 'Removing...' : 'Remove'}
            </Button>
          </>
        }
      >
        <p className="text-sm text-slate-600">
          Are you sure you want to remove this staff member? This action cannot be undone.
        </p>
      </Modal>
    </div>
  )
}
