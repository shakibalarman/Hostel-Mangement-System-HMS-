import { useQuery } from '@tanstack/react-query'
import { createColumnHelper } from '@tanstack/react-table'
import { studentsApi, type Student } from '../../api/students'
import { Card, CardBody, CardHeader } from '../../components/ui/Card'
import { DataTable } from '../../components/ui/DataTable'
import { Badge } from '../../components/ui/Badge'

const columnHelper = createColumnHelper<Student>()

export function StudentsPage() {
  const { data: students, isLoading } = useQuery({
    queryKey: ['students'],
    queryFn: studentsApi.list,
  })

  if (isLoading) {
    return <div className="p-8 text-slate-500">Loading students...</div>
  }

  const columns = [
    columnHelper.accessor('student_number', { header: 'Student Number' }),
    columnHelper.accessor('id', { header: 'ID' }),
    columnHelper.accessor('department', { header: 'Department' }),
    columnHelper.accessor('year_of_study', { header: 'Year' }),
    columnHelper.display({
      id: 'status',
      header: 'Status',
      cell: () => <Badge variant="success">Active</Badge>,
    }),
  ]

  return (
    <div className="p-8">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-slate-900">Students</h1>
        <p className="mt-1 text-sm text-slate-500">Manage student records</p>
      </div>
      <Card>
        <CardHeader title="All Students" subtitle={`${students?.length ?? 0} students`} />
        <CardBody>
          <DataTable columns={columns} data={students ?? []} />
        </CardBody>
      </Card>
    </div>
  )
}
