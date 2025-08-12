import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { api } from '../../lib/axios'
import { DataTable } from '../../components/DataTable'
import { Link } from 'react-router-dom'

export default function ProvidersList() {
  const [search, setSearch] = useState('')
  const { data, refetch } = useQuery(['providers', search], async () => (await api.get('/providers', { params: { search } })).data)

  const columns = [
    { header: 'ID', accessor: (p: any) => p.id },
    { header: 'Nombre', accessor: (p: any) => <Link className="text-gold" to={`/proveedores/${p.id}`}>{p.nombre}</Link> },
    { header: 'Email', accessor: (p: any) => p.email || '' },
  ]

  return (
    <div className="p-4 space-y-4">
      <div className="flex gap-2">
        <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Buscar" className="p-2 text-black flex-1" onKeyDown={e => { if (e.key === 'Enter') refetch() }} />
        <button onClick={() => refetch()} className="bg-gold text-black px-4">Buscar</button>
        <Link to="/proveedores/nuevo" className="bg-gray-700 px-4 py-2">Nuevo</Link>
      </div>
      {data && <DataTable columns={columns} data={data} />}
    </div>
  )
}
