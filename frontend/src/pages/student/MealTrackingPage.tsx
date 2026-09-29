import { useQuery } from '@tanstack/react-query'
import { useState } from 'react'
import { mealTrackingApi, type MealStats, type MealBalance, type MealRecord } from '../../api/mealTracking'
import { Card, CardBody, CardHeader } from '../../components/ui/Card'
import { Badge } from '../../components/ui/Badge'
import { DataTable } from '../../components/ui/DataTable'
import { createColumnHelper } from '@tanstack/react-table'
import { useAuth } from '../../context/AuthContext'

const columnHelper = createColumnHelper<MealRecord>()

export function MealTrackingPage() {
  const { user } = useAuth()
  const [showPurchase, setShowPurchase] = useState(false)
  const [purchaseAmount, setPurchaseAmount] = useState(30)

  const { data: stats } = useQuery({
    queryKey: ['meal-stats'],
    queryFn: mealTrackingApi.getStats,
    enabled: user?.role === 'STUDENT',
  })

  const { data: balance } = useQuery({
    queryKey: ['meal-balance'],
    queryFn: mealTrackingApi.getBalance,
    enabled: user?.role === 'STUDENT',
  })

  const { data: meals } = useQuery({
    queryKey: ['meal-records'],
    queryFn: () => mealTrackingApi.getMeals(),
    enabled: user?.role === 'STUDENT',
  })

  const columns = [
    columnHelper.accessor('meal_date', { header: 'Date' }),
    columnHelper.accessor('meal_type', {
      header: 'Meal Type',
      cell: (ctx) => <Badge variant="info">{ctx.getValue()}</Badge>,
    }),
    columnHelper.accessor('quantity', { header: 'Quantity' }),
    columnHelper.accessor('cost_per_meal', {
      header: 'Cost/Meal',
      cell: (ctx) => `$${ctx.getValue()}`,
    }),
    columnHelper.display({
      id: 'total',
      header: 'Total',
      cell: (ctx) => `$${ctx.row.original.quantity * ctx.row.original.cost_per_meal}`,
    }),
  ]

  return (
    <div className="p-8">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">Meal Tracking</h1>
          <p className="mt-1 text-sm text-slate-500">Track your daily meal consumption and balance</p>
        </div>
        <button
          onClick={() => setShowPurchase(!showPurchase)}
          className="rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700"
        >
          Purchase Meals
        </button>
      </div>

      {showPurchase && (
        <Card className="mb-6">
          <CardHeader title="Purchase Meals" subtitle="Add meals to your balance" />
          <CardBody>
            <div className="flex items-end gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700">Number of Meals</label>
                <input
                  type="number"
                  min={1}
                  max={1000}
                  value={purchaseAmount}
                  onChange={(e) => setPurchaseAmount(Number(e.target.value))}
                  className="mt-1 block w-32 rounded-md border border-slate-300 px-3 py-2 text-sm"
                />
              </div>
              <button
                onClick={async () => {
                  await mealTrackingApi.purchaseMeals(purchaseAmount)
                  setShowPurchase(false)
                }}
                className="rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700"
              >
                Confirm Purchase
              </button>
            </div>
          </CardBody>
        </Card>
      )}

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader title="Current Month" subtitle="Meals this month" />
          <CardBody>
            <p className="text-2xl font-bold text-slate-900">{stats?.current_month_meals ?? 0}</p>
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Last Month" subtitle="Meals last month" />
          <CardBody>
            <p className="text-2xl font-bold text-slate-900">{stats?.last_month_meals ?? 0}</p>
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Balance" subtitle="Meals remaining" />
          <CardBody>
            <p className={`text-2xl font-bold ${(stats?.balance ?? 0) > 10 ? 'text-green-600' : 'text-red-600'}`}>
              {stats?.balance ?? 0}
            </p>
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Total Spent" subtitle="All time" />
          <CardBody>
            <p className="text-2xl font-bold text-slate-900">${stats?.total_spent ?? 0}</p>
          </CardBody>
        </Card>
      </div>

      <div className="mt-8">
        <Card>
          <CardHeader title="Meal History" subtitle="Your recent meal records" />
          <CardBody>
            <DataTable columns={columns} data={meals ?? []} />
          </CardBody>
        </Card>
      </div>
    </div>
  )
}
