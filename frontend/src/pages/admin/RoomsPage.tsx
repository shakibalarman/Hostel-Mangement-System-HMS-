import { useQuery } from '@tanstack/react-query'
import { createColumnHelper } from '@tanstack/react-table'
import { roomsApi, type Room } from '../../api/hostels'
import { Card, CardBody, CardHeader } from '../../components/ui/Card'
import { DataTable } from '../../components/ui/DataTable'
import { Badge } from '../../components/ui/Badge'

const columnHelper = createColumnHelper<Room>()

export function RoomsPage() {
  const { data: rooms, isLoading } = useQuery({
    queryKey: ['rooms'],
    queryFn: () => roomsApi.list(),
  })

  if (isLoading) {
    return <div className="p-8 text-slate-500">Loading rooms...</div>
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'AVAILABLE':
        return <Badge variant="success">Available</Badge>
      case 'FULL':
        return <Badge variant="danger">Full</Badge>
      case 'MAINTENANCE':
        return <Badge variant="warning">Maintenance</Badge>
      default:
        return <Badge variant="default">{status}</Badge>
    }
  }

  const columns = [
    columnHelper.accessor('id', { header: 'ID' }),
    columnHelper.accessor('room_number', { header: 'Room Number' }),
    columnHelper.accessor('room_type', { header: 'Type' }),
    columnHelper.accessor('capacity', { header: 'Capacity' }),
    columnHelper.accessor('rent', { header: 'Rent' }),
    columnHelper.display({
      id: 'status',
      header: 'Status',
      cell: (ctx) => getStatusBadge(ctx.row.original.status),
    }),
  ]

  return (
    <div className="p-8">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-slate-900">Rooms</h1>
        <p className="mt-1 text-sm text-slate-500">Manage hostel rooms</p>
      </div>
      <Card>
        <CardHeader title="All Rooms" subtitle={`${rooms?.length ?? 0} rooms`} />
        <CardBody>
          <DataTable columns={columns} data={rooms ?? []} />
        </CardBody>
      </Card>
    </div>
  )
}
