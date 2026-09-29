import { useQuery } from '@tanstack/react-query'
import { createColumnHelper } from '@tanstack/react-table'
import { studentsApi } from '../../api/students'
import { paymentsApi, type Payment } from '../../api/finance'
import { Card, CardBody, CardHeader } from '../../components/ui/Card'
import { DataTable } from '../../components/ui/DataTable'
import { Badge } from '../../components/ui/Badge'
import { useAuth } from '../../context/AuthContext'

const columnHelper = createColumnHelper<Payment>()

export function PaymentsPage() {
  const { user } = useAuth()
  const { data: student } = useQuery({
    queryKey: ['student-profile'],
    queryFn: studentsApi.me,
    enabled: user?.role === 'STUDENT',
  })
  const { data: payments, isLoading } = useQuery({
    queryKey: ['student-payments'],
    queryFn: () => paymentsApi.list({ student_id: student?.id }),
    enabled: !!student,
  })

  if (isLoading) {
    return <div className="p-8 text-slate-500">Loading payments...</div>
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'PAID':
        return <Badge variant="success">Paid</Badge>
      case 'PENDING':
        return <Badge variant="warning">Pending</Badge>
      case 'FAILED':
        return <Badge variant="danger">Failed</Badge>
      default:
        return <Badge variant="default">{status}</Badge>
    }
  }

  const columns = [
    columnHelper.accessor('id', { header: 'ID' }),
    columnHelper.accessor('amount', { header: 'Amount' }),
    columnHelper.display({
      id: 'status',
      header: 'Status',
      cell: (ctx) => getStatusBadge(ctx.row.original.status),
    }),
    columnHelper.accessor('payment_date', { header: 'Payment Date' }),
    columnHelper.accessor('transaction_id', { header: 'Transaction ID' }),
  ]

  return (
    <div className="p-8">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-slate-900">Payments</h1>
        <p className="mt-1 text-sm text-slate-500">Your payment history</p>
      </div>
      <Card>
        <CardHeader title="Payment History" subtitle={`${payments?.length ?? 0} payments`} />
        <CardBody>
          <DataTable columns={columns} data={payments ?? []} />
        </CardBody>
      </Card>
    </div>
  )
}
