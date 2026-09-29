import type { ReactNode } from 'react'
import { cn } from '../../utils/cn'

type Tone = 'gray' | 'green' | 'red' | 'amber' | 'blue' | 'purple'

const tones: Record<Tone, string> = {
  gray: 'bg-slate-100 text-slate-700 ring-slate-200',
  green: 'bg-emerald-50 text-emerald-700 ring-emerald-200',
  red: 'bg-red-50 text-red-700 ring-red-200',
  amber: 'bg-amber-50 text-amber-700 ring-amber-200',
  blue: 'bg-blue-50 text-blue-700 ring-blue-200',
  purple: 'bg-purple-50 text-purple-700 ring-purple-200',
}

export function Badge({
  tone,
  variant,
  children,
  className,
}: {
  tone?: Tone
  variant?: 'default' | 'success' | 'danger' | 'warning' | 'info'
  children: ReactNode
  className?: string
}) {
  const toneMap: Record<string, Tone> = {
    default: 'gray',
    success: 'green',
    danger: 'red',
    warning: 'amber',
    info: 'blue',
  }
  const resolvedTone = tone ?? (variant ? toneMap[variant] : 'gray')
  return (
    <span
      className={cn(
        'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ring-1 ring-inset',
        tones[resolvedTone],
        className,
      )}
    >
      {children}
    </span>
  )
}
