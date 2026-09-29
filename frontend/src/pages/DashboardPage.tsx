import { useAuth } from '../context/AuthContext'
import { Card, CardBody, CardHeader } from '../components/ui/Card'

export function DashboardPage() {
  const { user } = useAuth()

  return (
    <div className="p-8">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-slate-900">
          Welcome back, {user?.full_name}
        </h1>
        <p className="mt-1 text-sm text-slate-500">
          Role: {user?.role} · Dashboard module arrives in Phase 10
        </p>
      </div>
      <Card>
        <CardHeader title="Dashboard" subtitle="Module under construction" />
        <CardBody>
          <p className="text-sm text-slate-500">
            The {user?.role.toLowerCase()} dashboard will be built in Phase 10
            with real statistics, charts and management screens.
          </p>
        </CardBody>
      </Card>
    </div>
  )
}
