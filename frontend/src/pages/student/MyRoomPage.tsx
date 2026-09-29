import { useQuery } from '@tanstack/react-query'
import { studentsApi } from '../../api/students'
import { allocationsApi } from '../../api/allocations'
import { Card, CardBody, CardHeader } from '../../components/ui/Card'
import { useAuth } from '../../context/AuthContext'

export function MyRoomPage() {
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

  const activeAllocation = allocations?.find(a => a.status === 'ACTIVE')

  return (
    <div className="p-8">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-slate-900">My Room</h1>
        <p className="mt-1 text-sm text-slate-500">Your room allocation details</p>
      </div>
      <Card>
        <CardHeader title="Room Allocation" subtitle="Current allocation status" />
        <CardBody>
          {activeAllocation ? (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-slate-500">Hostel</p>
                  <p className="text-lg font-semibold text-slate-900">Hostel #{activeAllocation.hostel_id}</p>
                </div>
                <div>
                  <p className="text-sm text-slate-500">Room</p>
                  <p className="text-lg font-semibold text-slate-900">Room #{activeAllocation.room_id}</p>
                </div>
                <div>
                  <p className="text-sm text-slate-500">Bed</p>
                  <p className="text-lg font-semibold text-slate-900">Bed #{activeAllocation.bed_id}</p>
                </div>
                <div>
                  <p className="text-sm text-slate-500">Check-in Date</p>
                  <p className="text-lg font-semibold text-slate-900">{activeAllocation.check_in_date ?? 'Not checked in'}</p>
                </div>
              </div>
            </div>
          ) : (
            <p className="text-slate-500">No active room allocation found.</p>
          )}
        </CardBody>
      </Card>
    </div>
  )
}
