import { useQuery } from '@tanstack/react-query'
import { reportsApi } from '../../api/reports'
import { Card, CardBody, CardHeader } from '../../components/ui/Card'

export function AdminDashboard() {
  const { data: stats, isLoading } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: reportsApi.dashboard,
  })

  if (isLoading) {
    return <div className="p-8 text-slate-500">Loading dashboard...</div>
  }

  const cards = [
    { label: 'Total Students', value: stats?.total_students ?? 0, color: 'bg-blue-500' },
    { label: 'Total Staff', value: stats?.total_staff ?? 0, color: 'bg-green-500' },
    { label: 'Total Hostels', value: stats?.total_hostels ?? 0, color: 'bg-purple-500' },
    { label: 'Total Rooms', value: stats?.total_rooms ?? 0, color: 'bg-orange-500' },
    { label: 'Total Beds', value: stats?.total_beds ?? 0, color: 'bg-teal-500' },
    { label: 'Occupied Beds', value: stats?.occupied_beds ?? 0, color: 'bg-red-500' },
    { label: 'Available Beds', value: stats?.available_beds ?? 0, color: 'bg-cyan-500' },
    { label: 'Pending Applications', value: stats?.pending_applications ?? 0, color: 'bg-yellow-500' },
    { label: 'Pending Payments', value: stats?.pending_payments ?? 0, color: 'bg-pink-500' },
    { label: 'Active Complaints', value: stats?.active_complaints ?? 0, color: 'bg-indigo-500' },
    { label: 'Pending Maintenance', value: stats?.pending_maintenance ?? 0, color: 'bg-lime-500' },
    { label: 'Monthly Revenue', value: `$${stats?.monthly_revenue ?? 0}`, color: 'bg-emerald-500' },
  ]

  return (
    <div className="p-8">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-slate-900">Admin Dashboard</h1>
        <p className="mt-1 text-sm text-slate-500">Overview of hostel management system</p>
      </div>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {cards.map((card) => (
          <Card key={card.label}>
            <CardBody>
              <div className="flex items-center gap-4">
                <div className={`h-12 w-12 rounded-lg ${card.color} flex items-center justify-center`}>
                  <span className="text-lg font-bold text-white">{typeof card.value === 'number' ? card.value : '#'}</span>
                </div>
                <div>
                  <p className="text-sm text-slate-500">{card.label}</p>
                  <p className="text-xl font-semibold text-slate-900">{card.value}</p>
                </div>
              </div>
            </CardBody>
          </Card>
        ))}
      </div>
      <div className="mt-8 grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader title="Monthly Revenue" subtitle="Revenue vs Expenses" />
          <CardBody>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-sm text-slate-600">Revenue</span>
                <span className="text-lg font-semibold text-green-600">${stats?.monthly_revenue ?? 0}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-slate-600">Expenses</span>
                <span className="text-lg font-semibold text-red-600">${stats?.monthly_expenses ?? 0}</span>
              </div>
              <div className="flex justify-between items-center border-t pt-2">
                <span className="text-sm font-medium text-slate-900">Net</span>
                <span className="text-lg font-semibold text-slate-900">
                  ${(stats?.monthly_revenue ?? 0) - (stats?.monthly_expenses ?? 0)}
                </span>
              </div>
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Bed Occupancy" subtitle="Current occupancy status" />
          <CardBody>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-600">Occupied</span>
                  <span className="text-slate-900">{stats?.occupied_beds ?? 0}</span>
                </div>
                <div className="w-full bg-slate-200 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full"
                    style={{ width: `${stats?.total_beds ? ((stats.occupied_beds / stats.total_beds) * 100) : 0}%` }}
                  />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-600">Available</span>
                  <span className="text-slate-900">{stats?.available_beds ?? 0}</span>
                </div>
                <div className="w-full bg-slate-200 rounded-full h-2">
                  <div
                    className="bg-green-600 h-2 rounded-full"
                    style={{ width: `${stats?.total_beds ? ((stats.available_beds / stats.total_beds) * 100) : 0}%` }}
                  />
                </div>
              </div>
            </div>
          </CardBody>
        </Card>
      </div>
    </div>
  )
}
