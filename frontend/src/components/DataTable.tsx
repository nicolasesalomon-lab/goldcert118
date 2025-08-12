import { ReactNode } from 'react'

export default function DataTable({ children }: { children: ReactNode }) {
  return <table className="min-w-full text-left">{children}</table>
}
