import { useQuery } from '@tanstack/react-query'
import { studentsApi } from '../../api/students'
import { allocationsApi } from '../../api/allocations'
import { paymentsApi } from '../../api/finance'
import { noticesApi } from '../../api/misc'
import { Card, CardBody, CardHeader } from '../../components/ui/Card'
import { useAuth } from '../../context/AuthContext'

export function StudentDashboard() {
  const { user } = useAuth()
  const { data: student } = useQuery({
    queryKey: ['student-profile'],
    queryFn: studentsApi.me,
    enabled: user?.role === 'STUDENT',
  })
  const { data: allocations } = useQuery({
    queryKey: ['student-allocations'],
    queryFn: () => allocationsApi.list({ student_id: student?.id }),
    enabled: !!student,
  })
  const { data: payments } = useQuery({
    queryKey: ['student-payments'],
    queryFn: () => paymentsApi.list({ student_id: student?.id }),
    enabled: !!student,
  })
  const { data: notices } = useQuery({
    queryKey: ['notices'],
    queryFn: () => noticesApi.list({ audience: 'STUDENT', is_active: true }),
  })

  const activeAllocation = allocations?.find(a => a.status === 'ACTIVE')
  const totalPaid = payments?.filter(p => p.status === 'PAID').reduce((sum, p) => sum + p.amount, 0) ?? 0
  const totalPending = payments?.filter(p => p.status === 'PENDING').reduce((sum, p) => sum + p.amount, 0) ?? 0

  return (
    <div className="p-8">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-slate-900">Student Dashboard</h1>
        <p className="mt-1 text-sm text-slate-500">Welcome back, {user?.full_name}</p>
      </div>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader title="Student ID" subtitle="Your student number" />
          <CardBody>
            <p className="text-lg font-semibold text-slate-900">{student?.student_number ?? '-'}</p>
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Room" subtitle="Allocated room" />
          <CardBody>
            <p className="text-lg font-semibold text-slate-900">
              {activeAllocation ? `Room ${activeAllocation.room_id}` : 'Not allocated'}
            </p>
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Total Paid" subtitle="Payments made" />
          <CardBody>
            <p className="text-lg font-semibold text-green-600">${totalPaid}</p>
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Outstanding" subtitle="Pending payments" />
          <CardBody>
            <p className="text-lg font-semibold text-red-600">${totalPending}</p>
          </CardBody>
        </Card>
      </div>
      <div className="mt-8 grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader title="Recent Notices" subtitle="Latest announcements" />
          <CardBody>
            <div className="space-y-3">
              {notices?.slice(0, 5).map((notice) => (
                <div key={notice.id} className="border-b border-slate-100 pb-3 last:border-0">
                  <p className="text-sm font-medium text-slate-900">{notice.title}</p>
                  <p className="text-xs text-slate-500 mt-1">{notice.content.substring(0, 100)}...</p>
                </div>
              ))}
              {(!notices || notices.length === 0) && (
                <p className="text-sm text-slate-500">No notices available</p>
              )}
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="My Details" subtitle="Profile information" />
          <CardBody>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-slate-500">Name</span>
                <span className="text-slate-900">{user?.full_name}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Email</span>
                <span className="text-slate-900">{user?.email}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Department</span>
                <span className="text-slate-900">{student?.department ?? '-'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Year</span>
                <span className="text-slate-900">{student?.year_of_study ?? '-'}</span>
              </div>
            </div>
          </CardBody>
        </Card>
      </div>
    </div>
  )
}
