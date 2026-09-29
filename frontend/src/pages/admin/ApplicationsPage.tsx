import { useQuery } from '@tanstack/react-query'
import { createColumnHelper } from '@tanstack/react-table'
import { applicationsApi, type Application } from '../../api/applications'
import { Card, CardBody, CardHeader } from '../../components/ui/Card'
import { DataTable } from '../../components/ui/DataTable'
import { Badge } from '../../components/ui/Badge'

const columnHelper = createColumnHelper<Application>()

export function ApplicationsPage() {
  const { data: applications, isLoading } = useQuery({
    queryKey: ['applications'],
    queryFn: () => applicationsApi.list(),
  })

  if (isLoading) {
    return <div className="p-8 text-slate-500">Loading applications...</div>
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'APPROVED':
        return <Badge variant="success">Approved</Badge>
      case 'REJECTED':
        return <Badge variant="danger">Rejected</Badge>
      default:
        return <Badge variant="warning">Pending</Badge>
    }
  }

  const columns = [
    columnHelper.accessor('id', { header: 'ID' }),
    columnHelper.accessor('student_id', { header: 'Student ID' }),
    columnHelper.accessor('preferred_room_type', { header: 'Room Type' }),
    columnHelper.display({
      id: 'status',
      header: 'Status',
      cell: (ctx) => getStatusBadge(ctx.row.original.status),
    }),
    columnHelper.accessor('created_at', { header: 'Applied Date' }),
  ]

  return (
    <div className="p-8">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-slate-900">Applications</h1>
        <p className="mt-1 text-sm text-slate-500">Manage hostel applications</p>
      </div>
      <Card>
        <CardHeader title="All Applications" subtitle={`${applications?.length ?? 0} applications`} />
        <CardBody>
          <DataTable columns={columns} data={applications ?? []} />
        </CardBody>
      </Card>
    </div>
  )
}
