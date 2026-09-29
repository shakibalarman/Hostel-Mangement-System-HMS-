import { useQuery } from '@tanstack/react-query'
import { createColumnHelper } from '@tanstack/react-table'
import { noticesApi, type Notice } from '../../api/misc'
import { Card, CardBody, CardHeader } from '../../components/ui/Card'
import { DataTable } from '../../components/ui/DataTable'
import { Badge } from '../../components/ui/Badge'

const columnHelper = createColumnHelper<Notice>()

export function NoticesPage() {
  const { data: notices, isLoading } = useQuery({
    queryKey: ['notices'],
    queryFn: () => noticesApi.list(),
  })

  if (isLoading) {
    return <div className="p-8 text-slate-500">Loading notices...</div>
  }

  const columns = [
    columnHelper.accessor('id', { header: 'ID' }),
    columnHelper.accessor('title', { header: 'Title' }),
    columnHelper.accessor('audience', { header: 'Audience' }),
    columnHelper.display({
      id: 'status',
      header: 'Status',
      cell: (ctx) =>
        ctx.row.original.is_active ? (
          <Badge variant="success">Active</Badge>
        ) : (
          <Badge variant="default">Inactive</Badge>
        ),
    }),
    columnHelper.accessor('created_at', { header: 'Date' }),
  ]

  return (
    <div className="p-8">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-slate-900">Notices</h1>
        <p className="mt-1 text-sm text-slate-500">Manage hostel notices</p>
      </div>
      <Card>
        <CardHeader title="All Notices" subtitle={`${notices?.length ?? 0} notices`} />
        <CardBody>
          <DataTable columns={columns} data={notices ?? []} />
        </CardBody>
      </Card>
    </div>
  )
}
