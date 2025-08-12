import React from 'react'

type Column<T> = { header: string; accessor: (row: T) => React.ReactNode }

export function DataTable<T>({ columns, data }: { columns: Column<T>[]; data: T[] }) {
  return (
    <table className="min-w-full border border-gray-700">
      <thead>
        <tr>
          {columns.map((col, i) => (
            <th key={i} className="p-2 border-b border-gray-700 text-left">{col.header}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, i) => (
          <tr key={i} className="odd:bg-gray-800">
            {columns.map((col, j) => (
              <td key={j} className="p-2 border-b border-gray-700">{col.accessor(row)}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  )
}
