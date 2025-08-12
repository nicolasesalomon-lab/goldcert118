import { useQuery } from '@tanstack/react-query'
import { api } from '../lib/axios'
import { Link } from 'react-router-dom'

export default function Dashboard() {
  const { data } = useQuery(['summary'], async () => (await api.get('/dashboard/summary')).data)

  if (!data) return <p className="p-4">Cargando...</p>

  return (
    <div className="p-4 space-y-6">
      <div className="grid grid-cols-3 md:grid-cols-6 gap-4">
        {Object.entries(data.kpis).map(([k, v]) => (
          <div key={k} className="bg-gray-800 p-3 rounded shadow text-center">
            <div className="text-sm">{k}</div>
            <div className="text-xl text-gold">{v as number}</div>
          </div>
        ))}
      </div>
      <div className="grid grid-cols-2 gap-6">
        <div>
          <h2 className="mb-2 text-lg">Vencen 90</h2>
          <ul className="space-y-1">
            {data.vencen_90.map((id: number) => (
              <li key={id}><Link className="text-gold" to={`/certificaciones/${id}`}>Cert #{id}</Link></li>
            ))}
          </ul>
        </div>
        <div>
          <h2 className="mb-2 text-lg">Suspendidos</h2>
          <ul className="space-y-1">
            {data.suspendidos.map((id: number) => (
              <li key={id}><Link className="text-gold" to={`/certificaciones/${id}`}>Cert #{id}</Link></li>
            ))}
          </ul>
        </div>
      </div>
      <div>
        <h2 className="mb-2 text-lg">Serie 12 meses</h2>
        <ul className="space-y-1">
          {data.serie.map((s: { month: string; count: number }) => (
            <li key={s.month}>{s.month}: {s.count}</li>
          ))}
        </ul>
      </div>
    </div>
  )
}
