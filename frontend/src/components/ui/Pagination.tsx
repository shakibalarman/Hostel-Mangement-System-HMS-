import { cn } from '../../utils/cn'

interface PaginationProps {
  page: number
  pages: number
  total: number
  onPageChange: (page: number) => void
}

export function Pagination({ page, pages, total, onPageChange }: PaginationProps) {
  if (pages <= 1) return null

  const items: (number | 'ellipsis')[] = []
  for (let i = 1; i <= pages; i++) {
    if (i === 1 || i === pages || Math.abs(i - page) <= 1) {
      items.push(i)
    } else if (items[items.length - 1] !== 'ellipsis') {
      items.push('ellipsis')
    }
  }

  return (
    <div className="flex items-center justify-between border-t border-slate-200 px-4 py-3">
      <p className="text-sm text-slate-500">
        Page {page} of {pages} · {total} results
      </p>
      <div className="flex items-center gap-1">
        <button
          disabled={page <= 1}
          onClick={() => onPageChange(page - 1)}
          className="rounded-md px-2.5 py-1.5 text-sm text-slate-600 hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-40"
        >
          Previous
        </button>
        {items.map((item, idx) =>
          item === 'ellipsis' ? (
            <span key={`e-${idx}`} className="px-1.5 text-sm text-slate-400">
              …
            </span>
          ) : (
            <button
              key={item}
              onClick={() => onPageChange(item)}
              className={cn(
                'rounded-md px-2.5 py-1.5 text-sm',
                item === page
                  ? 'bg-indigo-600 font-medium text-white'
                  : 'text-slate-600 hover:bg-slate-100',
              )}
            >
              {item}
            </button>
          ),
        )}
        <button
          disabled={page >= pages}
          onClick={() => onPageChange(page + 1)}
          className="rounded-md px-2.5 py-1.5 text-sm text-slate-600 hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-40"
        >
          Next
        </button>
      </div>
    </div>
  )
}
