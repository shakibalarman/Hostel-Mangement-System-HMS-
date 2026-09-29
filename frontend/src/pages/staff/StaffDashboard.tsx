import { useQuery } from '@tanstack/react-query'
import { reportsApi } from '../../api/reports'
import { Card, CardBody, CardHeader } from '../../components/ui/Card'

export function StaffDashboard() {
  const { data: stats, isLoading } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: reportsApi.dashboard,
  })

  if (isLoading) {
    return <div className="p-8 text-slate-500">Loading dashboard...</div>
  }

  return (
    <div className="p-8">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-slate-900">Staff Dashboard</h1>
        <p className="mt-1 text-sm text-slate-500">Operational overview</p>
      </div>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader title="Total Students" subtitle="Allocated students" />
          <CardBody>
            <p className="text-3xl font-bold text-slate-900">{stats?.total_students ?? 0}</p>
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Pending Maintenance" subtitle="Requests to handle" />
          <CardBody>
            <p className="text-3xl font-bold text-orange-600">{stats?.pending_maintenance ?? 0}</p>
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Active Complaints" subtitle="Complaints to resolve" />
          <CardBody>
            <p className="text-3xl font-bold text-red-600">{stats?.active_complaints ?? 0}</p>
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Pending Applications" subtitle="Applications to review" />
          <CardBody>
            <p className="text-3xl font-bold text-yellow-600">{stats?.pending_applications ?? 0}</p>
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Occupied Beds" subtitle="Current occupancy" />
          <CardBody>
            <p className="text-3xl font-bold text-blue-600">{stats?.occupied_beds ?? 0}</p>
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Available Beds" subtitle="Beds ready for allocation" />
          <CardBody>
            <p className="text-3xl font-bold text-green-600">{stats?.available_beds ?? 0}</p>
          </CardBody>
        </Card>
      </div>
    </div>
  )
}
