import { Link } from 'react-router-dom'
import { Button } from '../components/ui/Button'

export function UnauthorizedPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4 bg-slate-100">
      <h1 className="text-2xl font-semibold text-slate-900">403</h1>
      <p className="text-sm text-slate-500">
        You do not have permission to access this page.
      </p>
      <Link to="/">
        <Button variant="secondary">Go back</Button>
      </Link>
    </div>
  )
}
